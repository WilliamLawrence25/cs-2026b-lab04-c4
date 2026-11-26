from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

class EstadoPrestamo(Enum):
    RESERVADO = "RESERVADO"
    PRESTADO = "PRESTADO"
    VENCIDO = "VENCIDO"
    DEVUELTO = "DEVUELTO"
    CON_MULTA = "CON_MULTA"

@dataclass
class Estudiante:
    cui: str
    correo: str

    def consultar_estado(self) -> str:
        pass

@dataclass
class Libro:
    isbn: str
    titulo: str
    copias_disponibles: int

    def reservar_copia(self) -> None:
        if self.copias_disponibles > 0:
            self.copias_disponibles -= 1
        else:
            raise ValueError("No hay copias disponibles")

    def liberar_copia(self) -> None:
        self.copias_disponibles += 1

@dataclass
class Multa:
    id: UUID = field(default_factory=uuid4)
    monto: float = 0.0
    pagada: bool = False

    def calcular_dias_retraso(self) -> int:
        pass

    def calcular_monto_atraso(self, fecha_limite: datetime, fecha_devolucion: datetime, tarifa_diaria: float = 2.0) -> float:
        if fecha_devolucion <= fecha_limite:
            return 0.0
        fecha = fecha_limite.date() + timedelta(days=1)
        dias = 0
        while fecha <= fecha_devolucion.date():
            if fecha.weekday() != 6:
                dias += 1
            fecha += timedelta(days=1)
        self.monto = round(dias * tarifa_diaria, 2)
        return self.monto

    def pagar(self) -> None:
        self.pagada = True


@dataclass
class Prestamo:
    estudiante: Estudiante
    libro: Libro
    id: UUID = field(default_factory=uuid4)
    fecha_inicio: datetime = field(default_factory=datetime.now)
    fecha_limite: datetime = field(default_factory=datetime.now)
    fecha_devolucion: Optional[datetime] = None
    estado: EstadoPrestamo = EstadoPrestamo.RESERVADO
    multa: Optional[Multa] = None

    def confirmar_reserva(self, cui: str, isbn: str) -> None:
        self.libro.reservar_copia()
        self.estado = EstadoPrestamo.RESERVADO

    def registrar_entrega(self) -> None:
        self.estado = EstadoPrestamo.PRESTADO

    def registrar_devolucion(self) -> None:
        self.libro.liberar_copia()
        if self.multa and not self.multa.pagada:
            self.estado = EstadoPrestamo.CON_MULTA
        else:
            self.estado = EstadoPrestamo.DEVUELTO

    def aplicar_multa(self, monto: float) -> None:
        self.multa = Multa(monto=monto)
        self.estado = EstadoPrestamo.CON_MULTA

    def esta_vencido(self, fecha_corte: datetime) -> bool:
        # BUG ISSUE-03: ignora si el prestamo ya fue devuelto
        return fecha_corte > self.fecha_limite

class ValidadorMatricula(ABC):
    @abstractmethod
    def esta_matriculado(self, cui: str) -> bool:
        pass

class ApiUnsaAdapter(ValidadorMatricula):
    def esta_matriculado(self, cui: str) -> bool:
        raise NotImplementedError("Integrar con la API del Sistema Académico")

class ServicioPrestamos:
    def __init__(self, validador: Optional[ValidadorMatricula] = None):
        self.validador = validador

    def crear_reserva(self, estudiante: Estudiante, libro: Libro) -> Prestamo:
        # BUG ISSUE-02: omite validar si la matricula del estudiante esta vigente
        prestamo = Prestamo(estudiante=estudiante, libro=libro)
        prestamo.confirmar_reserva(estudiante.cui, libro.isbn)
        return prestamo