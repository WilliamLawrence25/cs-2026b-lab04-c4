# src/reservas/despues/servicio.py
from src.reservas.antes.servicio import Libro, Estudiante
from src.reservas.externos import NotificadorEmail
from src.reservas.despues.estrategias import ValidadorMatriculaAdapter, FabricaMultas, MultaPregrado, MultaPosgrado, MultaDocente
from src.reservas.despues.estados import Pendiente, Confirmada, Cancelada
from src.reservas.despues.eventos import PublicadorEventos, CorreoObserver, LogObserver
from src.reservas.despues.decoradores import ValidadorConCache

class Reserva:
    def __init__(self, estudiante, libro):
        self.estudiante = estudiante
        self.libro = libro
        self._estado = Pendiente()
        self.multa_acumulada = 0.0

    @property
    def estado(self): return self._estado.nombre

    @estado.setter
    def estado(self, valor):
        if valor == "CONFIRMADA": self._estado = Confirmada()
        elif valor == "CANCELADA": self._estado = Cancelada()
        elif valor == "PENDIENTE": self._estado = Pendiente()
        else: raise ValueError("Estado no válido")

    def cambiar_estado(self, nuevo_estado): self._estado = nuevo_estado
    def verificar_puede_procesar(self): self._estado.verificar_puede_procesar()
    def confirmar(self): self._estado.confirmar(self)
    def cancelar(self): self._estado.cancelar(self)

class ServicioReservas:
    def __init__(self, validador=None, fabrica_multas=None):
        # Decoramos el validador base con caché por defecto
        base_validador = validador or ValidadorMatriculaAdapter()
        self.validador = base_validador if hasattr(base_validador, 'llamadas_reales') else ValidadorConCache(base_validador)
        
        self.fabrica = fabrica_multas or FabricaMultas()
        if not fabrica_multas:
            self.fabrica.registrar("PREGRADO", MultaPregrado)
            self.fabrica.registrar("POSGRADO", MultaPosgrado)
            self.fabrica.registrar("DOCENTE", MultaDocente)

        self.email = NotificadorEmail()
        self.eventos = [] # Lista temporal para los tests de caracterización
        
        # PATRÓN OBSERVER: Configuración de suscripciones
        self.publicador = PublicadorEventos()
        correo_obs = CorreoObserver(self.email, self.eventos)
        log_obs = LogObserver(self.eventos)
        
        self.publicador.suscribir("sin_stock", correo_obs)
        self.publicador.suscribir("matricula_inactiva", correo_obs)
        self.publicador.suscribir("reserva_confirmada", correo_obs)
        self.publicador.suscribir("reserva_confirmada", log_obs)

    def procesar_reserva(self, reserva):
        reserva.verificar_puede_procesar()

        if reserva.libro.stock <= 0:
            reserva.cancelar()
            self.publicador.publicar("sin_stock", {"correo": reserva.estudiante.correo})
            return reserva.estado

        if not self.validador.es_matricula_activa(reserva.estudiante.dni):
            reserva.cancelar()
            self.publicador.publicar("matricula_inactiva", {"correo": reserva.estudiante.correo})
            return reserva.estado

        reserva.confirmar()
        reserva.multa_acumulada = self.fabrica.crear(reserva.estudiante.tipo).calcular()
        reserva.libro.stock -= 1
        
        self.publicador.publicar("reserva_confirmada", {
            "correo": reserva.estudiante.correo, 
            "dni": reserva.estudiante.dni, 
            "libro_id": reserva.libro.id
        })

        return reserva.estado