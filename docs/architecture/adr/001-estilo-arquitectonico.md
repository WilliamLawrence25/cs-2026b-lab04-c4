# ADR-001: Adoptar un monolito en capas para el MVP de BiblioUNSA

Estado: Aceptado
Fecha: 2026-09-29
Decisores: William Choquehuanca (Developer Full-stack)

## Contexto
El MVP debe estar en producción en 1 mes (R-01) y el equipo consta de un único desarrollador (R-02) sin presupuesto inicial para infraestructura compleja (R-03). El sistema requiere interoperabilidad (QA-01) para validar matrículas y manejar el flujo básico de préstamos (RF-02, RF-04).

## Alternativas consideradas
1. Monolito en capas (4.55): Simple, rápido de desarrollar y desplegar.
2. Monolito modular (4.00): Estructurado, pero requiere más tiempo para definir interfaces estrictas.
3. Microservicios (1.90): Escalable, pero su complejidad operativa y costo descartan su viabilidad para un solo desarrollador.

## Decisión
Usaremos un estilo arquitectónico de Monolito en capas (Layered Architecture). Toda la aplicación (Catálogo, Reservas, Préstamos) se desarrollará y desplegará como una única unidad, con una separación lógica tradicional: Capa de Presentación, Lógica de Negocio y Acceso a Datos.

## Consecuencias
Positivas: 
- Velocidad de desarrollo acelerada, crucial para cumplir el plazo (R-01).
- Despliegue muy simple y económico (un solo servidor/VPS cumple R-03).
Negativas / riesgos: 
- Alto acoplamiento interno; los cambios en un módulo podrían afectar a otros si no se mantiene la disciplina en el código.