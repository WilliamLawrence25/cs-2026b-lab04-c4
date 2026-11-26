# ADR-010: Arquitectura del sistema agéntico

**Estado:** Aceptado (26/11/2026)<br>
**Contexto:** Laboratorio 10 — BiblioUNSA

## Contexto

Los issues de préstamos requieren explorar el repositorio, ejecutar pruebas y proponer cambios acotados. El sistema debe conservar contratos verificables, evitar ediciones fuera de alcance y permitir que una persona supervise cambios antes de aumentar la autonomía. La solución también debe ejecutarse de manera reproducible en las pruebas, sin depender de un proveedor externo de modelos.

## Decisión

Se adopta un agente de código **ReAct** con bucle explícito y máquina de estados. Para cambios sencillos puede actuar un solo agente; cuando se necesita una segunda perspectiva, se coordina un **planificador–ejecutor–revisor actor-crítico**, con el revisor en modo de solo lectura y un máximo de dos rondas. El ejecutor puede activar la aprobación humana por consola antes de cada edición.

El sistema usa un contrato JSON para separar acciones y respuesta final; una política limita herramientas, rutas protegidas, comandos y pasos. El catálogo incluye lectura, búsqueda, mapa AST, memoria de notas, pruebas, diff y edición de archivos. Las grabaciones permiten reproducir decisiones en las pruebas; el historial funciona como memoria de corto plazo y `agentes/notas.md` como memoria persistente de la tarea.

La persona conserva la autoridad sobre las ediciones cuando `aprobar_edicion` está activa, revisa el resultado y decide sobre integración o despliegue. La hoja [agentes/delegacion.md](../../../agentes/delegacion.md) define los permisos y las evidencias requeridas para pasar por los roles ejecutor, revisor, colaborador y gobernador.

## Alternativas consideradas

| Alternativa | Motivo de descarte |
|---|---|
| Flujo fijo sin agente | Es más simple, pero no permite que el asistente elija herramientas en función de las observaciones del repositorio. Sigue siendo preferible para procesos completamente estables. |
| Agente único para todos los cambios | Reduce rondas y contexto, pero en ISSUE-02 pasó por alto una regresión con `validador=None`; se conserva para tareas pequeñas, no como única salvaguarda. |
| Múltiples agentes con edición libre | Aumentaría cambios concurrentes y riesgo de efectos secundarios difíciles de atribuir; se limita el revisor a lectura y el ejecutor a una tarea acotada. |
| Aprobación humana desactivada siempre | Hace las pruebas no interactivas, pero no ofrece control al integrante antes de una edición; se mantiene disponible como opción para demostración y producción supervisada. |
| LLM remoto en todas las pruebas | Introduce coste, credenciales, latencia y no determinismo; se usan decisiones grabadas para las pruebas repetibles y el modelo interactivo para la sesión manual. |

## Consecuencias

**Positivas**

- Los estados, decisiones, herramientas y resultados quedan registrados en trazas inspeccionables.
- La política aplica mínimo privilegio y las pruebas reproducen las trayectorias sin credenciales.
- El revisor encontró una incompatibilidad real que la prueba principal no cubría; la aprobación humana añade control explícito sobre cada edición.

**Costes y límites**

- La coordinación de ISSUE-02 necesitó 13 acciones y acumuló 28.009 caracteres de contexto frente a 6 acciones y 8.996 caracteres del agente único; el total multiagente agrega cinco historiales y no es una comparación por llamada equivalente.
- La revisión humana añade pausas y el registro de decisiones requiere mantenimiento.
- Las decisiones grabadas verifican el flujo del agente, no la calidad general de un modelo LLM en vivo. Los límites de política no sustituyen una revisión humana ni controles del sistema operativo.
