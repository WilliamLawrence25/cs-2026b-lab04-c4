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

## Diseño UML (Lab 05)

Como parte de la evolución de la arquitectura, se ha realizado el diseño detallado del módulo de Préstamos aplicando metodologías de **Diagram as Code** e **Ingeniería Inversa** con Python.

### Máquina de Estados: Ciclo de vida del Préstamo
```mermaid
stateDiagram-v2
    [*] --> RESERVADO: confirmarReserva() [matrícula vigente]
    
    RESERVADO --> PRESTADO: registrarEntrega()
    RESERVADO --> [*]: cancelarReserva() [no recogido en 24h]
    
    PRESTADO --> DEVUELTO: registrarDevolucion() [antes de fecha límite]
    PRESTADO --> VENCIDO: verificarVencimiento() [fecha límite superada]
    
    VENCIDO --> CON_MULTA: aplicarMulta()
    
    CON_MULTA --> DEVUELTO: registrarDevolucion() [multa pagada]
    
    DEVUELTO --> [*]
```

### Enlaces a Entregables del Diseño
- 🏗️ **Estructural:** [Diagrama de Clases](docs/design/img/clases.png) y [Diagrama de Paquetes](docs/design/img/paquetes.png)
- ⚙️ **Comportamiento:** [Diagrama de Secuencia (Reserva)](docs/design/img/secuencia-reserva.png) y [Diagrama de Actividades (Devolución y Multa)](docs/design/img/actividades-devolucion.png)
- 🔄 **Auditoría e IA:** [Análisis Round-Trip](docs/design/round-trip.md), [Reporte de Consistencia C1-C5](docs/design/consistencia.md) y [Bitácora de IA](docs/design/bitacora-ia.md).

## Arquitectura C4 (Lab 06)

El diseño arquitectónico del sistema BiblioUNSA ha sido modelado utilizando el enfoque de "Arquitectura como Código" mediante Structurizr DSL, garantizando la consistencia entre los distintos niveles de abstracción.

