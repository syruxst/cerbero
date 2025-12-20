# coding: utf-8
"""
Cerbero v7.0 - Motor 5: Permutación de Iniciales
Genera permutaciones de iniciales familiares con números clave
"""

from __future__ import annotations
import itertools
from typing import Iterator, List


def motor_5_permutacion_iniciales_stream(info: dict, text_words: List[str],
                                         numeric_words: List[str], symbols: List[str]) -> Iterator[str]:
    """
    Motor 5: Permutación de iniciales.

    Recopila iniciales de toda la familia y genera permutaciones con números clave.
    Ejemplo: Pml2590, Jma1876

    Args:
        info: Diccionario con información del objetivo
        text_words: Lista de palabras textuales (no usado)
        numeric_words: Lista de números (no usado)
        symbols: Lista de símbolos (no usado)

    Yields:
        Contraseñas generadas
    """
    all_initials = (
        [n[0] for n in info.get("persona_principal", {}).get("nombres", []) if n] +
        [n[0] for n in info.get("familia", {}).get("pareja", {}).get("nombres", []) if n] +
        [n[0] for h in info.get("familia", {}).get("hijos", []) for n in h.get("nombres", []) if n]
    )

    key_numbers = set()
    all_dates = (
        [info.get("persona_principal", {}).get("fecha_nacimiento"),
         info.get("familia", {}).get("pareja", {}).get("fecha_nacimiento")] +
        [h.get("fecha_nacimiento") for h in info.get("familia", {}).get("hijos", [])]
    )

    for f_nac in filter(None, all_dates):
        key_numbers.update([f"{f_nac.day:02d}", str(f_nac.year)[2:]])

    if len(all_initials) < 2 or len(key_numbers) < 2:
        return

    for i in range(3, min(len(all_initials) + 1, 6)):
        for p_initials in itertools.permutations(all_initials, i):
            initial_part = "".join(p_initials)
            initial_part_cased = initial_part[0].upper() + initial_part[1:].lower()
            for p_numbers in itertools.permutations(key_numbers, 2):
                number_part = "".join(p_numbers)
                yield f"{initial_part_cased}{number_part}"
