from datetime import datetime
from src.prestamos.dominio import Multa


def test_issue_01_multa_no_cuenta_domingos():
    multa = Multa()
    # Viernes 13/11/2026 -> Lunes 16/11/2026 = 3 dias calendario, pero el domingo 15/11 no cuenta (2 dias habiles * S/ 2.0 = S/ 4.0)
    fecha_limite = datetime(2026, 11, 13, 18, 0)
    fecha_devolucion = datetime(2026, 11, 16, 10, 0)
    monto = multa.calcular_monto_atraso(fecha_limite, fecha_devolucion, tarifa_diaria=2.0)
    assert monto == 4.0