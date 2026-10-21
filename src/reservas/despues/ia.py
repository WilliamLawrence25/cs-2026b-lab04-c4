# src/reservas/despues/ia.py
from abc import ABC, abstractmethod

# --- STRATEGY: Interfaz común para cualquier IA (Local, OpenAI, Claude, Simulado) ---
class ProveedorLLM(ABC):
    @abstractmethod
    def generar(self, prompt: str) -> str:
        pass

# --- ADAPTER: Simulador para no gastar API keys ni internet en las pruebas ---
class SimuladorLLMAdapter(ProveedorLLM):
    def __init__(self, respuestas_predefinidas: dict):
        self.respuestas = respuestas_predefinidas
    
    def generar(self, prompt: str) -> str:
        return self.respuestas.get(prompt, "Respuesta por defecto")

# --- DECORATOR: Caché para ahorrar tokens si piden recomendaciones del mismo libro ---
class LLMConCache(ProveedorLLM):
    def __init__(self, interno: ProveedorLLM):
        self._interno = interno
        self._cache = {}
        self.llamadas_reales = 0
    
    def generar(self, prompt: str) -> str:
        if prompt not in self._cache:
            self.llamadas_reales += 1
            self._cache[prompt] = self._interno.generar(prompt)
        return self._cache[prompt]

# --- CHAIN OF RESPONSIBILITY: Eslabones de validación (Guardrails) ---
class Guardrail(ABC):
    def __init__(self, siguiente=None):
        self._siguiente = siguiente

    def validar(self, texto: str) -> str:
        texto = self._aplicar(texto)
        if self._siguiente:
            return self._siguiente.validar(texto)
        return texto

    @abstractmethod
    def _aplicar(self, texto: str) -> str:
        pass

class SinRecomendacionesExternas(Guardrail):
    """Evita que la IA mande al alumno a comprar libros fuera de la universidad"""
    def _aplicar(self, texto: str) -> str:
        if "amazon" in texto.lower() or "comprar" in texto.lower():
            raise ValueError("Guardrail: La IA sugirió comprar libros en fuentes externas")
        return texto

class FormatoLista(Guardrail):
    """Obliga a que la IA devuelva una lista con guiones"""
    def _aplicar(self, texto: str) -> str:
        if "-" not in texto:
            raise ValueError("Guardrail: La IA no respetó el formato de lista")
        return texto

# --- CLIENTE: El generador que usa la estrategia, el caché y la cadena ---
class GeneradorRecomendaciones:
    def __init__(self, proveedor: ProveedorLLM, guardrail_chain: Guardrail = None):
        self.proveedor = proveedor
        self.guardrail = guardrail_chain

    def recomendar(self, libro_base: str) -> str:
        prompt = f"Recomienda 2 libros similares a '{libro_base}' de nuestro catálogo."
        respuesta = self.proveedor.generar(prompt)
        
        if self.guardrail:
            respuesta = self.guardrail.validar(respuesta)
            
        return respuesta