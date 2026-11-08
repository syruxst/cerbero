"""
Cerbero - Motor 13: Reglas estilo Hashcat.

Multiplica cada palabra base aplicando un conjunto de reglas de transformación
(subconjunto de la sintaxis Hashcat/John). Usa las reglas personalizadas del
perfil (`otros_datos["rules"]`) si existen; si no, las reglas por defecto.

Este es el motor de mayor "potencia" combinatoria: convierte las palabras
contextuales (nombres, apodos, mascota, frases) en candidatas realistas con
mutaciones que la gente usa de verdad.
"""
from __future__ import annotations

from collections.abc import Iterator
from typing import List

from .rules import DEFAULT_RULES, apply_rules


def motor_13_reglas_hashcat_stream(
    info: dict,
    text_words: List[str],
    numeric_words: List[str],
    symbols: List[str],
) -> Iterator[str]:
    """
    Motor 13: aplica reglas de transformación a cada palabra base.

    Ejemplos: maria -> Maria1, m4ri4, MARIA, aira m, maria2024, Maria!

    Args:
        info: Diccionario del objetivo. Si `otros_datos["rules"]` existe, se
            usan esas reglas (p. ej. cargadas de un .rule con --rules).
        text_words: Palabras base contextuales.
        numeric_words: No usado directamente (los años van en las reglas).
        symbols: No usado directamente.

    Yields:
        Contraseñas generadas.
    """
    if not text_words:
        return

    rules = info.get("otros_datos", {}).get("rules") or DEFAULT_RULES

    for word in text_words:
        if not word:
            continue
        yield from apply_rules(word, rules)
