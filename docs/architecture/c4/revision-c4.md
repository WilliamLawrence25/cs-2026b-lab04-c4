# Revisión del Modelo C4 - BiblioUNSA

| Vista | Pregunta de la lista oficial | Cumple | Verificación y Hallazgos de la IA |
| :--- | :--- | :--- | :--- |
| **Todas** | Generales: ¿Tienen título, leyenda y descripción clara? | Sí | Structurizr genera automáticamente títulos y leyendas basados en el bloque `views`. |
| **Contenedores** | Elementos: ¿Se indica la tecnología exacta de cada uno? | Sí | Especificado explícitamente: React / PWA, Python / Django, PostgreSQL 16. |
| **Componentes** | Relaciones: ¿Tienen verbo de intención y protocolo? | Sí | Las dependencias indican intenciones claras ("Verifica y reserva stock") sin ciclos. |
| **Contexto** | Relaciones: ¿Faltan tecnologías en las flechas de usuarios? | Sí | **Falso positivo de la IA:** La IA observó como error que la relación "Estudiante -> BiblioUNSA" no tuviera protocolo. Rechazado: En el Nivel 1 (Contexto) no se detallan protocolos técnicos hacia los usuarios humanos. |
| **Despliegue** | Elementos: ¿Se entienden los nodos de ejecución? | Sí | Se detalla el uso de Ubuntu 24.04 y Docker 27. |