# coding: utf-8
"""
Cerbero v7.0 - Motor 10: PCFG (Probabilistic Context-Free Grammar)
Aplica estructuras comunes de contraseñas reales al contexto biográfico

Inspirado por Prob-hashcat PCFG pero simplificado y pre-computado.
Basado en análisis de rockyou.txt y datasets de breach de 2025.
"""

from __future__ import annotations
from typing import Iterator, List, Tuple


# Estructuras pre-calculadas de rockyou.txt y breaches
# Formato: (patron, frecuencia_porcentaje)
COMMON_STRUCTURES: List[Tuple[str, float]] = [
    ("LnD4", 12.3),      # Palabra completa + 4 dígitos (ej: Maria1995)
    ("LnD2", 8.7),       # Palabra + 2 dígitos (ej: juan95)
    ("UnLnD4", 6.2),     # Upper+Lower+4 dígitos (ej: JUANperez2024)
    ("LnS1D2", 5.1),     # Palabra + símbolo + 2 dígitos (ej: maria#95)
    ("D2LnD2", 4.8),     # 2dig + palabra + 2dig (ej: 19maria95)
    ("LnD4S1", 4.2),     # Palabra + 4dig + símbolo (ej: juan1995!)
    ("D4Ln", 3.9),       # 4 dígitos + palabra (ej: 1995maria)
    ("LnLnD2", 3.5),     # Dos palabras + 2dig (ej: juanmaria95)
    ("LnS1", 2.8),       # Palabra + símbolo (ej: maria!)
    ("D4LnS1", 2.6),     # 4dig + palabra + símbolo (ej: 1995juan#)
    ("LnD2S1", 2.4),     # Palabra + 2dig + símbolo (ej: maria95!)
    ("LnLn", 2.1),       # Dos palabras concatenadas (ej: juanmaria)
    ("LnD6", 1.9),       # Palabra + 6 dígitos (ej: maria010595)
    ("D4LnD2", 1.7),     # 4dig + palabra + 2dig (ej: 1995maria95)
    ("LnS1Ln", 1.5),     # Palabra + símbolo + palabra (ej: juan#maria)
]


