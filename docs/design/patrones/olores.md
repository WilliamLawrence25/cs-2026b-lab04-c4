# Olores de Código Detectados en BiblioUNSA

| Olor detectado | Patrón propuesto | Principio SOLID | Decisión del equipo |
| :--- | :--- | :--- | :--- |
| if/elif anidados sobre `reserva.estado` ("PENDIENTE", "CONFIRMADA"). | **State** | OCP (Abierto/Cerrado), SRP | Aceptado: Implementaremos la máquina de estados del Lab 05. |
| El servicio conoce los detalles del diccionario del `SistemaAcademicoSDK`. | **Adapter** | DIP (Inversión de dependencias) | Aceptado: Aislará la API antigua de la UNSA. |
| if/elif que crece por tipo de usuario (`PREGRADO`, `POSGRADO`) para calcular la multa. | **Strategy** | OCP (Abierto/Cerrado) | Aceptado: Cada tipo de usuario será una estrategia de penalización. |
| El servicio mezcla la reserva con la creación manual de notificaciones y logs. | **Observer** | SRP (Responsabilidad Única) | Aceptado: Separará los eventos de la lógica de negocio. |