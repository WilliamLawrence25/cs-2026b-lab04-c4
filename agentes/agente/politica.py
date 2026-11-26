from dataclasses import dataclass, field
import posixpath
import re


@dataclass(frozen=True)
class Veredicto:
    permitido: bool
    motivo: str = ""


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
        return Veredicto(True)
