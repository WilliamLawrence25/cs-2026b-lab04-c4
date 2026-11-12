# proveedor_grabado.py
import pathlib


def call_api(prompt, options, context):
    vars_dict = (context or {}).get("vars") or (options or {}).get("vars") or {}
    historia_id = vars_dict.get("id", "H1")

    if "# ROL" in prompt or "<historia" in prompt:
        version = "v3"
    elif "Eres un analista de calidad (QA)" in prompt:
        version = "v2"
    else:
        version = "v1"

    ruta_base = pathlib.Path(f"grabaciones/{version}")
    if not ruta_base.exists():
        ruta_base = pathlib.Path("grabaciones/v1")

    archivo = ruta_base / f"{historia_id}.txt"

    if archivo.exists():
        output = archivo.read_text(encoding="utf-8")
    else:
        output = f'{{"historia_id": "{historia_id}", "invest_ok": true, "preguntas": [], "escenarios": []}}'

    return {"output": output}