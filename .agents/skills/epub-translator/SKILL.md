---
name: epub-translator
description: >-
  Use this skill whenever the user requests to translate, process, inspect, or repackage EPUB digital books into neutral Spanish or other languages while preserving 100% of the original CSS styling, layout, navigation, and embedded images.
---

# EPUB Translation Skill

Esta habilidad proporciona el flujo de trabajo completo para traducir libros digitales en formato `.epub` sustituyendo directamente los nodos de texto en el árbol DOM, garantizando que ninguna imagen, enlace o estilo visual se pierda.

## Flujo de Trabajo

### 1. Preparación del Entorno
Verifica que el entorno virtual `.venv` esté presente con las dependencias requeridas (`beautifulsoup4`, `lxml`, `Pillow`):
```bash
python3 -m venv .venv
.venv/bin/pip install beautifulsoup4 lxml pillow
```

### 2. Búsqueda de Traducción Editorial Oficial
Antes de traducir, investiga si la obra cuenta con una traducción oficial publicada en español:
1. Buscar en la web por título original, autor, editorial e ISBN en español.
2. **Jerarquía regional:**
   - *Prioridad 1:* Español neutro o ediciones para América Latina (México, Argentina, etc.).
   - *Prioridad 2:* Edición de España (solo si no existe edición latinoamericana).
3. Extraer el título oficial, índice de capítulos y glosario de términos clave usados por la editorial para alinearse con su estilo.

### 3. Ejecutar la Traducción
Ejecuta el script orquestador [scripts/translate_book.py](file:///home/lk/epub/scripts/translate_book.py):
```bash
.venv/bin/python scripts/translate_book.py \
  --epub "originales/<nombre_libro>.epub" \
  --workdir "work_<nombre>" \
  --cache "cache/cache_<nombre>.json" \
  --output "traducidos/<nombre_libro> [Español].epub" \
  --title "<Título traducido>" \
  --batch-size 15
```

### 4. Validación del Archivo Resultante
Ejecuta una verificación rápida de integridad del archivo generado:
- Primer archivo en el archivo ZIP: `mimetype` sin compresión (`ZIP_STORED`).
- Conteo de imágenes igual al original.
- Cero etiquetas huérfanas en el XHTML.

### 5. Limpieza
Elimina la carpeta temporal de trabajo `work_*`:
```bash
rm -rf work_<nombre>
```
Conserva siempre el archivo en `cache/` para que la memoria de traducción sirva para futuras revisiones o reediciones.

---

## Técnicas Avanzadas de Calidad Editorial
* **Ciclo de Reflexión (Andrew Ng / Translation-Agent):** Para fragmentos complejos, evaluar borrador -> autocrítica de naturalidad y calcos sintácticos -> refinamiento final.
* **Memoria de Contexto Móvil (*Handoff Reports*):** Persistir decisiones terminológicas clave entre capítulos para que el tono sea uniforme desde el primer hasta el último capítulo.
* **Presupuesto de Atención Terminológica:** Usar glosarios delimitados y precisos en las instrucciones de sistema (`system instructions`).
