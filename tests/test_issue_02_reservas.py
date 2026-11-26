import pytest
from src.prestamos.dominio import Estudiante, Libro, ServicioPrestamos, ValidadorMatricula


class ValidadorMatriculaFalso(ValidadorMatricula):
    def __init__(self, vigente: bool):
        self.vigente = vigente

    def esta_matriculado(self, cui: str) -> bool:
        return self.vigente


def test_issue_02_rechaza_reserva_con_matricula_vencida():
    estudiante = Estudiante(cui="20230512", correo="alumno@unsa.edu.pe")
    libro = Libro(isbn="978-0132350884", titulo="Clean Code", copias_disponibles=3)
    servicio = ServicioPrestamos(validador=ValidadorMatriculaFalso(vigente=False))

    with pytest.raises(ValueError, match="Matrícula vencida"):
        servicio.crear_reserva(estudiante, libro)

    assert libro.copias_disponibles == 3