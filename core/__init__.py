# coding: utf-8
"""
Cerbero v7.0 - Módulo Core
Exporta todas las funciones y clases principales del core
"""

from .config import (
    LEETSPEAK_MAP,
    DEFAULT_SYMBOLS,
    DEFAULT_MIN_LEN,
    DEFAULT_MAX_LEN,
    DEFAULT_NUMERIC_MIN,
    DEFAULT_NUMERIC_MAX,
    DEFAULT_OUTPUT_LIMIT,
    VERSION
)

from .utils import (
    Colors,
    BANNER,
    ETHICAL_DISCLAIMER,
    print_presentation,
    normalize_string,
    safe_input,
    estimate_entropy_bits,
    bytes_to_mb_str,
    validate_strength
)

from .generators import (
    full_leetspeak,
    apply_variations,
    apply_mangling_rules,
    generate_usernames
)

from .models import (
    DetailedStats
)

__all__ = [
    # Config
    'LEETSPEAK_MAP',
    'DEFAULT_SYMBOLS',
    'DEFAULT_MIN_LEN',
    'DEFAULT_MAX_LEN',
    'DEFAULT_NUMERIC_MIN',
    'DEFAULT_NUMERIC_MAX',
    'DEFAULT_OUTPUT_LIMIT',
    'VERSION',
    # Utils
    'Colors',
    'BANNER',
    'ETHICAL_DISCLAIMER',
    'print_presentation',
    'normalize_string',
    'safe_input',
    'estimate_entropy_bits',
    'bytes_to_mb_str',
    'validate_strength',
    # Generators
    'full_leetspeak',
    'apply_variations',
    'apply_mangling_rules',
    'generate_usernames',
    # Models
    'DetailedStats',
]
