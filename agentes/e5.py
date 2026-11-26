import argparse
import json
from pathlib import Path
from typing import Any

from agentes.agente.herramientas import Herramientas
from agentes.agente.modelo_grabado import ModeloGrabado
from agentes.agente.nucleo import Agente
from agentes.agente.politica import Politica, aprobar_edicion_en_consola


ROOT = Path(__file__).resolve().parents[1]
AGENTES = ROOT / "agentes"
TRAYECTORIAS = AGENTES / "trayectorias"
TRAZAS = AGENTES / "trazas"
ISSUE = "issues/ISSUE-02.md"
DOMINIO = ROOT / "src/prestamos/dominio.py"
RESERVA_BASE = (
    "        # BUG ISSUE-02: omite validar si la matricula del estudiante esta vigente\n"
    "        prestamo = Prestamo(estudiante=estudiante, libro=libro)\n"
)
RESERVA_INGENUA = (
    "        if not self.validador.esta_matriculado(estudiante.cui):\n"
    '            raise ValueError("Matrícula vencida: no puede realizar reservas")\n'
    "        prestamo = Prestamo(estudiante=estudiante, libro=libro)\n"
)
RESERVA_CORREGIDA = (
    "        if self.validador is not None and not self.validador.esta_matriculado(estudiante.cui):\n"
    '            raise ValueError("Matrícula vencida: no puede realizar reservas")\n'
    "        prestamo = Prestamo(estudiante=estudiante, libro=libro)\n"
)


def _objetivo(prefijo: str) -> str:
    issue = ROOT / ISSUE
    return (
        f"{prefijo}\nIssue:\n{issue.read_text(encoding='utf-8')}\n"
        f"Herramientas: {Herramientas(ROOT).catalogo()}"
    )


def _estado_inicial(contenido: str) -> str:
    if RESERVA_BASE in contenido:
        return contenido
    comentario = RESERVA_BASE.split("        prestamo =", 1)[0]
    for cambio in (RESERVA_INGENUA, RESERVA_CORREGIDA):
        if comentario + cambio in contenido:
            return contenido.replace(comentario + cambio, RESERVA_BASE, 1)
        if cambio in contenido:
            return contenido.replace(cambio, RESERVA_BASE, 1)
    raise RuntimeError(
        "No se reconoce el estado de ServicioPrestamos para reproducir E5; "
        "se conserva el archivo sin modificar."
    )


def _ejecutar(
    rol: str,
    trayectoria: str,
    traza: str,
    objetivo: str,
    politica: Politica | None = None,
) -> tuple[str, Agente]:
    agente = Agente(
        modelo=ModeloGrabado.desde_archivo(TRAYECTORIAS / trayectoria),
        herramientas=Herramientas(ROOT),
        politica=politica or Politica(),
        objetivo=objetivo,
        traza_archivo=TRAZAS / traza,
        trayectoria_archivo=TRAYECTORIAS / trayectoria.replace(".json", "-resultado.json"),
    )
    resultado = agente.ejecutar()
    print(f"{rol}: {resultado}")
    return resultado, agente


def _validar_evidencia(
    agente: Agente,
    codigos_pruebas: list[int],
    ediciones_exitosas: int = 0,
) -> None:
    acciones = [evento for evento in agente.eventos if evento.get("tipo") == "accion"]
    codigos_observados = []
    ediciones = []
    for evento in acciones:
        if evento.get("accion") in {"ejecutar_pruebas", "ejecutar_comando"}:
            salida = str(evento.get("observacion", ""))
            codigo = next(
                (linea.partition("=")[2] for linea in salida.splitlines() if linea.startswith("exit_code=")),
                None,
            )
            if codigo is None:
                raise RuntimeError(f"No se encontró exit_code en la evidencia: {salida}")
            codigos_observados.append(int(codigo))
        if evento.get("accion") == "editar_archivo":
            ediciones.append(str(evento.get("observacion", "")))

    if codigos_observados != codigos_pruebas:
        raise RuntimeError(
            f"Códigos de pruebas inesperados: {codigos_observados}; "
            f"se esperaban {codigos_pruebas}"
        )
    if len(ediciones) != ediciones_exitosas or any(
        not resultado.startswith("OK:") for resultado in ediciones
    ):
        raise RuntimeError(f"Resultado de edición inesperado: {ediciones}")


