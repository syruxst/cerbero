#!/usr/bin/env python3
# coding: utf-8
"""
Cerbero v7.0 - Generador Avanzado de Wordlists Contextuales
Autor: Daniel Ugalde

NUEVO en v7.0:
- Arquitectura modular profesional
- 12 motores de generación (8 originales + 4 nuevos)
- Bloom Filter para deduplicación escalable
- Barra de progreso en tiempo real
- Validador de fortaleza integrado
- Caché LRU para +30% velocidad
- Modo Preview
"""

from __future__ import annotations
import argparse
import sys

# Importar módulos core
from core import (
    Colors, BANNER, ETHICAL_DISCLAIMER, print_presentation,
    safe_input, DEFAULT_MIN_LEN, DEFAULT_MAX_LEN, DEFAULT_OUTPUT_LIMIT
)

# Importar todos los modos desde el módulo modes
from modes import (
    run_full_mode_interactive,
    run_numeric_mode_interactive,
    run_username_mode_interactive,
    run_merge_mode_interactive,
    run_audit_mode_interactive
)

# Importar utilidades adicionales para modo headless
import os
import gzip
from core import validate_strength
from ioutils import open_output_file


def run_merge_mode_headless(input_files_str: str, output_filename: str):
    """
    Modo merge headless (no interactivo).

    Args:
        input_files_str: Rutas de archivos separadas por comas
        output_filename: Nombre del archivo de salida
    """
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

    # Guardar resultados
    compress = output_filename.endswith('.gz')
    _, writer, closer = open_output_file(output_filename, compress)

    for p in sorted(unique_passwords):
        writer(p)

    closer()
    print(f"{Colors.GREEN}[+]{Colors.RESET} Lista unificada guardada en {output_filename}")


def run_audit_mode_headless(file_path: str, password_to_check: str):
    """
    Modo audit headless (no interactivo).

    Args:
        file_path: Ruta de la wordlist
        password_to_check: Contraseña a verificar
    """
    if not os.path.exists(file_path):
        print(f"\n{Colors.RED}[ERROR]{Colors.RESET} El archivo '{file_path}' no se encontró.")
        sys.exit(1)

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
        sys.exit(1)

    # Resultado de búsqueda
    print("-" * 70)
    if found:
        print(f"{Colors.RED}[!!!] ALERTA DE SEGURIDAD [!!!]{Colors.RESET}")
        print(f"Tu contraseña FUE ENCONTRADA en la lista (línea {line_number:,}).")
        print(f"{Colors.YELLOW}==> RECOMENDACIÓN: ¡Cámbiala inmediatamente por una más compleja! <=={Colors.RESET}")
    else:
        print(f"{Colors.GREEN}[✓] BUENA NOTICIA [✓]{Colors.RESET}")
        print("Tu contraseña NO FUE ENCONTRADA en esta wordlist.")

    # Análisis de fortaleza
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


def main():
    """Punto de entrada principal de Cerbero v7.0"""
    parser = argparse.ArgumentParser(
        prog="cerbero",
        description="Cerbero v7.0 - Generador avanzado de wordlists contextuales"
    )
    parser.add_argument('--no-interactive', action='store_true',
                       help="Ejecutar sin preguntar (headless) - requiere otros flags")
    parser.add_argument('--mode', choices=['full', 'numeric', 'username', 'audit', 'merge'],
                       help="Modo a ejecutar en modo no-interactivo")
    parser.add_argument('--output', help="Archivo de salida. Usa .gz para comprimir")
    parser.add_argument('--engines', help="Motores a ejecutar (ej: 1,2,3 o all)")
    parser.add_argument('--min-len', type=int, default=DEFAULT_MIN_LEN,
                       help="Longitud mínima de contraseñas")
    parser.add_argument('--max-len', type=int, default=DEFAULT_MAX_LEN,
                       help="Longitud máxima de contraseñas")
    parser.add_argument('--dry-run', action='store_true',
                       help="Simular sin escribir archivo")
    parser.add_argument('--limit', type=int, default=DEFAULT_OUTPUT_LIMIT,
                       help="Límite máximo de contraseñas (0 = sin límite)")
    # Argumentos específicos para modo merge
    parser.add_argument('--input-files', help="Archivos de entrada separados por comas (para modo merge)")
    # Argumentos específicos para modo audit
    parser.add_argument('--wordlist', help="Ruta de la wordlist (para modo audit)")
    parser.add_argument('--password', help="Contraseña a verificar (para modo audit)")

    args = parser.parse_args()

    # Modo interactivo por defecto
    if not args.no_interactive:
        # Mostrar presentación
        print_presentation()

        try:
            while True:
                print(f"\n{Colors.CYAN}Selecciona un modo de operación:{Colors.RESET}")
                print(f"  {Colors.YELLOW}1.{Colors.RESET} Modo Completo (Generar Wordlist Avanzada)")
                print(f"  {Colors.YELLOW}2.{Colors.RESET} Modo Numérico (Generar PINs / Códigos)")
                print(f"  {Colors.YELLOW}3.{Colors.RESET} Modo Nombres de Usuario (Generar Userlist)")
                print(f"  {Colors.YELLOW}4.{Colors.RESET} Modo Auditoría (Buscar tu contraseña + análisis)")
                print(f"  {Colors.YELLOW}5.{Colors.RESET} Modo Unir Wordlists (Combinar múltiples listas)")
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

                if choice in ['1', '2', '3', '4', '5']:
                    _ = safe_input("\nPresiona Enter para volver al menú principal...")

        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}[INFO]{Colors.RESET} Salida solicitada por el usuario. ¡Gracias por usar Cerbero!")
            sys.exit(0)
    else:
        # Modo headless (no interactivo)
        if not args.mode:
            print(f"{Colors.RED}En modo no interactivo debes usar --mode{Colors.RESET}")
            sys.exit(1)

        # Implementar modos headless
        if args.mode == 'merge':
            # Modo merge headless
            if not args.input_files or not args.output:
                print(f"{Colors.RED}Modo merge requiere --input-files y --output{Colors.RESET}")
                sys.exit(1)

            print(f"{Colors.CYAN}--- MODO MERGE (HEADLESS) ---{Colors.RESET}")
            run_merge_mode_headless(args.input_files, args.output)

        elif args.mode == 'audit':
            # Modo audit headless
            if not args.wordlist or not args.password:
                print(f"{Colors.RED}Modo audit requiere --wordlist y --password{Colors.RESET}")
                sys.exit(1)

            print(f"{Colors.CYAN}--- MODO AUDIT (HEADLESS) ---{Colors.RESET}")
            run_audit_mode_headless(args.wordlist, args.password)

        elif args.mode in ['full', 'numeric', 'username']:
            # Modos que requieren información biográfica
            print(f"{Colors.YELLOW}ADVERTENCIA: El modo '{args.mode}' requiere información biográfica detallada.{Colors.RESET}")
            print(f"{Colors.YELLOW}Por favor, usa el modo interactivo o crea un archivo de configuración JSON.{Colors.RESET}")
            print(f"\n{Colors.CYAN}Ejemplo de uso interactivo:{Colors.RESET}")
            print(f"  python cerbero.py")
            print(f"\n{Colors.CYAN}Para contribuir una implementación JSON headless completa,{Colors.RESET}")
            print(f"{Colors.CYAN}visita: https://github.com/tu-repo/cerbero{Colors.RESET}")
            sys.exit(1)

        else:
            print(f"{Colors.RED}Modo no reconocido: {args.mode}{Colors.RESET}")
            sys.exit(1)


if __name__ == "__main__":
    main()
