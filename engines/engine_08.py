# coding: utf-8
"""
Cerbero v7.0 - Motor 8: Cadenas Biográficas
Detecta patrones de inicial+año de familiares
"""

from __future__ import annotations
import itertools
from typing import Iterator, List


def motor_8_cadenas_biograficas_stream(info: dict, text_words: List[str],
                                       numeric_words: List[str], symbols: List[str]) -> Iterator[str]:
    """
    Motor 8: Cadenas biográficas.

    Genera permutaciones de longitud variable de inicial+año de familiares.
    Ejemplo: S76b96j14 (Sara'76, Bruno'96, Julia'14)

    Args:
        info: Diccionario con información del objetivo
        text_words: Lista de palabras textuales (no usado)
        numeric_words: Lista de números (no usado)
        symbols: Lista de símbolos (no usado)

    Yields:
        Contraseñas generadas
    """
    people = []

    # Pareja
    pareja = info.get("familia", {}).get("pareja", {})
    if pareja.get("nombres") and pareja.get("fecha_nacimiento"):
        people.append({
            "initial": pareja["nombres"][0][0],
            "year_short": str(pareja["fecha_nacimiento"].year)[2:]
        })

    # Hijos
    for hijo in info.get("familia", {}).get("hijos", []):
        if hijo.get("nombres") and hijo.get("fecha_nacimiento"):
            people.append({
                "initial": hijo["nombres"][0][0],
                "year_short": str(hijo["fecha_nacimiento"].year)[2:]
            })

    if len(people) < 2:
        return

    # Generar permutaciones de diferentes longitudes
    for length in range(2, len(people) + 1):
        for p_people in itertools.permutations(people, length):
            chunk_variations_for_permutation = []

            for person in p_people:
                initial_lower = person['initial'].lower()
                initial_upper = person['initial'].upper()
                year = person['year_short']
                chunk_variations_for_permutation.append([
                    f"{initial_lower}{year}",
                    f"{initial_upper}{year}"
                ])

            for combo in itertools.product(*chunk_variations_for_permutation):
                yield "".join(combo)
