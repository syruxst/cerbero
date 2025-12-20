# coding: utf-8
"""
Cerbero v7.0 - Módulo de Generadores
Funciones para generar variaciones, leetspeak y mangling de palabras
"""

from __future__ import annotations
from functools import lru_cache
import itertools
from datetime import datetime
from typing import List
from .config import LEETSPEAK_MAP
from .utils import Colors


def full_leetspeak(text: str) -> str:
    """
    Aplica transformación leetspeak completa a un texto.

    Args:
        text: Texto a transformar

    Returns:
        Texto con transformación leetspeak aplicada
    """
    text = text.lower()
    for char, replacements in LEETSPEAK_MAP.items():
        if replacements:
            text = text.replace(char, replacements[0])
    return text


@lru_cache(maxsize=10000)
def apply_variations(word: str) -> tuple:
    """
    Genera variaciones comunes de una palabra (lowercase, capitalize, uppercase).
    Usa LRU cache para evitar recalcular las mismas palabras.

    Args:
        word: Palabra base

    Returns:
        Tuple con variaciones (inmutable para poder usar cache)
    """
    w = word or ""
    w = w.strip()
    if not w:
        return tuple()

    # Retornamos tuple en lugar de list para que sea hasheable y cacheable
    return tuple({w, w.capitalize(), w.upper()})


def apply_mangling_rules(word: str) -> List[str]:
    """
    Aplica reglas de 'mangling' combinatorio con leetspeak.

    Para palabras largas (>7 chars) usa leetspeak completo.
    Para palabras cortas genera todas las combinaciones posibles de sustituciones leetspeak.

    Args:
        word: Palabra a 'destrozar'

    Returns:
        Lista de palabras mangleadas
    """
    if not word:
        return []

    word = word.lower()
    results = {word, word.upper(), word.capitalize()}

    # Para palabras largas, aplicar leetspeak completo directamente
    if len(word) > 7:
        leet_word = full_leetspeak(word)
        results.update([leet_word, leet_word.capitalize(), leet_word.upper()])
        return list(results)

    # Para palabras cortas, generar combinaciones
    chars_to_replace = [(i, char) for i, char in enumerate(word) if char in LEETSPEAK_MAP]

    for i in range(1, len(chars_to_replace) + 1):
        for positions_combo in itertools.combinations(chars_to_replace, i):
            indices = [p[0] for p in positions_combo]
            possible_replacements = [LEETSPEAK_MAP[p[1]] for p in positions_combo]

            for replacement_values in itertools.product(*possible_replacements):
                temp_word = list(word)
                for j, index in enumerate(indices):
                    temp_word[index] = replacement_values[j]
                mangled_word = "".join(temp_word)
                results.update([mangled_word, mangled_word.capitalize(), mangled_word.upper()])

    return list(results)


def generate_usernames(info: dict) -> List[str]:
    """
    Genera nombres de usuario potenciales a partir de información personal.

    Combina nombres, apellidos y apodos con separadores y sufijos numéricos.

    Args:
        info: Diccionario con claves 'nombres', 'apellidos', 'sobrenombre', 'birth_year'

    Returns:
        Lista ordenada de nombres de usuario únicos
    """
    if not info['nombres'] or not info['apellidos']:
        print(f"{Colors.YELLOW}[AVISO] Se necesita al menos un nombre y un apellido.{Colors.RESET}")
        return []

    fname = info['nombres'][0]
    lname = info['apellidos'][0]
    nickname = info['sobrenombre']
    usernames = set()

    # Patrones básicos
    patterns = [
        fname,
        lname,
        nickname,
        f"{fname}{lname}",
        f"{lname}{fname}",
        f"{fname[0]}{lname}",
        f"{fname}{lname[0]}"
    ]

    if nickname:
        patterns.extend([f"{nickname}{lname}", f"{fname}{nickname}"])

    for p in patterns:
        if p:
            usernames.add(p)

    # Separadores comunes
    separators = ['.', '_', '-']
    for sep in separators:
        usernames.add(f"{fname}{sep}{lname}")
        usernames.add(f"{fname[0]}{sep}{lname}")

    # Sufijos numéricos
    numeric_suffixes = []
    if info['birth_year']:
        numeric_suffixes.extend([info['birth_year'], info['birth_year'][2:]])
    numeric_suffixes.append(str(datetime.now().year)[2:])

    base_usernames = list(usernames)
    for user in base_usernames:
        for suffix in numeric_suffixes:
            usernames.add(f"{user}{suffix}")

    return list(sorted([u for u in usernames if u]))
