# src/reservas/despues/eventos.py
from abc import ABC, abstractmethod

class Suscriptor(ABC):
    @abstractmethod
    def actualizar(self, evento: str, datos: dict):
        pass

class PublicadorEventos:
    def __init__(self):
        self._suscriptores = {}

    def suscribir(self, evento: str, suscriptor: Suscriptor):
        self._suscriptores.setdefault(evento, []).append(suscriptor)

    def publicar(self, evento: str, datos: dict):
        for s in self._suscriptores.get(evento, []):
            s.actualizar(evento, datos)

# --- SUSCRIPTORES CONCRETOS ---
class CorreoObserver(Suscriptor):
    def __init__(self, email_sdk, lista_eventos):
        self.email = email_sdk
        self.eventos = lista_eventos # Mantenemos la lista para que las pruebas pasen

    def actualizar(self, evento: str, datos: dict):
        correo = datos.get("correo")
        if evento == "reserva_confirmada":
            self.email.send(correo, "Reserva exitosa", "Tu libro te espera")
            self.eventos.append(f"email: {correo}: Reserva confirmada")
        elif evento == "sin_stock":
            self.eventos.append(f"email: {correo}: Sin stock")
        elif evento == "matricula_inactiva":
            self.eventos.append(f"email: {correo}: Matricula inactiva")

class LogObserver(Suscriptor):
    def __init__(self, lista_eventos):
        self.eventos = lista_eventos

    def actualizar(self, evento: str, datos: dict):
        if evento == "reserva_confirmada":
            self.eventos.append(f"log: Reserva {datos['libro_id']} por {datos['dni']}")