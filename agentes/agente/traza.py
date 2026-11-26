import argparse
import json
from pathlib import Path


def _mermaid_text(value: object, max_len: int = 110) -> str:
    texto = str(value).replace("\n", " ").replace('"', "'").replace("|", "/")
    if len(texto) > max_len:
        texto = texto[:max_len].rsplit(" ", 1)[0] + "..."
    return texto


def _resumen_args(args: object) -> str:
    if not isinstance(args, dict):
        return ""
    valores = [
        f"{clave}={_mermaid_text(valor, 45)}"
        for clave, valor in args.items()
        if clave not in {"antes", "despues"}
    ]
    return ", ".join(valores)


def generar_diagrama(archivo_traza: Path) -> str:
    eventos = [
        json.loads(linea)
        for linea in archivo_traza.read_text(encoding="utf-8").splitlines()
        if linea.strip()
    ]
    lineas = [
        "sequenceDiagram",
        "    autonumber",
        "    participant A as Agente ReAct",
        "    participant M as ModeloInteractivo",
        "    participant H as Herramientas del repositorio",
    ]
    for evento in eventos:
        tipo = evento.get("tipo")
        if tipo == "estado":
            paso = evento.get("paso")
            sufijo = f", paso {paso}" if paso is not None else ""
            lineas.append(f"    Note over A: Estado {evento.get('estado')}{sufijo}")
        elif tipo == "objetivo":
            lineas.append(f"    A->>M: Objetivo: {_mermaid_text(evento.get('texto', ''))}")
        elif tipo == "accion":
            paso = evento.get("paso", "?")
            estado = evento.get("estado", "")
            accion = evento.get("accion", "")
            lineas.append(f"    A->>M: Decisión {paso}: {_mermaid_text(accion)}")
            if evento.get("bloqueada"):
                lineas.append(f"    M-->>A: {_mermaid_text(estado)}")
            else:
                args = _resumen_args(evento.get("args", {}))
                lineas.append(f"    A->>H: {accion}({args})")
                lineas.append(
                    f"    H-->>A: {_mermaid_text(evento.get('observacion', ''), 130)}"
                )
        elif tipo == "final":
            lineas.append(f"    A->>M: Final: {_mermaid_text(evento.get('texto', ''))}")
            lineas.append(f"    M-->>A: {evento.get('estado', 'FINALIZADO')}")
    return "\n".join(lineas) + "\n"


def main() -> None:
    raiz_agentes = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Genera un diagrama Mermaid desde una traza JSONL.")
    parser.add_argument(
        "traza",
        nargs="?",
        type=Path,
        default=raiz_agentes / "trazas/e2-issue-01.jsonl",
    )
    parser.add_argument("--salida", type=Path)
    args = parser.parse_args()
    archivo = args.traza.resolve()
    salida = args.salida or archivo.with_suffix(".mmd")
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(generar_diagrama(archivo), encoding="utf-8")
    print(f"Diagrama generado: {salida}")


if __name__ == "__main__":
    main()
