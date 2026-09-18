# Regla: Flujos Agénticos Avanzados de Traducción (Reflexión y Memoria de Contexto)

Esta regla incorpora las técnicas más avanzadas de la investigación en traducción con LLMs (inspiradas en *Translation Agent* de Andrew Ng, *TranslateBooksWithLLMs* y *bilingual_book_maker*).

---

## 1. El Ciclo de Reflexión Crítica (Reflection Workflow)

Para secciones densas, pasajes literarios complejos o capítulos cruciales, el agente debe aplicar un ciclo de traducción en tres fases:

1. **Borrador Inicial (Draft):**
   - Traduce el fragmento origen respetando el glosario base y la estructura XML/HTML.
2. **Reflexión y Crítica (Self-Reflection):**
   - El agente evalúa su propio borrador respondiendo a:
     * *¿Se detectan calcos sintácticos del inglés o falsos amigos?*
     * *¿El registro de tuteo en español neutro es 100% homogéneo?*
     * *¿Los modismos e idiotismos se tradujeron por equivalentes naturales o de forma literal?*
     * *¿Se respetó la terminología técnica sin desvíos?*
3. **Refinamiento Final (Improvement):**
   - Se genera la versión final incorporando las correcciones de la fase de reflexión.

---

## 2. Memoria de Contexto Móvil (*Handoff Reports*)

Para mantener la coherencia a lo largo de libros extensos (>50.000 palabras):

1. **Informe de Transferencia entre Capítulos:**
   - Al concluir cada capítulo o bloque principal, se debe generar y persistir un breve resumen de decisiones editoriales (*Handoff Report*):
     * Lista de nombres de personas, mascotas o lugares y si se adaptaron o mantuvieron.
     * Nuevos términos acuñados por el autor y la traducción elegida.
     * Tratamiento acordado para conceptos ambiguos.
2. **Inyección en el Siguiente Capítulo:**
   - El *Handoff Report* se inyecta como contexto previo en el prompt del siguiente capítulo, garantizando que el estilo y vocabulario del Capítulo 20 sea perfectamente coherente con el del Capítulo 1.

---

## 3. Presupuesto de Atención Terminológica (*Term Attention Budget*)

1. **Calidad sobre Cantidad:** Evitar listas interminables de términos en cada prompt. Limitar el glosario activo al 10–20% de términos verdaderamente críticos para la sección actual.
2. **Formato Determinista:** Presentar los términos en bloques estructurados:
   ```text
   [GLOSARIO ACTIVO]
   Término Original: Traducción Obligatoria (Aclaración contextual)
   ```
3. **Restricción Dura de Sistema:** Las directrices del glosario y preservación de etiquetas deben ubicarse en las instrucciones de sistema (`system instructions`) para evitar que el modelo las ignore o las considere opcionales.
