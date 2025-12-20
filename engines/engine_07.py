# coding: utf-8
"""
Cerbero v7.0 - Motor 7: Combinatorio Creativo
Combina palabras con números y símbolos de forma creativa
"""

from __future__ import annotations
import itertools
from datetime import datetime
from typing import Iterator, List
from core import apply_variations


def motor_7_combinatorio_creativo_stream(info: dict, text_words: List[str],
                                         numeric_words: List[str], symbols: List[str]) -> Iterator[str]:
    """
    Motor 7: Combinatorio creativo.

    Permutaciones de pares de palabras con números, con/sin separadores.
    Ejemplo: Amor-Ana99!, CasaTapia2025#

    Args:
        info: Diccionario con información del objetivo
        text_words: Lista de palabras textuales
        numeric_words: Lista de números
        symbols: Lista de símbolos

    Yields:
        Contraseñas generadas
    """
    # Generar sufijos numéricos si no hay
    numeric_suffixes = set(numeric_words or [])

    if not numeric_suffixes:
        numeric_suffixes.add(str(datetime.now().year))
        numeric_suffixes.add(str(datetime.now().year)[2:])

        # Añadir años desde fechas
        if info.get("persona_principal", {}).get("fecha_nacimiento"):
            numeric_suffixes.add(str(info["persona_principal"]["fecha_nacimiento"].year))
            numeric_suffixes.add(str(info["persona_principal"]["fecha_nacimiento"].year)[2:])

        # Sufijos comunes
        numeric_suffixes.update({'01', '99', '123', '007'})

    # Si solo hay una palabra, duplicarla
    if len(text_words) < 2:
        if len(text_words) == 1:
            text_words = text_words + [text_words[0]]
        else:
            return

    for combo in itertools.permutations(text_words, 2):
        for num in numeric_suffixes:
            w1, w2 = combo
            for v1 in apply_variations(w1):
                for v2 in apply_variations(w2):
                    # Sin separador
                    base = f"{v1}{v2}{num}"
                    yield base
                    for s in symbols:
                        yield f"{base}{s}"

                    # Con separador
                    base_sep = f"{v1}-{v2}{num}"
                    yield base_sep
                    for s in symbols:
                        yield f"{base_sep}{s}"
