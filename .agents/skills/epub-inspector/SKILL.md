---
name: epub-inspector
description: >-
  Use this skill before translating an EPUB to detect and diagnose edge cases: fixed-layout, DRM or encrypted fonts, malformed XML, unclosed tags, non-UTF8 encodings, and complex structures like MathML or SVG text.
---

# EPUB Pre-Translation Inspector & Edge Case Diagnostics

Esta habilidad proporciona el protocolo para inspeccionar archivos `.epub` antes de procesarlos, detectando anomalías que podrían causar fallos durante la extracción o traducción.

## Casos Borde y Cómo Resolverlos

### 1. Detección de DRM y Recursos Cifrados
* **Qué buscar:** Presencia de `META-INF/encryption.xml` o `META-INF/rights.xml`.
* **Diagnóstico:** Si contiene etiquetas `<EncryptedData>` para archivos HTML, el libro tiene DRM y debe ser desprotegido por el usuario antes de procesarlo. Si solo cifra fuentes tipográficas (algoritmos IDPF/Adobe de ofuscación de fuentes), los archivos XHTML pueden traducirse sin inconvenientes.

### 2. Formato: *Reflowable* (Redimensionable) vs *Fixed-Layout* (Diseño Fijo)
* **Qué buscar:** En `content.opf`, buscar:
  `<meta property="rendition:layout">pre-paginated</meta>`
* **Manejo:**
  - *Reflowable:* Estándar habitual (novelas, manuales). El texto puede expandirse libremente.
  - *Fixed-Layout:* Libros infantiles o cómics donde el texto tiene coordenadas fijas (`top`, `left` absolutos). Al traducir al español (que se expande un 15-20%), se debe cuidar que las fuentes no desborden los contenedores contenedores CSS.

### 3. Codificaciones de Caracteres y BOM
* **Problema:** Archivos guardados en Windows-1252, ISO-8859-1 o UTF-8 con BOM (`\xef\xbb\xbf`).
* **Solución:** Leer siempre con `encoding="utf-8-sig"` o decodificar con fallback para convertir internamente todo a UTF-8 puro sin BOM antes de parsear con BeautifulSoup o lxml.

### 4. Etiquetas XHTML Malformadas o No Cerradas
* **Problema:** En HTML clásico, etiquetas como `<br>`, `<hr>`, `<col>`, `<img>` no requieren cierre. En XHTML (obligatorio en EPUB), deben ser autocerradas (`<br/>`, `<hr/>`, `<img ... />`).
* **Solución:** Usar `BeautifulSoup(content, "xml")`. Si el parser XML estalla por sintaxis rota del editor original, sanitizar primero con `html.parser` y luego serializar como XML bien formado.

### 5. Notas al Pie y Enlaces Bidireccionales
* **Estructura EPUB 3:** `<a epub:type="noteref" href="#fn1">1</a>` y `<aside epub:type="footnote" id="fn1">`.
* **Regla:** Solo traducir el texto dentro de `<aside>`, preservando de forma inviolable los atributos `id`, `epub:type` y `href`.
