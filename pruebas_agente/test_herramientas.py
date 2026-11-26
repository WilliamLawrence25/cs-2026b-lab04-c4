import pytest

from agentes.agente.herramientas import Herramientas
from agentes.agente.politica import Politica


def test_mapa_repo_extrae_archivos_clases_y_firmas(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "ejemplo.py").write_text(
        "class Prestamo:\n"
        "    def esta_vencido(self, fecha_corte: str) -> bool:\n"
        "        return False\n"
        "\n"
        "async def consultar(cui: str) -> dict:\n"
        "    return {}\n",
        encoding="utf-8",
    )
    herramientas = Herramientas(tmp_path)

    resultado = herramientas.mapa_repo()

    assert "ejemplo.py" in resultado
    assert "class Prestamo" in resultado
    assert "def esta_vencido(self, fecha_corte: str) -> bool" in resultado
    assert "async def consultar(cui: str) -> dict" in resultado


def test_memoria_de_notas_persiste_y_agrega_notas(tmp_path):
    archivo_notas = tmp_path / "agentes/notas.md"
    herramientas = Herramientas(tmp_path, archivo_notas=archivo_notas)

    assert herramientas.leer_notas() == "(sin notas registradas)"
    assert "Nota guardada" in herramientas.anotar("Hipótesis: revisar Prestamo.esta_vencido")
    herramientas.anotar("Revisado: tests/test_issue_03_prestamos.py")

    notas = herramientas.leer_notas()
    assert "Hipótesis: revisar Prestamo.esta_vencido" in notas
    assert "Revisado: tests/test_issue_03_prestamos.py" in notas
    assert notas.count("\n") == 2


def test_memoria_rechaza_notas_vacias(tmp_path):
    herramientas = Herramientas(tmp_path, archivo_notas=tmp_path / "notas.md")

    with pytest.raises(ValueError, match="texto no vacío"):
        herramientas.anotar("  ")


def test_catalogo_y_politica_exponen_nuevas_herramientas(tmp_path):
    herramientas = Herramientas(tmp_path)
    politica = Politica()

    for nombre in ("mapa_repo", "anotar", "leer_notas"):
        assert nombre in herramientas.catalogo()
        assert nombre in politica.herramientas_permitidas