def _metricas(rondas: int, agentes: list[Agente], revisor_encontro: bool) -> dict[str, Any]:
    acciones = [
        evento
        for agente in agentes
        for evento in agente.eventos
        if evento.get("tipo") == "accion"
    ]
    def rol(agente: Agente) -> str:
        return agente.trayectoria_archivo.stem.removeprefix("e5-").removesuffix("-resultado")

    acciones_por_rol = {
        rol(agente): sum(evento.get("tipo") == "accion" for evento in agente.eventos)
        for agente in agentes
    }
    bloqueos_por_rol = {
        rol(agente): sum(
            evento.get("tipo") == "accion" and evento.get("estado") == "BLOQUEADO"
            for evento in agente.eventos
        )
        for agente in agentes
    }
    return {
        "rondas": rondas,
        "acciones": len(acciones),
        "acciones_por_rol": acciones_por_rol,
        "acciones_bloqueadas": sum(evento.get("estado") == "BLOQUEADO" for evento in acciones),
        "acciones_bloqueadas_por_rol": bloqueos_por_rol,
        "decisiones_rechazadas_contrato": sum(
            decision["contrato"] == "rechaza"
            for agente in agentes
            for decision in agente.decisiones
        ),
        "contexto_final_caracteres": sum(
            sum(len(mensaje["content"]) for mensaje in agente.historial)
            for agente in agentes
        ),
        "contexto_por_rol": {
            f"{agente.trayectoria_archivo.stem}": sum(
                len(mensaje["content"]) for mensaje in agente.historial
            )
            for agente in agentes
        },
        "revisor_encontro_algo_omitido_por_agente_unico": revisor_encontro,
    }


