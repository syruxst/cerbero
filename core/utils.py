# coding: utf-8
"""
Cerbero v7.0 - Módulo de Utilidades
Funciones de utilidad, colores, banner y entrada segura
"""

from __future__ import annotations
import os
import sys
import time
import math
import unicodedata
from typing import Optional

class Colors:
    """Códigos ANSI para colores en terminal"""
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
    --- v7.0 ---
{Colors.RESET}"""


ETHICAL_DISCLAIMER = f"""{Colors.YELLOW}
[!] ADVERTENCIA DE USO ÉTICO:
Esta herramienta está diseñada exclusivamente para fines educativos y para ser utilizada
en auditorías de seguridad (pentesting) con autorización explícita del propietario del sistema.
El uso de esta herramienta en sistemas para los cuales no tienes permiso es ilegal.
El autor no se hace responsable por el mal uso de este programa.
{Colors.RESET}"""


def print_presentation():
    """Imprime el banner animado y el disclaimer ético"""
    os.system('cls' if os.name == 'nt' else 'clear')
    for char in BANNER:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.001)
    print("\n" + "="*70 + f"\n {Colors.CYAN}Creado por: Daniel Ugalde{Colors.RESET}\n" + "="*70 + "\n")
    time.sleep(1)
    for line in ETHICAL_DISCLAIMER.splitlines():
        print(line)
        time.sleep(0.05)
    print("\n" + "="*70 + "\n")
    time.sleep(1)


def normalize_string(s: str) -> str:
    """
    Normaliza unicode a ascii y elimina espacios redundantes.

    Args:
        s: String a normalizar

    Returns:
        String normalizado sin caracteres combinados y espacios limpios
    """
    if not s:
        return ""
    s2 = unicodedata.normalize('NFKD', s)
    s2 = "".join(c for c in s2 if not unicodedata.combining(c))
    s2 = s2.replace('\u200b', '')  # Eliminar zero-width space
    s2 = " ".join(s2.split())  # Limpiar espacios múltiples
    return s2


def safe_input(prompt: str = "", default: Optional[str] = None,
               normalize: bool = False, allow_empty: bool = True) -> str:
    """
    Entrada interactiva con manejo de EOF/KeyboardInterrupt.

    Args:
        prompt: Mensaje a mostrar al usuario
        default: Valor por defecto si el usuario no ingresa nada
        normalize: Si True, aplica normalize_string al resultado
        allow_empty: Si False, no permite respuestas vacías

    Returns:
        String ingresado por el usuario (o default)
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
    Estimación simple de entropía: log2(alphabet_size ** len) = len * log2(|alphabet|)

    Args:
        s: String a analizar

    Returns:
        Entropía estimada en bits
    """
    if not s:
        return 0.0

    categories = set()
    for ch in s:
        if ch.islower():
            categories.add('l')
        elif ch.isupper():
            categories.add('L')
        elif ch.isdigit():
            categories.add('d')
        else:
            categories.add('s')

    size = 0
    if 'l' in categories:
        size += 26
    if 'L' in categories:
        size += 26
    if 'd' in categories:
        size += 10
    if 's' in categories:
        size += 32

    if size <= 1:
        size = 2

    return len(s) * math.log2(size)


def bytes_to_mb_str(num_bytes: int) -> str:
    """
    Convierte bytes a MB (decimal) y devuelve una cadena formateada.
    Usa 1 MB = 1_000_000 bytes (decimales).

    Args:
        num_bytes: Número de bytes

    Returns:
        String formateado (ej: "15.42 MB")
    """
    mb = num_bytes / 1_000_000
    return f"{mb:.2f} MB"


def validate_strength(password: str) -> dict:
    """
    Valida fortaleza de contraseña según múltiples criterios.

    Args:
        password: Contraseña a validar

    Returns:
        dict con 'score', 'strength', 'color', 'entropy', 'issues'
    """
    score = 0
    issues = []

    # Criterio 1: Longitud
    length = len(password)
    if length < 8:
        issues.append("Muy corta (< 8 caracteres)")
        score -= 20
    elif length >= 12:
        score += 20
    elif length >= 16:
        score += 30

    # Criterio 2: Diversidad de caracteres
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)

    char_types = sum([has_lower, has_upper, has_digit, has_symbol])
    score += char_types * 15

    if char_types < 3:
        issues.append(f"Baja diversidad de caracteres (solo {char_types} tipos)")

    # Criterio 3: Entropía
    entropy = estimate_entropy_bits(password)
    if entropy < 30:
        issues.append(f"Entropía muy baja ({entropy:.0f} bits)")
        score -= 20
    elif entropy > 60:
        score += 30
    elif entropy > 80:
        score += 40

    # Criterio 4: Patrones comunes
    common_patterns = ['123', 'abc', 'qwerty', '000', '111', 'password',
                       'admin', 'letmein', 'welcome']
    for pattern in common_patterns:
        if pattern in password.lower():
            issues.append(f"Contiene patrón común: '{pattern}'")
            score -= 15

    # Criterio 5: Secuencias repetitivas
    if any(password[i:i+3] == password[i]*3 for i in range(len(password)-2)):
        issues.append("Contiene caracteres repetidos (ej: 'aaa', '111')")
        score -= 10

    # Score final (0-100)
    score = max(0, min(100, score))

    # Clasificación
    if score < 40:
        strength = "Muy Débil"
        color = Colors.RED
    elif score < 60:
        strength = "Débil"
        color = Colors.YELLOW
    elif score < 80:
        strength = "Media"
        color = Colors.CYAN
    else:
        strength = "Fuerte"
        color = Colors.GREEN

    return {
        'score': score,
        'strength': strength,
        'color': color,
        'entropy': entropy,
        'issues': issues
    }
