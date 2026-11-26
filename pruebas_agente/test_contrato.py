import pytest

from agentes.agente.contrato import validar_decision


HERRAMIENTAS = {"leer_archivo", "ejecutar_pruebas"}


@pytest.mark.parametrize(
    ("decision", "motivo"),
    [
        (
            {
                "pensamiento": "Leeré el código",
                "accion": "leer_archivo",
                "args": {"ruta": "src.py"},
                "extra": True,
            },
            "campos no permitidos",
        ),
        (
            {"pensamiento": "Probaré el issue", "accion": "ejecutar_pruebas", "args": "tests"},
            "'args' debe ser un objeto JSON",
        ),
        (
            {"pensamiento": "Ejecutaré una acción", "accion": "", "args": {}},
            "herramienta desconocida",
        ),
        (
            {"pensamiento": "Haré algo", "accion": "borrar_todo", "args": {}},
            "herramienta desconocida",
        ),
        (
            {"pensamiento": "Terminé", "final": "Listo", "extra": "campo"},
            "campos no permitidos",
        ),
        ("leer_archivo('src.py')", "no es JSON válido"),
    ],
)
def test_contrato_rechaza_decisiones_invalidas(decision, motivo):
    valida, error = validar_decision(decision, HERRAMIENTAS)

    assert valida is False
    assert motivo in error


@pytest.mark.parametrize(
    "decision",
    [
        {"pensamiento": "Leeré el código", "accion": "leer_archivo", "args": {"ruta": "src.py"}},
        {"pensamiento": "El trabajo terminó", "final": "Prueba aprobada"},
    ],
)
def test_contrato_acepta_decisiones_validas(decision):
    valida, error = validar_decision(decision, HERRAMIENTAS)

    assert valida is True
    assert error == ""
