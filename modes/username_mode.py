# coding: utf-8
"""
Cerbero v7.0 - Modo Username
Generación de nombres de usuario potenciales
"""

from core import Colors, safe_input, generate_usernames
from ioutils import gather_username_info_interactive, open_output_file


def run_username_mode_interactive():
    """
    Modo generador de nombres de usuario.

    Características:
    - Recopila información de nombres y apellidos
    - Genera patrones comunes (nombre.apellido, inicial+apellido, etc.)
    - Añade sufijos numéricos (años de nacimiento, año actual)
    - Usa separadores: '.', '_', '-'
    """
    print(f"\n{Colors.CYAN}--- MODO GENERADOR DE NOMBRES DE USUARIO ---{Colors.RESET}\n")

    # Recopilar información
    info = gather_username_info_interactive()

    # Generar usernames
    username_list = generate_usernames(info)

    if username_list:
        print(f"\n{Colors.GREEN}[+]{Colors.RESET} Se generaron {len(username_list):,} nombres de usuario potenciales.")

        # Guardar resultados
        output_filename = safe_input("\nIntroduce el nombre del archivo de salida (ej: userlist.txt): ", allow_empty=False)
        compress = output_filename.endswith('.gz')
        _, writer, closer = open_output_file(output_filename, compress)

        for u in sorted(username_list):
            writer(u)

        closer()
        print(f"{Colors.GREEN}[+]{Colors.RESET} Archivo guardado: {output_filename}")
