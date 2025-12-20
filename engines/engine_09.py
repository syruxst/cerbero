# coding: utf-8
"""
Cerbero v7.0 - Motor 9: PRINCE (PRobability INfinite Chained Elements)
Genera permutaciones inteligentes de palabras contextuales

Inspirado por princeprocessor de Hashcat, pero contextualizado con OSINT.
"""

from __future__ import annotations
import itertools
from typing import Iterator, List
from core import apply_variations


def motor_9_prince_combinations_stream(info: dict, text_words: List[str],
                                       numeric_words: List[str], symbols: List[str]) -> Iterator[str]:
    """
    Motor 9: PRINCE - Permutaciones inteligentes de palabras contextuales.

    Combina palabras del contexto en todas las permutaciones posibles de 2-4 elementos.
    Diferenciador: A diferencia de princeprocessor genérico, usa contexto biográfico.

    Ejemplos:
        ["juan", "maria", "amor"] -> juanmaria, mariajuan, juanmariaamor
        + variaciones: Juanmaria, JUANMARIA
        + números: juanmaria2024, mariajuan1995!
        + símbolos: juanmaria2024!, mariajuan#1995

    Args:
        info: Diccionario con información del objetivo (no usado directamente)
        text_words: Lista de palabras contextuales
        numeric_words: Lista de números relevantes
        symbols: Lista de símbolos

    Yields:
        Contraseñas generadas mediante permutaciones
    """
    if len(text_words) < 2:
        return  # Necesitamos al menos 2 palabras para permutaciones

    # Limitar a palabras más relevantes (las primeras 10)
    top_words = text_words[:10]
    top_numbers = numeric_words[:5] if numeric_words else []
    top_symbols = symbols[:3] if symbols else []

    # Permutaciones de 2-4 palabras
    for r in range(2, min(5, len(top_words) + 1)):
        for combo in itertools.permutations(top_words, r):
            base = "".join(combo)

            # Variación 1: Solo palabras (sin números ni símbolos)
            for var in apply_variations(base):
                yield var

            # Variación 2: Palabras + números
            if top_numbers:
                for var in apply_variations(base):
                    for num in top_numbers:
                        yield f"{var}{num}"
                        yield f"{num}{var}"

            # Variación 3: Palabras + números + símbolos
            if top_numbers and top_symbols:
                for var in apply_variations(base):
                    for num in top_numbers:
                        for sym in top_symbols:
                            yield f"{var}{num}{sym}"
                            yield f"{var}{sym}{num}"
                            yield f"{num}{var}{sym}"

    # Variaciones adicionales con separadores
    if len(top_words) >= 2:
        for w1, w2 in itertools.permutations(top_words, 2):
            for var1 in apply_variations(w1):
                for var2 in apply_variations(w2):
                    # Con separador de espacio o guión
                    yield f"{var1} {var2}"
                    yield f"{var1}-{var2}"

                    if top_numbers:
                        for num in top_numbers[:3]:
                            yield f"{var1} {var2} {num}"
                            yield f"{var1}-{var2}-{num}"
