# ADR-005: Patrones de diseño en el módulo Reservas e IA

**Estado:** Aceptado (22/10/2026)

## Contexto
El método `procesar_reserva()` tenía una complejidad ciclomática alta (C) debido a condicionales anidados para validar estados y calcular multas por tipo de usuario. Además, el servicio estaba acoplado a un SDK externo y el componente de IA (para sugerir libros) requería protección, dado que los LLM son no deterministas y pueden alucinar.

## Decisión
* **State:** Para controlar el ciclo de vida de la reserva (`PENDIENTE`, `CONFIRMADA`, `CANCELADA`).
* **Strategy + Adapter + Factory:** Para aislar el SDK académico y calcular las multas dinámicamente según el tipo de usuario.
* **Observer:** Para desacoplar el envío de correos y el registro de logs.
* **Decorator + Chain of Responsibility:** Para guardar en caché las respuestas del LLM y validar su salida mediante guardrails (evitando recomendaciones externas).
* **Rechazados:** Singleton (rompe aislamiento de pruebas) y Abstract Factory (sobreingeniería detectada por "patternitis").

## Consecuencias
(+) Complejidad ciclomática máxima reducida de 9 a 2 (grado A).
(+) Alta extensibilidad: nuevos tipos de usuarios o notificaciones no tocan el código base (cumple Abierto/Cerrado).
(+) Interacciones con IA seguras, sin depender de red en pruebas.
(-) Aumento de líneas de código (de ~60 a ~200) y mayor indirección arquitectónica.