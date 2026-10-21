# src/reservas/despues/servicio.py
from src.reservas.antes.servicio import Reserva, Libro, Estudiante # Reutilizamos las clases de datos
from src.reservas.externos import NotificadorEmail
from src.reservas.despues.estrategias import (
    ValidadorMatriculaAdapter, FabricaMultas, 
    MultaPregrado, MultaPosgrado, MultaDocente
)

class ServicioReservas:
    def __init__(self, validador_adapter=None, fabrica_multas=None):
        # Inyectamos el Adapter
        self.validador = validador_adapter or ValidadorMatriculaAdapter()
        
        # Inyectamos o inicializamos la Factory con sus Strategies
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
        # Aún huele mal (if/elif anidados), lo arreglaremos en E3 con State
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

        # PATRÓN ADAPTER: Código limpio sin diccionarios nativos del SDK
        if not self.validador.es_matricula_activa(reserva.estudiante.dni):
            reserva.estado = "CANCELADA"
            self.eventos.append(f"email: {reserva.estudiante.correo}: Matricula inactiva")
            return reserva.estado

        # PATRÓN FACTORY + STRATEGY: Eliminamos los if/elif por tipo de usuario
        calculador = self.fabrica.crear(reserva.estudiante.tipo)
        reserva.multa_acumulada = calculador.calcular()

        reserva.estado = "CONFIRMADA"
        reserva.libro.stock -= 1
        
        self.email.send(reserva.estudiante.correo, "Reserva exitosa", "Tu libro te espera")
        self.eventos.append(f"email: {reserva.estudiante.correo}: Reserva confirmada")
        self.eventos.append(f"log: Reserva {reserva.libro.id} por {reserva.estudiante.dni}")

        return reserva.estado