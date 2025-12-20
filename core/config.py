# coding: utf-8
"""
Cerbero v7.0 - Módulo de Configuración
Constantes y configuración global del sistema
"""

# Mapa de leetspeak para transformaciones
LEETSPEAK_MAP = {
    'a': ['4', '@'],
    'e': ['3'],
    'i': ['1', '!'],
    'o': ['0'],
    's': ['5', '$'],
    't': ['7']
}

# Símbolos por defecto para generar contraseñas
DEFAULT_SYMBOLS = [
    '$', '#', '!', '*', '.', '&', '%', '@', '/', '?', '-', '_',
    '+', '=', '~', '^', '|', ':', ';', '<', '>', '`', '\\'
]

# Configuración de longitudes
DEFAULT_MIN_LEN = 6
DEFAULT_MAX_LEN = 20
DEFAULT_NUMERIC_MIN = 4
DEFAULT_NUMERIC_MAX = 12

# Límite por defecto de contraseñas a generar
DEFAULT_OUTPUT_LIMIT = 5_000_000

# Configuración de versión
VERSION = "7.0"
