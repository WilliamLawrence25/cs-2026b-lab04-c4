# E6: hoja de ruta de delegación progresiva

La autonomía aumenta solo cuando la evidencia de la etapa anterior demuestra que el agente respeta el alcance, el contrato y las pruebas. En todas las etapas, el agente trabaja en una rama de tarea; no recibe secretos ni puede fusionar o desplegar cambios.

| Etapa y rol humano | Permisos del agente | Evidencia necesaria para avanzar |
|---|---|---|
| **1. Ejecutor** — la persona autora del cambio aprueba cada edición desde la consola. | Leer el issue y el código relacionado, buscar y ejecutar pruebas permitidas. Puede editar archivos de implementación dentro del alcance; cada edición muestra ruta, contenido reemplazado y propuesta, y queda bloqueada si la respuesta no es `s`. No puede editar pruebas, aprobar sus propios cambios ni hacer merge. | En la traza, cada `editar_archivo` tiene un evento `aprobacion_humana` en estado `APROBADA`; no hay ediciones bloqueadas sin explicación; las pruebas del issue reproducen el criterio de aceptación. El rechazo debe dejar el archivo intacto y aparecer como `RECHAZADA`/`BLOQUEADO`. |
| **2. Revisor** — una persona distinta inspecciona el cambio. | Modo de solo lectura: leer, buscar, consultar diff y ejecutar pruebas. No puede editar archivos ni cambiar la política. | Diff limitado al issue; evidencia de pruebas focalizadas aprobadas; revisión confirma el orden de validación y que no se consume inventario ante rechazo. Los hallazgos quedan registrados antes de promover. |
| **3. Colaborador** — el responsable del módulo habilita tareas acotadas. | Puede proponer cambios en implementación, documentación y pruebas dentro de rutas autorizadas por tarea. Cada escritura sigue requiriendo aprobación humana; las pruebas se ejecutan después de editar. Sin acceso a secretos, dependencias externas o acciones de Git de escritura. | Varias tareas consecutivas con trazas completas, aprobaciones explícitas y regresiones cubiertas; el revisor confirma que el agente respetó rutas y límites. Solo entonces se amplían las rutas permitidas en una política nueva y revisada. |
| **4. Gobernador** — el responsable técnico define los límites de autonomía. | Puede ejecutar de forma autónoma acciones previamente permitidas y pruebas en una lista cerrada de rutas. Las ediciones de negocio, cambios de permisos, dependencias, migraciones, merge y despliegue siempre requieren autorización humana explícita. | Trazas auditables sin acciones fuera de política, suite completa aprobada, rollback definido y revisión humana final. La autorización se concede por tarea y puede revocarse; no se infiere de aprobaciones anteriores. |

## Evidencia del E6 en este repositorio

El ejecutor del actor-crítico usa `Politica.aprobar_edicion`. La aprobación solicita `s` o `n`, repite la pregunta ante cualquier otro valor y registra la decisión en la traza como `aprobacion_humana` (`APROBADA` o `RECHAZADA`). Para observar la interacción real, desde la raíz del repositorio ejecuta:

```bash
./.venv/bin/python -m agentes.e5 --variante actor-critico --aprobar-ediciones
```

Responde `s` para autorizar cada edición del ejecutor o `n` para bloquearla. Las trazas de esta ejecución se guardan como `agentes/trazas/e6-*.jsonl`; busca `aprobacion_humana` en `e6-ejecutor-r1.jsonl` y `e6-ejecutor-r2.jsonl` para ver las aprobaciones por ronda. La prueba automatizada comprueba aprobación y rechazo sin modificar el repositorio real.
