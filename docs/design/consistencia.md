# Revisión de Consistencia (Reglas C1-C5) - BiblioUNSA

| Regla | Hallazgo de la IA | Verificación del equipo | Decisión / Acción |
|---|---|---|---|
| **C1** | El mensaje `notificarReserva()` enviado a `NotificadorCorreo` en el diagrama de secuencia no existe como operación en el diagrama de clases. | **Verdadero positivo**. La operación fue omitida en el diseño estructural inicial. | **Corregir diagrama:** Se debe agregar la interfaz `NotificadorCorreo` al diagrama de clases. |
| **C2** | Las transiciones `cancelarReserva()` y `verificarVencimiento()` del diagrama de estados no existen como operaciones en la clase `Prestamo`. | **Verdadero positivo**. El ciclo de vida modeló flujos que no se planificaron en las clases. | **Corregir diagrama:** Se deben agregar estas operaciones a la clase `Prestamo`. |
| **C4** | La IA detecta una "dependencia cíclica" indicando que `api_academica` depende de `logica_negocio`. | **FALSO POSITIVO**. La IA leyó la flecha `PRES ..> API` al revés. El monolito depende de la API externa, no al revés. | **Rechazar hallazgo**. El diagrama de paquetes cumple la regla C4. |
| **C5** | Inconsistencia de convenciones: el diagrama UML usa `camelCase` (`estaMatriculado`), pero el código Python usa `snake_case` (`esta_matriculado`). | **Verdadero positivo**. Limitación estándar al pasar de UML a Python. | **Documentar limitación:** Se acepta por PEP 8. |