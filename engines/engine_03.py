# coding: utf-8
"""
Cerbero v7.0 - Motor 3: Leetspeak Moderno
Aplica transformaciones leetspeak con año actual
"""

from __future__ import annotations
from datetime import datetime
from typing import Iterator, List
from core import full_leetspeak


def motor_3_leetspeak_moderno_stream(info: dict, text_words: List[str],
                                    numeric_words: List[str], symbols: List[str]) -> Iterator[str]:
    """
    Motor 3: Leetspeak moderno.

    Aplica transformaciones leetspeak a nombres con año actual.
    Ejemplo: 2025R0b3rt0!, M4r14$2025

    Args:
        info: Diccionario con información del objetivo
        text_words: Lista de palabras textuales (no usado directamente)
        numeric_words: Lista de números (no usado directamente)
        symbols: Lista de símbolos

    Yields:
        Contraseñas generadas
    """
    current_year = str(datetime.now().year)
    names = {n.lower() for n in info.get("persona_principal", {}).get("nombres", []) if n}

    if info.get("persona_principal", {}).get("sobrenombre"):
        names.add(info["persona_principal"]["sobrenombre"].lower())

    for name in names:
        if len(name) > 1:
            leet_base = f"{name[0].upper()}{full_leetspeak(name[1:])}"
            for sym in symbols:
                yield f"{current_year}{leet_base}{sym}"
                yield f"{leet_base}{current_year}{sym}"
                yield f"{leet_base}{sym}{current_year}"
