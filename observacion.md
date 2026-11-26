# E7: Observación y bitácora del sistema agéntico

## Métricas de las trazas de los tres issues

Se contaron como **pasos** todas las decisiones registradas, incluida la respuesta final. Las **acciones** son llamadas a herramientas observadas en JSONL; las herramientas listadas son las distintas utilizadas. Para ISSUE-02, la ejecución coordinada agrega las decisiones y herramientas de planificador, ejecutores y revisores de ambas rondas. El contexto es la suma del historial final de los participantes coordinados. E2 no almacenó ese contador en su trayectoria, por lo que su valor es la reconstrucción documentada en el informe E4.

| Issue / ejecución | Pasos (decisiones) | Rondas | Herramientas utilizadas (acciones) | Decisiones rechazadas por contrato | Acciones bloqueadas | Contexto final |
|---|---:|---:|---|---:|---:|---:|
| ISSUE-01 — E2, agente ReAct | 9 | 1 | `leer_archivo`, `ejecutar_pruebas`, `buscar`, `editar_archivo`, `ver_cambios` (8 acciones) | 0 | 0 | 9.969 caracteres* |
| ISSUE-02 — E5, agente único | 7 | 1 | `leer_archivo`, `ejecutar_pruebas`, `editar_archivo`, `ver_cambios` (6 acciones) | 0 | 0 | 8.996 caracteres |
| ISSUE-02 — E5, actor-crítico | 18 | 2 | `leer_archivo`, `mapa_repo`, `editar_archivo`, `ejecutar_pruebas`, `ejecutar_comando`, `ver_cambios` (13 acciones) | 0 | 0 | 28.009 caracteres** |
| ISSUE-03 — E4, agente ReAct | 9 | 1 | `mapa_repo`, `leer_archivo`, `ejecutar_pruebas`, `anotar`, `editar_archivo`, `ver_cambios`, `leer_notas` (8 acciones) | 0 | 0 | 10.686 caracteres |

\* E2 no guardó el contador de contexto en la trayectoria; se reconstruyó de la sesión y quedó documentado en [agentes/README.md](./agentes/README.md).<br>
\** En la variante coordinada se suman los historiales de cinco participantes; no es una medida equivalente al historial de una sola llamada.

El primer intento del ejecutor en ISSUE-02 pasó la prueba del issue, pero falló una prueba de compatibilidad añadida para `validador=None`. El revisor detectó el problema y solicitó el guard opcional en la primera ronda. La prueba es una ejecución de herramienta normal: no se cuenta como acción bloqueada por la política ni como rechazo del contrato.

## Trayectoria observada: actor-crítico para ISSUE-02

```mermaid
sequenceDiagram
    autonumber
    participant P as Planificador
    participant E as Ejecutor
    participant R as Revisor (solo lectura)
    participant H as Repositorio y pruebas
    P->>H: Lee ISSUE-02 y mapa AST
    P-->>E: Plan: validar antes de reservar; revisar compatibilidad
    E->>H: Ronda 1: agrega validación de matrícula
    E->>H: Ejecuta test_issue_02_reservas.py
    H-->>E: 1 passed
    R->>H: Revisa diff y prueba con ServicioPrestamos() sin validador
    H-->>R: Falla: AttributeError al invocar el validador None
    R-->>E: CAMBIOS SOLICITADOS: proteger validador opcional
    E->>H: Ronda 2: añade guard self.validador is not None
    E->>H: Ejecuta prueba ISSUE-02 y prueba de compatibilidad
    H-->>E: 2 passed
    R->>H: Revisa diff y repite ambas pruebas
    H-->>R: 2 passed; comportamiento compatible
    R-->>P: APROBADO en la ronda 2
```

La secuencia también está disponible como archivo independiente en [agentes/trazas/e5-actor-critico.mmd](./agentes/trazas/e5-actor-critico.mmd). Los conteos de decisiones, herramientas y bloqueos se obtuvieron de las trayectorias y trazas JSONL de E2, E4 y E5; las métricas de coordinación se conservan en [agentes/resultados/e5-comparacion.json](./agentes/resultados/e5-comparacion.json).
