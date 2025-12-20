# coding: utf-8
"""
Cerbero v7.0 - Modo Merge
Une múltiples wordlists eliminando duplicados
"""

import os
import gzip
from core import Colors, safe_input
from ioutils import open_output_file


def run_merge_mode_interactive():
    """
    Modo unir wordlists.

    Características:
    - Une múltiples archivos de wordlists
    - Soporta archivos .gz comprimidos
    - Elimina duplicados automáticamente
    - Ordena resultados alfabéticamente
    """
    print(f"\n{Colors.CYAN}--- MODO UNIR WORDLISTS ---{Colors.RESET}\n")

    # Solicitar archivos de entrada
    input_files_str = safe_input("Introduce las rutas de los archivos a unir (separadas por coma): ")
    if not input_files_str:
        print(f"{Colors.YELLOW}[AVISO]{Colors.RESET} No se especificaron archivos.")
        return

    file_paths = [path.strip() for path in input_files_str.split(',')]

    # Procesar archivos
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

    # Guardar resultados
    output_filename = safe_input("\nIntroduce el nombre del archivo de salida para la lista unificada: ", allow_empty=False)
    compress = output_filename.endswith('.gz')
    _, writer, closer = open_output_file(output_filename, compress)

    for p in sorted(unique_passwords):
        writer(p)

    closer()
    print(f"{Colors.GREEN}[+]{Colors.RESET} Lista unificada guardada en {output_filename}")
