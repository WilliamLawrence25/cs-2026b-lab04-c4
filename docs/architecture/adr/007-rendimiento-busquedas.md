# ADR-007: Optimización de Búsquedas Masivas en Catálogo

**Estado:** Aceptado (29/10/2026)

## Contexto
El sistema colapsaba (latencia > 4s) al recibir 5000 peticiones de búsqueda concurrentes durante picos de uso (QA-01). Escalar verticalmente el VPS sobrepasaba el presupuesto.

## Decisión
Adoptar la táctica de **Optimizar Consultas** (índices B-Tree en título y autor) y **Caché** en memoria (Redis) con un TTL de 30 segundos.

## Consecuencias
* (+) Reducción drástica del p95 a 0.3 segundos y menor carga de CPU.
* (-) Riesgo asumido (Trade-off): Posibilidad de mostrar disponibilidad de stock temporalmente desactualizada (mitigado al momento de confirmar la reserva).