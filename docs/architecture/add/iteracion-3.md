# Iteración 3: Seguridad y Aislamiento entre Facultades

**Objetivo:** QA-04 - Un usuario de la Facultad A no puede acceder a reservas de la Facultad B modificando la URL -> 100% bloqueos.
**Elemento a refinar:** Capa de datos y autorización.

## Conceptos de Diseño Evaluados (Evidencia: Comparación)

| Alternativa Multitenencia | Aislamiento | Costo Operativo | Decisión |
| :--- | :--- | :--- | :--- |
| **1 BD por Facultad** | Máximo | Muy Alto (mantener 20+ bases de datos en un VPS es inviable). | **Rechazada** |
| **1 Esquema por Facultad** | Alto | Alto (las migraciones se complican). | **Rechazada** |
| **Columna `facultad_id` + Row-Level Security (RLS) + JWT** | Alto | Bajo (Todo nativo en PostgreSQL). | **Aceptada** |

## Decisión y Mitigación de Riesgos
Se adopta **Row-Level Security (RLS)** en PostgreSQL. Al decodificar el JWT del estudiante en la API, se extrae su `facultad_id` y se inyecta en la sesión de base de datos. PostgreSQL filtra automáticamente las filas a nivel de motor.

* **Mitigación de riesgo:** La IA detectó en la evaluación (E3) que un RLS mal configurado expone datos. Esto se mitigará en el E5 creando una *Fitness Function* que ejecute consultas cruzadas obligando a que retornen error.

**Conclusión:** Se cumple el escenario QA-04, garantizando el aislamiento mediante tácticas de "Limitar acceso".