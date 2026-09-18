# Regla de Resiliencia, Lotes y Tolerancia a Fallos

Esta regla establece las pautas de ingeniería para procesar libros sin pérdida de información ni consumo innecesario de recursos.

## 1. Memoria de Traducción Persistente (Caché SHA-256)

1. Cada fragmento de texto o nodo traducido debe ser indexado por su hash SHA-256 en un archivo de caché persistente dentro de `cache/`.
2. Si el proceso de traducción se cancela, se interrumpe la red o se detiene el sistema, la reanudación debe consultar la caché para reutilizar instantáneamente todos los fragmentos previamente completados.
3. El archivo de caché debe guardarse de forma segura mediante escritura en archivo temporal y reemplazo atómico (`os.replace`).

## 2. Procesamiento por Lotes y Fallbacks

1. **Tamaño de Lote Óptimo:** Agrupar los fragmentos en lotes de 10 a 20 párrafos para mantener velocidad y contexto lingüístico sin exceder límites de tokens.
2. **Reintentos con Backoff:** Ante cualquier respuesta inválida del LLM o fallo temporal, reintentar con espera exponencial.
3. **Desglose Progresivo (Fallback):** Si un lote completo de 15 párrafos genera un error de parsing o discrepancia de longitud, el sistema debe automáticamente degradar y procesar los elementos uno por uno o en sub-lotes de 3-5, asegurando que ninguna sección quede bloqueada.
