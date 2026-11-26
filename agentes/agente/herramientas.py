from pathlib import Path
import re
import shlex
import subprocess
import sys


class Herramientas:
    def __init__(self, raiz: str | Path):
        self.raiz = Path(raiz).resolve()

    def catalogo(self) -> dict[str, str]:
        return {
            "listar_archivos": "args: ruta (opcional)",
            "leer_archivo": "args: ruta",
            "buscar": "args: termino, ruta (opcional)",
            "ejecutar_pruebas": "args: ruta (opcional)",
            "editar_archivo": "args: ruta, antes, despues",
            "ver_cambios": "args: ruta (opcional)",
            "ejecutar_comando": "args: comando (sujeto a lista permitida)",
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
