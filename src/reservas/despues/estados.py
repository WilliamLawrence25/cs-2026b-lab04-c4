# src/reservas/despues/estados.py

class EstadoReserva:
    """Clase base: por defecto, prohíbe todas las transiciones."""
    nombre = "?"
    
    def verificar_puede_procesar(self):
        raise ValueError(f"La reserva ya fue {self.nombre.lower()}")
        
    def confirmar(self, reserva):
        raise ValueError(f"La reserva ya fue {self.nombre.lower()}")
        
    def cancelar(self, reserva):
        raise ValueError(f"La reserva ya fue {self.nombre.lower()}")

class Pendiente(EstadoReserva):
    """Único estado que permite avanzar el flujo."""
    nombre = "PENDIENTE"
    
    def verificar_puede_procesar(self):
        pass # Todo en orden, se puede procesar
        
    def confirmar(self, reserva):
        reserva.cambiar_estado(Confirmada())
        
    def cancelar(self, reserva):
        reserva.cambiar_estado(Cancelada())

class Confirmada(EstadoReserva):
    nombre = "CONFIRMADA"
    # Hereda las prohibiciones de la clase base

class Cancelada(EstadoReserva):
    nombre = "CANCELADA"
    # Hereda las prohibiciones de la clase base