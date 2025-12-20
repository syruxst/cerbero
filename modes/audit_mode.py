# coding: utf-8
"""
Cerbero v7.0 - Modo Auditoría
Busca contraseñas en wordlists y analiza su fortaleza
"""

import os
import gzip
from core import Colors, safe_input, validate_strength


def run_audit_mode_interactive():
    """
    Modo auditoría: Buscar contraseña en wordlist + análisis de fortaleza.

    NUEVO en v7.0: Incluye validador de fortaleza integrado
    """
    print(f"\n{Colors.CYAN}--- MODO AUDITORÍA: BUSCAR CONTRASEÑA EN WORDLIST ---{Colors.RESET}\n")

    file_path = safe_input("Introduce la ruta del archivo de la wordlist a revisar: ", allow_empty=False)

    if not os.path.exists(file_path):
        print(f"\n{Colors.RED}[ERROR]{Colors.RESET} El archivo '{file_path}' no se encontró.")
        return

    print(f"\n{Colors.GREEN}[SUCCESS]{Colors.RESET} Wordlist '{file_path}' cargada. Puedes empezar a auditar.")

    # Bucle de auditoría
    while True:
        password_to_check = safe_input("\nIntroduce la contraseña a verificar (o presiona Enter para volver al menú): ")

        if not password_to_check:
            break

        # Buscar en wordlist
        print(f"\n{Colors.YELLOW}[INFO]{Colors.RESET} Buscando la contraseña en '{file_path}'...")
        found = False
        line_number = 0

        try:
            open_func = gzip.open if file_path.endswith('.gz') else open
            with open_func(file_path, 'rt', encoding='utf-8', errors='ignore') as f:
                for idx, line in enumerate(f, 1):
                    if line.strip() == password_to_check:
                        found = True
                        line_number = idx
                        break
        except Exception as e:
            print(f"\n{Colors.RED}[ERROR]{Colors.RESET} Ocurrió un error al leer el archivo: {e}")
            return

        # Resultado de búsqueda
        print("-" * 70)
        if found:
            print(f"{Colors.RED}[!!!] ALERTA DE SEGURIDAD [!!!]{Colors.RESET}")
            print(f"Tu contraseña FUE ENCONTRADA en la lista (línea {line_number:,}).")
            print(f"{Colors.YELLOW}==> RECOMENDACIÓN: ¡Cámbiala inmediatamente por una más compleja! <=={Colors.RESET}")
        else:
            print(f"{Colors.GREEN}[✓] BUENA NOTICIA [✓]{Colors.RESET}")
            print("Tu contraseña NO FUE ENCONTRADA en esta wordlist.")

        # NUEVO en v7.0: Análisis de fortaleza
        print(f"\n{Colors.CYAN}--- ANÁLISIS DE FORTALEZA ---{Colors.RESET}")
        analysis = validate_strength(password_to_check)

        print(f"  Score: {analysis['color']}{analysis['score']}/100 - {analysis['strength']}{Colors.RESET}")
        print(f"  Entropía: {analysis['entropy']:.1f} bits")

        if analysis['issues']:
            print(f"\n  {Colors.YELLOW}Problemas detectados:{Colors.RESET}")
            for issue in analysis['issues']:
                print(f"    • {issue}")

        # Recomendación final
        print(f"\n  {Colors.CYAN}Recomendación General:{Colors.RESET}")
        if found:
            print(f"  {Colors.RED}CRÍTICO: Cambiar contraseña URGENTEMENTE{Colors.RESET}")
        elif analysis['score'] < 60:
            print(f"  {Colors.RED}IMPORTANTE: Cambiar contraseña por una más fuerte{Colors.RESET}")
        elif analysis['score'] < 80:
            print(f"  {Colors.YELLOW}SUGERENCIA: Considera mejorar la contraseña{Colors.RESET}")
        else:
            print(f"  {Colors.GREEN}ACEPTABLE: Contraseña tiene buena fortaleza{Colors.RESET}")

        print(f"{Colors.RESET}{'-' * 70}")
