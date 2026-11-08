"""
Cerbero - Modelo de Markov a nivel de carácter.

Aprende las transiciones entre caracteres de las palabras del contexto
(nombres, apellidos, apodos, mascota, frases) y genera **tokens nuevos
plausibles** con el mismo "estilo". La generación es por búsqueda en haz
(beam search) determinista y acotada, ordenada por probabilidad, de modo que
la salida sea reproducible entre ejecuciones.

No pretende competir con un Markov entrenado sobre breaches masivos; su valor
es contextual: a partir de "juan", "maria", "perez" produce candidatas como
"mariaperez", "juanez", "marez"… que una persona real podría haber usado.
"""
from __future__ import annotations

import heapq
import math
from collections import Counter, defaultdict
from typing import Dict, List

_START = "\x02"  # marcador de inicio
_END = "\x03"    # marcador de fin


class MarkovModel:
    """Cadena de Markov de caracteres de orden configurable."""

    def __init__(self, order: int = 2) -> None:
        self.order = max(1, order)
        self._counts: Dict[str, Counter] = defaultdict(Counter)
        self._trained = False

    def train(self, words: List[str]) -> MarkovModel:
        """Entrena el modelo con una lista de palabras (se pasan a minúsculas)."""
        for raw in words:
            w = (raw or "").strip().lower()
            if not w:
                continue
            padded = _START * self.order + w + _END
            for i in range(len(padded) - self.order):
                context = padded[i : i + self.order]
                nxt = padded[i + self.order]
                self._counts[context][nxt] += 1
        self._trained = bool(self._counts)
        return self

    def _transitions(self, context: str) -> List[tuple[str, float]]:
        """Devuelve [(char, logprob)] para un contexto, ordenado y determinista."""
        counter = self._counts.get(context)
        if not counter:
            return []
        total = sum(counter.values())
        # Orden determinista: por probabilidad desc y luego por carácter.
        items = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
        return [(ch, math.log(cnt / total)) for ch, cnt in items]

    def generate(
        self,
        *,
        max_results: int = 500,
        min_len: int = 3,
        max_len: int = 16,
        beam_width: int = 50,
    ) -> List[str]:
        """
        Genera tokens por beam search, ordenados por probabilidad (desc).

        Devuelve una lista de palabras únicas (sin los marcadores), deterministas.
        """
        if not self._trained:
            return []

        start_ctx = _START * self.order
        # Cada haz: (logprob_acumulado, texto_generado, contexto_actual)
        beams: List[tuple[float, str, str]] = [(0.0, "", start_ctx)]
        completed: Dict[str, float] = {}

        for _ in range(max_len + 1):
            if not beams:
                break
            candidates: List[tuple[float, str, str]] = []
            for logp, text, context in beams:
                for ch, lp in self._transitions(context):
                    new_logp = logp + lp
                    if ch == _END:
                        # Conservar la mejor (mayor) probabilidad por palabra.
                        if min_len <= len(text) <= max_len and (
                            text not in completed or new_logp > completed[text]
                        ):
                            completed[text] = new_logp
                        continue
                    if len(text) + 1 > max_len:
                        continue
                    new_context = (context + ch)[-self.order :]
                    candidates.append((new_logp, text + ch, new_context))

            if not candidates:
                break
            # Quedarnos con los beam_width mejores (desempate determinista por texto).
            beams = heapq.nlargest(beam_width, candidates, key=lambda c: (c[0], c[1]))

        ranked = sorted(completed.items(), key=lambda kv: (-kv[1], kv[0]))
        return [word for word, _ in ranked[:max_results]]
