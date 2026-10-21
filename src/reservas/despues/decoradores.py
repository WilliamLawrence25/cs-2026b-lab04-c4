# src/reservas/despues/decoradores.py

class ValidadorConCache:
    """DECORATOR: Evita llamar al SDK si el DNI ya fue consultado recientemente."""
    def __init__(self, validador_interno):
        self._interno = validador_interno
        self._cache = {}
        self.llamadas_reales = 0 # Contador para demostrar que funciona en las pruebas

    def es_matricula_activa(self, dni: str) -> bool:
        if dni not in self._cache:
            self.llamadas_reales += 1
            self._cache[dni] = self._interno.es_matricula_activa(dni)
        return self._cache[dni]