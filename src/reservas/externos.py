# src/reservas/externos.py

class SistemaAcademicoSDK:
    """SDK falso de la universidad (API antigua)"""
    def consultar_matricula(self, dni):
        # Retorna un diccionario. '1' es activo, '0' inactivo
        return {"estado_matricula": "1"}

class NotificadorEmail:
    """SDK falso para enviar emails"""
    def send(self, to, subject, body):
        return True