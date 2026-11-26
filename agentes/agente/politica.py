from dataclasses import dataclass, field
import posixpath
import re
from collections.abc import Callable


@dataclass(frozen=True)
class Veredicto:
    permitido: bool
    motivo: str = ""
    aprobacion_humana: bool | None = None


@dataclass
class Politica:
    herramientas_permitidas: set[str] = field(
        default_factory=lambda: {
            "listar_archivos",
            "leer_archivo",
            "buscar",
            "ejecutar_pruebas",
            "editar_archivo",
            "ver_cambios",
            "ejecutar_comando",
            "mapa_repo",
            "anotar",
            "leer_notas",
        }
    )
    max_pasos: int = 12
    rutas_protegidas: tuple[str, ...] = ("tests/",)
    aprobar_edicion: Callable[[str, str, str], bool] | None = None
    comandos_permitidos: tuple[str, ...] = (
        r"^python -m pytest(?:\s+.*)?$",
        r"^radon cc(?:\s+.*)?$",
        r"^lint-imports$",
        r"^git (?:status|diff)(?:\s+.*)?$",
    )

    def evaluar(self, accion: str, args: dict, paso: int) -> Veredicto:
        if paso > self.max_pasos:
            return Veredicto(False, f"Se alcanzó el máximo de {self.max_pasos} pasos")
        if accion not in self.herramientas_permitidas:
            return Veredicto(False, f"Herramienta no permitida: {accion}")
        if accion == "ejecutar_comando":
            comando = args.get("comando", "")
            if not isinstance(comando, str) or not any(
                re.fullmatch(patron, comando) for patron in self.comandos_permitidos
            ):
                return Veredicto(False, f"Comando fuera de la lista permitida: {comando!r}")
        if accion == "editar_archivo":
            ruta = args.get("ruta", "")
            ruta_normalizada = posixpath.normpath(ruta.replace("\\", "/")).removeprefix("./")
            if any(ruta_normalizada.startswith(r) for r in self.rutas_protegidas):
                return Veredicto(False, f"Ruta protegida: {ruta}")
            if self.aprobar_edicion is not None:
                aprobado = self.aprobar_edicion(
                    str(ruta),
                    str(args.get("antes", "")),
                    str(args.get("despues", "")),
                )
                if not aprobado:
                    return Veredicto(
                        False,
                        "Edición rechazada por aprobación humana",
                        aprobacion_humana=False,
                    )
                return Veredicto(
                    True,
                    "Edición aprobada por un integrante",
                    aprobacion_humana=True,
                )
        return Veredicto(True)


def aprobar_edicion_en_consola(ruta: str, antes: str, despues: str) -> bool:
    print(f"\nEl agente solicita editar: {ruta}")
    print("--- Contenido que reemplazará ---")
    print(antes)
    print("--- Contenido propuesto ---")
    print(despues)
    while True:
        respuesta = input("¿Apruebas esta edición? [s/n]: ").strip().lower()
        if respuesta in {"s", "n"}:
            return respuesta == "s"
        print("Respuesta no válida. Escribe 's' para aprobar o 'n' para rechazar.")
