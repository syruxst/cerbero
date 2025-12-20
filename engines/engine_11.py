# coding: utf-8
"""
Cerbero v7.0 - Motor 11: Keyboard Walk (Patrones de Teclado)
Genera combinaciones de secuencias de teclado con contexto personal

Inspirado por hashcat keyboard-walk, pero contextualizado.
"""

from __future__ import annotations
from typing import Iterator, List, Dict


# Patrones de teclado comunes (QWERTY)
KEYBOARD_PATTERNS: Dict[str, str] = {
    'qwerty_row1': 'qwertyuiop',
    'qwerty_row2': 'asdfghjkl',
    'qwerty_row3': 'zxcvbnm',
    'diagonal_qaz': 'qaz',
    'diagonal_wsx': 'wsx',
    'diagonal_edc': 'edc',
    'diagonal_rfv': 'rfv',
    'numbers': '1234567890',
    'neighbors_123': '147258369',  # Vecinos numéricos del teclado numérico
}


def motor_11_keyboard_walk_stream(info: dict, text_words: List[str],
                                  numeric_words: List[str], symbols: List[str]) -> Iterator[str]:
    """
    Motor 11: Keyboard Walk - Patrones de teclado + contexto biográfico.

    Genera combinaciones de secuencias de teclado comunes con datos personales.
    Diferenciador: Único en generadores contextuales, muy común en contraseñas hispanas.

    Ejemplos:
        qwe123maria, Juanasdfgh!, 2024qwerty, asdfJuan123
        qazMaria!, wsx2024, maria123qwe

    Args:
        info: Diccionario con información del objetivo (no usado directamente)
        text_words: Lista de palabras contextuales
        numeric_words: Lista de números relevantes
        symbols: Lista de símbolos

    Yields:
        Contraseñas generadas con patrones de teclado
    """
    if not text_words:
        return

    top_words = text_words[:10]
    top_numbers = numeric_words[:5] if numeric_words else []
    top_symbols = symbols[:3] if symbols else []

    for pattern_name, pattern in KEYBOARD_PATTERNS.items():
        # Diferentes longitudes de patrón (3-6 caracteres)
        for length in [3, 4, 5, 6]:
            if length > len(pattern):
                continue

            segment = pattern[:length]

            # Variación 1: Patrón solo
            yield segment
            yield segment.capitalize()
            yield segment.upper()

            # Variación 2: Patrón + palabra
            for word in top_words:
                # Patrón antes de palabra
                yield f"{segment}{word}"
                yield f"{segment}{word.capitalize()}"
                yield f"{segment.capitalize()}{word}"

                # Patrón después de palabra
                yield f"{word}{segment}"
                yield f"{word.capitalize()}{segment}"

            # Variación 3: Patrón + número
            if top_numbers:
                for num in top_numbers:
                    yield f"{segment}{num}"
                    yield f"{num}{segment}"
                    yield f"{segment.capitalize()}{num}"

            # Variación 4: Patrón + palabra + número
            if top_numbers:
                for word in top_words:
                    for num in top_numbers:
                        # Diferentes ordenamientos
                        yield f"{word}{segment}{num}"
                        yield f"{segment}{word}{num}"
                        yield f"{word}{num}{segment}"
                        yield f"{num}{segment}{word}"

                        # Con capitalize
                        yield f"{word.capitalize()}{segment}{num}"
                        yield f"{segment.capitalize()}{word}{num}"

            # Variación 5: Con símbolos
            if top_symbols:
                for sym in top_symbols:
                    yield f"{segment}{sym}"
                    yield f"{sym}{segment}"

                    # Patrón + palabra + símbolo
                    for word in top_words:
                        yield f"{word}{segment}{sym}"
                        yield f"{segment}{word}{sym}"
                        yield f"{word.capitalize()}{segment}{sym}"

    # Variaciones especiales: números repetidos (patrón numérico común)
    number_patterns = ['123', '321', '147', '741', '159', '951', '246', '642', '369', '963', '000', '111']
    for num_pattern in number_patterns:
        yield num_pattern

        for word in top_words[:5]:
            yield f"{word}{num_pattern}"
            yield f"{num_pattern}{word}"
            yield f"{word.capitalize()}{num_pattern}"

            if top_symbols:
                for sym in top_symbols[:2]:
                    yield f"{word}{num_pattern}{sym}"
                    yield f"{word.capitalize()}{num_pattern}{sym}"
