# proveedor_grabado.py
import pathlib

class GrabadoProvider:
    def __init__(self, provider_options=None):
        self.options = provider_options or {}

    def call_api(self, prompt, options=None):
        # Lee las variables de contexto pasadas por promptfoo para identificar el caso (H1, H2, etc.)
        context = options.get("vars", {}) if options else {}
        historia_id = context.get("id", "H1")
        
        # Simulamos la versión actual del prompt que se está evaluando
        # Buscamos qué archivo de grabación corresponde
        ruta_base = pathlib.Path("grabaciones/v1")
        archivo = ruta_base / f"{historia_id}.txt"
        
        if archivo.exists():
            output = archivo.read_text(encoding="utf-8")
        else:
            output = f"Respuesta por defecto para {historia_id} (simulada v1)"
            
        return {
            "output": output
        }