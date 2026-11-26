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

## E5: comparación de agente único y actor-crítico

Ejecuta ambas variantes desde la raíz del repositorio:

```bash
./.venv/bin/python -m agentes.e5 --variante ambas
```

El modelo grabado reproduce las decisiones sin depender de un servicio externo. El agente único resuelve ISSUE-02 y comprueba su prueba específica. En la variante coordinada, planificador, ejecutor y revisor de solo lectura trabajan en un máximo de dos rondas. La primera solución valida una matrícula vencida, pero el revisor detecta que falla el comportamiento previo cuando `ServicioPrestamos` se crea sin validador; el ejecutor agrega el guard opcional en la segunda ronda.

### Resultados observados

| Medida | Agente único | Actor-crítico |
| :--- | ---: | ---: |
| Rondas | 1 | 2 |
| Acciones de herramienta | 6 | 13 |
| Acciones bloqueadas / decisiones rechazadas por contrato | 0 / 0 | 0 / 0 |
| Contexto final acumulado | 8.996 caracteres | 28.009 caracteres |
| Hallazgo del revisor que el agente único omitió | — | Sí: compatibilidad con `validador=None` |

El agente único pasa la prueba de ISSUE-02, pero su guard incondicional falla la prueba de compatibilidad. El revisor reprodujo ese fallo en la ronda 1; tras el cambio pedido, ambas pruebas pasan (`2 passed`) y la revisión aprueba. El contexto coordinado suma el historial de los cinco participantes y no es una comparación de contexto por llamada directamente equivalente al agente único.

### Conclusión de parsimonia

El agente único necesitó una ronda y seis acciones, por lo que fue la alternativa más parsimoniosa.<br>
Sin embargo, validó únicamente el caso de matrícula vencida y no comprobó la compatibilidad con el validador opcional.<br>
El revisor detectó esta regresión con una prueba de reserva sin validador.<br>
El ejecutor corrigió la condición en la segunda ronda y las dos pruebas terminaron aprobadas.<br>
La coordinación elevó el trabajo a trece acciones y acumuló más contexto entre cinco participantes.<br>
Ese contexto agregado no equivale al historial de una sola llamada y debe interpretarse con cautela.<br>
Para un cambio pequeño puede bastar el agente único; la revisión aporta valor cuando hay comportamiento previo que preservar.

### Evidencias para el informe

- `trayectorias/e5-agente-unico.json` y `trazas/e5-agente-unico.jsonl`: fallo inicial reproducido y prueba específica aprobada tras el cambio.
- `trayectorias/e5-planificador.json`, `e5-ejecutor-r1.json`, `e5-revisor-r1.json`, `e5-ejecutor-r2.json` y `e5-revisor-r2.json`, junto con sus trazas `.jsonl`: decisiones y observaciones de cada rol.
- `resultados/e5-comparacion.json`: métricas por variante y por rol.
- `trazas/e5-agente-unico.mmd` y `trazas/e5-actor-critico.mmd`: diagramas para capturar.
- `../pruebas_agente/test_issue02_compat.py`: regresión de compatibilidad que motivó la segunda ronda.

Para las capturas, ejecuta el comando anterior y captura el resumen de métricas en la terminal; abre `trazas/e5-actor-critico.mmd` y `resultados/e5-comparacion.json` en VS Code; finalmente captura la salida de `./.venv/bin/pytest -q tests/test_issue_02_reservas.py pruebas_agente/test_issue02_compat.py`.

## E6: aprobación humana y delegación progresiva

La política del ejecutor permite activar aprobación por consola antes de cada edición. Ejecuta desde la raíz del repositorio:

```bash
./.venv/bin/python -m agentes.e5 --variante actor-critico --aprobar-ediciones
```

Inspecciona la ruta y los fragmentos que presenta el programa; escribe `s` para aprobar o `n` para rechazar. Otras respuestas no autorizan la edición y la solicitud vuelve a mostrarse. El resultado se registra como evento `aprobacion_humana` en la traza de cada ejecutor. Las pruebas cubren aprobación, rechazo, reintento de respuesta inválida y evidencia en JSONL: `./.venv/bin/pytest -q pruebas_agente/test_aprobacion_edicion.py`.

La hoja [delegacion.md](delegacion.md) describe los permisos del agente y la evidencia requerida para avanzar por los roles ejecutor, revisor, colaborador y gobernador. Para el informe, captura la solicitud en consola con su respuesta y el evento correspondiente de `agentes/trazas/e6-ejecutor-r1.jsonl`; añade la tabla de la hoja de ruta y la salida de las pruebas E6.
