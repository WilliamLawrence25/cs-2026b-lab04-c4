# tests/test_patrones.py
import pytest
from src.reservas.antes.servicio import Estudiante, Libro
from src.reservas.despues.estrategias import FabricaMultas, CalculadorMulta, MultaPregrado, MultaPosgrado, MultaDocente
from src.reservas.despues.servicio import ServicioReservas, Reserva # ¡Aquí importamos la Reserva nueva!

# Nueva variante externa sin tocar el servicio
class MultaInvitado(CalculadorMulta):
    def calcular(self) -> float:
        return 10.0

def test_open_closed_nuevo_tipo_sin_modificar_servicio():
    fabrica = FabricaMultas()
    fabrica.registrar("PREGRADO", MultaPregrado)
    fabrica.registrar("POSGRADO", MultaPosgrado)
    fabrica.registrar("DOCENTE", MultaDocente)
    fabrica.registrar("INVITADO", MultaInvitado)
    
    servicio = ServicioReservas(fabrica_multas=fabrica)
    estudiante = Estudiante(dni="999", correo="invi@test.com", tipo="INVITADO")
    # Ahora usamos la Reserva que entiende el patrón State
    reserva = Reserva(estudiante, Libro("L003", "Test", 1))
    
    assert servicio.procesar_reserva(reserva) == "CONFIRMADA"
    assert reserva.multa_acumulada == 10.0

def test_state_impide_transiciones_invalidas():
    # Creamos un estudiante y libro falsos solo para la prueba
    estudiante = Estudiante("1", "a@a.com", "PREGRADO")
    reserva = Reserva(estudiante, Libro("L1", "T", 1))
    
    # Lo forzamos a estado cancelado
    reserva.estado = "CANCELADA"
    
    # Comprobamos que el State bloquea el intento de confirmarlo
    with pytest.raises(ValueError, match="La reserva ya fue cancelada"):
        reserva.confirmar()