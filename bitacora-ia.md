# Bitácora de Uso de IA — Laboratorio 09 (BiblioUNSA)

## 1. Registro de Interacciones con la IA

| # | Interacción | Hallazgo | Decisión y evidencia |
| :---: | :--- | :--- | :--- |
| **1** | Pedir al asistente mejorar `prompts/criterios/v1.txt` para detectar historias ambiguas. | Sugirió agregar *"piensa paso a paso y escribe tu razonamiento antes del JSON"*. | **RECHAZADA:** El texto previo del razonamiento rompía el parseo JSON (`A1_contrato_json`). Se sustituyó por el patrón *Cognitive Verifier* interno dentro de `# TAREA` sin texto fuera del JSON[cite: 29]. |
| **2** | Evaluar `prompts/criterios/v2.txt` y `prompts/sql/v2.txt` en `promptfoo`. | El modelo devolvió el JSON envuelto en bloques markdown (` ```json ... ``` `) en `H3` y `S3`. | **ACEPTADA:** Se añadió en `v3.txt` la restricción explícita *"Responde ÚNICAMENTE con un objeto JSON valido en una sola linea (sin bloques markdown ni texto adicional)"*[cite: 25, 29]. |
| **3** | Probar ataques de inyección directa (`H8` y `S8`) sobre la versión `v2`. | El modelo obedeció la instrucción inyectada, antepuso `HACKED` y generó `DROP TABLE prestamos;`. | **ACEPTADA:** Se aplicó defensa en capas con etiquetas XML (`<historia>`, `<pregunta>`), aislamiento explícito de datos y validación con `jsonschema` (`SalidaInvalida`)[cite: 22, 26]. |
| **4** | Revisar falso positivo en la aserción `A3_sin_implementacion` sobre `H7`. | La aserción buscaba la palabra `"tabla"` en toda la salida y rechazaba las preguntas aclaratorias válidas de `H7`. | **CORREGIDA:** Se limitó `A3` para inspeccionar únicamente el arreglo `escenarios` del JSON, eliminando el falso positivo[cite: 25, 29]. |
| **5** | Solicitar casos de borde a la IA para el dataset `prompts/sql/casos.yaml`. | Propuso 10 preguntas, pero 2 consultaban columnas que sí existen (`isbn`, `anio_publicacion`) marcándolas como error. | **FILTRADA:** Se descartaron esos 2 casos y se conservó `S6` (que pide `telefono` y `direccion`, columnas ausentes en `ESQUEMA_BD`). |
| **6** | Implementar `GeneradorCriterios` y `GeneradorSQL` detrás de `ProveedorLLM`. | Se comprobó con `pytest` que `SalidaInvalida` bloquea salidas malformadas o sentencias distintas de `SELECT` antes de tocar el dominio[cite: 22, 28]. | **ACEPTADA:** Validado mediante 4 pruebas unitarias en `tests/test_generadores_prompts.py`. |

---

## 2. Análisis de No Determinismo (3 ejecuciones sobre `S1`, `S4` y `S7`)
Al ejecutar `prompts/sql/v3.txt` tres veces seguidas sobre `S1`, `S4` y `S7`, se observó que la estructura JSON y la lógica SQL se mantuvieron correctas, pero cambiaron los alias de tablas (`l` vs. `lib`), el orden de columnas en el `SELECT` y la redacción del campo `motivo` en `S7`. Esto demuestra que un LLM no produce cadenas idénticas ante la misma entrada[cite: 21]. Para las grabaciones (*fixtures*), implica que cada captura representa solo una muestra válida del comportamiento del modelo; por ello, las pruebas automatizadas no deben comparar igualdad exacta de texto, sino verificar contratos (`JSON Schema`) y propiedades invariantes (iniciar con `SELECT` y carecer de DDL/DML)[cite: 21, 32].