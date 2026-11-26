import json
from pathlib import Path
from typing import Any


class ModeloGrabado:
    def __init__(self, decisiones: list[dict[str, Any]]):
        self._decisiones = iter(decisiones)
        self.ultima_respuesta = ""

    @classmethod
    def desde_archivo(cls, ruta: str | Path) -> "ModeloGrabado":
        archivo = Path(ruta)
        datos = json.loads(archivo.read_text(encoding="utf-8"))
        decisiones = datos["decisiones"]
        if not isinstance(decisiones, list) or not decisiones:
            raise ValueError(f"La trayectoria no contiene decisiones: {archivo}")
        return cls(decisiones)

    def decidir(self, _historial: list[dict[str, str]]) -> dict[str, Any]:
        decision = next(self._decisiones)
        self.ultima_respuesta = json.dumps(decision, ensure_ascii=False)
        return decision
