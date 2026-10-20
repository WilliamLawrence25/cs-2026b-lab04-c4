# Bitácora de uso de IA - Modelo C4 (Lab 06)

| Fecha | Herramienta | Prompt (resumen) | Propuesta de la IA | Verificación / Decisión |
| :--- | :--- | :--- | :--- | :--- |
| 2026-10-20 | Gemini | Actúa como experto en Structurizr DSL y genera el Nivel 1 y 2. | Creó la estructura inicial pero puso a "Docker" como un contenedor interno. | Corregida. Docker es infraestructura (nodo de despliegue), no contenedor lógico C4. |
| 2026-10-20 | Gemini | Agrega la vista de componentes (E3) basada en mi diagrama de paquetes. | Sugirió llamadas bidireccionales entre `prestamos` y `multas`. | Corregida. Se ajustó a relación unidireccional para evitar dependencias cíclicas. |
| 2026-10-20 | Gemini | Crea la vista dinámica del flujo de reserva de libros. | Detalló llamadas a nivel de código (`reservar_copia()`). | Corregida. Se elevó la abstracción a nivel de componentes (pasos genéricos). |
| 2026-10-20 | Gemini | Prompt Auditor: Revisa mis vistas con la lista oficial C4. | Indicó como "error" que faltan protocolos de red entre el actor "Estudiante" y el sistema. | Falso positivo documentado. En el contexto (Nivel 1) esto no es requerido. |
| 2026-10-20 | Gemini | Prompt Explicación: Explica el sistema a un público no técnico. | Generó un párrafo mencionando "APIs" y "bases de datos SQL". | Corregida. Se limpió la jerga técnica para adaptarla al Director de la biblioteca. |