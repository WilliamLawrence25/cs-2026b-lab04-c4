# ADR-003: Uso de PostgreSQL como base de datos relacional

Estado: Aceptado
Fecha: 2026-09-29
Decisores: William Choquehuanca (Developer Full-stack)

## Contexto
El sistema debe registrar catálogos, reservas concurrentes, préstamos y control de multas (RF-01, RF-02, RF-04, RF-05). Se requiere alta consistencia en los datos para evitar préstamos duplicados. Además, el presupuesto es nulo (R-03).

## Alternativas consideradas
1. PostgreSQL (Base de datos relacional SQL).
2. MongoDB (Base de datos documental NoSQL).

## Decisión
Usaremos PostgreSQL como nuestro motor de base de datos principal. Los modelos de libros, reservas y usuarios estarán estrictamente tipados e interrelacionados.

## Consecuencias
Positivas: 
- Garantiza propiedades ACID, cruciales para la consistencia transaccional de las reservas de libros.
- Es de código abierto y sin costo de licencia (respeta R-03).
Negativas / riesgos: 
- Esquema rígido que requerirá migraciones estructuradas ante cualquier cambio en el modelo de datos.