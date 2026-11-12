import json
import pathlib
import re
from jsonschema import ValidationError, validate
from src.reservas.despues.ia import ProveedorLLM
from src.reservas.despues.generador_criterios import SalidaInvalida

RAIZ = pathlib.Path(__file__).resolve().parents[3]
ESQUEMA_SQL = json.loads((RAIZ / "prompts" / "sql" / "esquema.json").read_text(encoding="utf-8"))
PATRON_PROHIBIDO = re.compile(r"\b(insert|update|delete|drop|alter|truncate|grant|revoke|exec|create)\b", re.I)


class ProveedorGrabadoSQL:
    """Adaptador de ProveedorLLM para las grabaciones de Text-to-SQL."""

    def __init__(self, version: str = "v3", base_dir: pathlib.Path | None = None):
        self.version = version
        self._base = base_dir or (RAIZ / "prompts" / "sql" / "grabaciones")

    def completar(self, prompt: str) -> str:
        matches = re.findall(r'<pregunta id="([^"]+)">', prompt) or re.findall(r"\((S\d+)\)", prompt)
        pregunta_id = matches[-1] if matches else "S1"
        archivo = self._base / self.version / f"{pregunta_id}.txt"
        return archivo.read_text(encoding="utf-8")


class GeneradorSQL:
    def __init__(self, proveedor: ProveedorLLM, version: str = "v3"):
        self._proveedor = proveedor
        self.version = version
        self._plantilla = (RAIZ / "prompts" / "sql" / f"{version}.txt").read_text(encoding="utf-8")

    def traducir(self, id_pregunta: str, pregunta: str) -> dict:
        prompt = self._plantilla.replace("{{id}}", id_pregunta).replace("{{pregunta}}", pregunta)
        texto = self._proveedor.completar(prompt)
        try:
            resultado = json.loads(texto)
            validate(resultado, ESQUEMA_SQL)
        except (json.JSONDecodeError, ValidationError) as e:
            raise SalidaInvalida(f"{self.version}/{id_pregunta}: {e}") from e

        sql = resultado["sql"].strip()
        if resultado["permitida"]:
            if not re.match(r"^select\b", sql, re.I) or PATRON_PROHIBIDO.search(sql) or ";" in sql:
                raise SalidaInvalida(f"{self.version}/{id_pregunta}: SQL fuera de política de solo lectura")

        return resultado