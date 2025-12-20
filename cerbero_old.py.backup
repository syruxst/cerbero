#!/usr/bin/env python3
# coding: utf-8
"""
Cerbero v5.3 -> v6.0 (mejorado)
Autor original: Daniel Ugalde

Resumen de mejoras:
- Streaming de salida (no guardar todo en memoria).
- Modo CLI con argparse (permite ejecución no interactiva).
- Opción de salida comprimida (.gz).
- Reanudación simple (append a archivo y skip de duplicados con Bloom-lite en disco).
- Estimación de entropía por contraseña.
- Límite máximo configurable para evitar generadas inmanejables.
- Mejor normalización Unicode.
- Organización modular, typing, docstrings.
- Estadísticas y tiempos por motor.
- Seguridad: advertencias y 'safe mode' que evita ejecutar motores que puedan explotar datos sensibles sin confirmación.
"""

from __future__ import annotations
import argparse
from collections import deque
from datetime import datetime
import errno
import gzip
import itertools
import json
import math
import multiprocessing as mp
import os
import queue
import sys
import time
import unicodedata
from typing import Iterable, Iterator, List, Set, Tuple, Dict, Callable, Optional

# -------------------------
# Colores y banner (estilo)
# -------------------------
class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"

BANNER = f"""{Colors.MAGENTA}
██████╗ ███████╗██████╗ ██████╗ ███████╗██████╗  ██████╗ 
██╔════╝ ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗██═══██╗
██║      █████╗  ██████╔╝██████╔╝█████╗  ██████╔╝██║   ██║
██║      ██╔══╝  ██╔══██╗██╔══██╗██╔══╝  ██╔══██╗██║   ██║
╚██████╗ ███████╗██║  ██║██████╔╝███████╗██║  ██║╚██████╔╝
 ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ 
    --- v6.0 ---
{Colors.RESET}"""

ETHICAL_DISCLAIMER = f"""{Colors.YELLOW}
[!] ADVERTENCIA DE USO ÉTICO:
Esta herramienta está diseñada exclusivamente para fines educativos y para ser utilizada
en auditorías de seguridad (pentesting) con autorización explícita del propietario del sistema.
El uso de esta herramienta en sistemas para los cuales no tienes permiso es ilegal.
El autor no se hace responsable por el mal uso de este programa.
{Colors.RESET}"""

def print_presentation():
    os.system('cls' if os.name == 'nt' else 'clear')
    for char in BANNER: sys.stdout.write(char); sys.stdout.flush(); time.sleep(0.001)
    print("\n" + "="*70 + f"\n {Colors.CYAN}Creado por: Daniel Ugalde{Colors.RESET}\n" + "="*70 + "\n")
    time.sleep(1)
    for line in ETHICAL_DISCLAIMER.splitlines(): print(line); time.sleep(0.05)
    print("\n" + "="*70 + "\n"); time.sleep(1)

# -------------------------
# Configuración y constantes
# -------------------------
LEETSPEAK_MAP = {'a': ['4', '@'], 'e': ['3'], 'i': ['1', '!'], 'o': ['0'], 's': ['5', '$'], 't': ['7']}
DEFAULT_SYMBOLS = ['$', '#', '!', '*', '.', '&', '%', '@', '/', '?', '-', '_', '+', '=', '~', '^', '|', ':', ';', '<', '>', '`', '\\']
DEFAULT_MIN_LEN = 6
DEFAULT_MAX_LEN = 20
DEFAULT_NUMERIC_MIN = 4
DEFAULT_NUMERIC_MAX = 12
DEFAULT_OUTPUT_LIMIT = 5_000_000 

# -------------------------
# Utilidades
# -------------------------
def normalize_string(s: str) -> str:
    """Normaliza unicode a ascii y elimina espacios redundantes."""
    if not s:
        return ""
    s2 = unicodedata.normalize('NFKD', s)
    s2 = "".join(c for c in s2 if not unicodedata.combining(c))
    s2 = s2.replace('\u200b', '')
    s2 = " ".join(s2.split())
    return s2

def safe_input(prompt: str = "", default: Optional[str] = None, normalize: bool = False, allow_empty: bool = True) -> str:
    """
    Entrada interactiva con manejo de EOF. Si es normalize==True aplica normalize_string.
    """
    try:
        value = input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        if default is not None:
            return default
        print("\n" + Colors.YELLOW + "[INFO] Entrada terminada por el usuario." + Colors.RESET)
        sys.exit(0)
    if not value and not allow_empty:
        return safe_input(prompt, default=default, normalize=normalize, allow_empty=allow_empty)
    return normalize_string(value) if normalize and value else value

def estimate_entropy_bits(s: str) -> float:
    """
    Estimación muy simple de entropía: log2(alphabet_size ** len) = len * log2(|alphabet|)
    - Esto es aproximado pero útil para comparar longitudes/variedades.
    """
    if not s:
        return 0.0
    categories = set()
    for ch in s:
        if ch.islower(): categories.add('l')
        elif ch.isupper(): categories.add('L')
        elif ch.isdigit(): categories.add('d')
        else: categories.add('s')

    size = 0
    if 'l' in categories: size += 26
    if 'L' in categories: size += 26
    if 'd' in categories: size += 10
    if 's' in categories: size += 32 
    if size <= 1:
        size = 2
    return len(s) * math.log2(size)

def bytes_to_mb_str(num_bytes: int) -> str:
    """
    Convierte bytes a MB (decimal) y devuelve una cadena formateada con 2 decimales.
    Usa 1 MB = 1_000_000 bytes (decimales) — tal como pediste.
    """
    mb = num_bytes / 1_000_000
    return f"{mb:.2f} MB"

# -------------------------
# Generadores y motores
# -------------------------
def full_leetspeak(text: str) -> str:
    text = text.lower()
    for char, replacements in LEETSPEAK_MAP.items():
        if replacements:
            text = text.replace(char, replacements[0])
    return text

