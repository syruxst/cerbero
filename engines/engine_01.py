# coding: utf-8
"""
Cerbero v7.0 - Motor 1: Combinaciones Simples
Genera variaciones básicas de palabras con números
"""

from __future__ import annotations
from typing import Iterator, List
from core import apply_variations


def motor_1_combinaciones_simples_stream(info: dict, text_words: List[str],
                                        numeric_words: List[str], symbols: List[str]) -> Iterator[str]:
    """
    Motor 1: Combinaciones simples, en streaming.

    Genera variaciones básicas: original, capitalize, upper + números.
    Ejemplo: maria, Maria, MARIA, maria1995, MARIA1995

    Args:
        info: Diccionario con información del objetivo
        text_words: Lista de palabras textuales
        numeric_words: Lista de números
        symbols: Lista de símbolos (no usado en este motor)

    Yields:
        Contraseñas generadas
    """
    for text in text_words:
        for var in apply_variations(text):
            yield var
            for num in numeric_words:
                yield f"{var}{num}"
