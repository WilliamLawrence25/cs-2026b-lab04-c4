# HU-01: Reservar libro con validación de matrícula

**Como** estudiante de la UNSA,
**quiero** reservar un libro en el catálogo en línea verificando mi matrícula vigente,
**para** asegurar la disponibilidad del texto antes de ir a la biblioteca.

## Criterios de aceptación

1. **Reserva exitosa:** Dado un libro con stock disponible y un estudiante con matrícula vigente (validada en el Sistema Académico), cuando el estudiante confirma la reserva, entonces el stock del libro disminuye en 1, el estado del préstamo pasa a RESERVADO y se notifica por correo institucional.
2. **Matrícula inválida:** Dado un estudiante sin matrícula activa en el semestre en curso, cuando intenta reservar un libro, entonces el sistema rechaza la operación, el stock no se altera y se muestra un mensaje de "Matrícula no vigente".