from datetime import datetime
import json
from pathlib import Path
import time

from .contrato import validar_decision


class Agente:
    def __init__(
        self,
        modelo,
        herramientas,
        politica,
        objetivo: str,
        traza_archivo: str | Path,
        trayectoria_archivo: str | Path,
    ):
        self.modelo = modelo
        self.herramientas = herramientas
        self.politica = politica
        self.historial = [{"role": "user", "content": objetivo}]
        self.traza_archivo = Path(traza_archivo)
        self.trayectoria_archivo = Path(trayectoria_archivo)
        self.eventos = []
        self.decisiones = []

    def _registrar(self, **evento) -> None:
        self.eventos.append(
            {
                "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
                **evento,
            }
        )

    def _transicionar(self, estado: str, paso: int | None = None) -> None:
        evento = {"tipo": "estado", "estado": estado}
        if paso is not None:
            evento["paso"] = paso
        self._registrar(**evento)

    def _guardar_evidencia(self) -> None:
        self.traza_archivo.parent.mkdir(parents=True, exist_ok=True)
        self.trayectoria_archivo.parent.mkdir(parents=True, exist_ok=True)
        self.traza_archivo.write_text(
            "".join(json.dumps(evento, ensure_ascii=False) + "\n" for evento in self.eventos),
            encoding="utf-8",
        )
        self.trayectoria_archivo.write_text(
            json.dumps(
                {
                    "modelo": "ModeloInteractivo",
                    "decisiones": self.decisiones,
                    "contexto_final_caracteres": sum(
                        len(mensaje["content"]) for mensaje in self.historial
                    ),
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    def ejecutar(self) -> str:
        inicio = time.perf_counter()
        objetivo = self.historial[0]["content"]
        conocidas = set(self.herramientas.catalogo())
        self._transicionar("INICIO")
        self._registrar(tipo="objetivo", estado="INICIO", texto=objetivo)
        resultado_final = "(sin respuesta final)"

        for paso in range(1, self.politica.max_pasos + 1):
            self._transicionar("DECIDIENDO", paso)
            decision = self.modelo.decidir(self.historial)
            respuesta = getattr(self.modelo, "ultima_respuesta", "")
            self._transicionar("VALIDANDO_CONTRATO", paso)
            valida, motivo = validar_decision(decision, conocidas)
            self.decisiones.append(
                {
                    "paso": paso,
                    "respuesta": respuesta,
                    "decision": decision,
                    "contrato": "valida" if valida else "rechaza",
                    "motivo": motivo,
                }
            )
            self.historial.append(
                {
                    "role": "assistant",
                    "content": respuesta or json.dumps(decision, ensure_ascii=False),
                }
            )

            if not valida:
                self._transicionar("CONTRATO_INVALIDO", paso)
                observacion = (
                    f"ERROR DE CONTRATO: {motivo}. "
                    "Responde solo con el JSON del protocolo."
                )
                self._registrar(
                    tipo="accion",
                    estado="CONTRATO_INVALIDO",
                    paso=paso,
                    pensamiento=str(decision)[:200],
                    accion="(ninguna)",
                    args={},
                    observacion=observacion,
                    bloqueada=True,
                )
                self._transicionar("OBSERVANDO", paso)
            elif "final" in decision:
                resultado_final = decision["final"]
                self._transicionar("FINALIZADO", paso)
                self._registrar(
                    tipo="final",
                    estado="FINALIZADO",
                    paso=paso,
                    pensamiento=decision["pensamiento"],
                    texto=resultado_final,
                )
                break
            else:
                accion = decision["accion"]
                args = decision.get("args", {})
                self._transicionar("EVALUANDO_POLITICA", paso)
                veredicto = self.politica.evaluar(accion, args, paso)
                if veredicto.permitido:
                    self._transicionar("EJECUTANDO", paso)
                    try:
                        observacion = getattr(self.herramientas, accion)(**args)
                    except Exception as error:
                        observacion = f"ERROR: {type(error).__name__}: {error}"
                    self._transicionar("OBSERVANDO", paso)
                    self._registrar(
                        tipo="accion",
                        estado="OBSERVANDO",
                        paso=paso,
                        pensamiento=decision["pensamiento"],
                        accion=accion,
                        args=args,
                        observacion=str(observacion)[:1200],
                        bloqueada=False,
                    )
                else:
                    self._transicionar("BLOQUEADO", paso)
                    observacion = f"BLOQUEADO POR LA POLÍTICA: {veredicto.motivo}"
                    self._transicionar("OBSERVANDO", paso)
                    self._registrar(
                        tipo="accion",
                        estado="BLOQUEADO",
                        paso=paso,
                        pensamiento=decision["pensamiento"],
                        accion=accion,
                        args=args,
                        observacion=observacion,
                        bloqueada=True,
                    )
                self.historial.append(
                    {"role": "user", "content": f"Observación: {observacion}"}
                )
        else:
            self._transicionar("LIMITE_ALCANZADO", self.politica.max_pasos)
            self._registrar(
                tipo="final",
                estado="LIMITE_ALCANZADO",
                paso=self.politica.max_pasos,
                texto="Se alcanzó el máximo de pasos sin una respuesta final.",
            )
            resultado_final = "Se alcanzó el máximo de pasos sin una respuesta final."

        self._transicionar("FIN")
        self._registrar(
            tipo="resumen",
            estado="FIN",
            duracion_segundos=round(time.perf_counter() - inicio, 3),
        )
        self._guardar_evidencia()
        return resultado_final
