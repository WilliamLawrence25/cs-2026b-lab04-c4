# Bitácora de uso de IA - Laboratorio 07 (Patrones de Diseño)

| Fecha | Prompt (resumen) | Propuesta de la IA | Verificación / Decisión |
| :--- | :--- | :--- | :--- |
| 2026-10-22 | Analizar olores en `antes/servicio.py`. | Propuso State, Strategy, Adapter y Singleton para las multas. | Aceptados los 3 primeros. Singleton rechazado para evitar estado global que rompe las pruebas unitarias. |
| 2026-10-22 | Refactorizar cálculo de multas (E2). | Sugirió Strategy, Adapter y Abstract Factory. | Factory Method simple aceptado. Abstract Factory rechazado por ser sobreingeniería (no hay familias de productos). |
| 2026-10-22 | Eliminar condicionales de estado (E3). | Implementó patrón State clásico con delegación. | Aceptado. Se verificó con pruebas parametrizadas y se demostró que el estado incorrecto lanza excepción. |
| 2026-10-22 | Proteger el sistema de la IA (E5). | Propuso aislar al LLM con Decorator para caché y Chain of Responsibility para los guardrails. | Aceptado. La IA es no determinista y debe ser tratada como entrada insegura. |
| 2026-10-22 | Prompt Evaluador: Verificar el flujo de Guardrails. | La IA sugirió usar a "otro LLM" como juez para validar los resultados del primero. | Rechazado. Aumenta latencia, costos y sigue siendo no determinista. Se optó por guardrails basados en código duro. |