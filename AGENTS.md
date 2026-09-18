# Instrucciones de Agente para Traducción Profesional de EPUBs

Este repositorio está configurado como un entorno especializado para la **traducción de libros digitales en formato EPUB a Español Neutro** con estándar de calidad editorial, preservación del 100% del diseño original, estilos CSS, tipografía y todas las imágenes.

---

## 1. Estructura del Repositorio

```text
.
├── AGENTS.md               # Directrices maestras de comportamiento para el agente
├── .gitignore              # Excluye binarios .epub, venvs y carpetas temporales
├── .agents/                # Configuración de agente para Antigravity / agy
│   ├── rules/              # Reglas activas por contexto
│   └── skills/             # Habilidades reusables (epub-translator)
├── originales/             # Coloca aquí los archivos .epub originales en inglés
├── traducidos/             # Salida final de los archivos .epub traducidos [Español]
├── cache/                  # Memorias de traducción persistentes en JSON (SHA-256)
├── scripts/                # Motores de traducción y empaquetado IDPF
│   ├── translate_book.py   # Orquestador CLI principal de traducción
│   └── translator_engine.py# Motor LLM, manejo de lotes, caché y empaquetado ZIP
└── .venv/                  # Entorno virtual con dependencias (BeautifulSoup4, lxml, Pillow)
```

---

## 2. Protocolo de Acción cuando el Usuario Pide Traducir un Libro

Cuando el usuario te solicite traducir uno o más libros en este espacio, sigue **siempre** este protocolo estricto:

### Paso 1: Inspección, Diagnóstico e Investigación Editorial
1. **Inspección del EPUB:**
   - Verifica los archivos `.epub` disponibles en `originales/` (o en la raíz). Si están en la raíz, muévelos a `originales/`.
   - Inspecciona la estructura interna: número de archivos XHTML/HTML, número de imágenes y conteo estimado de palabras.
2. **Investigación de Traducción Oficial Publicada:**
   - Busca en la web y catálogos bibliográficos si el libro ya cuenta con una **traducción oficial al español** publicada por alguna editorial reconocida.
   - **Jerarquía de variantes regionales:**
     1. *Prioridad 1:* Edición en Español Neutro o publicada para Latinoamérica / Hispanoamérica (con preferencia en ediciones de México o Argentina).
     2. *Prioridad 2:* Edición publicada en España, únicamente si no existe una edición para Latinoamérica.
   - **Extracción de criterios editoriales:** Si encuentras la edición oficial, identifica:
     - El título oficial comercial registrado.
     - Los títulos oficiales de los capítulos e índice.
     - La forma en que la editorial tradujo los conceptos clave, nombres de métodos y términos propios del autor.
     - El tono y estilo (registro de tuteo, formalidad, naturalidad).
3. **Plan de Ejecución:** Informa al usuario sobre la extensión del libro, si se localizó una edición oficial de referencia y el plan de traducción.

### Paso 2: Ejecución del Pipeline con Checkpoints
1. Usa el script modular [scripts/translate_book.py](file:///home/lk/epub/scripts/translate_book.py) con el entorno virtual `.venv`.
2. **Parámetros requeridos:**
   - `--epub`: Ruta al archivo original.
   - `--workdir`: Carpeta de trabajo temporal (ej. `work_<nombre>`).
   - `--cache`: Archivo JSON en `cache/cache_<nombre>.json` para persistencia.
   - `--output`: Destino en `traducidos/<Nombre del Libro> [Español].epub`.
   - `--title`: Título oficial traducido al español.
   - `--batch-size`: Tamaño de lote recomendado: `15` para equilibrio entre velocidad y contexto.
3. Si el libro es extenso (>50.000 palabras), ejecuta el comando en segundo plano con `run_command` y monitoriza el progreso mediante `manage_task` o el archivo de log.

### Paso 3: Verificación Automática Post-Traducción
Antes de dar la tarea por finalizada, ejecuta una verificación de integridad:
1. **Estándar IDPF:** Verificar que `mimetype` sea el primer archivo en el ZIP y esté sin compresión (`ZIP_STORED`).
2. **Conteo de imágenes:** Comprobar que el número de imágenes en el EPUB traducido coincida exactamente con el original.
3. **Validación XML/XHTML:** Asegurar que los archivos XHTML parseen correctamente sin tags rotos ni entidades corruptas.
4. **Muestra de lectura:** Extraer un fragmento traducido para verificar la naturalidad del español neutro.

### Paso 4: Limpieza
Elimina la carpeta temporal de trabajo (`work_*`) para no consumir espacio en disco, pero **conserva siempre el archivo en `cache/`** para mantener la memoria de traducción.

---

## 3. Principios Inquebrantables de Calidad

* **Cero pérdida visual:** Ninguna etiqueta `<img>`, clase CSS o enlace interno (`<a href="...">`, `<a id="...">`) debe ser eliminada o alterada.
* **Español Neutro:** Utiliza un léxico internacional comprensible tanto en Latinoamérica como en España, evitando giros regionales exclusivos de un solo país.
* **Consistencia Terminológica:** Respeta los glosarios de la materia del libro (en libros de etología/adiestramiento canino: *detonante*, *umbral*, *reforzador funcional*, *señales de calma/corte*).
