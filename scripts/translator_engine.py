import os
import sys
import json
import hashlib
import zipfile
import subprocess
import time
import re
from bs4 import BeautifulSoup

GLOSSARY_PROMPT = """Eres un traductor profesional de libros especializado en etología canina, adiestramiento respetuoso y modificación de conducta (en particular el método BAT - Behavior Adjustment Training).
Tu tarea es traducir al ESPAÑOL NEUTRO una lista de fragmentos de texto extraídos de un libro EPUB.

CRITERIOS OBLIGATORIOS:
1. ESPAÑOL NEUTRO: Usa un registro claro, natural y accesible para cualquier hispanohablante de América Latina o España. Usa "tú" si el autor se dirige al lector, pero sin modismos locales (evita regionalismos de un solo país).
2. TERMINOLOGÍA CANINA ESPECIALIZADA:
   - "Behavior Adjustment Training (BAT)" -> "Entrenamiento de Ajuste Conductual (BAT)" (mantén la sigla BAT).
   - "trigger" -> "detonante" o "estímulo desencadenante".
   - "threshold" / "under threshold" / "over threshold" -> "umbral" / "por debajo del umbral (sub-umbral)" / "por encima del umbral".
   - "functional reward" -> "reforzador funcional" o "recompensa funcional".
   - "cut-off cues" / "calming signals" -> "señales de corte" / "señales de calma".
   - "displacement behaviors" -> "conductas de desplazamiento".
   - "reactivity" -> "reactividad".
   - "leash handling" -> "manejo de la correa".
   - "loose leash" -> "correa floja / relajada".
   - "desensitization" / "counterconditioning" -> "desensibilización" / "contracondicionamiento".
3. ETIQUETAS HTML Y FORMATO:
   - Conserva EXACTAMENTE intactas todas las etiquetas HTML internas si las hay (como <i>, </i>, <b>, </b>, <span>, </span>, <a ...>, </a>, <small>, etc.).
   - No elimines ni modifiques atributos HTML como id, class o href.
   - Solo traduce el texto humano contenido en ellas o a su alrededor.
4. FORMATO DE SALIDA ESTRICTO:
   - Debes devolver ÚNICAMENTE un arreglo JSON válido de cadenas (array of strings), exactamente con la misma cantidad de elementos que la entrada.
   - Sin texto introductorio, sin explicaciones, sin bloques ```json. Solo el arreglo JSON crudo.
"""

def get_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

class TranslationCache:
    def __init__(self, cache_file):
        self.cache_file = cache_file
        self.data = {}
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception as e:
                print(f"[CACHE] Error loading {cache_file}: {e}")
                self.data = {}

    def get(self, text):
        h = get_hash(text)
        return self.data.get(h)

    def set(self, text, translated):
        h = get_hash(text)
        self.data[h] = translated

    def save(self):
        tmp_file = self.cache_file + ".tmp"
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=1)
        os.replace(tmp_file, self.cache_file)

def call_llm(prompt_text, retries=3):
    cmd = [
        "agy",
        "--model", "gemini-3.8-flash-low",
        "--effort", "low",
        "--print", prompt_text
    ]
    for attempt in range(retries):
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if res.returncode == 0:
                raw = res.stdout.strip()
                # Clean possible markdown wrapping
                if raw.startswith("```"):
                    lines = raw.splitlines()
                    if lines[0].startswith("```"):
                        lines = lines[1:]
                    if lines and lines[-1].startswith("```"):
                        lines = lines[:-1]
                    raw = "\n".join(lines).strip()
                # Find the JSON array
                start = raw.find("[")
                end = raw.rfind("]")
                if start != -1 and end != -1 and end > start:
                    json_str = raw[start:end+1]
                    return json.loads(json_str)
            print(f"[LLM WARN] Attempt {attempt+1} failed: {res.stderr.strip() or res.stdout.strip()[:100]}")
        except Exception as e:
            print(f"[LLM ERR] Attempt {attempt+1} exception: {e}")
        time.sleep(2 * (attempt + 1))
    return None

def translate_batch(texts, cache, max_batch_size=15):
    """
    Translates a list of texts using the cache and batching with the LLM.
    """
    results = [None] * len(texts)
    missing_indices = []
    missing_texts = []

    for idx, t in enumerate(texts):
        cached = cache.get(t)
        if cached is not None:
            results[idx] = cached
        else:
            missing_indices.append(idx)
            missing_texts.append(t)

    if not missing_texts:
        return results

    # Process missing in batches
    for i in range(0, len(missing_texts), max_batch_size):
        chunk_indices = missing_indices[i:i+max_batch_size]
        chunk_texts = missing_texts[i:i+max_batch_size]

        prompt = (
            GLOSSARY_PROMPT + "\n\n"
            f"Traduce este arreglo JSON de {len(chunk_texts)} elementos al español neutro:\n"
            + json.dumps(chunk_texts, ensure_ascii=False)
        )

        translated_chunk = call_llm(prompt)
        if translated_chunk and len(translated_chunk) == len(chunk_texts):
            for orig, trans, full_idx in zip(chunk_texts, translated_chunk, chunk_indices):
                cache.set(orig, trans)
                results[full_idx] = trans
            cache.save()
        else:
            print(f"[WARN] Batch of {len(chunk_texts)} failed or length mismatch. Translating one by one...")
            for orig, full_idx in zip(chunk_texts, chunk_indices):
                single_prompt = (
                    GLOSSARY_PROMPT + "\n\n"
                    "Traduce este arreglo JSON de 1 elemento al español neutro:\n"
                    + json.dumps([orig], ensure_ascii=False)
                )
                single_res = call_llm(single_prompt)
                if single_res and len(single_res) == 1:
                    cache.set(orig, single_res[0])
                    results[full_idx] = single_res[0]
                else:
                    print(f"[ERROR] Failed translating: {orig[:40]}...")
                    results[full_idx] = orig  # Fallback to original text if absolute failure
            cache.save()

    return results

def repack_epub(source_dir, output_epub_path):
    """
    Repacks an extracted EPUB directory into a standard-compliant EPUB file.
    The 'mimetype' file MUST be stored first without compression.
    """
    if os.path.exists(output_epub_path):
        os.remove(output_epub_path)

    with zipfile.ZipFile(output_epub_path, "w") as zout:
        # 1. mimetype first, uncompressed
        mimetype_path = os.path.join(source_dir, "mimetype")
        if os.path.exists(mimetype_path):
            zout.write(mimetype_path, "mimetype", compress_type=zipfile.ZIP_STORED)

        # 2. All other files compressed
        for root, dirs, files in os.walk(source_dir):
            for f in sorted(files):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, source_dir)
                if rel_path == "mimetype":
                    continue
                zout.write(full_path, rel_path, compress_type=zipfile.ZIP_DEFLATED)

    print(f"[REPACK] Created EPUB at {output_epub_path} ({os.path.getsize(output_epub_path)} bytes)")