def ejecutar_agente_unico() -> dict[str, Any]:
    contenido_original = DOMINIO.read_text(encoding="utf-8")
    try:
        resultado, agente = _ejecutar(
            "Agente único",
            "e5-agente-unico.json",
            "e5-agente-unico.jsonl",
            _objetivo(
                "Resuelve ISSUE-02. Reproduce el fallo, valida matrícula antes de reservar "
                "y comprueba la prueba específica."
            ),
        )
        _validar_evidencia(agente, [1, 0], ediciones_exitosas=1)
        metricas = _metricas(1, [agente], False)
        metricas["resultado"] = resultado
        archivo = AGENTES / "resultados/e5-agente-unico.json"
        archivo.parent.mkdir(parents=True, exist_ok=True)
        archivo.write_text(
            json.dumps(metricas, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return metricas
    finally:
        if DOMINIO.read_text(encoding="utf-8") != contenido_original:
            DOMINIO.write_text(contenido_original, encoding="utf-8")


def ejecutar_actor_critico(aprobar_ediciones: bool = False) -> dict[str, Any]:
    prefijo_traza = "e6" if aprobar_ediciones else "e5"
    objetivo_plan = _objetivo("Prepara un plan breve y seguro para resolver ISSUE-02.")
    _, planificador = _ejecutar(
        "Planificador",
        "e5-planificador.json",
        f"{prefijo_traza}-planificador.jsonl",
        objetivo_plan,
        Politica(
            herramientas_permitidas={"leer_archivo", "mapa_repo"},
            max_pasos=4,
        ),
    )
    plan = planificador.decisiones[-1]["decision"].get("final", "")
    ejecutados = [planificador]
    resultado_revisor = ""
    revisor_encontro = False

    for ronda in range(1, 3):
        retroalimentacion = ""
        if ronda > 1:
            retroalimentacion = (
                f"\nRetroalimentación del revisor: {resultado_revisor}\n"
                "Aplica únicamente la corrección solicitada y vuelve a verificar."
            )
        objetivo_ejecutor = _objetivo(
            f"Ejecuta este plan para ISSUE-02:\n{plan}{retroalimentacion}"
        )
        _, ejecutor = _ejecutar(
            f"Ejecutor ronda {ronda}",
            f"e5-ejecutor-r{ronda}.json",
            f"{prefijo_traza}-ejecutor-r{ronda}.jsonl",
            objetivo_ejecutor,
            Politica(
                max_pasos=8,
                aprobar_edicion=aprobar_edicion_en_consola if aprobar_ediciones else None,
            ),
        )
        _validar_evidencia(ejecutor, [0], ediciones_exitosas=1)
        ejecutados.append(ejecutor)

        objetivo_revision = _objetivo(
            f"Revisa el cambio de ISSUE-02 en modo solo lectura. "
            f"Verifica la corrección y compatibilidad.\nResumen del ejecutor:\n"
            f"{ejecutor.decisiones[-1]['decision'].get('final', '')}"
        )
        resultado_revisor, revisor = _ejecutar(
            f"Revisor ronda {ronda}",
            f"e5-revisor-r{ronda}.json",
            f"{prefijo_traza}-revisor-r{ronda}.jsonl",
            objetivo_revision,
            Politica(
                herramientas_permitidas={
                    "leer_archivo",
                    "buscar",
                    "ejecutar_pruebas",
                    "ver_cambios",
                    "ejecutar_comando",
                },
                max_pasos=8,
            ),
        )
        _validar_evidencia(revisor, [1] if ronda == 1 else [0])
        ejecutados.append(revisor)
        if resultado_revisor.startswith("APROBADO"):
            break
        if not resultado_revisor.startswith("CAMBIOS SOLICITADOS"):
            raise RuntimeError(f"Respuesta de revisor no reconocida: {resultado_revisor}")
        revisor_encontro = True
    else:
        raise RuntimeError("El revisor no aprobó el cambio en el máximo de dos rondas")

    metricas = _metricas(
        ronda,
        ejecutados,
        revisor_encontro=revisor_encontro,
    )
    metricas["plan"] = plan
    metricas["resultado_revisor"] = resultado_revisor
    archivo = AGENTES / "resultados/e5-actor-critico.json"
    archivo.parent.mkdir(parents=True, exist_ok=True)
    archivo.write_text(json.dumps(metricas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return metricas


def main() -> None:
    parser = argparse.ArgumentParser(description="Reproduce las dos variantes de coordinación E5.")
    parser.add_argument("--variante", choices=("unico", "actor-critico", "ambas"), default="ambas")
    parser.add_argument(
        "--aprobar-ediciones",
        action="store_true",
        help="solicita aprobación por consola antes de cada edición del ejecutor",
    )
    args = parser.parse_args()
    if args.aprobar_ediciones and args.variante == "unico":
        parser.error("--aprobar-ediciones requiere --variante actor-critico o ambas")

    contenido_original = DOMINIO.read_text(encoding="utf-8")
    contenido_base = _estado_inicial(contenido_original)
    try:
        if args.variante in ("unico", "ambas"):
            DOMINIO.write_text(contenido_base, encoding="utf-8")
            print("=== Agente único ===")
            print(json.dumps(ejecutar_agente_unico(), ensure_ascii=False, indent=2))
        if args.variante in ("actor-critico", "ambas"):
            DOMINIO.write_text(contenido_base, encoding="utf-8")
            print("=== Actor-crítico ===")
            print(
                json.dumps(
                    ejecutar_actor_critico(aprobar_ediciones=args.aprobar_ediciones),
                    ensure_ascii=False,
                    indent=2,
                )
            )
        if args.variante == "ambas":
            comparacion = {
                "agente_unico": json.loads(
                    (AGENTES / "resultados/e5-agente-unico.json").read_text(encoding="utf-8")
                ),
                "actor_critico": json.loads(
                    (AGENTES / "resultados/e5-actor-critico.json").read_text(encoding="utf-8")
                ),
            }
            destino = AGENTES / "resultados/e5-comparacion.json"
            destino.write_text(
                json.dumps(comparacion, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print(f"Comparación guardada en {destino.relative_to(ROOT)}")
    except Exception:
        DOMINIO.write_text(contenido_original, encoding="utf-8")
        raise
    finally:
        if args.variante == "unico":
            DOMINIO.write_text(contenido_original, encoding="utf-8")


if __name__ == "__main__":
    main()