### Nivel 1: Contexto del Sistema
```mermaid
C4Context
  title Contexto de BiblioUNSA
  
  Person(estudiante, "Estudiante", "Estudiante matriculado en la UNSA")
  Person(bibliotecario, "Bibliotecario", "Personal de la biblioteca")
  
  System(bibliounsa, "BiblioUNSA", "Gestión de catálogo, reservas y préstamos")
  
  System_Ext(sistemaAcademico, "Sistema Académico UNSA", "Validación de matrículas")
  System_Ext(ssoGoogle, "Google Workspace", "SSO Institucional")

  Rel(estudiante, bibliounsa, "Busca libros y realiza reservas")
  Rel(bibliotecario, bibliounsa, "Gestiona préstamos y cobra multas")
  Rel(bibliounsa, sistemaAcademico, "Valida matrícula vigente", "HTTPS/JSON")
  Rel(bibliounsa, ssoGoogle, "Delega autenticación", "OAuth 2.0")
  
  UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

### Enlaces a las 5 Vistas del Modelo C4
* 🌐 **Nivel 1 (Contexto):** [Ver diagrama de contexto](## Patrones de Diseño (Lab 07)

Se aplicó refactorización hacia patrones GoF guiada por pruebas de caracterización y métricas (radon).

### Resumen de Refactorización
| Olor detectado | Patrón Aplicado | Prueba de verificación |
| :--- | :--- | :--- |
| if/elif anidados sobre `reserva.estado` | **State** | `test_state_impide_transiciones_invalidas` |
| if/elif para cálculo de multas | **Strategy + Factory** | `test_open_closed_nuevo_tipo_sin_modificar_servicio` |
| SDK de la UNSA fuertemente acoplado | **Adapter** | Pruebas de caracterización originales |
| Notificaciones mezcladas en el servicio | **Observer** | `test_observer_nuevo_suscriptor_sin_tocar_el_servicio` |
| Consultas repetitivas a APIs | **Decorator** | `test_decorator_cache_evita_llamadas_repetidas` |
| IA generativa sin filtros | **Chain of Responsibility** | `test_chain_of_responsibility_bloquea_ia_alucinando` |

### Métricas de Complejidad (procesar_reserva)
| Métrica | Antes (Ingenua) | Después (Patrones) |
| :--- | :--- | :--- |
| **Complejidad (Radon)** | C (9) | A (2) |
| **Líneas de código** | ~60 | ~200 |docs/architecture/c4/img/structurizr-Contexto.png)
* 📦 **Nivel 2 (Contenedores):** [Ver diagrama de contenedores](docs/architecture/c4/img/structurizr-Contenedores.png)
* 🧩 **Nivel 3 (Componentes):** [Ver diagrama de componentes](docs/architecture/c4/img/structurizr-Componentes.png)
* 🔄 **Vista Dinámica (Reserva):** [Ver diagrama dinámico](docs/architecture/c4/img/structurizr-ReservaLibro.png)
* 🚀 **Vista de Despliegue:** [Ver diagrama de despliegue](docs/architecture/c4/img/structurizr-Despliegue.png)

### Auditoría y Documentación
* [Inventario de elementos](docs/architecture/c4/inventario.md)
* [Revisión con checklist C4](docs/architecture/c4/revision-c4.md)
* [Explicación para público no técnico](docs/architecture/c4/explicacion.md)
* [Bitácora de IA y falsos positivos](docs/architecture/c4/bitacora-ia.md)
* [Comparación Modelado vs Diagramación](docs/architecture/c4/comparacion.md)

## Patrones de Diseño (Lab 07)

Se aplicó refactorización hacia patrones GoF guiada por pruebas de caracterización y métricas (radon).

### Resumen de Refactorización
| Olor detectado | Patrón Aplicado | Prueba de verificación |
| :--- | :--- | :--- |
| if/elif anidados sobre `reserva.estado` | **State** | `test_state_impide_transiciones_invalidas` |
| if/elif para cálculo de multas | **Strategy + Factory** | `test_open_closed_nuevo_tipo_sin_modificar_servicio` |
| SDK de la UNSA fuertemente acoplado | **Adapter** | Pruebas de caracterización originales |
| Notificaciones mezcladas en el servicio | **Observer** | `test_observer_nuevo_suscriptor_sin_tocar_el_servicio` |
| Consultas repetitivas a APIs | **Decorator** | `test_decorator_cache_evita_llamadas_repetidas` |
| IA generativa sin filtros | **Chain of Responsibility** | `test_chain_of_responsibility_bloquea_ia_alucinando` |

### Métricas de Complejidad (procesar_reserva)
| Métrica | Antes (Ingenua) | Después (Patrones) |
| :--- | :--- | :--- |
| **Complejidad (Radon)** | C (9) | A (2) |
| **Líneas de código** | ~60 | ~200 |

## Diseño de la Arquitectura (Lab 08)

[![Fitness Functions](https://github.com/WilliamLawrence25/cs-2026b-lab04-c4/actions/workflows/fitness.yml/badge.svg)](https://github.com/TU_USUARIO/cs-2026b-lab04-c4/actions/workflows/fitness.yml)

Se aplicó el método **Attribute-Driven Design (ADD 3.0)** para guiar la evolución de BiblioUNSA frente a su expansión a todas las facultades, validando cada decisión mediante simulaciones y *Fitness Functions*.

### Árbol de Utilidad (Priorización)
![Árbol de Utilidad](docs/architecture/utilidad/arbol.png)

### Resumen de Iteraciones ADD
| Escenario Prioritario | Táctica Adoptada | Evidencia | ¿Cumple? | ADR |
| :--- | :--- | :--- | :--- | :--- |
| **QA-02:** Caída de API Académica | Circuit Breaker + Outbox en BD Local | Simulación de Caída (0 reservas perdidas). | Sí | [ADR-006](docs/architecture/adr/006-disponibilidad-api-academica.md) |
| **QA-01:** Búsquedas concurrentes | Optimizar Consultas (Índices) + Caché | Simulación M/G/c (p95 baja a 0.3s). | Sí | [ADR-007](docs/architecture/adr/007-rendimiento-busquedas.md) |
| **QA-04:** Aislamiento de Facultades | Row-Level Security (RLS) en PostgreSQL | Prueba de Integración / Fitness Function. | Sí | [ADR-008](docs/architecture/adr/008-aislamiento-facultades-rls.md) |

## Prompt engineering (Lab 09)

Implementación de prompts tratados como artefactos de software versionados, evaluados mediante `promptfoo` y validados contractualmente con `JSON Schema` detrás del puerto `ProveedorLLM` para el sistema **BiblioUNSA**[cite: 19, 22, 28].

### Tabla de versiones y tasas de aprobación

| Versión | Técnicas y elementos aplicados | Tarea A: Criterios de Aceptación (8 casos) | Tarea B: Text-to-SQL Solo Lectura (8 casos) |
| :--- | :--- | :---: | :---: |
| **`v1`** | *Zero-shot* ingenuo (solo instrucción directa sin formato ni restricciones)[cite: 20, 25]. | **0.0%** (0/8) | **0.0%** (0/8) |
| **`v2`** | Patrones *Persona* y *Template* + contexto del dominio y esquema JSON[cite: 21, 25]. | **50.0%** (4/8) | **50.0%** (4/8) |
| **`v3`** | 7 elementos de anatomía + *Cognitive Verifier*, *Flipped Interaction*, *Few-shot* y defensa en capas con delimitadores XML (`<historia>`, `<pregunta>`)[cite: 19, 21, 22, 26]. | **100.0%** (8/8) | **100.0%** (8/8) |

### Gráfico de resultados

![Tasa de aprobación por versión](docs/resultados_lab09.png)

### Lecciones aprendidas
1. **Un prompt es una especificación ejecutada por código:** Sin un contrato `JSON Schema` (`additionalProperties: false`) y restricciones explícitas de salida pura, los modelos envuelven las respuestas en bloques Markdown (` ```json `) o incluyen texto conversacional que rompe el parseo automático[cite: 19, 23, 25].
2. **Defensa en capas contra inyección (OWASP LLM01):** Encapsular la entrada del usuario entre etiquetas XML (`<historia>`, `<pregunta>`), instruir explícitamente que el contenido delimitado es dato no confiable y validar la salida antes de tocar el dominio neutralizó ataques de inyección directa (`HACKED` y `DROP TABLE`)[cite: 22, 26].
3. **Evaluación basada en propiedades frente al no determinismo:** Dado que un LLM varía alias SQL, orden de columnas y redacción entre ejecuciones idénticas, las aserciones deben comprobar estructura e invariantes (iniciar con `SELECT` y prohibir DDL/DML) respaldadas por respuestas grabadas (*fixtures*) para garantizar reproducibilidad en CI[cite: 21, 32, 33].

