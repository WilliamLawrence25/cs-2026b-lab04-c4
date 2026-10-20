# Comparación: UML vs C4 (Vista Dinámica)

El diagrama de secuencia UML detalla la lógica de control exacta: muestra retornos, llamadas a métodos de clases, mensajes asíncronos y fragmentos alternativos (`alt`/`loop`), siendo ideal para que los **desarrolladores** implementen el código. Por otro lado, la vista dinámica de C4 omite estos detalles internos y de flujo para enfocarse únicamente en cómo interactúan los componentes y contenedores a alto nivel, siendo perfecta para que **arquitectos y líderes técnicos** entiendan la integración del sistema.

## Comparación: Modelado (Structurizr) vs Diagramación (PlantUML manual) - E6

**1. Tiempo invertido:** 
Escribir el diagrama a mano en PlantUML es rápido inicialmente para una sola vista. Sin embargo, estructurar las 5 vistas completas en Structurizr DSL requirió un poco más de tiempo de configuración al principio, pero automatizó la generación masiva de todos los diagramas y formatos.

**2. Errores encontrados:** 
Al diagramar a mano es muy fácil olvidar la leyenda, equivocarse en la sintaxis de las macros de C4 o romper la consistencia (ej. llamar al actor "Estudiante" en un diagrama y "Alumno" en otro). Con Structurizr, la CLI valida la sintaxis y garantiza que cada elemento sea exactamente el mismo en todas las vistas.

**3. Ante un cambio (ej. renombrar un contenedor):** 
- En el **enfoque manual (diagramación)**, tendríamos que buscar y reemplazar el nombre archivo por archivo (en la vista de contenedores, componentes, despliegue y dinámica), con un alto riesgo de introducir inconsistencias.
- En el **enfoque de modelado (Structurizr)**, solo cambiamos el nombre del `container` una vez en el modelo central (`workspace.dsl`). Al ejecutar el exportador, todas las vistas se actualizan automáticamente manteniendo una coherencia absoluta.