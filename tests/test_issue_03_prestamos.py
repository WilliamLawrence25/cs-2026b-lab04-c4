from datetime import datetime
from src.prestamos.dominio import EstadoPrestamo, Estudiante, Libro, Prestamo


def test_issue_03_prestamo_devuelto_no_esta_vencido():
    estudiante = Estudiante(cui="20230512", correo="alumno@unsa.edu.pe")
    libro = Libro(isbn="978-0132350884", titulo="Clean Code", copias_disponibles=2)
    prestamo = Prestamo(
        estudiante=estudiante,
        libro=libro,
        fecha_inicio=datetime(2026, 11, 1, 10, 0),
        fecha_limite=datetime(2026, 11, 5, 18, 0),
        fecha_devolucion=datetime(2026, 11, 4, 15, 0),
        estado=EstadoPrestamo.DEVUELTO,
    )
    assert prestamo.esta_vencido(datetime(2026, 11, 10, 12, 0)) is False