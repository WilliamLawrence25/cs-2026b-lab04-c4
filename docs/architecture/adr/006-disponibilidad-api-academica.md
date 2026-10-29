# ADR-006: Disponibilidad ante fallas del Sistema Académico

**Estado:** Aceptado (29/10/2026)

## Contexto
Durante la matrícula, la API de la UNSA suele caer o saturarse, lo que en la arquitectura original provocaba la pérdida inmediata de la reserva de libros (QA-02).

## Decisión
Implementar un patrón **Circuit Breaker** para cortar rápidamente las llamadas a la API caída, combinado con una táctica de **Cola de pendientes (Outbox)** en la base de datos local. Un componente asíncrono (Worker) procesará las reservas cuando el servicio se restablezca.

## Consecuencias
* (+) Cero reservas perdidas ante caídas (demostrado en simulación).
* (+) Evita ataques de denegación de servicio a la API académica.
* (-) Cambia la consistencia estricta por consistencia eventual (el estudiante debe esperar la confirmación final).