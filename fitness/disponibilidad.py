# fitness/disponibilidad.py
import random

def simular_caida_api(tactica="ninguna", total_reservas=1000, probabilidad_falla=0.8):
    """
    Simula intentos de reserva durante una congestión/caída de la API de la UNSA.
    """
    random.seed(42)
    reservas_exitosas = 0
    reservas_perdidas = 0
    llamadas_a_api = 0
    en_cola_outbox = 0

    for _ in range(total_reservas):
        api_responde = random.random() > probabilidad_falla
        
        if tactica == "ninguna":
            llamadas_a_api += 1
            if api_responde:
                reservas_exitosas += 1
            else:
                reservas_perdidas += 1

        elif tactica == "reintentos":
            # Táctica: Reintentar hasta 3 veces
            exito = False
            for intento in range(3):
                llamadas_a_api += 1
                if api_responde:
                    exito = True
                    break
            
            if exito: reservas_exitosas += 1
            else: reservas_perdidas += 1

        elif tactica == "circuit_breaker_y_cola":
            # Táctica: Circuit Breaker + Outbox (Cola de pendientes)
            # Si detecta falla, corta rápido y lo guarda en base de datos local
            llamadas_a_api += 1 # Falla rápida o éxito
            if api_responde:
                reservas_exitosas += 1
            else:
                # No se pierde, se guarda para cuando la API regrese
                en_cola_outbox += 1

    # Procesamos la cola cuando la API regresa
    if tactica == "circuit_breaker_y_cola":
        reservas_exitosas += en_cola_outbox
        reservas_perdidas = 0 # NINGUNA reserva perdida
        en_cola_outbox = 0

    return {
        "tactica": tactica,
        "exitosas": reservas_exitosas,
        "perdidas": reservas_perdidas,
        "llamadas_fallidas_api": llamadas_a_api - reservas_exitosas
    }

if __name__ == "__main__":
    print(f"{'Táctica':<25} | {'Éxitos':<6} | {'Perdidas':<8} | {'Sobrecarga API (Llamadas fallidas)'}")
    print("-" * 75)
    for tactica in ["ninguna", "reintentos", "circuit_breaker_y_cola"]:
        res = simular_caida_api(tactica)
        print(f"{res['tactica']:<25} | {res['exitosas']:<6} | {res['perdidas']:<8} | {res['llamadas_fallidas_api']}")