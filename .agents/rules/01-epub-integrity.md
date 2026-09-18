# Regla de Integridad Estructural y Formato EPUB (IDPF)

Esta regla aplica a toda operación de extracción, modificación o reempaquetado de archivos `.epub`.

## 1. Preservación del Árbol DOM XHTML

1. **Etiquetas de imagen (`<img>` / `<svg>`):**
   - NUNCA deben eliminarse ni modificarse sus atributos (`src`, `class`, `style`, `width`, `height`).
   - Las imágenes inline dentro de párrafos o listas deben conservarse exactamente en la misma posición relativa respecto al texto traducido.
2. **Atributos de navegación e hipervínculos:**
   - Conservar intactos todos los atributos `id="..."` y etiquetas de anclaje `<a id="..."></a>`. Son marcadores indispensables de paginación e índice.
   - Conservar todos los `href="..."` hacia archivos internos o anclas relativas (ej. `href="../Text/split.html#toc6"`).
3. **Estilos y Tipografías:**
   - Nunca modificar las rutas a las hojas de estilo `<link rel="stylesheet" ...>` ni alterar las clases CSS asignadas a los elementos.

## 2. Empaquetado Estándar IDPF

Al generar el archivo `.epub` comprimido final:
1. El archivo `mimetype` debe situarse obligatoriamente en el **offset 0 del archivo ZIP**.
2. El archivo `mimetype` debe almacenarse **sin compresión** (`compression = zipfile.ZIP_STORED`).
3. Todos los demás archivos (`META-INF/`, `.opf`, `.ncx`, `.xhtml`, `.css`, imágenes, fuentes) deben comprimirse con `ZIP_DEFLATED`.
4. El archivo generado debe validarse asegurando que cualquier lector estándar pueda abrirlo sin errores de sintaxis XML o de archivo corrupto.
