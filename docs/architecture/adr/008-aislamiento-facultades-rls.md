# ADR-008: Multitenencia y Aislamiento entre Facultades

**Estado:** Aceptado (29/10/2026)

## Contexto
Se requiere garantizar que un estudiante de una facultad no pueda consultar o alterar las reservas de otra facultad, incluso modificando las peticiones a la API (QA-04).

## Decisión
Implementar **Row-Level Security (RLS)** nativo en PostgreSQL. La API extraerá el reclamo `facultad_id` del token JWT del estudiante y lo inyectará en la sesión de base de datos, delegando el filtro al motor de datos.

## Consecuencias
* (+) Aislamiento criptográfico y a nivel de base de datos altamente seguro.
* (+) Evita gestionar y migrar múltiples bases de datos o esquemas por cada facultad.
* (-) Complejidad moderada para probar y depurar las políticas RLS.