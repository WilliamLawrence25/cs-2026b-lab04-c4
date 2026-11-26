import argparse
from pathlib import Path

from .herramientas import Herramientas
from .modelo import ModeloInteractivo
from .nucleo import Agente
from .politica import Politica


def main() -> None:
    parser = argparse.ArgumentParser(description="Ejecuta un agente ReAct en modo interactivo.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--issue", default="issues/ISSUE-01.md")
    parser.add_argument("--trace", default="agentes/trazas/e2-issue-01.jsonl")
    parser.add_argument("--trajectory", default="agentes/trayectorias/e2-issue-01.json")
    args = parser.parse_args()

    raiz = args.root.resolve()
    issue = (raiz / args.issue).resolve()
    if raiz not in issue.parents:
        parser.error("--issue debe estar dentro de la raíz del repositorio")
    objetivo = (
        f"Resuelve el issue descrito en {args.issue}. "
        "Inspecciona el código, reproduce primero la falla, realiza un cambio mínimo "
        "fuera de tests/, y ejecuta la prueba del issue para verificar la solución. "
        f"Herramientas disponibles: {Herramientas(raiz).catalogo()}\n\n"
        f"Issue:\n{issue.read_text(encoding='utf-8')}"
    )

    agente = Agente(
        modelo=ModeloInteractivo(),
        herramientas=Herramientas(raiz),
        politica=Politica(),
        objetivo=objetivo,
        traza_archivo=raiz / args.trace,
        trayectoria_archivo=raiz / args.trajectory,
    )
    print(agente.ejecutar())
    print(f"Traza: {args.trace}")
    print(f"Trayectoria: {args.trajectory}")


if __name__ == "__main__":
    main()
