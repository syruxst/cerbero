"""
Cerbero - Motor de reglas estilo Hashcat.

Implementa un subconjunto de la sintaxis de reglas de Hashcat/John para
transformar palabras base. Cada "regla" es una secuencia de funciones que se
aplican de izquierda a derecha sobre una palabra.

Funciones soportadas:
    :            nada (passthrough)
    l u c C t    lower / upper / capitalize / inv-capitalize / toggle-all
    r            invertir (reverse)
    d            duplicar (word -> wordword)
    f            reflejar (word -> word + reverse)
    {  }         rotar a la izquierda / derecha
    [  ]         borrar primer / último carácter
    $X           anexar el carácter X al final
    ^X           anteponer el carácter X al inicio
    TN           alternar mayús/minús en la posición N (0-9)
    sXY          sustituir todas las apariciones de X por Y

Las reglas no soportadas se ignoran de forma segura (la palabra pasa sin
esa transformación), de modo que un .rule de hashcat se pueda cargar sin
fallar aunque use funciones avanzadas.
"""
from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import List, Optional

# Conjunto de reglas por defecto: compacto pero efectivo, inspirado en los
# patrones más productivos de best64. Operan sobre cada palabra base.
DEFAULT_RULES: List[str] = [
    ":",            # tal cual
    "l",            # minúsculas
    "c",            # Capitalizar
    "u",            # MAYÚSCULAS
    "t",            # alternar
    "r",            # invertir
    "d",            # duplicar
    "$1",           # +1
    "$2",
    "$7",
    "$!",           # +!
    "$#",
    "$1$2$3",       # +123
    "$0$1",         # +01
    "$2$0$2$4",     # +2024
    "$2$0$2$5",     # +2025
    "c$1",          # Capitaliza + 1
    "c$!",          # Capitaliza + !
    "c$1$2$3",      # Capitaliza + 123
    "c$2$0$2$4",    # Capitaliza + 2024
    "c$2$0$2$5",    # Capitaliza + 2025
    "sa@",          # a -> @
    "se3",          # e -> 3
    "si1",          # i -> 1
    "so0",          # o -> 0
    "sa@se3",       # leet combinado
    "c$1$!",        # Capitaliza + 1!
    "^!",           # prefijo !
    "}$!",          # rotar derecha + !
]


def _toggle_char(ch: str) -> str:
    """Alterna mayúscula/minúscula de un carácter."""
    if ch.islower():
        return ch.upper()
    if ch.isupper():
        return ch.lower()
    return ch


def apply_rule(word: str, rule: str) -> Optional[str]:
    """
    Aplica una regla (secuencia de funciones) a una palabra.

    Devuelve la palabra transformada, o None si la regla es inválida o
    produce una cadena vacía.
    """
    w = word
    i = 0
    n = len(rule)
    while i < n:
        fn = rule[i]
        if fn == ":":
            i += 1
        elif fn == "l":
            w = w.lower()
            i += 1
        elif fn == "u":
            w = w.upper()
            i += 1
        elif fn == "c":
            w = w.capitalize()
            i += 1
        elif fn == "C":
            w = w[:1].lower() + w[1:].upper() if w else w
            i += 1
        elif fn == "t":
            w = "".join(_toggle_char(c) for c in w)
            i += 1
        elif fn == "r":
            w = w[::-1]
            i += 1
        elif fn == "d":
            w = w + w
            i += 1
        elif fn == "f":
            w = w + w[::-1]
            i += 1
        elif fn == "{":
            w = w[1:] + w[:1] if w else w
            i += 1
        elif fn == "}":
            w = w[-1:] + w[:-1] if w else w
            i += 1
        elif fn == "[":
            w = w[1:]
            i += 1
        elif fn == "]":
            w = w[:-1]
            i += 1
        elif fn == "$":
            if i + 1 >= n:
                return None
            w = w + rule[i + 1]
            i += 2
        elif fn == "^":
            if i + 1 >= n:
                return None
            w = rule[i + 1] + w
            i += 2
        elif fn == "T":
            if i + 1 >= n or not rule[i + 1].isdigit():
                return None
            pos = int(rule[i + 1])
            if pos < len(w):
                w = w[:pos] + _toggle_char(w[pos]) + w[pos + 1 :]
            i += 2
        elif fn == "s":
            if i + 2 >= n:
                return None
            w = w.replace(rule[i + 1], rule[i + 2])
            i += 3
        else:
            # Función no soportada: la ignoramos (compat con .rule avanzados).
            i += 1

    return w or None


def apply_rules(word: str, rules: Iterable[str]) -> Iterator[str]:
    """Aplica varias reglas a una palabra y produce los resultados no vacíos."""
    for rule in rules:
        out = apply_rule(word, rule)
        if out:
            yield out


def load_rules_file(path: str) -> List[str]:
    """
    Carga un archivo .rule (una regla por línea).

    Ignora líneas vacías y comentarios (que empiezan por '#').
    """
    rules: List[str] = []
    with open(path, encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.lstrip().startswith("#"):
                continue
            rules.append(line)
    return rules
