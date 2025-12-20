# coding: utf-8
"""
Cerbero v7.0 - Motor 2: Patrones Complejos
Genera patrones tipo WiFi/corporativos con separadores
"""

from __future__ import annotations
import itertools
from datetime import datetime
from typing import Iterator, List
from core import apply_variations


def motor_2_patrones_complejos_stream(info: dict, text_words: List[str],
                                     numeric_words: List[str], symbols: List[str]) -> Iterator[str]:
    """
    Motor 2: Patrones complejos.

    Usa text_words (ej: ['kasa','tapia']) y busca números en múltiples fuentes.
    Genera patrones con separadores: '-', '_', '.', '' y '/' antes del número.
    Ejemplo: kasa-tapia/38, juan_perez#92

    Args:
        info: Diccionario con información del objetivo
        text_words: Lista de palabras textuales
        numeric_words: Lista de números
        symbols: Lista de símbolos

    Yields:
        Contraseñas generadas
    """
    # Separadores entre palabras
    separators = ['-', '_', '.', '']

    # Recolectar números candidatos desde distintas fuentes
    nums = set(numeric_words or [])

    # Buscar en otros_datos numéricos
    try:
        other_nums = info.get("otros_datos", {}).get("numeros_importantes", []) or []
        for n in other_nums:
            n_clean = str(n).strip()
            if n_clean:
                nums.add(n_clean)
    except Exception:
        pass

    # Añadir años de fechas de nacimiento
    try:
        if info.get("persona_principal", {}).get("fecha_nacimiento"):
            nums.add(str(info["persona_principal"]["fecha_nacimiento"].year))
            nums.add(str(info["persona_principal"]["fecha_nacimiento"].year)[2:])
        if info.get("familia", {}).get("pareja", {}).get("fecha_nacimiento"):
            nums.add(str(info["familia"]["pareja"]["fecha_nacimiento"].year))
            nums.add(str(info["familia"]["pareja"]["fecha_nacimiento"].year)[2:])
        for h in info.get("familia", {}).get("hijos", []):
            if h.get("fecha_nacimiento"):
                nums.add(str(h["fecha_nacimiento"].year))
                nums.add(str(h["fecha_nacimiento"].year)[2:])
    except Exception:
        pass

    # Detectar números en text_words
    for w in list(text_words):
        digits = ''.join(ch for ch in w if ch.isdigit())
        if digits:
            nums.add(digits)

    # Si no hay números, generar sufijos por defecto
    if not nums:
        nums.update({str(datetime.now().year), str(datetime.now().year)[2:], '01', '99'})

    # Producir permutaciones de palabras
    for w1, w2 in itertools.permutations(text_words, 2):
        for var1 in apply_variations(w1):
            for var2 in apply_variations(w2):
                for sep in separators:
                    base = f"{var1}{sep}{var2}"
                    # Base sola
                    yield base
                    # Base con barra antes del número
                    for num in nums:
                        yield f"{base}/{num}"
                    # Base con símbolos intercalados y número
                    for num in nums:
                        for sym in symbols:
                            if sym == '/':
                                continue
                            yield f"{base}{sym}{num}"
                    # Base concatenada con número
                    for num in nums:
                        yield f"{base}{num}"
