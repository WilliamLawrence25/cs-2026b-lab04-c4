import ast
from datetime import datetime
from pathlib import Path
import re
import shlex
import subprocess
import sys


class Herramientas:
    def __init__(self, raiz: str | Path, archivo_notas: str | Path | None = None):
        self.raiz = Path(raiz).resolve()
        self.archivo_notas = Path(archivo_notas) if archivo_notas else self.raiz / "agentes/notas.md"

    def catalogo(self) -> dict[str, str]:
        return {
            "listar_archivos": "args: ruta (opcional)",
            "leer_archivo": "args: ruta",
            "buscar": "args: termino, ruta (opcional)",
            "mapa_repo": "args: ruta (opcional); lista archivos Python, clases y firmas AST",
            "ejecutar_pruebas": "args: ruta (opcional)",
            "editar_archivo": "args: ruta, antes, despues",
            "ver_cambios": "args: ruta (opcional)",
            "ejecutar_comando": "args: comando (sujeto a lista permitida)",
            "anotar": "args: texto; agrega hipótesis o archivos revisados a agentes/notas.md",
            "leer_notas": "sin args; devuelve la memoria persistente de la tarea",
        }

    def _ruta(self, ruta: str) -> Path:
        destino = (self.raiz / ruta).resolve()
        if destino != self.raiz and self.raiz not in destino.parents:
            raise PermissionError(f"Ruta fuera del sandbox: {ruta}")
        return destino

    def listar_archivos(self, ruta: str = ".") -> str:
        base = self._ruta(ruta)
        excluidos = {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules"}
        archivos = [
            str(path.relative_to(self.raiz))
            for path in base.rglob("*")
            if path.is_file() and not excluidos.intersection(path.parts)
        ]
        return "\n".join(archivos[:100]) or "(sin archivos)"

    def leer_archivo(self, ruta: str) -> str:
        contenido = self._ruta(ruta).read_text(encoding="utf-8")
        return contenido[:6000] + ("\n[contenido truncado]" if len(contenido) > 6000 else "")

    def buscar(self, termino: str, ruta: str = "src") -> str:
        base = self._ruta(ruta)
        archivos = [base] if base.is_file() else base.rglob("*.py")
        resultados = []
        excluidos = {".git", ".venv", "__pycache__", ".pytest_cache"}
        for archivo in archivos:
            if excluidos.intersection(archivo.parts):
                continue
            try:
                for numero, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), 1):
                    if re.search(termino, linea, re.IGNORECASE):
                        resultados.append(
                            f"{archivo.relative_to(self.raiz)}:{numero}:{linea.strip()}"
                        )
            except (UnicodeDecodeError, OSError):
                continue
            if len(resultados) >= 50:
                break
        return "\n".join(resultados) or "(sin coincidencias)"

    @staticmethod
    def _firma(funcion: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
        prefijo = "async def" if isinstance(funcion, ast.AsyncFunctionDef) else "def"
        firma = f"{prefijo} {funcion.name}({ast.unparse(funcion.args)})"
        if funcion.returns is not None:
            firma += f" -> {ast.unparse(funcion.returns)}"
        return firma

    def mapa_repo(self, ruta: str = "src") -> str:
        base = self._ruta(ruta)
        excluidos = {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules"}
        archivos = [base] if base.is_file() else sorted(base.rglob("*.py"))
        lineas = []

        for archivo in archivos:
            if not archivo.is_file() or excluidos.intersection(archivo.parts):
                continue
            arbol = ast.parse(archivo.read_text(encoding="utf-8"), filename=str(archivo))
            lineas.append(f"{archivo.relative_to(self.raiz)}")
            for nodo in ast.iter_child_nodes(arbol):
                if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    lineas.append(f"  {self._firma(nodo)}")
                elif isinstance(nodo, ast.ClassDef):
                    bases = ", ".join(ast.unparse(base) for base in nodo.bases)
                    sufijo = f"({bases})" if bases else ""
                    lineas.append(f"  class {nodo.name}{sufijo}")
                    for miembro in nodo.body:
                        if isinstance(miembro, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            lineas.append(f"    {self._firma(miembro)}")

            if sum(len(linea) + 1 for linea in lineas) >= 8000:
                lineas.append("[mapa truncado]")
                break

        return "\n".join(lineas) or "(sin módulos Python)"

    def anotar(self, texto: str) -> str:
        if not isinstance(texto, str) or not texto.strip():
            raise ValueError("La nota debe contener texto no vacío")

        archivo = self._ruta(str(self.archivo_notas))
        archivo.parent.mkdir(parents=True, exist_ok=True)
        marca_tiempo = datetime.now().astimezone().isoformat(timespec="seconds")
        with archivo.open("a", encoding="utf-8") as notas:
            notas.write(f"- {marca_tiempo}: {texto.strip()}\n")
        return f"Nota guardada en {archivo.relative_to(self.raiz)}"

    def leer_notas(self) -> str:
        archivo = self._ruta(str(self.archivo_notas))
        if not archivo.exists():
            return "(sin notas registradas)"
        return archivo.read_text(encoding="utf-8")

    def ejecutar_pruebas(self, ruta: str = "tests/test_issue_01_multas.py") -> str:
        destino = self._ruta(ruta)
        if not destino.is_file() or not str(destino.relative_to(self.raiz)).startswith("tests/"):
            raise ValueError("Solo se pueden ejecutar pruebas dentro de tests/")
        resultado = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", str(destino)],
            cwd=self.raiz,
            capture_output=True,
            text=True,
            timeout=90,
            check=False,
        )
        salida = (resultado.stdout + resultado.stderr).strip()
        return f"exit_code={resultado.returncode}\n{salida}"[:4000]

    def editar_archivo(self, ruta: str, antes: str, despues: str) -> str:
        destino = self._ruta(ruta)
        contenido = destino.read_text(encoding="utf-8")
        coincidencias = contenido.count(antes)
        if not antes or coincidencias != 1:
            return f"ERROR: el fragmento aparece {coincidencias} veces; debe aparecer exactamente 1"
        destino.write_text(contenido.replace(antes, despues, 1), encoding="utf-8")
        return f"OK: {ruta} modificado"

    def ver_cambios(self, ruta: str = "src/prestamos/dominio.py") -> str:
        self._ruta(ruta)
        resultado = subprocess.run(
            ["git", "diff", "--", ruta],
            cwd=self.raiz,
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        return (resultado.stdout or resultado.stderr or "(sin cambios)")[:4000]

    def ejecutar_comando(self, comando: str) -> str:
        argumentos = shlex.split(comando)
        if argumentos[:3] == ["python", "-m", "pytest"]:
            argumentos = [sys.executable, "-m", "pytest", *argumentos[3:]]
        resultado = subprocess.run(
            argumentos,
            cwd=self.raiz,
            capture_output=True,
            text=True,
            timeout=90,
            check=False,
        )
        return f"exit_code={resultado.returncode}\n{resultado.stdout}{resultado.stderr}"[:4000]
