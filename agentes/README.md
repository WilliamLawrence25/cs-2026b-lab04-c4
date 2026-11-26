# Lab 10 — Sistemas agénticos

## E2: agente ReAct para ISSUE-01

Desde la raíz del repositorio, inicia el modo interactivo:

```bash
./.venv/bin/python -m agentes.agente.ejecutar
```

En cada paso, copia el contexto mostrado al asistente y pega una decisión JSON del protocolo. El agente valida la respuesta, aplica la política y guarda la trayectoria y la traza. No requiere claves de API.

Para generar el diagrama Mermaid desde `agentes/`:

```bash
../.venv/bin/python agente/traza.py
```

Artefactos del E2:

- `trayectorias/e2-issue-01.json`: respuestas y validación del contrato.
- `trazas/e2-issue-01.jsonl`: eventos de ejecución.
- `trazas/e2-issue-01.mmd`: diagrama de secuencia.

Para el informe, captura la salida de la prueba del ISSUE-01 fallando antes del cambio, la prueba aprobada después y el diagrama Mermaid. La suite completa aún incluye ISSUE-02 e ISSUE-03, pendientes de sus respectivos ejercicios.