## Sistemas agénticos (Lab 10)

La arquitectura elegida usa un agente ReAct con contrato JSON, política de herramientas y máquina de estados. Para tareas pequeñas se ejecuta un agente único; en ISSUE-02 se comparó con coordinación planificador–ejecutor–revisor de solo lectura, limitada a dos rondas. La aprobación interactiva de ediciones se puede activar en el ejecutor. Las decisiones grabadas permiten repetir las trayectorias y pruebas sin claves externas.

### Decisión arquitectónica

La decisión completa, alternativas y consecuencias están en [ADR-010: arquitectura del sistema agéntico](docs/architecture/adr/010-sistema-agentico.md). La política limita los pasos, protege rutas de pruebas y restringe los comandos; el revisor no puede editar. El historial conserva el contexto de la ejecución y las notas de E4 sirven como memoria persistente. El [plan de delegación progresiva](agentes/delegacion.md) especifica los permisos humanos y del agente en cada nivel.

### Máquina de estados ReAct

![Máquina de estados del agente ReAct](agentes/diseno/estados.png)

```mermaid
stateDiagram-v2
    [*] --> INICIO
    INICIO --> DECIDIENDO
    DECIDIENDO --> VALIDANDO_CONTRATO
    VALIDANDO_CONTRATO --> CONTRATO_INVALIDO: decisión inválida
    CONTRATO_INVALIDO --> OBSERVANDO
    VALIDANDO_CONTRATO --> FINALIZADO: respuesta final válida
    FINALIZADO --> FIN
    VALIDANDO_CONTRATO --> EVALUANDO_POLITICA: acción válida
    EVALUANDO_POLITICA --> BLOQUEADO: política deniega
    BLOQUEADO --> OBSERVANDO
    EVALUANDO_POLITICA --> EJECUTANDO: política permite
    EJECUTANDO --> OBSERVANDO: resultado o error
    OBSERVANDO --> DECIDIENDO: quedan pasos
    OBSERVANDO --> LIMITE_ALCANZADO: se agotan los pasos
    LIMITE_ALCANZADO --> FIN
    FIN --> [*]
```

