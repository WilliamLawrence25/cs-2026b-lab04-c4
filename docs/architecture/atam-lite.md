# Evaluación ATAM-lite (BiblioUNSA)

**Evaluador:** Grupo Simulado (IA Adversaria)
**Objetivo evaluado:** Iteración 1 de ADD (Disponibilidad ante caída de API Académica con Circuit Breaker + Outbox).

## 1. Hallazgos y Respuestas del Equipo

| Tipo | Hallazgo del Evaluador (IA / Otro Grupo) | Respuesta de nuestro equipo |
| :--- | :--- | :--- |
| **Sensibilidad** | El tiempo de sincronización cuando la API regresa depende totalmente de la capacidad de procesamiento (throughput) del *worker* en background. | **Aceptado.** Si el worker procesa 10 req/s, tardará 100 segundos en vaciar una cola de 1000 reservas. Se debe monitorear la métrica de tamaño de cola. |
| **Trade-off** | Disponibilidad vs Consistencia Estricta: Ganan 0 reservas perdidas, pero el usuario no sabe inmediatamente si su reserva es válida académicamente. | **Aceptado.** Es el costo arquitectónico. Lo mitigaremos a nivel de UI mostrando el mensaje: *"Reserva recibida, confirmación pendiente de validación académica"*. |
| **Riesgo R1** | Si la API de la UNSA cae por días, la tabla Outbox crecerá infinitamente llenando el disco del VPS. (Probabilidad: 3, Impacto: 4) | **Aceptado.** Se mitigará implementando un límite de tiempo (TTL) para purgar reservas pendientes mayores a 24 horas y notificar al usuario. |
| **Riesgo R2** | Problemas de concurrencia: si escalan a 2 *workers*, ambos podrían procesar la misma reserva en la cola Outbox. (Probabilidad: 2, Impacto: 5) | **Aceptado.** Para el MVP de 1 mes usamos 1 solo worker. A futuro se mitigará usando `SELECT ... FOR UPDATE SKIP LOCKED` en la base de datos. |
| **No Riesgo** | Sobrecarga de escritura en la base de datos local al guardar las 1000 reservas diferidas en la tabla Outbox. | **Confirmado.** Escribir 1000 filas simples en PostgreSQL toma menos de 1 segundo, no afecta el rendimiento del monolito. |
| **"Riesgo" (Falso Positivo IA)** | "Redis es obligatorio para usar colas de pendientes; PostgreSQL se va a bloquear". | **Rechazado.** Falso positivo por "sesgo hacia la moda". Para 1000 peticiones diarias, la tabla Outbox transaccional de PostgreSQL es más que suficiente y evita añadir la complejidad/costo de mantener un clúster de Redis[cite: 32]. |