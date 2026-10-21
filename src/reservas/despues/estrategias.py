# src/reservas/despues/estrategias.py
from abc import ABC, abstractmethod
from src.reservas.externos import SistemaAcademicoSDK

# --- ADAPTER: Aísla y traduce el SDK de la UNSA ---
class ValidadorMatriculaAdapter:
    def __init__(self):
        self._sdk = SistemaAcademicoSDK()
    
    def es_matricula_activa(self, dni: str) -> bool:
        respuesta = self._sdk.consultar_matricula(dni)
        return respuesta.get("estado_matricula") == "1"

# --- STRATEGY: Interfaz común para el cálculo de multas ---
class CalculadorMulta(ABC):
    @abstractmethod
    def calcular(self) -> float:
        pass

class MultaPregrado(CalculadorMulta):
    def calcular(self) -> float:
        return 2.0

class MultaPosgrado(CalculadorMulta):
    def calcular(self) -> float:
        return 5.0

class MultaDocente(CalculadorMulta):
    def calcular(self) -> float:
        return 0.0

# --- FACTORY: Registro dinámico de estrategias ---
class FabricaMultas:
    def __init__(self):
        self._creadores = {}
    
    def registrar(self, tipo: str, creador):
        self._creadores[tipo] = creador
    
    def crear(self, tipo: str) -> CalculadorMulta:
        if tipo not in self._creadores:
            raise ValueError(f"Tipo de usuario no soportado: {tipo}")
        return self._creadores[tipo]()