# Matriz de decisión Caso 4: BiblioUNSA

## Alternativas
**A. Monolito en capas (Layered Monolith):** Sistema en un solo despliegue con separación lógica tradicional (Presentación, Lógica de Negocio, Acceso a Datos).
**B. Monolito modular:** Un solo despliegue estructurado en dominios independientes (Catálogo, Reservas, Préstamos) que se comunican por interfaces internas.
**C. Microservicios:** Múltiples servicios desplegados independientemente conectados por red/API.

## Criterios y pesos (deben sumar 100%)
| Criterio | Peso | Justificación (driver relacionado) |
|---|---|---|
| Tiempo de entrega | 30% | R-01: El MVP debe salir en 1 mes. |
| Simplicidad operativa | 25% | R-02: Solo hay 1 developer para desarrollar, desplegar y mantener todo. |
| Costo operativo | 15% | R-03: Presupuesto mínimo (capa gratuita o servidor básico). |
| Interoperabilidad | 15% | QA-01: Integración crítica con el sistema académico vía API. |
| Seguridad | 15% | QA-02: Autenticación estricta con SSO de la UNSA. |

## Matriz (puntaje 1 = muy malo, 5 = excelente)
| Criterio (peso) | A (Capas) | B (Modular) | C (Microservicios) |
|---|---|---|---|
| Tiempo de entrega (30%) | 5 | 4 | 1 |
| Simplicidad operativa (25%) | 5 | 4 | 1 |
| Costo operativo (15%) | 5 | 4 | 1 |
| Interoperabilidad (15%) | 3 | 4 | 5 |
| Seguridad (15%) | 4 | 4 | 3 |
| **Total ponderado** | **4.55** | **4.00** | **1.90** |

## Conclusión
Elegimos el **Monolito en capas** porque maximiza la velocidad de entrega y la simplicidad operativa, factores críticos al tener un solo developer (R-02) y un plazo estricto de 1 mes (R-01). Aunque los microservicios ofrecen alta interoperabilidad, su complejidad y costo operativo exceden las capacidades actuales del proyecto. Ver [ADR-001](adr/001-estilo-arquitectonico.md).