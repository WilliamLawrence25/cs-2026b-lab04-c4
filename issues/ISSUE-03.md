# Issue #03: Un préstamo ya devuelto sigue figurando como vencido

**Reportado por:** Módulo de Consultas — BiblioUNSA
**Observado:** `Prestamo.esta_vencido(fecha_corte)` en `src/prestamos/dominio.py` solo compara `fecha_corte > self.fecha_limite`, marcando como vencidos préstamos que ya tienen `fecha_devolucion` registrada o estado `DEVUELTO`.
**Esperado:** Debe retornar `False` cuando `self.fecha_devolucion is not None` o `self.estado == EstadoPrestamo.DEVUELTO`.
**Prueba que reproduce el error:**
`tests/test_issue_03_prestamos.py::test_issue_03_prestamo_devuelto_no_esta_vencido`