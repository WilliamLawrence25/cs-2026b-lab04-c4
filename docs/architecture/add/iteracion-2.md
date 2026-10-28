# Iteración 2: Rendimiento en búsquedas masivas

**Objetivo:** QA-01 - 5000 alumnos buscan libros a la vez en la biblioteca virtual -> p95 de latencia <= 1.5 s.
**Elemento a refinar:** `Catálogo` y Base de Datos principal.

## Conceptos de Diseño Evaluados

1. **Escalamiento Vertical (Subir CPU/RAM del VPS):**
   * *Propuesta:* Aumentar los recursos del servidor para procesar más rápido.
   * *Decisión:* **Rechazada**. Viola la restricción de presupuesto (costo mensual alto) y no resuelve el cuello de botella de I/O en la base de datos.
2. **Índices en BD + Caché (Redis):**
   * *Propuesta:* Aplicar táctica "Optimizar consultas" (índice B-Tree en título/autor) y táctica "Caché" (Redis con TTL de 30s) para las búsquedas más comunes.
   * *Decisión:* **Aceptada**. Mejora radicalmente el rendimiento con costo de infraestructura casi nulo. Genera el riesgo de mostrar stock temporalmente desactualizado (Trade-off aceptado).

## Evidencia (Simulación M/G/c)
Se adaptó el script de simulación de rendimiento (`fitness/rendimiento.py`) para el pico de 5000 peticiones:
* **Sin tácticas:** p95 = 4.2 s (Satura el sistema).
* **Solo Índices:** p95 = 1.2 s (Cumple el objetivo, pero deja la CPU al 85%).
* **Índices + Caché (80% hits):** p95 = 0.3 s (CPU relajada al 30%).

**Conclusión:** Se cumple ampliamente el escenario QA-01 adoptando Índices y Caché.