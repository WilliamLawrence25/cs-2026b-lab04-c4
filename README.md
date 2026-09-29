# BiblioUNSA - Laboratorio 04: Fundamentos de arquitectura de software
Construcción de Software - EPIS-UNSA

## Integrantes
- 2026-B Grupo 01
- William Choquehuanca Berna | Developer Full-Stack, Redactor de ADR, Diagramador y Verificador de IA

## Caso
El sistema BiblioUNSA permite gestionar el préstamo y la reserva de libros en las bibliotecas de la universidad. Los estudiantes pueden consultar el catálogo en línea y reservar textos, mientras que los bibliotecarios gestionan los préstamos mediante el escaneo de un carné QR y controlan las multas. El atributo de calidad crítico es la **Interoperabilidad**, ya que el sistema debe validar si la matrícula del estudiante está vigente consultando el sistema académico mediante una API externa, manteniendo la seguridad e independencia de los datos.

## Arquitectura elegida
```mermaid
flowchart TB
    EST["Estudiante"]
    BIB["Bibliotecario"]

    subgraph APP ["BiblioUNSA (Monolito en capas)"]
        subgraph PRES ["Capa de Presentación"]
            UI["Interfaz Web (Catálogo y Gestión)"]
        end
        
        subgraph BLL ["Capa de Lógica de Negocio"]
            CAT["Gestión de Catálogo"]
            RES["Gestión de Reservas"]
            PRE["Control de Préstamos y Multas"]
        end
        
        subgraph DAL ["Capa de Acceso a Datos"]
            REP["Repositorios / ORM"]
        end
    end

    DB[("Base de Datos<br/>(PostgreSQL)")]
    ACA["API Sistema Académico<br/>(Servicio Externo)"]
    SSO["Google Workspace<br/>(SSO UNSA)"]

    EST & BIB --> UI
    UI --> CAT & RES & PRE
    
    %% Integraciones externas desde la lógica
    RES & PRE -.->|Validación de matrícula| ACA
    UI -.->|Autenticación| SSO

    CAT & RES & PRE --> REP
    REP --> DB

    classDef mod fill:#E8F5E9,stroke:#2E7D32,color:#000
    classDef ext fill:#F2F2F2,stroke:#7F7F7F,color:#000,stroke-dasharray: 4 3
    classDef usr fill:#FDEDEC,stroke:#C8310E,color:#000
    
    class UI,CAT,RES,PRE,REP mod
    class ACA,SSO ext
    class EST,BIB usr
```

## Decisiones arquitectónicas
- [ADR-001: Adoptar un monolito en capas para el MVP](docs/architecture/adr/001-estilo-arquitectonico.md)
- [ADR-002: Uso de OAuth 2.0 (Google Workspace) para autenticación](docs/architecture/adr/002-autenticacion-sso.md)
- [ADR-003: Uso de PostgreSQL como base de datos relacional](docs/architecture/adr/003-base-de-datos.md)

## Reflexión sobre el uso de la IA
El uso de asistentes de IA fue fundamental para agilizar la generación de diagramas como código y estructurar rápidamente la documentación de las decisiones. Sin embargo, la herramienta demostró un sesgo evidente hacia arquitecturas complejas, recomendando inicialmente un enfoque de microservicios. Como único desarrollador con un plazo de entrega de un mes y presupuesto nulo, aplicar esa recomendación habría llevado al fracaso operativo del proyecto. Esto subraya que la IA es excelente proponiendo y redactando, pero el juicio arquitectónico y la validación estricta contra las restricciones reales siguen siendo responsabilidad exclusiva del ingeniero.