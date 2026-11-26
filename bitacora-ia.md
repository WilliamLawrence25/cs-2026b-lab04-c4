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

## 3. Registro de interacciones — Laboratorio 10

| # | Interacción con el asistente | Hallazgo o error observado | Decisión y evidencia |
| :---: | :--- | :--- | :--- |
| **1** | Solicitar la implementación del E2 para ISSUE-01 y verificar el comportamiento antes y después. | La prueba específica reprodujo que el cálculo incluía domingos en los días de atraso. | Se ajustó el cálculo para excluir domingos; la trayectoria y traza están en `agentes/trayectorias/e2-issue-01.json` y `agentes/trazas/e2-issue-01.jsonl`. |
| **2** | Solicitar E3: máquina de estados, contrato estructurado y pruebas. | La revisión comprobó que las decisiones del protocolo debían distinguirse entre válidas e inválidas y que la traza debía registrar transiciones. | Se añadieron y ejecutaron pruebas de contrato y estados; el resultado quedó registrado en el historial del laboratorio y en `pruebas_agente/`. |
| **3** | Solicitar E4 con una herramienta de mapa AST y memoria de notas, usando ISSUE-03. | La prueba del issue permitió verificar que un préstamo devuelto no debía permanecer vencido; mapa y notas aportaron evidencia de la exploración. | Se mantuvieron `mapa_repo`, `anotar` y `leer_notas`; las evidencias están en `agentes/trayectorias/e4-issue-03.json` y `agentes/trazas/e4-issue-03.jsonl`. |
| **4** | Solicitar E5 comparando agente único y actor-crítico sobre ISSUE-02. | **Error detectado por el revisor:** el agente único validó el caso principal, pero su llamada incondicional a `validador.esta_matriculado` fallaba cuando `validador=None`. | Se rechazó la primera solución coordinada y se añadió la comprobación opcional. En la segunda ronda aprobaron las dos pruebas; consultar `agentes/trazas/e5-revisor-r1.jsonl` y `e5-revisor-r2.jsonl`. |
| **5** | Solicitar E6 para que las ediciones del ejecutor requirieran aprobación humana y definir niveles de delegación. | La política debía bloquear ediciones rechazadas, pedir una respuesta válida y dejar evidencia verificable de la decisión. | Se agregaron pruebas de aprobación, rechazo y respuesta inválida, y se registraron aprobaciones de las dos rondas en `agentes/trazas/e6-ejecutor-r1.jsonl` y `e6-ejecutor-r2.jsonl`. |

Las interacciones 1–5 corresponden al trabajo de los ejercicios y se respaldan con las pruebas, trayectorias o trazas mencionadas; la cuarta registra explícitamente una regresión encontrada por el revisor y corregida antes de aprobar el cambio.