# Bitácora de uso de IA Caso 4: BiblioUNSA

| # | Fecha | Herramienta | Prompt (resumen) | Qué propuso la IA | Qué verificamos o corregimos | Decisión |
|---|---|---|---|---|---|---|
| 1 | 2026-09-29 | Gemini | Propón 3 alternativas de estilo arquitectónico para BiblioUNSA con 1 developer y 1 mes. | Microservicios como mejor opción por su "alta escalabilidad". | Excede R-01 (1 mes) y R-02 (1 developer). Imposible orquestar microservicios en solitario. | Rechazada |
| 2 | 2026-09-29 | Gemini | Actúa como abogado del diablo y critica tu recomendación de Microservicios. | Identificó altos costos operativos, sobrecarga cognitiva y lentitud de despliegue inicial. | Confirmó nuestras sospechas. Descartamos definitivamente la opción para el MVP. | Aceptada |
| 3 | 2026-09-29 | Gemini | Genera el código Mermaid para un Monolito en capas de este caso. | Diagrama genérico con base de datos local y login propio. | Faltaban las integraciones clave. Se corrigió manualmente para incluir API Académico y SSO Google. | Corregida |
| 4 | 2026-09-29 | Gemini | Redacta los ADRs para arquitectura, base de datos y autenticación. | ADRs bien estructurados pero sugería AWS RDS y Cognito (servicios en la nube de pago). | Se modificaron para usar PostgreSQL en VPS y Google Workspace gratis, respetando la R-03. | Corregida |
| 5 | 2026-09-29 | Gemini | Script en Python Diagrams para la vista de despliegue. | Diagrama usando proveedores de la nube (AWS EC2, RDS). | Se modificó el código para usar la librería genérica `onprem` (Nginx, Django, PostgreSQL) reflejando un VPS económico. | Corregida |

## Anexo: Prompts utilizados

**Prompt 1 (Generación de alternativas):**
"Actúa como arquitecto senior. Contexto: Sistema BiblioUNSA para préstamo y reserva de libros. Restricciones: 1 solo developer, 1 mes de plazo, presupuesto cero. Propón 3 alternativas de estilo arquitectónico. Para cada una indica fortalezas, debilidades, riesgos y qué atributos de calidad favorece."

**Prompt 2 (Crítica adversarial):**
"Ahora actúa como 'abogado del diablo'. Critica duramente la alternativa de Microservicios considerando que soy 1 solo developer y tengo 1 mes de plazo. Enumera los riesgos más graves para estas restricciones."

**Prompt 3 (Código Mermaid):**
"Genera el código Mermaid (`flowchart TB`) para la arquitectura elegida: Monolito en capas. Incluye a los actores (estudiante, bibliotecario) y los módulos lógicos (catálogo, reservas y préstamos). Usa estilos y colores diferenciados."

**Prompt 4 (Redacción ADRs):**
"Usando el formato estándar de Architecture Decision Records, redacta 3 decisiones: estilo arquitectónico (Monolito en capas), base de datos relacional y autenticación segura para el sistema BiblioUNSA."

**Prompt 5 (Despliegue Python Diagrams):**
"Genera un script en Python usando la librería 'diagrams' de mingrammer para mostrar la vista de despliegue de esta aplicación. Debe mostrar a los usuarios accediendo desde móviles/web hacia un proxy Nginx, la app, una base de datos PostgreSQL y los servicios externos."