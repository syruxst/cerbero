# coding: utf-8
"""
Cerbero v7.0 - Módulo de Motores
Exporta todos los motores de generación de contraseñas
"""

from .engine_01 import motor_1_combinaciones_simples_stream
from .engine_02 import motor_2_patrones_complejos_stream
from .engine_03 import motor_3_leetspeak_moderno_stream
from .engine_04 import motor_4_centrado_en_hijos_stream
from .engine_05 import motor_5_permutacion_iniciales_stream
from .engine_06 import motor_6_mangler_frases_stream
from .engine_07 import motor_7_combinatorio_creativo_stream
from .engine_08 import motor_8_cadenas_biograficas_stream

# Motores nuevos (v7.0)
from .engine_09 import motor_9_prince_combinations_stream
from .engine_10 import motor_10_pcfg_stream
from .engine_11 import motor_11_keyboard_walk_stream
from .engine_12 import motor_12_ml_patterns_stream


# Registro de motores disponibles
ENGINE_STREAMS = {
    '1': motor_1_combinaciones_simples_stream,
    '2': motor_2_patrones_complejos_stream,
    '3': motor_3_leetspeak_moderno_stream,
    '4': motor_4_centrado_en_hijos_stream,
    '5': motor_5_permutacion_iniciales_stream,
    '6': motor_6_mangler_frases_stream,
    '7': motor_7_combinatorio_creativo_stream,
    '8': motor_8_cadenas_biograficas_stream,
    '9': motor_9_prince_combinations_stream,       # NUEVO en v7.0
    '10': motor_10_pcfg_stream,                    # NUEVO en v7.0
    '11': motor_11_keyboard_walk_stream,           # NUEVO en v7.0
    '12': motor_12_ml_patterns_stream,             # NUEVO en v7.0
}


# Descripciones de motores
ENGINE_DESCRIPTIONS = {
    '1': "Combinaciones simples (ej: maria1995)",
    '2': "Patrones complejos (ej: juan-perez/92)",
    '3': "Leetspeak moderno (ej: 2025R0b3rt0!)",
    '4': "Centrado en Hijos (ej: 2018Sgl#)",
    '5': "Permutación de iniciales (ej: Pml2590)",
    '6': "Mangler de frases (ej: M1Cl4v32024*)",
    '7': "Combinatorio creativo (ej: Amor-Ana99!)",
    '8': "Cadenas biográficas (ej: C80l05m10)",
    '9': "PRINCE - Permutaciones inteligentes (ej: juanmaria2024!)",
    '10': "PCFG - Gramática probabilística (ej: Maria1995#)",
    '11': "Keyboard Walk - Patrones de teclado (ej: qwe123maria)",
    '12': "ML-Patterns - Estructuras frecuentes (ej: Juan$95)",
}


__all__ = [
    'ENGINE_STREAMS',
    'ENGINE_DESCRIPTIONS',
    # Motores individuales (1-8)
    'motor_1_combinaciones_simples_stream',
    'motor_2_patrones_complejos_stream',
    'motor_3_leetspeak_moderno_stream',
    'motor_4_centrado_en_hijos_stream',
    'motor_5_permutacion_iniciales_stream',
    'motor_6_mangler_frases_stream',
    'motor_7_combinatorio_creativo_stream',
    'motor_8_cadenas_biograficas_stream',
    # Motores nuevos (9-12) - v7.0
    'motor_9_prince_combinations_stream',
    'motor_10_pcfg_stream',
    'motor_11_keyboard_walk_stream',
    'motor_12_ml_patterns_stream',
]
