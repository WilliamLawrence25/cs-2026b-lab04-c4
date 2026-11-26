import json

from agentes.agente.nucleo import Agente
from agentes.agente.politica import Politica


class ModeloDosDecisiones:
    def __init__(self):
        self.decisiones = iter(
            [
                {"pensamiento": "Acción sin nombre", "accion": "", "args": {}},
                {"pensamiento": "Terminé", "final": "Decisión inválida rechazada"},
            ]
        )
        self.ultima_respuesta = ""

    def decidir(self, historial):
        decision = next(self.decisiones)
        self.ultima_respuesta = json.dumps(decision)
        return decision


class HerramientasVacias:
    def catalogo(self):
        return {}


def test_traza_registra_transiciones_de_contrato_y_final(tmp_path):
    traza = tmp_path / "traza.jsonl"
    trayectoria = tmp_path / "trayectoria.json"
    agente = Agente(
        modelo=ModeloDosDecisiones(),
        herramientas=HerramientasVacias(),
        politica=Politica(max_pasos=2),
        objetivo="Prueba de máquina de estados",
        traza_archivo=traza,
        trayectoria_archivo=trayectoria,
    )

    resultado = agente.ejecutar()
    estados = [
        json.loads(linea)["estado"]
        for linea in traza.read_text(encoding="utf-8").splitlines()
        if json.loads(linea)["tipo"] == "estado"
    ]

    assert resultado == "Decisión inválida rechazada"
    assert estados == [
        "INICIO",
        "DECIDIENDO",
        "VALIDANDO_CONTRATO",
        "CONTRATO_INVALIDO",
        "OBSERVANDO",
        "DECIDIENDO",
        "VALIDANDO_CONTRATO",
        "FINALIZADO",
        "FIN",
    ]
