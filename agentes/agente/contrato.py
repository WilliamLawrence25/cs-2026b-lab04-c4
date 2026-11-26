import json


def validar_decision(decision, herramientas_conocidas: set[str]) -> tuple[bool, str]:
    if isinstance(decision, str):
        try:
            decision = json.loads(decision)
        except json.JSONDecodeError:
            return False, "la decisión no es JSON válido"

    if not isinstance(decision, dict):
        return False, "la decisión debe ser un objeto JSON"
    if not isinstance(decision.get("pensamiento"), str) or not decision["pensamiento"].strip():
        return False, "falta 'pensamiento' (texto no vacío)"
    if ("final" in decision) == ("accion" in decision):
        return False, "debe incluir 'accion' o 'final', pero no ambos"

    if "final" in decision:
        extra = set(decision) - {"pensamiento", "final"}
        if extra:
            return False, f"campos no permitidos: {sorted(extra)}"
        if not isinstance(decision["final"], str):
            return False, "'final' debe ser texto"
        return True, ""

    if not isinstance(decision["accion"], str):
        return False, "'accion' debe ser texto"
    if decision["accion"] not in herramientas_conocidas:
        return False, f"herramienta desconocida: {decision['accion']!r}"
    if not isinstance(decision.get("args", {}), dict):
        return False, "'args' debe ser un objeto JSON"

    extra = set(decision) - {"pensamiento", "accion", "args"}
    if extra:
        return False, f"campos no permitidos: {sorted(extra)}"
    return True, ""
