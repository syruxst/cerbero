"""
Cerbero - Motor 14: Markov contextual.

Entrena una cadena de Markov de caracteres con las palabras del contexto y
genera tokens nuevos plausibles, que luego combina con variaciones de caso y
años para producir candidatas de contraseña usables.
"""
from __future__ import annotations

from collections.abc import Iterator
from typing import List

from .markov import MarkovModel

# Orden por defecto del modelo (bigramas de caracteres).
DEFAULT_ORDER = 2
# Cuántos tokens plausibles generar antes de expandir con años/caso.
MAX_TOKENS = 300


def motor_14_markov_stream(
    info: dict,
    text_words: List[str],
    numeric_words: List[str],
    symbols: List[str],
) -> Iterator[str]:
    """
    Motor 14: genera tokens al estilo del objetivo con un modelo de Markov.

    Ejemplos (entrenado con juan/maria/perez): mariaperez, juanez, marez...
    Cada token se emite tal cual, Capitalizado y sufijado con los años del
    contexto.

    Args:
        info: Diccionario del objetivo. `otros_datos["markov_order"]` ajusta el
            orden del modelo (2 por defecto).
        text_words: Palabras base de entrenamiento.
        numeric_words: Números del contexto (se usan los años de 4 dígitos).
        symbols: No usado.

    Yields:
        Contraseñas generadas.
    """
    if not text_words or len(text_words) < 2:
        return

    order = info.get("otros_datos", {}).get("markov_order", DEFAULT_ORDER)
    model = MarkovModel(order=order).train(text_words)
    tokens = model.generate(max_results=MAX_TOKENS, min_len=4, max_len=16)
    if not tokens:
        return

    years = [n for n in numeric_words if len(n) == 4 and n.isdigit()]

    for token in tokens:
        yield token
        yield token.capitalize()
        for year in years:
            yield f"{token}{year}"
            yield f"{token.capitalize()}{year}"