def apply_variations(word: str) -> List[str]:
    w = word or ""
    w = w.strip()
    if not w:
        return []
    return list({w, w.capitalize(), w.upper()})

def apply_mangling_rules(word: str) -> List[str]:
    if not word:
        return []
    word = word.lower()
    results = {word, word.upper(), word.capitalize()}
    if len(word) > 7:
        leet_word = full_leetspeak(word)
        results.update([leet_word, leet_word.capitalize(), leet_word.upper()])
        return list(results)
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

# Cada motor recibe info y devuelve un iterator/generator de strings (stream-friendly)
def motor_1_combinaciones_simples_stream(info: dict, text_words: List[str], numeric_words: List[str], symbols: List[str]) -> Iterator[str]:
    """Combinaciones simples, en streaming."""
    for text in text_words:
        for var in apply_variations(text):
            yield var
            for num in numeric_words:
                yield f"{var}{num}"

def motor_2_patrones_complejos_stream(info: dict, text_words: List[str], numeric_words: List[str], symbols: List[str]) -> Iterator[str]:
    """
    Motor 2 mejorado: Patrones complejos.
    - Usa text_words (p. ej. ['kasa','tapia'])
    - Busca números en numeric_words PLUS en info['otros_datos']['numeros_importantes'] y en fechas
    - Genera patrones con separadores: '-', '_', '.', '' y '/' antes del número (ej: kasa-tapia/38)
    """
    # Separadores entre palabras (para el 'base' tipo 'kasa-tapia')
    separators = ['-', '_', '.', '']
    # Recolectar números candidatos desde distintas fuentes
    nums = set(numeric_words or [])
    # Buscar en otros_datos numericos (ej: número de casa)
    try:
        other_nums = info.get("otros_datos", {}).get("numeros_importantes", []) or []
        for n in other_nums:
            n_clean = str(n).strip()
            if n_clean:
                nums.add(n_clean)
    except Exception:
        pass
    # Añadir años u otros números detectados en fechas
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

    # Extra: detectar números que puedan estar pegados a text_words (ej: 'kasa38')
    for w in list(text_words):
        digits = ''.join(ch for ch in w if ch.isdigit())
        if digits:
            nums.add(digits)

    # Si no hay números, generamos sufijos numéricos por defecto (año, 01, 99) para no quedarse vacio
    if not nums:
        nums.update({str(datetime.now().year), str(datetime.now().year)[2:], '01', '99'})

    # Ahora producir permutaciones de palabras y aplicar variaciones
    for w1, w2 in itertools.permutations(text_words, 2):
        for var1 in apply_variations(w1):
            for var2 in apply_variations(w2):
                for sep in separators:
                    base = f"{var1}{sep}{var2}"
                    # 1) base sola (sin número)
                    yield base
                    # 2) base con barra antes del número (ej: base/38) - pedido explicito
                    for num in nums:
                        yield f"{base}/{num}"
                    # 3) base con símbolos intercalados y número (ej: base!38 o base#38)
                    for num in nums:
                        for sym in symbols:
                            # Evitamos duplicar la barra si sym == '/'
                            if sym == '/':
                                continue
                            yield f"{base}{sym}{num}"
                    # 4) base concatenada con número (sin separador) por si interesa
                    for num in nums:
                        yield f"{base}{num}"


def motor_3_leetspeak_moderno_stream(info: dict, text_words: List[str], numeric_words: List[str], symbols: List[str]) -> Iterator[str]:
    current_year = str(datetime.now().year)
    names = {n.lower() for n in info.get("persona_principal", {}).get("nombres", []) if n}
    if info.get("persona_principal", {}).get("sobrenombre"): names.add(info["persona_principal"]["sobrenombre"].lower())
    for name in names:
        if len(name) > 1:
            leet_base = f"{name[0].upper()}{full_leetspeak(name[1:])}"
            for sym in symbols:
                yield f"{current_year}{leet_base}{sym}"
                yield f"{leet_base}{current_year}{sym}"
                yield f"{leet_base}{sym}{current_year}"

def motor_4_centrado_en_hijos_stream(info: dict, text_words: List[str], numeric_words: List[str], symbols: List[str]) -> Iterator[str]:
    for hijo in info.get("familia", {}).get("hijos", []):
        if hijo.get("fecha_nacimiento") and hijo.get("nombres"):
            year = str(hijo["fecha_nacimiento"].year)
            initials = "".join([n[0] for n in hijo["nombres"] if n] + [a[0] for a in hijo.get("apellidos", []) if a]).lower()
            if initials:
                initials_cased = initials.capitalize()
                for sym in symbols:
                    yield f"{year}{initials_cased}{sym}"
                    yield f"{initials_cased}{year}{sym}"
                    yield f"{initials_cased}{sym}{year}"

def motor_5_permutacion_iniciales_stream(info: dict, text_words: List[str], numeric_words: List[str], symbols: List[str]) -> Iterator[str]:
    all_initials = [n[0] for n in info.get("persona_principal", {}).get("nombres", []) if n] + \
                   [n[0] for n in info.get("familia", {}).get("pareja", {}).get("nombres", []) if n] + \
                   [n[0] for h in info.get("familia", {}).get("hijos", []) for n in h.get("nombres", []) if n]
    key_numbers = set()
    all_dates = [info.get("persona_principal", {}).get("fecha_nacimiento"), info.get("familia", {}).get("pareja", {}).get("fecha_nacimiento")] + \
                [h.get("fecha_nacimiento") for h in info.get("familia", {}).get("hijos", [])]
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

