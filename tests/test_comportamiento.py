# tests/test_comportamiento.py
import pytest
import importlib

# Parametrizamos para probar la versión "antes" (y luego agregaremos "despues")
@pytest.fixture(params=["src.reservas.antes.servicio"])
def m(request):
    return importlib.import_module(request.param)

def estudiante_pregrado(m):
    return m.Estudiante(dni="70123456", correo="estudiante@unsa.edu.pe", tipo="PREGRADO")

def libro_disponible(m):
    return m.Libro(id="L001", titulo="Clean Code", stock=5)

def test_reserva_exitosa_confirma_y_notifica(m):
    servicio = m.ServicioReservas()
    reserva = m.Reserva(estudiante_pregrado(m), libro_disponible(m))
    
    assert servicio.procesar_reserva(reserva) == "CONFIRMADA"
    assert reserva.libro.stock == 4
    assert reserva.multa_acumulada == 2.0
    assert "email: estudiante@unsa.edu.pe: Reserva confirmada" in servicio.eventos

def test_reserva_sin_stock_cancela(m):
    servicio = m.ServicioReservas()
    libro = m.Libro(id="L002", titulo="Patrones", stock=0)
    reserva = m.Reserva(estudiante_pregrado(m), libro)
    
    assert servicio.procesar_reserva(reserva) == "CANCELADA"
    assert "email: estudiante@unsa.edu.pe: Sin stock" in servicio.eventos

def test_tipo_usuario_no_soportado_lanza_error(m):
    servicio = m.ServicioReservas()
    est = m.Estudiante(dni="111", correo="x@x.com", tipo="EXTERNO")
    reserva = m.Reserva(est, libro_disponible(m))
    
    with pytest.raises(ValueError, match="Tipo de usuario no soportado"):
        servicio.procesar_reserva(reserva)

def test_estado_invalido_lanza_error(m):
    servicio = m.ServicioReservas()
    reserva = m.Reserva(estudiante_pregrado(m), libro_disponible(m))
    reserva.estado = "CONFIRMADA"
    
    with pytest.raises(ValueError, match="La reserva ya fue confirmada"):
        servicio.procesar_reserva(reserva)