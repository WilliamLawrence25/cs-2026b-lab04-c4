workspace "BiblioUNSA" "Modelo C4 del Sistema de Bibliotecas de la UNSA" {

    !identifiers hierarchical

    model {
        estudiante = person "Estudiante" "Estudiante matriculado en la UNSA que busca y reserva libros."
        bibliotecario = person "Bibliotecario" "Personal de la biblioteca encargado de gestionar préstamos y multas."

        bibliounsa = softwareSystem "BiblioUNSA" "Permite gestionar el catálogo de libros, reservas, préstamos y multas de la biblioteca." {
            
            web = container "Aplicación Web" "Interfaz principal para estudiantes y bibliotecarios." "React / PWA" "Web Browser"
            
            api = container "API REST" "Monolito en capas que procesa la lógica de negocio de préstamos y reservas." "Python / Django" {
                catalogo = component "Módulo Catálogo" "Gestiona la disponibilidad de libros y el inventario." "Django App"
                reservas = component "Módulo Reservas" "Maneja la creación y validación de reservas de estudiantes." "Django App"
                prestamos = component "Módulo Préstamos" "Gestiona el ciclo de vida del préstamo y las devoluciones." "Django App"
                multas = component "Módulo Multas" "Calcula y registra penalizaciones por atrasos." "Django App"
            }
            
            db = container "Base de Datos" "Almacena información de catálogo, préstamos y multas." "PostgreSQL 16" "Database"
        }

        sistemaAcademico = softwareSystem "Sistema Académico UNSA" "Sistema central para validar matrículas." "Externo"
        ssoGoogle = softwareSystem "Google Workspace" "SSO para autenticación institucional." "Externo"

        // Relaciones Nivel 1 (Contexto)
        estudiante -> bibliounsa "Busca libros y realiza reservas"
        bibliotecario -> bibliounsa "Gestiona préstamos y cobra multas"
        bibliounsa -> sistemaAcademico "Valida matrícula vigente" "HTTPS/JSON"
        bibliounsa -> ssoGoogle "Delega autenticación" "OAuth 2.0"

        // Relaciones Nivel 2 (Contenedores)
        estudiante -> bibliounsa.web "Usa" "HTTPS"
        bibliotecario -> bibliounsa.web "Usa" "HTTPS"
        bibliounsa.web -> ssoGoogle "Autentica usuario" "OAuth 2.0"

        // Relaciones Nivel 3 (Componentes hacia afuera)
        bibliounsa.web -> bibliounsa.api.catalogo "Consulta catálogo" "HTTPS/JSON"
        bibliounsa.web -> bibliounsa.api.reservas "Gestiona reservas" "HTTPS/JSON"
        bibliounsa.web -> bibliounsa.api.prestamos "Gestiona préstamos" "HTTPS/JSON"
        bibliounsa.web -> bibliounsa.api.multas "Consulta multas" "HTTPS/JSON"

        bibliounsa.api.reservas -> sistemaAcademico "Valida matrícula (ValidadorMatricula)" "HTTPS/JSON"

        bibliounsa.api.catalogo -> bibliounsa.db "Lee y escribe" "SQL/TCP"
        bibliounsa.api.reservas -> bibliounsa.db "Lee y escribe" "SQL/TCP"
        bibliounsa.api.prestamos -> bibliounsa.db "Lee y escribe" "SQL/TCP"
        bibliounsa.api.multas -> bibliounsa.db "Lee y escribe" "SQL/TCP"

        // Relaciones Nivel 3 (Componentes internos)
        bibliounsa.api.reservas -> bibliounsa.api.catalogo "Verifica y reserva stock"
        bibliounsa.api.prestamos -> bibliounsa.api.catalogo "Libera stock al devolver"
        bibliounsa.api.prestamos -> bibliounsa.api.multas "Genera multa si hay retraso"
        bibliounsa.api.prestamos -> bibliounsa.api.reservas "Actualiza estado de reserva"

        // E5: ENTORNO DE DESPLIEGUE
        produccion = deploymentEnvironment "Producción" {
            deploymentNode "Dispositivo del Usuario" "" "Navegador Web (PC / Móvil)" {
                containerInstance bibliounsa.web
            }

            deploymentNode "Data Center UNSA" "" "Servidor Ubuntu 24.04 LTS, 4 vCPU, 8 GB RAM" {
                deploymentNode "Docker Compose" "" "Docker 27" {
                    containerInstance bibliounsa.api
                    containerInstance bibliounsa.db
                }
            }
        }
    }

    views {
        systemContext bibliounsa "Contexto" "Nivel 1: BiblioUNSA y su entorno institucional." {
            include *
            autolayout lr
        }

        container bibliounsa "Contenedores" "Nivel 2: contenedores internos de BiblioUNSA." {
            include *
            autolayout lr
        }

        component bibliounsa.api "Componentes" "Nivel 3: módulos internos de la API REST." {
            include *
            autolayout lr
        }

        dynamic bibliounsa.api "ReservaLibro" "Dinámico: Estudiante reserva un libro validando matrícula." {
            estudiante -> bibliounsa.web "1. Solicita reservar un libro"
            bibliounsa.web -> bibliounsa.api.reservas "2. POST /api/reservas"
            bibliounsa.api.reservas -> sistemaAcademico "3. Verifica matrícula vigente"
            bibliounsa.api.reservas -> bibliounsa.api.catalogo "4. Valida y reduce stock disponible"
            bibliounsa.api.reservas -> bibliounsa.db "5. Registra la reserva en la BD"
            autolayout lr
        }

        // E5: VISTA DE DESPLIEGUE
        deployment bibliounsa produccion "Despliegue" "Despliegue en producción (Data Center UNSA)." {
            include *
            autolayout lr
        }

        styles {
            element "Person" {
                shape person
                background #08427B
                color #ffffff
            }
            element "Software System" {
                background #1168BD
                color #ffffff
            }
            element "Externo" {
                background #999999
                color #ffffff
            }
            element "Container" {
                background #438DD5
                color #ffffff
            }
            element "Component" {
                background #85BBF0
                color #000000
            }
            element "Database" {
                shape cylinder
            }
            element "Web Browser" {
                shape WebBrowser
            }
        }
    }
}