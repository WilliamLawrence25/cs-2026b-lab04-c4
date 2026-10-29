# Evaluación ATAM-lite (BiblioUNSA)

**Evaluador:** Grupo Simulado (IA Adversaria)
**Objetivos evaluados:** QA-01 (Rendimiento), QA-02 (Disponibilidad), QA-04 (Seguridad).

## 1. Hallazgos y Respuestas del Equipo

| Tipo | Hallazgo del Evaluador | Respuesta de nuestro equipo |
| :--- | :--- | :--- |
| **Sensibilidad** | El tiempo de recuperación post-caída depende del *throughput* del worker asíncrono. | **Aceptado.** Monitorearemos el tamaño de la cola Outbox. |
| **Trade-off** | Rendimiento vs Stock Fresco: La caché de 30s puede mostrar stock fantasma. | **Aceptado.** Se valida el stock real en la base de datos al momento exacto de confirmar la reserva. |
| **Trade-off** | Disponibilidad vs Consistencia Estricta (Circuit Breaker). | **Aceptado.** La UI informará que la confirmación de matrícula está en proceso. |
| **Riesgo R1** | Llenado de disco por cola Outbox infinita si la API académica cae por días. | **Aceptado.** (Prob: 3, Impacto: 4). |
| **Riesgo R2** | Un RLS mal configurado expone reservas de otras facultades. | **Aceptado.** (Prob: 2, Impacto: 5). |
| **No Riesgo** | Sobrecarga por escrituras diferidas en PostgreSQL. | **Confirmado.** PostgreSQL soporta holgadamente las escrituras requeridas. |
| **Falso Positivo** | "Redis es obligatorio para usar colas de pendientes; PostgreSQL se va a bloquear". | **Rechazado.** Para la carga de BiblioUNSA, la tabla Outbox transaccional de PostgreSQL es óptima. |

## 2. Matriz de Riesgos y Mitigaciones (Zona Crítica)

| Riesgo | Probabilidad (1-5) | Impacto (1-5) | Zona | Mitigación (Acción tomada) |
| :--- | :--- | :--- | :--- | :--- |
| **R1: Outbox infinito** | 3 | 4 | **Crítica (12)** | Se programará un TTL en el Worker para purgar o marcar como fallidas las reservas con más de 24h en cola. |
| **R2: Fuga por RLS** | 2 | 5 | **Crítica (10)** | Mitigado implementando la Fitness Function `test_ff04_aislamiento_rls` en el pipeline CI/CD (E5) que bloquea el merge si el RLS falla. |