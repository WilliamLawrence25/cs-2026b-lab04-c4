# Issue #02: ServicioPrestamos permite reservar un libro con matrícula vencida

**Reportado por:** Coordinación Académica — BiblioUNSA
**Observado:** `ServicioPrestamos.crear_reserva()` en `src/prestamos/dominio.py` crea y confirma la reserva sin consultar `self.validador.esta_matriculado(estudiante.cui)`.
**Esperado:** Si `self.validador` está configurado y `esta_matriculado(estudiante.cui)` retorna `False`, debe lanzar `ValueError("Matrícula vencida: no puede realizar reservas")` sin descontar copias del libro.
**Prueba que reproduce el error:**
`tests/test_issue_02_reservas.py::test_issue_02_rechaza_reserva_con_matricula_vencida`