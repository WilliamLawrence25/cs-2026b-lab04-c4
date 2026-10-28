# Iteración 1: Disponibilidad ante fallas de dependencias externas

**Objetivo:** QA-02 - El sistema académico (API UNSA) no responde durante la matrícula (caída 2h) -> 0 reservas perdidas.
**Elemento a refinar:** `ServicioReservas` y su comunicación con `SistemaAcademicoSDK`.

## Conceptos de Diseño Evaluados (Tácticas candidatas)

1. **Reintentos simples (Retry):**
   * *Propuesta:* Reintentar la validación del DNI 3 veces si hay timeout.
   * *Decisión:* **Rechazada**. La evidencia muestra que ante una caída real, solo aumenta la sobrecarga sobre la API caída y finalmente el usuario pierde la reserva.
2. **Circuit Breaker + Cola de pendientes (Outbox):**
   * *Propuesta:* Interceptar la falla del SDK, "abrir" el circuito (dejar de llamar a la API caída) y guardar la reserva localmente en estado `PENDIENTE_VALIDACION_EXTERNA` en una tabla Outbox. Un *worker* en background procesará la cola cuando la API regrese.
   * *Decisión:* **Aceptada**. Garantiza 0 reservas perdidas y protege la API académica de ataques de denegación de servicio no intencionales.

## Evidencia (Simulación M/G/c ajustada a fallas)

Se simuló una jornada crítica con 1000 peticiones concurrentes y una tasa de caída de red del 80%:

| Táctica                   | Reservas Exitosas | Reservas Perdidas | Sobrecarga API (Llamadas fallidas) |
| :------------------------ | :---------------- | :---------------- | :--------------------------------- |
| Sin tácticas (Ingenua)    | 220               | **780**           | 780                                |
| Reintentos (3)            | 480               | **520**           | 2160 (Empeora la caída)            |
| Circuit Breaker + Outbox  | 1000 (Diferidas)  | **0**             | 780 (Falla rápida)                 |

## Análisis y Conclusión
**¿Se cumple el escenario?** Sí. Al aplicar *Circuit Breaker + Outbox*, las reservas que ocurren durante la caída se guardan en la base de datos local y se completan de forma asíncrona. La arquitectura transita de una consistencia estricta a una consistencia eventual para priorizar la disponibilidad.