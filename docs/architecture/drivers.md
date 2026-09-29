# Drivers arquitectónicos Caso 4: BiblioUNSA

## 1. Requisitos funcionales clave
| ID | Requisito | Actor | Prioridad |
|---|---|---|---|
| RF-01 | El estudiante consulta el catálogo de libros en línea y verifica disponibilidad. | Estudiante | Alta |
| RF-02 | El estudiante reserva un libro disponible a través de la plataforma. | Estudiante | Alta |
| RF-03 | El sistema valida que el estudiante tenga matrícula vigente consultando el sistema académico. | Sistema académico | Alta |
| RF-04 | El bibliotecario registra el retiro y devolución del libro escaneando el carné QR del estudiante. | Bibliotecario | Alta |
| RF-05 | El sistema calcula y el bibliotecario gestiona el control de multas por devoluciones tardías. | Bibliotecario | Media |

## 2. Atributos de calidad (ordenados por prioridad)
1. **Interoperabilidad (Crítico):** Debe integrarse al sistema académico mediante API para validar matrículas sin exponer ni tocar la base de datos central de la universidad.
2. **Seguridad:** El acceso debe estar estrictamente restringido al correo institucional (`@unsa.edu.pe`) para evitar suplantaciones.
3. **Rendimiento:** Las búsquedas en el catálogo deben ser ágiles incluso en épocas de parciales/finales cuando muchos alumnos buscan bibliografía al mismo tiempo.
4. **Disponibilidad:** El catálogo y la reserva deben funcionar incluso si la API del sistema académico sufre caídas temporales.

## 3. Restricciones
| ID | Tipo | Restricción |
|---|---|---|
| R-01 | Plazo | MVP en producción en 1 mes. |
| R-02 | Equipo | 1 developer (Full-stack), asumiendo toda la carga de frontend, backend y despliegue (modo Solo). |
| R-03 | Presupuesto | Costo cero o mínimo (uso de capa gratuita en la nube, VPS básico o servidor local de la escuela). |
| R-04 | Normativa | Cumplimiento de la Ley 29733 de Protección de Datos Personales (manejo seguro de datos de alumnos). |

## 4. Escenarios de atributos de calidad

| ID | Atributo | Fuente | Estímulo | Entorno | Artefacto | Respuesta | Medida |
|---|---|---|---|---|---|---|---|
| QA-01 | Interoperabilidad | Módulo de Reservas | Solicita validar la matrícula de un alumno para aprobar un préstamo | Operación normal, inicio de semestre | API del Sistema Académico | Se consume el endpoint de validación de la UNSA de forma aislada | 100% de consultas vía API (0 conexiones directas a la BD externa) |
| QA-02 | Seguridad | Estudiante | Intenta iniciar sesión en el sistema web | Red pública o Wi-Fi de la universidad | Módulo de Autenticación | El sistema redirige al SSO (OAuth) de Google Workspace | 100% de logins exitosos pertenecen al dominio `@unsa.edu.pe` |
| QA-03 | Rendimiento | 100 estudiantes concurrentes | Buscan y filtran libros en el catálogo | Semana de exámenes (alta demanda) | API del Catálogo | Devuelve la lista de resultados paginada | p95 del tiempo de respuesta ≤ 1.5 s |