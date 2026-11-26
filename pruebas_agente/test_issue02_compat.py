from src.prestamos.dominio import Estudiante, Libro, ServicioPrestamos


def test_servicio_sin_validador_conserva_reserva_existente():
    estudiante = Estudiante(cui="20230512", correo="alumno@unsa.edu.pe")
    libro = Libro(isbn="978-0132350884", titulo="Clean Code", copias_disponibles=2)

    prestamo = ServicioPrestamos().crear_reserva(estudiante, libro)

    assert prestamo.estudiante == estudiante
    assert libro.copias_disponibles == 1
