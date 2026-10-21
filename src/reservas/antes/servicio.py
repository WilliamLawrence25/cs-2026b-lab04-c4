# src/reservas/antes/servicio.py
from dataclasses import dataclass
from src.reservas.externos import SistemaAcademicoSDK, NotificadorEmail

@dataclass
class Libro:
    id: str
    titulo: str
    stock: int
    es_coleccion_reserva: bool = False

@dataclass
class Estudiante:
    dni: str
    correo: str
    tipo: str = "PREGRADO" # PREGRADO, POSGRADO, DOCENTE

class Reserva:
    def __init__(self, estudiante, libro):
        self.estudiante = estudiante
        self.libro = libro
        self.estado = "PENDIENTE"
        self.multa_acumulada = 0.0

class ServicioReservas:
    def __init__(self):
        self.api_unsa = SistemaAcademicoSDK()
        self.email = NotificadorEmail()
        self.eventos = []

    def procesar_reserva(self, reserva):
        # OLOR 1: Condicionales anidados basados en estado
        if reserva.estado != "PENDIENTE":
            if reserva.estado == "CANCELADA":
                raise ValueError("La reserva ya fue cancelada")
            elif reserva.estado == "CONFIRMADA":
                raise ValueError("La reserva ya fue confirmada")
            else:
                raise ValueError("Estado no válido")

        if reserva.libro.stock <= 0:
            reserva.estado = "CANCELADA"
            self.eventos.append(f"email: {reserva.estudiante.correo}: Sin stock")
            return reserva.estado

        # OLOR 2: Conoce detalles internos del SDK de la UNSA
        respuesta = self.api_unsa.consultar_matricula(reserva.estudiante.dni)
        if respuesta.get("estado_matricula") != "1":
            reserva.estado = "CANCELADA"
            self.eventos.append(f"email: {reserva.estudiante.correo}: Matricula inactiva")
            return reserva.estado

        # OLOR 3: if/elif que crece por tipo de usuario (para la penalización)
        if reserva.estudiante.tipo == "PREGRADO":
            reserva.multa_acumulada = 2.0  # 2 soles por día de atraso
        elif reserva.estudiante.tipo == "POSGRADO":
            reserva.multa_acumulada = 5.0
        elif reserva.estudiante.tipo == "DOCENTE":
            reserva.multa_acumulada = 0.0
        else:
            raise ValueError(f"Tipo de usuario no soportado: {reserva.estudiante.tipo}")

        reserva.estado = "CONFIRMADA"
        reserva.libro.stock -= 1
        
        # OLOR 4: Arma las notificaciones a mano
        self.email.send(reserva.estudiante.correo, "Reserva exitosa", "Tu libro te espera")
        self.eventos.append(f"email: {reserva.estudiante.correo}: Reserva confirmada")
        self.eventos.append(f"log: Reserva {reserva.libro.id} por {reserva.estudiante.dni}")

        return reserva.estado