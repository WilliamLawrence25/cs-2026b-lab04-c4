# ADR-002: Uso de OAuth 2.0 (Google Workspace) para autenticación de estudiantes

Estado: Aceptado
Fecha: 2026-09-29
Decisores: William Choquehuanca (Developer Full-stack)

## Contexto
El sistema debe garantizar que solo estudiantes de la universidad accedan (QA-02) y se debe cumplir con la normativa de protección de datos personales (R-04) evitando almacenar contraseñas sensibles en nuestra propia base de datos. 

## Alternativas consideradas
1. Autenticación delegada vía OAuth 2.0 (SSO de Google Workspace con @unsa.edu.pe).
2. Registro manual y gestión propia de usuarios con contraseñas (JWT/Session).

## Decisión
Implementaremos la autenticación delegada mediante OAuth 2.0 integrando el Single Sign-On (SSO) de Google Workspace. Solo se aceptarán tokens de acceso que provengan del dominio `@unsa.edu.pe`.

## Consecuencias
Positivas: 
- Alta seguridad (QA-02) delegando el manejo de credenciales a Google.
- Cumplimiento de protección de datos (R-04) ya que no almacenamos contraseñas.
- Menor tiempo de desarrollo al no programar flujos de recuperación de contraseñas.
Negativas / riesgos: 
- Fuerte dependencia de la disponibilidad del servicio de Google.