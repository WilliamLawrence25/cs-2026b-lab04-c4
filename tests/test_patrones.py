# tests/test_patrones.py
import pytest
from src.reservas.antes.servicio import Reserva, Estudiante, Libro
from src.reservas.despues.estrategias import FabricaMultas, CalculadorMulta, MultaPregrado, MultaPosgrado, MultaDocente
from src.reservas.despues.servicio import ServicioReservas

# Nueva variante externa sin tocar el servicio
class MultaInvitado(CalculadorMulta):
    def calcular(self) -> float:
        return 10.0

def test_open_closed_nuevo_tipo_sin_modificar_servicio():
    fabrica = FabricaMultas()
    fabrica.registrar("PREGRADO", MultaPregrado)
    fabrica.registrar("POSGRADO", MultaPosgrado)
    fabrica.registrar("DOCENTE", MultaDocente)
    # Registramos el nuevo tipo (Extensión abierta) sin tocar el if/elif (Modificación cerrada)
    fabrica.registrar("INVITADO", MultaInvitado)
    
    servicio = ServicioReservas(fabrica_multas=fabrica)
    estudiante = Estudiante(dni="999", correo="invi@test.com", tipo="INVITADO")
    reserva = Reserva(estudiante, Libro("L003", "Test", 1))
    
    assert servicio.procesar_reserva(reserva) == "CONFIRMADA"
    assert reserva.multa_acumulada == 10.0