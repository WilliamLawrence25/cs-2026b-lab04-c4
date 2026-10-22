# E6: Métricas y Análisis de Trade-off (BiblioUNSA)

## 1. Comparación de Complejidad (Radon) y Tamaño (SLOC)

| Métrica | Versión Antes (Ingenua) | Versión Después (Con Patrones) |
| :--- | :--- | :--- |
| **Complejidad `procesar_reserva()`** | C (9) - 10 caminos | A (2) - 2 caminos |
| **Complejidad promedio** | B (6.0) | A (1.5) |
| **Líneas de código (SLOC) aprox.** | ~60 líneas | ~200 líneas |
| **Archivos involucrados** | 1 archivo (`servicio.py`) | 6 archivos (servicio, estados, estrategias, eventos, decoradores, ia) |

## 2. Análisis del Trade-off
Ganamos una altísima extensibilidad y seguridad: ahora podemos agregar nuevos tipos de estudiantes (Strategy), nuevos canales de notificación (Observer) y aislar las "alucinaciones" de la IA (Chain of Responsibility) sin modificar ni una sola línea del servicio principal (cumpliendo Abierto/Cerrado). Sin embargo, el costo arquitectónico es evidente: el código triplicó su tamaño y aumentó la indirección, exigiendo que el equipo conozca el catálogo GoF para entender el flujo. La versión *antes* habría sido completamente suficiente y preferible si BiblioUNSA fuera un sistema estático donde los tipos de usuarios y las reglas de negocio nunca fueran a cambiar, y si no se integraran LLMs impredecibles.

## 3. Patrones Rechazados
* **Singleton (para `FabricaMultas` o `PublicadorEventos`):** Aunque la IA (y muchos tutoriales) sugieren usar Singleton para fábricas y gestores de eventos, lo rechazamos porque introduce *estado global*. Esto habría acoplado fuertemente las clases e impedido correr nuestras pruebas unitarias de forma aislada e independiente. Preferimos *Inyectar la Dependencia* a través del constructor.
* **Abstract Factory:** Rechazado por ser sobreingeniería. Solo necesitábamos crear objetos para calcular multas (un solo producto), no "familias" de productos relacionados. Usar el registro simple de una Factory Method fue más directo y limpio.