def motor_10_pcfg_stream(info: dict, text_words: List[str],
                         numeric_words: List[str], symbols: List[str]) -> Iterator[str]:
    """
    Motor 10: PCFG - Gramática probabilística contextual.

    Aplica las 15 estructuras más comunes de contraseñas reales al contexto biográfico.
    Diferenciador: PCFG completo requiere ML training; esta versión es pre-computada
    y enfocada en español/contexto latino.

    Ejemplos:
        Estructura "LnD4": Maria1995, juan2024
        Estructura "LnS1D2": maria#95, juan!24
        Estructura "D4Ln": 1995Maria

    Args:
        info: Diccionario con información del objetivo (no usado directamente)
        text_words: Lista de palabras contextuales
        numeric_words: Lista de números relevantes
        symbols: Lista de símbolos

    Yields:
        Contraseñas generadas siguiendo estructuras comunes
    """
    if not text_words:
        return

    # Limitar a elementos más relevantes
    top_words = text_words[:15]
    top_numbers = numeric_words[:8] if numeric_words else []
    top_symbols = symbols[:5] if symbols else []

    # Aplicar cada estructura en orden de frecuencia (más probable primero)
    for struct_pattern, probability in COMMON_STRUCTURES:

        # Aplicar estructura según el patrón
        if struct_pattern == "LnD4":
            # Palabra completa + 4 dígitos
            for word in top_words:
                for num_str in top_numbers:
                    if len(num_str) >= 4:
                        pwd = f"{word}{num_str[:4]}"
                        yield pwd
                        yield pwd.capitalize()

        elif struct_pattern == "LnD2":
            # Palabra + 2 dígitos
            for word in top_words:
                for num_str in top_numbers:
                    if len(num_str) >= 2:
                        pwd = f"{word}{num_str[:2]}"
                        yield pwd
                        yield pwd.capitalize()

        elif struct_pattern == "UnLnD4":
            # Upper+Lower+4 dígitos
            if len(top_words) >= 2:
                for w1 in top_words[:5]:
                    for w2 in top_words[:5]:
                        for num_str in top_numbers:
                            if len(num_str) >= 4:
                                pwd = f"{w1.upper()}{w2.lower()}{num_str[:4]}"
                                yield pwd

        elif struct_pattern == "LnS1D2":
            # Palabra + símbolo + 2 dígitos
            for word in top_words:
                for sym in top_symbols:
                    for num_str in top_numbers:
                        if len(num_str) >= 2:
                            pwd = f"{word}{sym}{num_str[:2]}"
                            yield pwd
                            yield pwd.capitalize()

        elif struct_pattern == "D2LnD2":
            # 2dig + palabra + 2dig
            for word in top_words:
                for num1 in top_numbers:
                    for num2 in top_numbers:
                        if len(num1) >= 2 and len(num2) >= 2:
                            pwd = f"{num1[:2]}{word}{num2[:2]}"
                            yield pwd
                            yield pwd.capitalize()

        elif struct_pattern == "LnD4S1":
            # Palabra + 4dig + símbolo
            for word in top_words:
                for num_str in top_numbers:
                    for sym in top_symbols:
                        if len(num_str) >= 4:
                            pwd = f"{word}{num_str[:4]}{sym}"
                            yield pwd
                            yield pwd.capitalize()

        elif struct_pattern == "D4Ln":
            # 4 dígitos + palabra
            for num_str in top_numbers:
                for word in top_words:
                    if len(num_str) >= 4:
                        pwd = f"{num_str[:4]}{word}"
                        yield pwd
                        yield pwd.capitalize()

        elif struct_pattern == "LnLnD2":
            # Dos palabras + 2dig
            if len(top_words) >= 2:
                for w1 in top_words[:5]:
                    for w2 in top_words[:5]:
                        for num_str in top_numbers:
                            if len(num_str) >= 2:
                                pwd = f"{w1}{w2}{num_str[:2]}"
                                yield pwd
                                yield pwd.capitalize()

        elif struct_pattern == "LnS1":
            # Palabra + símbolo
            for word in top_words:
                for sym in top_symbols:
                    pwd = f"{word}{sym}"
                    yield pwd
                    yield pwd.capitalize()

        elif struct_pattern == "D4LnS1":
            # 4dig + palabra + símbolo
            for num_str in top_numbers:
                for word in top_words:
                    for sym in top_symbols:
                        if len(num_str) >= 4:
                            pwd = f"{num_str[:4]}{word}{sym}"
                            yield pwd
                            yield pwd.capitalize()

        elif struct_pattern == "LnD2S1":
            # Palabra + 2dig + símbolo
            for word in top_words:
                for num_str in top_numbers:
                    for sym in top_symbols:
                        if len(num_str) >= 2:
                            pwd = f"{word}{num_str[:2]}{sym}"
                            yield pwd
                            yield pwd.capitalize()

        elif struct_pattern == "LnLn":
            # Dos palabras concatenadas
            if len(top_words) >= 2:
                for w1 in top_words[:5]:
                    for w2 in top_words[:5]:
                        if w1 != w2:
                            pwd = f"{w1}{w2}"
                            yield pwd
                            yield pwd.capitalize()
                            yield f"{w1.capitalize()}{w2.capitalize()}"

        elif struct_pattern == "LnD6":
            # Palabra + 6 dígitos
            for word in top_words:
                for num_str in top_numbers:
                    if len(num_str) >= 6:
                        pwd = f"{word}{num_str[:6]}"
                        yield pwd
                        yield pwd.capitalize()

        elif struct_pattern == "D4LnD2":
            # 4dig + palabra + 2dig
            for num1 in top_numbers:
                for word in top_words:
                    for num2 in top_numbers:
                        if len(num1) >= 4 and len(num2) >= 2:
                            pwd = f"{num1[:4]}{word}{num2[:2]}"
                            yield pwd
                            yield pwd.capitalize()

        elif struct_pattern == "LnS1Ln":
            # Palabra + símbolo + palabra
            if len(top_words) >= 2:
                for w1 in top_words[:5]:
                    for sym in top_symbols:
                        for w2 in top_words[:5]:
                            if w1 != w2:
                                pwd = f"{w1}{sym}{w2}"
                                yield pwd
                                yield pwd.capitalize()
                                yield f"{w1.capitalize()}{sym}{w2.capitalize()}"
