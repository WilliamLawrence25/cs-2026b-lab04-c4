# Issue #01: El cálculo de multa por atraso cuenta los domingos

**Reportado por:** Oficina de Circulación — BiblioUNSA
**Observado:** `Multa.calcular_monto_atraso()` en `src/prestamos/dominio.py` cobra S/ 2.00 por cada día calendario entre `fecha_limite` y `fecha_devolucion`, incluyendo los domingos en que la biblioteca no atiende.
**Esperado:** Debe excluir los domingos (`fecha.weekday() == 6`) al contar los días de retraso.
**Prueba que reproduce el error:**
`tests/test_issue_01_multas.py::test_issue_01_multa_no_cuenta_domingos`