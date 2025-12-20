# coding: utf-8
"""
Cerbero v7.0 - Motor 4: Centrado en Hijos
Genera contraseñas basadas en datos de hijos
"""

from __future__ import annotations
from typing import Iterator, List


def motor_4_centrado_en_hijos_stream(info: dict, text_words: List[str],
                                     numeric_words: List[str], symbols: List[str]) -> Iterator[str]:
    """
    Motor 4: Centrado en hijos.

    Genera patrones basados en datos de hijos: año + iniciales + símbolo.
    Ejemplo: 2018Sgl#, Abc2015!

    Args:
        info: Diccionario con información del objetivo
        text_words: Lista de palabras textuales (no usado)
        numeric_words: Lista de números (no usado)
        symbols: Lista de símbolos

    Yields:
        Contraseñas generadas
    """
    for hijo in info.get("familia", {}).get("hijos", []):
        if hijo.get("fecha_nacimiento") and hijo.get("nombres"):
            year = str(hijo["fecha_nacimiento"].year)
            initials = "".join([n[0] for n in hijo["nombres"] if n] +
                             [a[0] for a in hijo.get("apellidos", []) if a]).lower()
            if initials:
                initials_cased = initials.capitalize()
                for sym in symbols:
                    yield f"{year}{initials_cased}{sym}"
                    yield f"{initials_cased}{year}{sym}"
                    yield f"{initials_cased}{sym}{year}"
