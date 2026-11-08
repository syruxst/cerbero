"""
Cerbero v7.0 - Módulo Core
Exporta todas las funciones y clases principales del core
"""

from .config import (
    DEFAULT_MAX_LEN,
    DEFAULT_MIN_LEN,
    DEFAULT_NUMERIC_MAX,
    DEFAULT_NUMERIC_MIN,
    DEFAULT_OUTPUT_LIMIT,
    DEFAULT_SYMBOLS,
    LEETSPEAK_MAP,
    VERSION,
)
from .console import RICH_AVAILABLE, ConsoleProxy, console, err_console
from .generators import apply_mangling_rules, apply_variations, full_leetspeak, generate_usernames
from .logging_config import get_logger, setup_logging
from .models import DetailedStats
from .profile import EXAMPLE_PROFILE_YAML, ProfileError, build_info, load_profile

# NOTA: `pipeline` NO se importa aquí a propósito. Depende de `engines` e
# `ioutils`, que a su vez importan de `cerbero.core`; cargarlo en el __init__
# del paquete crearía un ciclo de importación. Impórtalo de forma directa:
#     from cerbero.core.pipeline import run_generation
from .utils import (
    BANNER,
    ETHICAL_DISCLAIMER,
    Colors,
    bytes_to_mb_str,
    estimate_entropy_bits,
    normalize_string,
    print_presentation,
    safe_input,
    validate_strength,
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
    # Console / logging
    'console',
    'err_console',
    'ConsoleProxy',
    'RICH_AVAILABLE',
    'setup_logging',
    'get_logger',
    # Profiles (headless)
    'load_profile',
    'build_info',
    'ProfileError',
    'EXAMPLE_PROFILE_YAML',
]
