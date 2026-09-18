---
name: epub-qa-verifier
description: >-
  Use this skill after generating a translated EPUB to execute a comprehensive quality assurance audit: IDPF standard compliance, image and asset parity, intra-book hyperlink integrity, mojibake/encoding corruption detection, and text expansion ratio checks.
---

# EPUB Quality Assurance (QA) & Verification Skill

Esta habilidad define la auditoría técnica post-traducción para certificar que el archivo `.epub` final cumple con los más altos estándares editoriales antes de entregarse.

## Lista de Comprobaciones Automatizadas (Audit Checklist)

### 1. Validación del Estándar IDPF del Contenedor ZIP
* El archivo `mimetype` debe ser estrictamente el **primer archivo** en el índice ZIP (`namelist()[0] == 'mimetype'`).
* El método de compresión de `mimetype` debe ser **`zipfile.ZIP_STORED` (sin comprimir)**.
* No debe existir compresión ni metadatos adicionales en la cabecera del archivo `mimetype`.

### 2. Paridad 1:1 de Recursos Binarios (Imágenes, Fuentes, Estilos)
* Comprobar que la cantidad y los nombres de archivos de imagen (`.jpg`, `.jpeg`, `.png`, `.svg`, `.gif`, `.webp`) en el EPUB traducido coincidan **exactamente al 100%** con el original.
* Los hashes o tamaños de las imágenes deben ser idénticos (garantizando que ninguna imagen fue reemplazada, comprimida o eliminada).

### 3. Integridad de Hipervínculos Internos e Índices
* Extraer todos los enlaces `<a href="destino.xhtml#ancla">` en los archivos XHTML.
* Verificar que para cada enlace:
  1. El archivo destino exista en el manifiesto.
  2. El identificador del ancla (`id="ancla"`) exista dentro del archivo destino.
  3. No existan enlaces rotos hacia capítulos o notas al pie.

### 4. Detección de Corrupción de Caracteres (*Mojibake*)
* Escanear todos los archivos XHTML en busca de patrones de corrupción comunes causados por malas conversiones UTF-8:
  * `Ã¡`, `Ã©`, `Ã­`, `Ã³`, `Ãº`, `Ã±`, `Â¿`, `Â¡` (Doble codificación UTF-8).
  * `â€™`, `â€œ`, `â€` (Comillas tipográficas o guiones mal decodificados).
  * `&#xFFFD;` o caracteres de reemplazo ``.
* Si se detecta alguno, corregir inmediatamente el juego de caracteres en origen.

### 5. Verificación de Ratio de Expansión Textual
* El español suele ser un **10% a 25% más extenso** en número de palabras que el inglés.
* Si el conteo de palabras de un capítulo traducido es notablemente inferior (ej. más de un 25% menor al original), se activa una alerta: indica que el modelo omitió párrafos o truncó el texto por límite de tokens.
