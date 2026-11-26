import json
import sys


class ModeloInteractivo:
    def __init__(self, entrada=None, salida=None):
        self.entrada = entrada or sys.stdin
        self.salida = salida or sys.stdout
        self.ultima_respuesta = ""

    def decidir(self, historial: list[dict]) -> dict | str:
        self.salida.write("\n--- CONTEXTO PARA EL ASISTENTE ---\n")
        for mensaje in historial:
            self.salida.write(f"{mensaje['role'].upper()}: {mensaje['content']}\n")
        self.salida.write(
            "\nResponde con una sola decisión JSON del protocolo. "
            "Pégala aquí y presiona Enter:\n> "
        )
        self.salida.flush()
        self.ultima_respuesta = self.entrada.readline().strip()
        try:
            return json.loads(self.ultima_respuesta)
        except json.JSONDecodeError:
            return self.ultima_respuesta
