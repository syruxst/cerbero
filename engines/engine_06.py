# coding: utf-8
"""
Cerbero v7.0 - Motor 6: Mangler de Frases
Aplica mangling combinatorio con leetspeak a frases
"""

from __future__ import annotations
from datetime import datetime
from typing import Iterator, List
from core import apply_mangling_rules


# Límite de outputs por frase para evitar explosión combinatoria
MAX_MANGLING_OUTPUTS = 100_000


def motor_6_mangler_frases_stream(info: dict, text_words: List[str],
                                  numeric_words: List[str], symbols: List[str]) -> Iterator[str]:
    """
    Motor 6: Mangler de frases.

    Aplica mangling avanzado a frases completas con leetspeak combinatorio.
    Ejemplo: M1Cl4v32024*, R3dS3gur4!#

    Args:
        info: Diccionario con información del objetivo
        text_words: Lista de palabras textuales (fallback si no hay frases)
        numeric_words: Lista de números
        symbols: Lista de símbolos (no usado directamente)

    Yields:
        Contraseñas generadas
    """
    # Buscar frases para mangler
    mangle_phrases = [p for p in info.get("otros_datos", {}).get("mangle_phrases", []) if p]

    # Fallback a otras frases
    if not mangle_phrases:
        mangle_phrases = [p for p in info.get("otros_datos", {}).get("frases", []) if p]

    # Si no hay frases, construir desde text_words
    if not mangle_phrases:
        if text_words:
            if len(text_words) >= 2:
                mangle_phrases = [f"{text_words[0]} {text_words[1]}"]
            else:
                mangle_phrases = [text_words[0]]

    if not mangle_phrases:
        return

    # Recopilar años
    years = {str(datetime.now().year)}
    if info.get("persona_principal", {}).get("fecha_nacimiento"):
        years.add(str(info["persona_principal"]["fecha_nacimiento"].year))

    # Añadir años desde numeric_words
    for n in numeric_words:
        if len(n) == 4 and n.isdigit():
            years.add(n)

    complex_suffixes = ["!", "#", "!#", "@#", "!!", "*", "01", "99"]

    for phrase in mangle_phrases:
        words = phrase.strip().split()
        output_count = 0  # Contador para límite

        if len(words) >= 2:
            w1, w2 = words[0], words[1]
            mangled1_list = apply_mangling_rules(w1)
            mangled2_list = apply_mangling_rules(w2)

            for m1 in mangled1_list:
                for m2 in mangled2_list:
                    base = f"{m1}{m2}"
                    yield base
                    output_count += 1

                    for year in years:
                        pass_year = f"{base}{year}"
                        yield pass_year
                        output_count += 1

                        for suffix in complex_suffixes:
                            yield f"{pass_year}{suffix}"
                            output_count += 1

                            # Early termination si superamos límite
                            if output_count >= MAX_MANGLING_OUTPUTS:
                                return
        else:
            # Una sola palabra
            w = words[0]
            mangled_list = apply_mangling_rules(w)

            for m in mangled_list:
                yield m
                output_count += 1

                for year in years:
                    yield f"{m}{year}"
                    output_count += 1

                    for suffix in complex_suffixes:
                        yield f"{m}{year}{suffix}"
                        output_count += 1

                        # Early termination
                        if output_count >= MAX_MANGLING_OUTPUTS:
                            return
