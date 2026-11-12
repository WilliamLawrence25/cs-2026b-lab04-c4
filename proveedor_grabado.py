import pathlib


def call_api(prompt, options, context):
    vars_dict = (context or {}).get("vars") or (options or {}).get("vars") or {}
    caso_id = vars_dict.get("id", "H1")

    es_sql = (
        "ESQUEMA_BD" in prompt
        or "<pregunta" in prompt
        or "especialista en bases de datos PostgreSQL" in prompt
        or "Convierte esta pregunta del bibliotecario" in prompt
    )

    if es_sql:
        if "ESQUEMA_BD" in prompt or "<pregunta" in prompt:
            version = "v3"
        elif "especialista en bases de datos PostgreSQL" in prompt:
            version = "v2"
        else:
            version = "v1"
        base = pathlib.Path(f"prompts/sql/grabaciones/{version}")
    else:
        if "# ROL" in prompt or "<historia" in prompt:
            version = "v3"
        elif "Eres un analista de calidad (QA)" in prompt:
            version = "v2"
        else:
            version = "v1"
        base = pathlib.Path(f"grabaciones/{version}")

    archivo = base / f"{caso_id}.txt"
    if archivo.exists():
        return {"output": archivo.read_text(encoding="utf-8")}

    return {"output": f'{{"error": "Falta grabacion {archivo}"}}'}