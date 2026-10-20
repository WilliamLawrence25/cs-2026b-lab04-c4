workspace "BiblioUNSA" "Modelo C4 del Sistema de Bibliotecas de la UNSA" {

    !identifiers hierarchical

    model {
        estudiante = person "Estudiante" "Estudiante matriculado en la UNSA que busca y reserva libros."
        bibliotecario = person "Bibliotecario" "Personal de la biblioteca encargado de gestionar préstamos y multas."

        bibliounsa = softwareSystem "BiblioUNSA" "Permite gestionar el catálogo de libros, reservas, préstamos y multas de la biblioteca." {
            web = container "Aplicación Web" "Interfaz principal para estudiantes y bibliotecarios." "React / PWA" "Web Browser"
            api = container "API REST" "Monolito en capas que procesa la lógica de negocio de préstamos y reservas." "Python / Django"
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
        bibliounsa.web -> bibliounsa.api "Llama a" "HTTPS/JSON"
        bibliounsa.api -> bibliounsa.db "Lee y escribe" "SQL/TCP"
        bibliounsa.api -> sistemaAcademico "Valida matrícula" "HTTPS/JSON"
        bibliounsa.web -> ssoGoogle "Autentica usuario" "OAuth 2.0"
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
            element "Database" {
                shape cylinder
            }
            element "Web Browser" {
                shape WebBrowser
            }
        }
    }
}