### Trayectoria del actor-crítico en ISSUE-02

```mermaid
sequenceDiagram
    autonumber
    participant P as Planificador
    participant E as Ejecutor
    participant R as Revisor (solo lectura)
    participant H as Repositorio y pruebas
    P->>H: Lee ISSUE-02 y mapa AST
    P-->>E: Plan: validar antes de reservar; revisar compatibilidad
    E->>H: Ronda 1: agrega validación de matrícula
    E->>H: Ejecuta test_issue_02_reservas.py
    H-->>E: 1 passed
    R->>H: Revisa diff y prueba con ServicioPrestamos() sin validador
    H-->>R: Falla: AttributeError al invocar el validador None
    R-->>E: CAMBIOS SOLICITADOS: proteger validador opcional
    E->>H: Ronda 2: añade guard self.validador is not None
    E->>H: Ejecuta prueba ISSUE-02 y prueba de compatibilidad
    H-->>E: 2 passed
    R->>H: Revisa diff y repite ambas pruebas
    H-->>R: 2 passed; comportamiento compatible
    R-->>P: APROBADO en la ronda 2
```

Diagrama generado y artefactos: [traza Mermaid E5](agentes/trazas/e5-actor-critico.mmd), [comparación de métricas](agentes/resultados/e5-comparacion.json), [observación E7](observacion.md) y [bitácora de IA](bitacora-ia.md).

### Métricas observadas (E7)

Los pasos cuentan decisiones incluida la respuesta final; las acciones cuentan llamadas a herramientas.

| Issue / ejecución | Pasos | Rondas | Herramientas utilizadas (acciones) | Decisiones rechazadas por contrato | Acciones bloqueadas | Contexto final |
|---|---:|---:|---|---:|---:|---:|
| ISSUE-01 — E2, agente ReAct | 9 | 1 | `leer_archivo`, `ejecutar_pruebas`, `buscar`, `editar_archivo`, `ver_cambios` (8) | 0 | 0 | 9.969 caracteres* |
| ISSUE-02 — E5, agente único | 7 | 1 | `leer_archivo`, `ejecutar_pruebas`, `editar_archivo`, `ver_cambios` (6) | 0 | 0 | 8.996 caracteres |
| ISSUE-02 — E5, actor-crítico | 18 | 2 | `leer_archivo`, `mapa_repo`, `editar_archivo`, `ejecutar_pruebas`, `ejecutar_comando`, `ver_cambios` (13) | 0 | 0 | 28.009 caracteres** |
| ISSUE-03 — E4, agente ReAct | 9 | 1 | `mapa_repo`, `leer_archivo`, `ejecutar_pruebas`, `anotar`, `editar_archivo`, `ver_cambios`, `leer_notas` (8) | 0 | 0 | 10.686 caracteres |

\* E2 no persistió su contador de contexto; se reconstruyó de la sesión.<br>
\** El contexto multiagente suma los historiales de cinco participantes y no equivale al de una llamada individual.

Para las evidencias y la interpretación completa de las métricas, consulta [observacion.md](observacion.md). El repositorio del proyecto es [github.com/WilliamLawrence25/cs-2026b-lab04-c4](https://github.com/WilliamLawrence25/cs-2026b-lab04-c4).