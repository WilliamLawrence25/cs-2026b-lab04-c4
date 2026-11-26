import json

from agentes.agente.herramientas import Herramientas
from agentes.agente.modelo_grabado import ModeloGrabado
from agentes.agente.nucleo import Agente
from agentes.agente.politica import Politica, aprobar_edicion_en_consola


def _agente(tmp_path, politica):
    archivo = tmp_path / "ejemplo.txt"
    archivo.write_text("antes\n", encoding="utf-8")
    decisiones = [
        {
            "pensamiento": "Solicito editar el archivo.",
            "accion": "editar_archivo",
            "args": {
                "ruta": "ejemplo.txt",
                "antes": "antes\n",
                "despues": "después\n",
            },
        },
        {"pensamiento": "Terminé.", "final": "Fin de la prueba."},
    ]
    agente = Agente(
        modelo=ModeloGrabado(decisiones),
        herramientas=Herramientas(tmp_path),
        politica=politica,
        objetivo="Prueba de aprobación humana.",
        traza_archivo=tmp_path / "traza.jsonl",
        trayectoria_archivo=tmp_path / "trayectoria.json",
    )
    return agente, archivo


def test_aprobacion_consola_reintenta_hasta_recibir_s_o_n(monkeypatch, capsys):
    respuestas = iter(["tal vez", " s "])
    monkeypatch.setattr("builtins.input", lambda _: next(respuestas))

    assert aprobar_edicion_en_consola("ejemplo.txt", "antes", "después")
    salida = capsys.readouterr().out
    assert "Respuesta no válida" in salida
    assert "Contenido propuesto" in salida


def test_edicion_aprobada_se_ejecuta_y_queda_en_traza(tmp_path, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "s")
    agente, archivo = _agente(
        tmp_path,
        Politica(aprobar_edicion=aprobar_edicion_en_consola),
    )

    agente.ejecutar()

    assert archivo.read_text(encoding="utf-8") == "después\n"
    eventos = [
        json.loads(linea)
        for linea in (tmp_path / "traza.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    aprobaciones = [evento for evento in eventos if evento["tipo"] == "aprobacion_humana"]
    assert len(aprobaciones) == 1
    assert aprobaciones[0]["estado"] == "APROBADA"


def test_edicion_rechazada_no_se_ejecuta_y_queda_en_traza(tmp_path, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    agente, archivo = _agente(
        tmp_path,
        Politica(aprobar_edicion=aprobar_edicion_en_consola),
    )

    agente.ejecutar()

    assert archivo.read_text(encoding="utf-8") == "antes\n"
    eventos = [
        json.loads(linea)
        for linea in (tmp_path / "traza.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    aprobaciones = [evento for evento in eventos if evento["tipo"] == "aprobacion_humana"]
    assert len(aprobaciones) == 1
    assert aprobaciones[0]["estado"] == "RECHAZADA"
    assert any(evento.get("estado") == "BLOQUEADO" for evento in eventos)
