workspace "BiblioUNSA" "Modelo C4 del Sistema de Bibliotecas de la UNSA" {

    !identifiers hierarchical

    model {
        estudiante = person "Estudiante" "Estudiante matriculado en la UNSA que busca y reserva libros."
        bibliotecario = person "Bibliotecario" "Personal de la biblioteca encargado de gestionar préstamos y multas."

        bibliounsa = softwareSystem "BiblioUNSA" "Permite gestionar el catálogo de libros, reservas, préstamos y multas de la biblioteca." {
            // Los contenedores se añadirán en el E2
        }

        sistemaAcademico = softwareSystem "Sistema Académico UNSA" "Sistema central de la universidad para validar matrículas." "Externo"
        ssoGoogle = softwareSystem "Google Workspace" "Servicio de SSO para autenticación con cuentas institucionales." "Externo"

        estudiante -> bibliounsa "Busca libros, realiza reservas y consulta su estado"
        bibliotecario -> bibliounsa "Gestiona préstamos, devoluciones y cobra multas"
        
        bibliounsa -> sistemaAcademico "Valida matrícula vigente" "HTTPS/JSON"
        bibliounsa -> ssoGoogle "Delega autenticación de usuarios" "OAuth 2.0"
    }

    views {
        systemContext bibliounsa "Contexto" "Nivel 1: BiblioUNSA y su entorno institucional." {
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
            }
        }
    }
}