def motor_6_mangler_frases_stream(info: dict, text_words: List[str], numeric_words: List[str], symbols: List[str]) -> Iterator[str]:
    # Buscamos frases para 'mangler' en varias claves (compatibilidad)
    mangle_phrases = [p for p in info.get("otros_datos", {}).get("mangle_phrases", []) if p]
    # Fallback a otras frases que el usuario pudo haber puesto
    if not mangle_phrases:
        mangle_phrases = [p for p in info.get("otros_datos", {}).get("frases", []) if p]
    if not mangle_phrases:
        # Si no hay frases, intentamos construir pequeñas frases a partir de text_words
        if text_words:
            # combinar primeras dos palabras como frase candidata
            if len(text_words) >= 2:
                mangle_phrases = [f"{text_words[0]} {text_words[1]}"]
            else:
                mangle_phrases = [text_words[0]]
    if not mangle_phrases:
        return

    years = {str(datetime.now().year)}
    if info.get("persona_principal", {}).get("fecha_nacimiento"):
        years.add(str(info["persona_principal"]["fecha_nacimiento"].year))
    # También añadir años detectados en numeric_words (ej: 1990, 2024)
    for n in numeric_words:
        if len(n) == 4 and n.isdigit():
            years.add(n)

    complex_suffixes = ["!", "#", "!#", "@#", "!!", "*", "01", "99"]
    for phrase in mangle_phrases:
        words = phrase.strip().split()
        # Si tiene 2 o más palabras, hacemos mangling combinando ambas; si tiene 1, aplicamos reglas sobre esa sola
        if len(words) >= 2:
            w1, w2 = words[0], words[1]
            mangled1_list = apply_mangling_rules(w1)
            mangled2_list = apply_mangling_rules(w2)
            for m1 in mangled1_list:
                for m2 in mangled2_list:
                    base = f"{m1}{m2}"
                    yield base
                    for year in years:
                        pass_year = f"{base}{year}"
                        yield pass_year
                        for suffix in complex_suffixes:
                            yield f"{pass_year}{suffix}"
        else:
            # una sola palabra: aplicamos mangling y añadimos sufijos/años
            w = words[0]
            mangled_list = apply_mangling_rules(w)
            for m in mangled_list:
                yield m
                for year in years:
                    yield f"{m}{year}"
                    for suffix in complex_suffixes:
                        yield f"{m}{year}{suffix}"

def motor_7_combinatorio_creativo_stream(info: dict, text_words: List[str], numeric_words: List[str], symbols: List[str]) -> Iterator[str]:
    # Si no hay numeric_words, generamos sufijos numéricos útiles (año actual, años de nacimiento, '01','99')
    numeric_suffixes = set(numeric_words or [])
    if not numeric_suffixes:
        numeric_suffixes.add(str(datetime.now().year))
        numeric_suffixes.add(str(datetime.now().year)[2:])
        # Añadir años desde fechas en info
        if info.get("persona_principal", {}).get("fecha_nacimiento"):
            numeric_suffixes.add(str(info["persona_principal"]["fecha_nacimiento"].year))
            numeric_suffixes.add(str(info["persona_principal"]["fecha_nacimiento"].year)[2:])
        # sufijos comunes
        numeric_suffixes.update({'01', '99', '123', '007'})

    if len(text_words) < 2:
        # Si solo hay una palabra de texto, duplicarla con variaciones para formar pares
        if len(text_words) == 1:
            text_words = text_words + [text_words[0]]
        else:
            return

    for combo in itertools.permutations(text_words, 2):
        for num in numeric_suffixes:
            w1, w2 = combo
            for v1 in apply_variations(w1):
                for v2 in apply_variations(w2):
                    base = f"{v1}{v2}{num}"
                    yield base
                    for s in symbols:
                        yield f"{base}{s}"
                    base_sep = f"{v1}-{v2}{num}"
                    yield base_sep
                    for s in symbols:
                        yield f"{base_sep}{s}"

def motor_8_cadenas_biograficas_stream(info: dict, text_words: List[str], numeric_words: List[str], symbols: List[str]) -> Iterator[str]:
    people = []
    pareja = info.get("familia", {}).get("pareja", {})
    if pareja.get("nombres") and pareja.get("fecha_nacimiento"):
        people.append({"initial": pareja["nombres"][0][0], "year_short": str(pareja["fecha_nacimiento"].year)[2:]})
    for hijo in info.get("familia", {}).get("hijos", []):
        if hijo.get("nombres") and hijo.get("fecha_nacimiento"):
            people.append({"initial": hijo["nombres"][0][0], "year_short": str(hijo["fecha_nacimiento"].year)[2:]})
    if len(people) < 2:
        return
    for length in range(2, len(people) + 1):
        for p_people in itertools.permutations(people, length):
            chunk_variations_for_permutation = []
            for person in p_people:
                initial_lower = person['initial'].lower()
                initial_upper = person['initial'].upper()
                year = person['year_short']
                chunk_variations_for_permutation.append([f"{initial_lower}{year}", f"{initial_upper}{year}"])
            for combo in itertools.product(*chunk_variations_for_permutation):
                yield "".join(combo)

# Map id -> generator function
ENGINE_STREAMS = {
    '1': motor_1_combinaciones_simples_stream,
    '2': motor_2_patrones_complejos_stream,
    '3': motor_3_leetspeak_moderno_stream,
    '4': motor_4_centrado_en_hijos_stream,
    '5': motor_5_permutacion_iniciales_stream,
    '6': motor_6_mangler_frases_stream,
    '7': motor_7_combinatorio_creativo_stream,
    '8': motor_8_cadenas_biograficas_stream,
}

ENGINE_DESCRIPTIONS = {
    '1': "Combinaciones simples (ej: maria1995)",
    '2': "Patrones complejos (ej: juan-perez/92)",
    '3': "Leetspeak moderno (ej: 2025R0b3rt0!)",
    '4': "Centrado en Hijos (ej: 2018Sgl#)",
    '5': "Permutación de iniciales (ej: Pml2590)",
    '6': "Mangler de frases (ej: M1Cl4v32024*)",
    '7': "Combinatorio creativo (ej: Amor-Ana99!)",
    '8': "Cadenas biográficas (ej: C80l05m10)",
}

