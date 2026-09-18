# Traductor Profesional de Libros EPUB a Español Neutro

Herramienta y entorno automatizado para traducir libros digitales en formato `.epub` al español neutro con calidad editorial, **preservando el 100% de las imágenes, maquetación visual, estilos CSS, índices interactivos y notas al pie**.

---

## 📁 Estructura del Proyecto

* **`originales/`**: Coloca aquí los archivos `.epub` en inglés que quieras traducir.
* **`traducidos/`**: Aquí se guardarán automáticamente los libros `.epub` traducidos al español.
* **`scripts/`**: Código en Python encargado de parsear el XML, traducir por lotes y reempaquetar el EPUB.
* **`cache/`**: Memoria de traducción en JSON. Si una traducción se detiene, continúa desde aquí sin repetir trabajo ni gastar tiempo.
* **`.agents/`**: Reglas de estilo y habilidades configuradas para que el asistente de IA traduzca con máxima precisión.

---

## 🚀 Cómo Traducir un Libro

Tienes dos formas muy sencillas de hacerlo:

### Opción 1: Pidiéndoselo al Asistente (La más fácil)
1. Coloca tu archivo `.epub` en la carpeta `originales/`.
2. Escríbele al asistente en el chat:
   > *"Traduce el libro que puse en originales al español neutro."*
3. El agente se encargará de inspeccionar el libro, procesar cada capítulo, mantener todas las imágenes intactas y entregarte el archivo listo en `traducidos/`.

---

### Opción 2: Desde la Terminal (Modo Manual)
Si prefieres ejecutar la traducción tú mismo desde la línea de comandos:

1. **Activa el entorno virtual:**
   ```bash
   source .venv/bin/activate
   ```

2. **Ejecuta el script de traducción:**
   ```bash
   python scripts/translate_book.py \
     --epub "originales/TuLibro.epub" \
     --workdir "work_tulibro" \
     --cache "cache/cache_tulibro.json" \
     --output "traducidos/TuLibro [Español].epub" \
     --title "Título del Libro en Español" \
     --batch-size 15
   ```

3. **Borra la carpeta temporal al terminar:**
   ```bash
   rm -rf work_tulibro
   ```

---

## ✨ Características Principales

* **Cero pérdida de imágenes:** Todas las fotos, dibujos y diagramas se mantienen en su posición exacta y con su resolución original.
* **Español Neutro:** Léxico internacional sin modismos de un solo país, respetando glosarios técnicos (como etología y adiestramiento canino).
* **Compatibilidad Total (Norma IDPF):** Los libros generados abren sin problemas en cualquier lector (Apple Books, Kindle, Kobo, Moon+ Reader, Calibre, etc.).
* **Memoria Persistente:** Puedes pausar o cancelar el proceso en cualquier momento; al volver a ejecutarlo continuará exactamente donde se quedó.
