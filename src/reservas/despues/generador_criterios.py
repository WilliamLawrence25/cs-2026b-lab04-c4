import json
import pathlib
import re
from jsonschema import ValidationError, validate
from src.reservas.despues.ia import ProveedorLLM

RAIZ = pathlib.Path(__file__).resolve().parents[3]
ESQUEMA_CRITERIOS = json.loads((RAIZ / "asserts" / "esquema.json").read_text(encoding="utf-8"))


class SalidaInvalida(Exception):
    """La respuesta del LLM no cumple el contrato JSON Schema: se descarta y se registra."""


class ProveedorGrabadoCriterios:
    """Adaptador de ProveedorLLM que lee respuestas grabadas para pruebas reproducibles."""

    def __init__(self, version: str = "v3", base_dir: pathlib.Path | None = None):
        self.version = version
        self._base = base_dir or (RAIZ / "grabaciones")

    def completar(self, prompt: str) -> str:
        matches = re.findall(r'<historia id="([^"]+)">', prompt) or re.findall(r"\((H\d+)\)", prompt)
        historia_id = matches[-1] if matches else "H1"
        archivo = self._base / self.version / f"{historia_id}.txt"
        return archivo.read_text(encoding="utf-8")


class GeneradorCriterios:
    def __init__(self, proveedor: ProveedorLLM, version: str = "v3"):
        self._proveedor = proveedor
        self.version = version
        self._plantilla = (RAIZ / "prompts" / "criterios" / f"{version}.txt").read_text(encoding="utf-8")

    def generar(self, id_historia: str, historia: str) -> dict:
        prompt = self._plantilla.replace("{{id}}", id_historia).replace("{{historia}}", historia)
        texto = self._proveedor.completar(prompt)
        try:
            criterios = json.loads(texto)
            validate(criterios, ESQUEMA_CRITERIOS)
        except (json.JSONDecodeError, ValidationError) as e:
            raise SalidaInvalida(f"{self.version}/{id_historia}: {e}") from e
        return criterios