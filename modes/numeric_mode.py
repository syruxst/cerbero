# coding: utf-8
"""
Cerbero v7.0 - Modo Numérico
Generación de PINs y códigos numéricos
"""

import itertools
from core import (
    Colors,
    safe_input,
    DEFAULT_NUMERIC_MIN,
    DEFAULT_NUMERIC_MAX
)
from ioutils import gather_numeric_info_interactive, open_output_file


def run_numeric_mode_interactive():
    """
    Modo numérico: Generación de PINs y códigos numéricos.

    Características:
    - Recopila datos numéricos (fechas, años, PINs conocidos)
    - Genera permutaciones de 2-3 elementos
    - Filtra por longitud configurable
    """
    print(f"\n{Colors.CYAN}--- MODO NUMÉRICO: PINS / CÓDIGOS ---{Colors.RESET}\n")

    # Recopilar información numérica
    base_numbers = gather_numeric_info_interactive()
    print(f"\n{Colors.GREEN}[+]{Colors.RESET} Se recopilaron {len(base_numbers)} piezas de datos numéricos.")

    # Configuración de longitudes
    try:
        min_len = int(safe_input(f"Longitud numérica MÍNIMA [{DEFAULT_NUMERIC_MIN}]: ") or DEFAULT_NUMERIC_MIN)
        max_len = int(safe_input(f"Longitud numérica MÁXIMA [{DEFAULT_NUMERIC_MAX}]: ") or DEFAULT_NUMERIC_MAX)
    except ValueError:
        min_len, max_len = DEFAULT_NUMERIC_MIN, DEFAULT_NUMERIC_MAX
        print(f"{Colors.YELLOW}Entrada inválida. Usando rango por defecto {min_len}-{max_len}.{Colors.RESET}")

    # Generar códigos
    passwords = set()

    # Agregar números base
    for num in base_numbers:
        if min_len <= len(num) <= max_len:
            passwords.add(num)

    # Permutaciones de 2 a 3 elementos
    for r in range(2, 4):
        for combo in itertools.permutations(base_numbers, r):
            password = "".join(combo)
            if min_len <= len(password) <= max_len:
                passwords.add(password)

    if not passwords:
        print(f"{Colors.YELLOW}[AVISO]{Colors.RESET} No se generaron códigos numéricos válidos.")
        return

    # Guardar resultados
    output_filename = safe_input("\nIntroduce el nombre del archivo de salida (ej: wordlist_numeric.txt): ", allow_empty=False)
    compress = output_filename.endswith('.gz')
    _, writer, closer = open_output_file(output_filename, compress)

    for p in sorted(passwords):
        writer(p)

    closer()
    print(f"{Colors.GREEN}[+]{Colors.RESET} Se generaron {len(passwords):,} códigos. Archivo: {output_filename}")
