# Regla: Alineación con Traducciones Editoriales Oficiales

Esta regla establece el protocolo obligatorio de investigación editorial previa a la traducción de cualquier obra.

## 1. Protocolo de Investigación Editorial Previa

Antes de iniciar la traducción de cualquier libro en inglés, el agente debe investigar si la obra ya cuenta con una **edición oficial publicada en español**:

1. **Búsqueda Bibliográfica y Web:**
   - Buscar el título original en inglés junto con el autor, términos como `"edición en español"`, `"traducción"`, `"editorial"` y `"ISBN"`.
   - Consultar plataformas editoriales, catálogos (Google Books, Amazon, Casa del Libro, librerías latinoamericanas) o webs oficiales de los autores/editoriales.
2. **Jerarquía Geográfica de Variantes:**
   - **Prioridad 1 (Principal):** Español Neutro o ediciones para Hispanoamérica / Latinoamérica (con preferencia en variantes de amplia difusión como México o Argentina).
   - **Prioridad 2 (Secundaria):** Español de España (Castellano peninsular), a utilizar **únicamente si no existe** una edición publicada para el mercado latinoamericano.
3. **Extracción de Criterios y Huella Editorial:**
   - **Título oficial comercial:** Identificar cómo tituló la editorial la obra en español.
   - **Índice y capítulos:** Verificar cómo se tradujeron los títulos de los capítulos y secciones principales.
   - **Glosario específico de la obra:** Identificar cómo resolvió el traductor oficial los conceptos clave, términos acuñados por el autor o modismos recurrentes.
   - **Voz y registro:** Analizar fragmentos de muestra o extractos publicados para identificar si la editorial empleó tuteo, redacción impersonal o fórmulas específicas.

## 2. Inyección de Criterios en el Pipeline de Traducción

Si se localiza una traducción oficial o sus muestras:
1. Se debe incorporar el glosario editorial y las decisiones terminológicas de dicha traducción dentro de las directrices del motor de traducción.
2. El título del libro en el archivo `.opf` y la portada/portadilla debe respetar el título oficial registrado por la editorial en la región correspondiente.
3. Si la única traducción disponible es de España, se debe tomar como referencia su rigor conceptual y terminológico, pero **neutralizando giros o modismos estrictamente peninsulares** (por ejemplo: convertir *vosotros* o giros locales en un español neutro internacional).
