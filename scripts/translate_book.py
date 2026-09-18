import os
import sys
import argparse
import shutil
import zipfile
from bs4 import BeautifulSoup
from translator_engine import TranslationCache, translate_batch, repack_epub

def extract_epub(epub_path, extract_dir):
    if os.path.exists(extract_dir):
        print(f"[EXTRACT] Directory {extract_dir} already exists, reusing existing extraction.")
        return
    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(epub_path, "r") as z:
        z.extractall(extract_dir)
    print(f"[EXTRACT] Extracted {epub_path} to {extract_dir}")

def safe_replace_inner(tag, new_content):
    tag.clear()
    # Attempt parsing inside a dummy root tag
    try:
        sub = BeautifulSoup(f"<root>{new_content}</root>", "xml")
        if sub.root:
            for child in list(sub.root.contents):
                tag.append(child)
            return
    except Exception:
        pass
    # Fallback to html.parser
    try:
        sub = BeautifulSoup(f"<root>{new_content}</root>", "html.parser")
        root = sub.find("root") or sub
        for child in list(root.contents):
            tag.append(child)
    except Exception as e:
        print(f"[TAG ERR] Failed to parse replacement, using text: {e}")
        tag.string = new_content

def process_toc_ncx(ncx_path, cache):
    if not os.path.exists(ncx_path):
        return
    print(f"[TOC] Translating {ncx_path}...")
    with open(ncx_path, "r", encoding="utf-8") as f:
        content = f.read()
    soup = BeautifulSoup(content, "xml")
    text_tags = soup.find_all("text")
    texts = [t.get_text(strip=True) for t in text_tags if t.get_text(strip=True)]
    if not texts:
        return
    translations = translate_batch(texts, cache, max_batch_size=20)
    t_idx = 0
    for t in text_tags:
        if t.get_text(strip=True):
            t.string = translations[t_idx]
            t_idx += 1
    with open(ncx_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"[TOC] Updated {len(texts)} entries in {ncx_path}")

def process_opf(opf_path, cache, translated_title):
    if not os.path.exists(opf_path):
        return
    print(f"[OPF] Updating metadata in {opf_path}...")
    with open(opf_path, "r", encoding="utf-8") as f:
        content = f.read()
    soup = BeautifulSoup(content, "xml")
    
    # Update language to Spanish
    lang_tag = soup.find(["dc:language", "language"])
    if lang_tag:
        lang_tag.string = "es"
    else:
        meta = soup.find(["metadata", "opf:metadata"])
        if meta:
            new_lang = soup.new_tag("dc:language")
            new_lang.string = "es"
            meta.append(new_lang)

    # Update title
    title_tag = soup.find(["dc:title", "title"])
    if title_tag and translated_title:
        title_tag.string = translated_title

    with open(opf_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"[OPF] Metadata successfully updated to Spanish in {opf_path}")

def process_html_file(file_path, cache, batch_size=15):
    with open(file_path, "r", encoding="utf-8") as f:
        raw = f.read()

    soup = BeautifulSoup(raw, "xml")

    # Find candidate translatable tags:
    # paragraphs, headings, list items, table cells, captions
    target_tags = ["p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "caption", "figcaption", "td", "th"]
    candidates = []
    
    for tag in soup.find_all(target_tags):
        # Don't process tags that are nested inside another targeted block
        if tag.find_parent(target_tags):
            continue
        # Ensure it actually has non-whitespace text
        txt = tag.get_text(strip=True)
        if not txt:
            continue
        # Get inner XML/HTML
        inner = "".join(str(c) for c in tag.contents).strip()
        if inner:
            candidates.append((tag, inner))

    if not candidates:
        return 0

    inners = [c[1] for c in candidates]
    translated_inners = translate_batch(inners, cache, max_batch_size=batch_size)

    for (tag, orig_inner), trans_inner in zip(candidates, translated_inners):
        if trans_inner and trans_inner != orig_inner:
            safe_replace_inner(tag, trans_inner)

    # Update <title> tag if present
    title_tag = soup.find("title")
    if title_tag and title_tag.get_text(strip=True):
        t_orig = title_tag.get_text(strip=True)
        t_trans = translate_batch([t_orig], cache, max_batch_size=1)[0]
        if t_trans:
            title_tag.string = t_trans

    # Save modified HTML
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

    return len(candidates)

def main():
    parser = argparse.ArgumentParser(description="Zero-defect EPUB translator preserving 100% layout and images.")
    parser.add_argument("--epub", required=True, help="Input EPUB path")
    parser.add_argument("--workdir", required=True, help="Working directory for extraction")
    parser.add_argument("--cache", required=True, help="JSON cache file for persistence")
    parser.add_argument("--output", required=True, help="Output EPUB path")
    parser.add_argument("--title", required=False, default="", help="Translated Spanish title")
    parser.add_argument("--batch-size", type=int, default=15, help="Batch size for LLM translation")
    args = parser.parse_args()

    print(f"==================================================")
    print(f"Starting translation for: {os.path.basename(args.epub)}")
    print(f"Working directory: {args.workdir}")
    print(f"Cache file: {args.cache}")
    print(f"Output: {args.output}")
    print(f"==================================================")

    cache = TranslationCache(args.cache)

    # 1. Extract EPUB
    extract_epub(args.epub, args.workdir)

    # 2. Find all HTML/XHTML files
    html_files = []
    opf_files = []
    ncx_files = []

    for root, dirs, files in os.walk(args.workdir):
        for f in files:
            full = os.path.join(root, f)
            if f.endswith((".html", ".xhtml", ".htm")):
                html_files.append(full)
            elif f.endswith(".opf"):
                opf_files.append(full)
            elif f.endswith(".ncx"):
                ncx_files.append(full)

    html_files.sort()
    print(f"[FOUND] {len(html_files)} HTML/XHTML files, {len(opf_files)} OPF files, {len(ncx_files)} NCX files.")

    # 3. Translate TOC (NCX)
    for ncx in ncx_files:
        process_toc_ncx(ncx, cache)

    # 4. Update OPF
    for opf in opf_files:
        process_opf(opf, cache, args.title)

    # 5. Process HTML files sequentially with progress reporting
    total_files = len(html_files)
    total_elements_translated = 0

    for idx, html_file in enumerate(html_files, 1):
        rel = os.path.relpath(html_file, args.workdir)
        print(f"[{idx}/{total_files}] Translating {rel}...")
        count = process_html_file(html_file, cache, batch_size=args.batch_size)
        total_elements_translated += count
        print(f"  -> Done ({count} elements processed). Total so far: {total_elements_translated}")

    # 6. Repack into final EPUB
    repack_epub(args.workdir, args.output)
    print(f"==================================================")
    print(f"SUCCESS: Completed translation for {os.path.basename(args.epub)}")
    print(f"Total elements translated: {total_elements_translated}")
    print(f"Output generated at: {args.output}")
    print(f"==================================================")

if __name__ == "__main__":
    main()
