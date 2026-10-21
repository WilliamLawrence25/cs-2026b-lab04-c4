# src/reservas/despues/servicio.py
from src.reservas.antes.servicio import Libro, Estudiante
from src.reservas.externos import NotificadorEmail
from src.reservas.despues.estrategias import (
    ValidadorMatriculaAdapter, FabricaMultas, 
    MultaPregrado, MultaPosgrado, MultaDocente
)
from src.reservas.despues.estados import Pendiente, Confirmada, Cancelada

class Reserva:
    """Entidad Reserva ahora gobernada por el patrón State"""
    def __init__(self, estudiante, libro):
        self.estudiante = estudiante
        self.libro = libro
        self._estado = Pendiente()
        self.multa_acumulada = 0.0

    @property
    def estado(self):
        return self._estado.nombre

    @estado.setter
    def estado(self, valor):
        # Mantiene compatibilidad con las pruebas de caracterización del E1
        if valor == "CONFIRMADA": self._estado = Confirmada()
        elif valor == "CANCELADA": self._estado = Cancelada()
        elif valor == "PENDIENTE": self._estado = Pendiente()
        else: raise ValueError("Estado no válido")

    def cambiar_estado(self, nuevo_estado):
        self._estado = nuevo_estado

    def verificar_puede_procesar(self):
        self._estado.verificar_puede_procesar()

    def confirmar(self):
        self._estado.confirmar(self)

    def cancelar(self):
        self._estado.cancelar(self)


class ServicioReservas:
    def __init__(self, validador_adapter=None, fabrica_multas=None):
        self.validador = validador_adapter or ValidadorMatriculaAdapter()
        
        if fabrica_multas:
            self.fabrica = fabrica_multas
        else:
            self.fabrica = FabricaMultas()
            self.fabrica.registrar("PREGRADO", MultaPregrado)
            self.fabrica.registrar("POSGRADO", MultaPosgrado)
            self.fabrica.registrar("DOCENTE", MultaDocente)

        self.email = NotificadorEmail()
        self.eventos = []

    def procesar_reserva(self, reserva):
        # PATRÓN STATE: Delegamos la validación inicial al objeto estado (Adiós if/elif)
        reserva.verificar_puede_procesar()

        if reserva.libro.stock <= 0:
            reserva.cancelar()
            self.eventos.append(f"email: {reserva.estudiante.correo}: Sin stock")
            return reserva.estado

        # PATRÓN ADAPTER
        if not self.validador.es_matricula_activa(reserva.estudiante.dni):
            reserva.cancelar()
            self.eventos.append(f"email: {reserva.estudiante.correo}: Matricula inactiva")
            return reserva.estado

        # PATRÓN STATE: Cambia su estado internamente
        reserva.confirmar()

        # PATRÓN FACTORY + STRATEGY
        calculador = self.fabrica.crear(reserva.estudiante.tipo)
        reserva.multa_acumulada = calculador.calcular()

        reserva.libro.stock -= 1
        
        self.email.send(reserva.estudiante.correo, "Reserva exitosa", "Tu libro te espera")
        self.eventos.append(f"email: {reserva.estudiante.correo}: Reserva confirmada")
        self.eventos.append(f"log: Reserva {reserva.libro.id} por {reserva.estudiante.dni}")

        return reserva.estado