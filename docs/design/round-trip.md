# Análisis Round-Trip: Módulo de Préstamos BiblioUNSA

| Diferencia observada | Causa | Acción |
|---|---|---|
| No aparecen las multiplicidades (ej. `Estudiante "1" -- "0..*" Prestamo`). | La herramienta `pyreverse` no infiere directamente las cardinalidades UML a partir de los *type hints* estáticos de Python. | Ninguna: limitación de la herramienta analítica. El diagrama de diseño inicial (E1) se mantiene como fuente de verdad. |
| Los nombres de operaciones están en formato `snake_case` (ej. `confirmar_reserva`) frente al `camelCase` del diagrama E1. | Al generar el código Python con IA, se aplicaron las convenciones estándar de estilo PEP 8. | Aceptable; se documenta la equivalencia de nombres cumpliendo con la Regla de consistencia (C5). |
| La interfaz `ValidadorMatricula` se muestra como una clase abstracta de la cual hereda el adaptador. | En Python no existen las "interfaces" puras de UML, se implementan heredando de la clase `ABC` (Abstract Base Class). | Aceptable en el contexto técnico de Python; el adaptador igual lanza `NotImplementedError`. |