# -------------------------
# Base words extraction
# -------------------------
def generate_base_words(info: dict) -> List[str]:
    """Extrae palabras base desde la info (sin números)."""
    words: Set[str] = set()
    def extract_words(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "fecha_nacimiento" and value:
                    # añadimos partes de la fecha (día, mes, año corto/largo)
                    words.add(str(value.day)); words.add(f"{value.day:02d}")
                    words.add(str(value.month)); words.add(f"{value.month:02d}")
                    words.add(str(value.year)); words.add(str(value.year)[2:])
                else:
                    extract_words(value)
        elif isinstance(data, list):
            for item in data:
                extract_words(item)
        elif isinstance(data, str) and data:
            for word in data.strip().lower().split():
                cleaned = normalize_string(word)
                if cleaned:
                    words.add(cleaned)
    extract_words(info)
    return sorted([w for w in words if not w.isdigit()])

# -------------------------
# Streaming writer y control
# -------------------------
def open_output_file(path: str, compress: bool) -> Tuple[object, Callable[[str], None], Callable[[], None]]:
    """Abre archivo para escritura y devuelve write_line func y close func."""
    if compress:
        gz = gzip.open(path, 'at', encoding='utf-8', errors='replace')
        def w(line: str):
            gz.write(line + '\n')
        def c():
            gz.close()
        return gz, w, c
    else:
        f = open(path, 'a', encoding='utf-8', errors='replace')
        def w(line: str):
            f.write(line + '\n')
        def c():
            f.close()
        return f, w, c

def stream_generate_and_write(generator: Iterable[str],
                              output_writer: Callable[[str], None],
                              min_len: int,
                              max_len: int,
                              limit: Optional[int] = None,
                              seen_filter: Optional[Set[str]] = None,
                              stats: Optional[dict] = None):
    """Consume generator y escribe líneas válidas (entre min/max) al writer.
       - seen_filter: conjunto para evitar duplicados (mejor si es un set)
       - stats: diccionario donde acumulamos contadores
    """
    written = 0
    t0 = time.time()
    for pwd in generator:
        if not pwd:
            continue
        lp = len(pwd)
        if lp < min_len or lp > max_len:
            continue
        if seen_filter is not None:
            if pwd in seen_filter:
                continue
            seen_filter.add(pwd)
        output_writer(pwd)
        written += 1
        # estadística rápida
        if stats is not None:
            stats['written'] = stats.get('written', 0) + 1
        if limit and written >= limit:
            break
    stats['time'] = time.time() - t0 if stats is not None else 0
    return written

# -------------------------
# Modos y flujos interactivos
# -------------------------
def gather_smart_information(required_sections: Set[str]) -> dict:
    """Versión interactiva mejorada de recopilación de info."""
    print(f"{Colors.CYAN}--- Recopilación de Información Personal (deja en blanco si no aplica) ---{Colors.RESET}")
    info = {"persona_principal": {}, "familia": {"pareja": {}, "hijos": []}, "otros_datos": {}}
    if 'principal' in required_sections:
        print(f"\n{Colors.GREEN}[+]{Colors.RESET} Datos del objetivo principal:")
        nombres_raw = safe_input("Nombres (ej: José): ", normalize=True)
        apellidos_raw = safe_input("Apellidos (ej: Núñez): ", normalize=True)
        info["persona_principal"]["nombres"] = [normalize_string(n) for n in nombres_raw.split()] if nombres_raw else []
        info["persona_principal"]["apellidos"] = [normalize_string(a) for a in apellidos_raw.split()] if apellidos_raw else []
        fecha = safe_input("Fecha de nacimiento (DD/MM/YYYY): ")
        try:
            info["persona_principal"]["fecha_nacimiento"] = datetime.strptime(fecha, "%d/%m/%Y") if fecha else None
        except ValueError:
            info["persona_principal"]["fecha_nacimiento"] = None
        info["persona_principal"]["sobrenombre"] = normalize_string(safe_input("Sobrenombre/Apodo: ", normalize=True))
    if 'pareja' in required_sections:
        print(f"\n{Colors.GREEN}[+]{Colors.RESET} Datos de la Pareja:")
        nombres_p = safe_input("Nombres de la pareja: ", normalize=True)
        apellidos_p = safe_input("Apellidos de la pareja: ", normalize=True)
        info["familia"]["pareja"]["nombres"] = [normalize_string(n) for n in nombres_p.split()] if nombres_p else []
        info["familia"]["pareja"]["apellidos"] = [normalize_string(a) for a in apellidos_p.split()] if apellidos_p else []
        fecha_p = safe_input("Fecha de nacimiento de la pareja (DD/MM/YYYY): ")
        try:
            info["familia"]["pareja"]["fecha_nacimiento"] = datetime.strptime(fecha_p, "%d/%m/%Y") if fecha_p else None
        except ValueError:
            info["familia"]["pareja"]["fecha_nacimiento"] = None
    if 'hijos' in required_sections:
        while True:
            add_h = safe_input("\n¿Deseas agregar un hijo? (s/n): ").lower()
            if add_h != 's':
                break
            hijo = {}
            nombres_h = safe_input("Nombres del hijo/a: ", normalize=True)
            apellidos_h = safe_input("Apellidos del hijo/a: ", normalize=True)
            fecha_h = safe_input("Fecha de nacimiento del hijo/a (DD/MM/YYYY): ")
            hijo["nombres"] = [normalize_string(n) for n in nombres_h.split()] if nombres_h else []
            hijo["apellidos"] = [normalize_string(a) for a in apellidos_h.split()] if apellidos_h else []
            try:
                hijo["fecha_nacimiento"] = datetime.strptime(fecha_h, "%d/%m/%Y") if fecha_h else None
            except ValueError:
                hijo["fecha_nacimiento"] = None
            info["familia"]["hijos"].append(hijo)
    if 'otros' in required_sections:
        print(f"\n{Colors.GREEN}[+]{Colors.RESET} Otros Datos Relevantes:")
        info["otros_datos"]["mascota"] = normalize_string(safe_input("Nombre de mascota: ", normalize=True))
        frases = safe_input("Palabras clave (SSID, etc. separadas por coma): ", normalize=True)
        info["otros_datos"]["frases"] = [normalize_string(p) for p in frases.split(',')] if frases else []
        nums = safe_input("Números importantes (n° de casa, etc. separados por coma): ")
        info["otros_datos"]["numeros_importantes"] = [p.strip() for p in nums.split(',')] if nums else []
    if 'mangle' in required_sections:
        frases_m = safe_input("Frases a 'destrozar' (ej: Red Segura) separadas por coma: ", normalize=True)
        info["otros_datos"]["mangle_phrases"] = [normalize_string(p) for p in frases_m.split(',')] if frases_m else []
    return info

def gather_numeric_info_interactive() -> List[str]:
    """Recopila números para modo numérico (interactivo)."""
    print(f"\n{Colors.CYAN}--- Recopilación de Datos para Generación Numérica ---{Colors.RESET}")
    numeric_data = set()
    rut = safe_input("RUT o DNI (sin puntos, con guión si aplica): ")
    if rut:
        numeric_data.add(normalize_string(rut).split('-')[0])
    print("\nFechas de Nacimiento (DD/MM/YYYY):")
    dates = []
    fecha = safe_input("  - Persona principal: ")
    if fecha:
        try:
            dates.append(datetime.strptime(fecha, "%d/%m/%Y"))
        except ValueError:
            pass
    fecha = safe_input("  - Pareja: ")
    if fecha:
        try:
            dates.append(datetime.strptime(fecha, "%d/%m/%Y"))
        except ValueError:
            pass
    child_count = 1
    while True:
        fecha = safe_input(f"  - Hijo/a {child_count}: ")
        if fecha:
            try:
                dates.append(datetime.strptime(fecha, "%d/%m/%Y"))
                child_count += 1
                continue
            except ValueError:
                pass
        otra = safe_input("¿Agregar otro hijo? (s/n): ").lower()
        if otra != 's':
            break
    for d in dates:
        numeric_data.update([str(d.day), f"{d.day:02d}", str(d.month), f"{d.month:02d}", str(d.year), str(d.year)[2:], f"{d.day:02d}{d.month:02d}", f"{d.month:02d}{d.day:02d}"])
    casa = safe_input("  - Número de casa/departamento: ")
    ult4 = safe_input("  - Últimos 4 dígitos del teléfono/tarjeta: ")
    if casa:
        numeric_data.add(casa.strip())
    if ult4:
        numeric_data.add(ult4.strip())
    return [n for n in numeric_data if n]

def gather_username_info_interactive() -> dict:
    print(f"\n{Colors.CYAN}--- Recopilación para nombres de usuario ---{Colors.RESET}")
    nombres = safe_input("Nombres (separados por espacio): ", normalize=True).lower()
    apellidos = safe_input("Apellidos (separados por espacio): ", normalize=True).lower()
    apodo = safe_input("Sobrenombre/Apodo: ", normalize=True).lower()
    birth = safe_input("Fecha de nacimiento (para usar el año): ")
    birth_year = None
    try:
        if birth:
            bd = datetime.strptime(birth, "%d/%m/%Y")
            birth_year = str(bd.year)
    except ValueError:
        birth_year = None
    return {
        'nombres': nombres.split() if nombres else [],
        'apellidos': apellidos.split() if apellidos else [],
        'sobrenombre': apodo or "",
        'birth_year': birth_year
    }

def generate_usernames(info: dict) -> List[str]:
    if not info['nombres'] or not info['apellidos']:
        print(f"{Colors.YELLOW}[AVISO] Se necesita al menos un nombre y un apellido.{Colors.RESET}")
        return []
    fname, lname, nickname, usernames = info['nombres'][0], info['apellidos'][0], info['sobrenombre'], set()
    patterns = [fname, lname, nickname, f"{fname}{lname}", f"{lname}{fname}", f"{fname[0]}{lname}", f"{fname}{lname[0]}"]
    if nickname:
        patterns.extend([f"{nickname}{lname}", f"{fname}{nickname}"])
    for p in patterns:
        if p:
            usernames.add(p)
    separators = ['.', '_', '-']
    for sep in separators:
        usernames.add(f"{fname}{sep}{lname}"); usernames.add(f"{fname[0]}{sep}{lname}")
    numeric_suffixes = []
    if info['birth_year']:
        numeric_suffixes.extend([info['birth_year'], info['birth_year'][2:]])
    numeric_suffixes.append(str(datetime.now().year)[2:])
    base_usernames = list(usernames)
    for user in base_usernames:
        for suffix in numeric_suffixes:
            usernames.add(f"{user}{suffix}")
    return list(sorted([u for u in usernames if u]))

# -------------------------
# Modo principal (generación)
# -------------------------
def run_full_mode_interactive():
    print(BANNER)
    print(ETHICAL_DISCLAIMER)
    print(f"\n{Colors.CYAN}--- MODO COMPLETO: WORDLIST AVANZADA ---{Colors.RESET}\n")
    print("Motores de Generación Disponibles:")
    for k, desc in ENGINE_DESCRIPTIONS.items():
        print(f"  {k}. {desc}")
    engines_input = safe_input("¿Qué motores deseas ejecutar? (ej: 1,3,8 o 'all' para todos) [all]: ", default="all")
    engines_to_run = [e.strip() for e in engines_input.lower().split(',')]
    if 'all' in engines_to_run:
        selected = list(ENGINE_STREAMS.keys())
    else:
        selected = [e for e in engines_to_run if e in ENGINE_STREAMS]
    # dependencias (mínimas)
    required_sections = set()
    if 'all' in engines_to_run:
        required_sections = {'principal', 'pareja', 'hijos', 'otros', 'mangle', 'familia'}
    else:
        # simplificado: pedimos principal por defecto
        required_sections = {'principal'}
    info = gather_smart_information(required_sections)
    base_words = generate_base_words(info)
    print(f"\n{Colors.GREEN}[+]{Colors.RESET} Se encontraron {len(base_words):,} palabras base.")
    try:
        min_length = int(safe_input(f"Introduce la longitud MÍNIMA [{DEFAULT_MIN_LEN}]: ") or DEFAULT_MIN_LEN)
        max_length = int(safe_input(f"Introduce la longitud MÁXIMA [{DEFAULT_MAX_LEN}]: ") or DEFAULT_MAX_LEN)
    except ValueError:
        min_length, max_length = DEFAULT_MIN_LEN, DEFAULT_MAX_LEN
        print(f"{Colors.YELLOW}Entrada inválida. Usando rango por defecto {min_length}-{max_length}.{Colors.RESET}")
    dry_run_input = safe_input(f"¿Ejecutar en modo simulación (dry run)? {Colors.YELLOW}*** NOTA: Esto no generará una lista ***{Colors.RESET} (s/n) [n]: ", default="n")
    dry_run = True if dry_run_input.lower() == 's' else False
    output_filename = None
    compress = False
    if not dry_run:
        output_filename = safe_input("\nIntroduce el nombre del archivo de salida (ej: wordlist.txt): ", allow_empty=False)
        if output_filename.endswith('.gz'):
            compress = True
        # seguridad: confirmar tamaño
        limit = int(safe_input(f"Introduce límite máximo de contraseñas a generar (0 = sin límite) [{DEFAULT_OUTPUT_LIMIT}]: ") or DEFAULT_OUTPUT_LIMIT)
        if limit == 0:
            limit = None
    else:
        limit = DEFAULT_OUTPUT_LIMIT
    # construimos generadores y stream
    symbols = DEFAULT_SYMBOLS
    text_words = base_words
    numeric_words = [w for w in base_words if w.isdigit()]
    engines = selected
    stats = {}
    total_written = 0
    if dry_run:
        print(f"\n{Colors.YELLOW}[ESTIMACIÓN]{Colors.RESET} Modo dry-run: calculando estimación rápida. Esto no escribirá archivos.")
    else:
        print(f"\n{Colors.GREEN}[+]{Colors.RESET} Salida a: {output_filename} {'(comprimido)' if compress else ''}")
        fh, writer, closer = open_output_file(output_filename, compress)
        # si el archivo existe y no está vacío, cargamos un pequeño conjunto "seen" para evitar duplicados simples
        seen = set()
        if os.path.exists(output_filename) and os.path.getsize(output_filename) > 0:
            try:
                with (gzip.open(output_filename, 'rt', encoding='utf-8', errors='ignore') if compress else open(output_filename, 'r', encoding='utf-8', errors='ignore')) as r:
                    for i, line in enumerate(r):
                        if i > 10000:  # guardamos solo primeros 10k para acelerar reanudación
                            break
                        seen.add(line.strip())
            except Exception:
                seen = set()
    # Ejecutamos motores uno por uno para controlar memoria y estadísticas
    start_all = time.time()
    for engine_id in engines:
        func = ENGINE_STREAMS.get(engine_id)
        if not func:
            continue
        print(f"\n{Colors.CYAN}->{Colors.RESET} Ejecutando motor {engine_id}: {ENGINE_DESCRIPTIONS.get(engine_id)}")
        t0 = time.time()
        gen = func(info, text_words, numeric_words, symbols)
        engine_stats = {'written': 0}
        if dry_run:
            # contamos sin escribir: limitamos muestras para estimación
            sample_count = 0
            for pwd in gen:
                if sample_count >= 100000:  # límite de muestreo
                    break
                if min_length <= len(pwd) <= max_length:
                    engine_stats['written'] += 1
                sample_count += 1
            engine_stats['time'] = time.time() - t0
            print(f"  {Colors.GREEN}[DRY]{Colors.RESET} Muestra procesada: {engine_stats['written']:,} candidatas válidas en {engine_stats['time']:.2f}s")
            stats[f"Motor {engine_id}"] = engine_stats
            total_written += engine_stats['written']
        else:
            # stream write con filtro "seen"
            written = stream_generate_and_write(gen, writer, min_length, max_length, limit, seen, engine_stats)
            engine_stats['written'] = written
            engine_stats['time'] = time.time() - t0
            print(f"  {Colors.GREEN}[OK]{Colors.RESET} Escritas {written:,} contraseñas desde Motor {engine_id} en {engine_stats['time']:.2f}s")
            total_written += written
            # detener si alcanzamos límite global
            if limit and total_written >= limit:
                print(f"{Colors.YELLOW}[LÍMITE]{Colors.RESET} Se alcanzó el límite global de {limit:,} contraseñas.")
                break
    end_all = time.time()
    # cerrar archivo si corresponde
    if not dry_run:
        closer()
    # mostrar estadística
    print(f"\n{Colors.CYAN}--- ESTADÍSTICAS DE GENERACIÓN ---{Colors.RESET}")
    for k, v in stats.items():
        print(f"  - {k}: {Colors.GREEN}{v.get('written',0):,}{Colors.RESET} candidatas en {v.get('time',0):.2f}s.")
    print("------------------------------------")
    print(f"{Colors.GREEN}[+]{Colors.RESET} Total generado/escrito: {total_written:,}")
    print(f"Tiempo total: {end_all - start_all:.2f} segundos.")
    if not dry_run:
        file_size = os.path.getsize(output_filename)
        print(f"Archivo final: {output_filename} (tamaño: {bytes_to_mb_str(file_size)})")
        # print(f"Archivo final: {output_filename} (tamaño: {os.path.getsize(output_filename):,} bytes)")
    else:
        print(f"{Colors.YELLOW}Dry run completado. Ningún archivo fue creado.{Colors.RESET}")

def run_numeric_mode_interactive():
    print(f"\n{Colors.CYAN}--- MODO NUMÉRICO: PINS / CÓDIGOS ---{Colors.RESET}\n")
    base_numbers = gather_numeric_info_interactive()
    print(f"\n{Colors.GREEN}[+]{Colors.RESET} Se recopilaron {len(base_numbers)} piezas de datos numéricos.")
    try:
        min_len = int(safe_input(f"Longitud numérica MÍNIMA [{DEFAULT_NUMERIC_MIN}]: ") or DEFAULT_NUMERIC_MIN)
        max_len = int(safe_input(f"Longitud numérica MÁXIMA [{DEFAULT_NUMERIC_MAX}]: ") or DEFAULT_NUMERIC_MAX)
    except ValueError:
        min_len, max_len = DEFAULT_NUMERIC_MIN, DEFAULT_NUMERIC_MAX
        print(f"{Colors.YELLOW}Entrada inválida. Usando rango por defecto {min_len}-{max_len}.{Colors.RESET}")
    passwords = set()
    for num in base_numbers:
        if min_len <= len(num) <= max_len:
            passwords.add(num)
    # permutaciones de 2 a 3
    for r in range(2, 4):
        for combo in itertools.permutations(base_numbers, r):
            password = "".join(combo)
            if min_len <= len(password) <= max_len:
                passwords.add(password)
    if not passwords:
        print(f"{Colors.YELLOW}[AVISO]{Colors.RESET} No se generaron códigos numéricos válidos.")
        return
    output_filename = safe_input("\nIntroduce el nombre del archivo de salida (ej: wordlist_numeric.txt): ", allow_empty=False)
    compress = output_filename.endswith('.gz')
    _, writer, closer = open_output_file(output_filename, compress)
    for p in sorted(passwords):
        writer(p)
    closer()
    print(f"{Colors.GREEN}[+]{Colors.RESET} Se generaron {len(passwords):,} códigos. Archivo: {output_filename}")

def run_username_mode_interactive():
    print(f"\n{Colors.CYAN}--- MODO GENERADOR DE NOMBRES DE USUARIO ---{Colors.RESET}\n")
    info = gather_username_info_interactive()
    username_list = generate_usernames(info)
    if username_list:
        print(f"\n{Colors.GREEN}[+]{Colors.RESET} Se generaron {len(username_list):,} nombres de usuario potenciales.")
        output_filename = safe_input("\nIntroduce el nombre del archivo de salida (ej: userlist.txt): ", allow_empty=False)
        compress = output_filename.endswith('.gz')
        _, writer, closer = open_output_file(output_filename, compress)
        for u in sorted(username_list):
            writer(u)
        closer()
        print(f"{Colors.GREEN}[+]{Colors.RESET} Archivo guardado: {output_filename}")

def run_audit_mode_interactive():
    print(f"\n{Colors.CYAN}--- MODO AUDITORÍA: BUSCAR CONTRASEÑA EN WORDLIST ---{Colors.RESET}\n")
    file_path = safe_input("Introduce la ruta del archivo de la wordlist a revisar: ", allow_empty=False)
    if not os.path.exists(file_path):
        print(f"\n{Colors.RED}[ERROR]{Colors.RESET} El archivo '{file_path}' no se encontró.")
        return
    print(f"\n{Colors.GREEN}[SUCCESS]{Colors.RESET} Wordlist '{file_path}' cargada. Puedes empezar a auditar.")
    # No cargamos todo, buscamos linea por linea
    while True:
        password_to_check = safe_input("\nIntroduce la contraseña a verificar (o presiona Enter para volver al menú): ")
        if not password_to_check:
            break
        print(f"\n{Colors.YELLOW}[INFO]{Colors.RESET} Buscando la contraseña en '{file_path}'...")
        found = False
        try:
            open_func = gzip.open if file_path.endswith('.gz') else open
            with open_func(file_path, 'rt', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if line.strip() == password_to_check:
                        found = True
                        break
        except Exception as e:
            print(f"\n{Colors.RED}[ERROR]{Colors.RESET} Ocurrió un error al leer el archivo: {e}")
            return
        print("-" * 50)
        if found:
            print(f"{Colors.RED}[!!!] ALERTA DE SEGURIDAD [!!!]{Colors.RESET}")
            print("Tu contraseña FUE ENCONTRADA en la lista.")
            print(f"{Colors.YELLOW}==> RECOMENDACIÓN: ¡Cámbiala inmediatamente por una más compleja! <==")
        else:
            print(f"{Colors.GREEN}[✓] BUENA NOTICIA [✓]{Colors.RESET}")
            print("Tu contraseña NO FUE ENCONTRADA en esta wordlist.")
        print(f"{Colors.RESET}{'-' * 50}")

def run_merge_mode_interactive():
    print(f"\n{Colors.CYAN}--- MODO UNIR WORDLISTS ---{Colors.RESET}\n")
    input_files_str = safe_input("Introduce las rutas de los archivos a unir (separadas por coma): ")
    if not input_files_str:
        print(f"{Colors.YELLOW}[AVISO]{Colors.RESET} No se especificaron archivos.")
        return
    file_paths = [path.strip() for path in input_files_str.split(',')]
    unique_passwords = set()
    total_lines_read = 0
    print(f"\n{Colors.YELLOW}[INFO]{Colors.RESET} Procesando archivos...")
    for path in file_paths:
        if not os.path.exists(path):
            print(f"  {Colors.YELLOW}[AVISO]{Colors.RESET} El archivo '{path}' no se encontró y será omitido.")
            continue
        try:
            open_func = gzip.open if path.endswith('.gz') else open
            with open_func(path, 'rt', encoding='utf-8', errors='ignore') as f:
                lines = [line.strip() for line in f if line.strip()]
                unique_passwords.update(lines)
                total_lines_read += len(lines)
                print(f"  {Colors.GREEN}[+]{Colors.RESET} Procesado '{path}', leídas {len(lines):,} líneas.")
        except Exception as e:
            print(f"  {Colors.RED}[ERROR]{Colors.RESET} No se pudo leer el archivo '{path}': {e}")
    print(f"\n{Colors.GREEN}[+]{Colors.RESET} Total de líneas leídas: {total_lines_read:,}")
    print(f"{Colors.GREEN}[+]{Colors.RESET} Total de contraseñas únicas encontradas: {len(unique_passwords):,}")
    if not unique_passwords:
        print(f"{Colors.YELLOW}[AVISO]{Colors.RESET} No se encontraron contraseñas para guardar.")
        return
    output_filename = safe_input("\nIntroduce el nombre del archivo de salida para la lista unificada: ", allow_empty=False)
    compress = output_filename.endswith('.gz')
    _, writer, closer = open_output_file(output_filename, compress)
    for p in sorted(unique_passwords):
        writer(p)
    closer()
    print(f"{Colors.GREEN}[+]{Colors.RESET} Lista unificada guardada en {output_filename}")

# -------------------------
# CLI entrypoint y menú
# -------------------------
def main():
    parser = argparse.ArgumentParser(prog="cerbero", description="Generador avanzado de wordlists / usernames / numeric codes.")
    parser.add_argument('--no-interactive', action='store_true', help="Ejecutar sin preguntar (headless) - requiere otros flags")
    parser.add_argument('--mode', choices=['full','numeric','username','audit','merge'], help="Modo a ejecutar en modo no-interactivo")
    parser.add_argument('--output', help="Archivo de salida (usado por modo full/numeric/username/merge). Usa .gz para comprimir")
    parser.add_argument('--engines', help="Motores a ejecutar (ej: 1,2,3 o all). Sólo para modo full")
    parser.add_argument('--min-len', type=int, default=DEFAULT_MIN_LEN, help="Longitud mínima de contraseñas")
    parser.add_argument('--max-len', type=int, default=DEFAULT_MAX_LEN, help="Longitud máxima de contraseñas")
    parser.add_argument('--dry-run', action='store_true', help="Simular sin escribir archivo (dry-run)")
    parser.add_argument('--limit', type=int, default=DEFAULT_OUTPUT_LIMIT, help="Límite máximo de contraseñas a generar (0 = sin límite)")
    args = parser.parse_args()

    # Modo interactivo por defecto
    if not args.no_interactive:
        print(BANNER)
        print(ETHICAL_DISCLAIMER)
        print_presentation()
        try:
            while True:
                print(f"\n{Colors.CYAN}Selecciona un modo de operación:{Colors.RESET}")
                print(f"  {Colors.YELLOW}1.{Colors.RESET} Modo Completo (Generar Wordlist Avanzada)")
                print(f"  {Colors.YELLOW}2.{Colors.RESET} Modo Numérico (Generar PINs / Códigos)")
                print(f"  {Colors.YELLOW}3.{Colors.RESET} Modo Nombres de Usuario (Generar Userlist)")
                print(f"  {Colors.YELLOW}4.{Colors.RESET} Modo Auditoría (Buscar tu contraseña en una lista)")
                print(f"  {Colors.YELLOW}5.{Colors.RESET} Modo Unir Wordlists (Combinar múltiples listas en una)")
                print(f"  {Colors.YELLOW}6.{Colors.RESET} Salir")
                choice = safe_input("Opción: ")
                if choice == '1':
                    run_full_mode_interactive()
                elif choice == '2':
                    run_numeric_mode_interactive()
                elif choice == '3':
                    run_username_mode_interactive()
                elif choice == '4':
                    run_audit_mode_interactive()
                elif choice == '5':
                    run_merge_mode_interactive()
                elif choice == '6':
                    print(f"\n{Colors.CYAN}Saliendo de Cerbero. ¡Hasta la próxima!{Colors.RESET}")
                    break
                else:
                    print(f"{Colors.YELLOW}Opción no válida.{Colors.RESET}")
                if choice in ['1','2','3','4','5']:
                    _ = safe_input("\nPresiona Enter para volver al menú principal...")
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}[INFO]{Colors.RESET} Salida solicitada por el usuario. ¡Gracias por usar Cerbero!")
            sys.exit(0)
    else:
        # Headless: validar args
        if not args.mode:
            print(f"{Colors.RED}En modo no interactivo debes usar --mode{Colors.RESET}")
            sys.exit(1)
        if args.mode == 'full':
            # mínima implementación headless: pedimos un archivo con JSON de info si no hay interacción
            info_json = os.getenv('CERBERO_INFO_JSON')
            if not info_json:
                print(f"{Colors.RED}En modo headless 'full' debes exportar CERBERO_INFO_JSON con la info necesaria o usar modo interactivo{Colors.RESET}")
                sys.exit(1)
            try:
                info = json.loads(info_json)
            except Exception as e:
                print(f"{Colors.RED}No se pudo parsear CERBERO_INFO_JSON: {e}{Colors.RESET}")
                sys.exit(1)
            engines_to_run = args.engines or 'all'
            engines = [e.strip() for e in engines_to_run.split(',')]
            # construir base_words y correr motores similar a modo interactivo (pero simplificado)
            base_words = generate_base_words(info)
            text_words = base_words
            numeric_words = [w for w in base_words if w.isdigit()]
            symbols = DEFAULT_SYMBOLS
            output = args.output or "wordlist.txt"
            compress = output.endswith('.gz')
            fh, writer, closer = open_output_file(output, compress)
            seen = set()
            total_written = 0
            limit = None if args.limit == 0 else args.limit
            for engine_id in (list(ENGINE_STREAMS.keys()) if 'all' in engines else engines):
                func = ENGINE_STREAMS.get(engine_id)
                if not func:
                    continue
                gen = func(info, text_words, numeric_words, symbols)
                stats = {'written': 0}
                written = stream_generate_and_write(gen, writer, args.min_len, args.max_len, limit, seen, stats)
                total_written += written
                if limit and total_written >= limit:
                    break
            closer()
            print(f"{Colors.GREEN}Headless: escrito {total_written} líneas en {output}{Colors.RESET}")
        else:
            print(f"{Colors.RED}Modos headless distintos a 'full' no implementados en este script. Usa modo interactivo.{Colors.RESET}")
            sys.exit(1)

if __name__ == "__main__":
    main()
