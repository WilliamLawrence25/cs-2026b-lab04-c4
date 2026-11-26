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

## E3: estados y contrato

- `diseno/estados.puml`: máquina de estados del bucle ReAct.
- `diseno/estados.png`: render del diagrama para revisión e informe.
- `pruebas_agente/test_contrato.py`: decisiones válidas e inválidas para el contrato.
- `pruebas_agente/test_estados.py`: comprueba que la traza registra las transiciones previstas.

Ejecuta `./.venv/bin/pytest -q pruebas_agente` desde la raíz para validar E3. Para el informe, captura el diagrama de estados y el resultado de las pruebas de contrato.

![Máquina de estados del agente ReAct](diseno/estados.png)

## E4: mapa AST y memoria de notas

La herramienta `mapa_repo(ruta)` recorre los módulos Python y presenta clases y firmas de funciones/métodos mediante `ast`. `anotar(texto)` agrega hipótesis o archivos revisados a `agentes/notas.md`, y `leer_notas()` recupera esas notas.

La prueba del ISSUE-03 se ejecutó antes y después del cambio. La trayectoria y la traza están en `trayectorias/e4-issue-03.json` y `trazas/e4-issue-03.jsonl`; el diagrama de esta ejecución está en `trazas/e4-issue-03.mmd`.

### Comparación observada con E2

| Medida | E2 — ISSUE-01 | E4 — ISSUE-03 |
| :--- | ---: | ---: |
| Decisiones del agente | 9 | 9 |
| Caracteres del contexto final | 9,969* | 10,686 |

En esta ejecución E4 no redujo los pasos y el contexto final fue 717 caracteres (7.2 %) mayor. El valor marcado con * para E2 se reconstruyó del contexto interactivo guardado en la sesión, pues E2 aún no registraba ese contador. Como los ejercicios resolvieron issues distintos, la comparación es descriptiva, no un experimento controlado. El mapa AST permitió localizar la clase y la firma del método; la nota de hipótesis y archivos revisados se guardó y luego se recuperó desde `notas.md`.

Ejecuta `./.venv/bin/pytest -q pruebas_agente tests/test_issue_03_prestamos.py` para validar las nuevas herramientas, la memoria y el arreglo del issue.

Para el informe, captura la salida del mapa AST y de las notas recuperadas, el resultado de las pruebas E4 y el diagrama de secuencia de `e4-issue-03.mmd`.
