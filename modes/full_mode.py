# coding: utf-8
"""
Cerbero v7.0 - Modo Completo (Full Mode)
Generación avanzada de wordlists usando múltiples motores
"""

import os
import time
import gzip
from core import (
    Colors,
    BANNER,
    ETHICAL_DISCLAIMER,
    safe_input,
    bytes_to_mb_str,
    DEFAULT_MIN_LEN,
    DEFAULT_MAX_LEN,
    DEFAULT_SYMBOLS,
    DEFAULT_OUTPUT_LIMIT
)
from engines import ENGINE_STREAMS, ENGINE_DESCRIPTIONS

# Usar imports absolutos con paréntesis para evitar colisión con io estándar
from ioutils import (
    gather_smart_information,
    generate_base_words,
    generate_numeric_words,
    open_output_file,
    stream_generate_and_write
)


def run_full_mode_interactive():
    """
    Modo completo: Generación avanzada de wordlists.

    Características:
    - Selección de motores (1-12 o 'all')
    - Recopilación inteligente de datos personales
    - Dry-run para estimación
    - Streaming con estadísticas por motor
    - Reanudación con deduplicación simple (primeros 10k)
    """
    print(BANNER)
    print(ETHICAL_DISCLAIMER)
    print(f"\n{Colors.CYAN}--- MODO COMPLETO: WORDLIST AVANZADA ---{Colors.RESET}\n")

    # Mostrar motores disponibles
    print("Motores de Generación Disponibles:")
    for k, desc in ENGINE_DESCRIPTIONS.items():
        print(f"  {k}. {desc}")

    # Selección de motores
    engines_input = safe_input("¿Qué motores deseas ejecutar? (ej: 1,3,8 o 'all' para todos) [all]: ", default="all")
    engines_to_run = [e.strip() for e in engines_input.lower().split(',')]

    if 'all' in engines_to_run:
        selected = list(ENGINE_STREAMS.keys())
    else:
        selected = [e for e in engines_to_run if e in ENGINE_STREAMS]

    # Determinar secciones de información requeridas
    required_sections = set()
    if 'all' in engines_to_run:
        required_sections = {'principal', 'pareja', 'hijos', 'otros', 'mangle', 'familia'}
    else:
        # Simplificado: pedimos principal por defecto
        required_sections = {'principal'}

    # Recopilar información
    info = gather_smart_information(required_sections)
    base_words = generate_base_words(info)

    print(f"\n{Colors.GREEN}[+]{Colors.RESET} Se encontraron {len(base_words):,} palabras base.")

    # Generar números para mostrar información antes de continuar
    numeric_words_preview = generate_numeric_words(info)
    print(f"{Colors.GREEN}[+]{Colors.RESET} Se generaron {len(numeric_words_preview):,} variantes numéricas.")

    # Configuración de longitudes
    try:
        min_length = int(safe_input(f"Introduce la longitud MÍNIMA [{DEFAULT_MIN_LEN}]: ") or DEFAULT_MIN_LEN)
        max_length = int(safe_input(f"Introduce la longitud MÁXIMA [{DEFAULT_MAX_LEN}]: ") or DEFAULT_MAX_LEN)
    except ValueError:
        min_length, max_length = DEFAULT_MIN_LEN, DEFAULT_MAX_LEN
        print(f"{Colors.YELLOW}Entrada inválida. Usando rango por defecto {min_length}-{max_length}.{Colors.RESET}")

    # Modo dry-run
    dry_run_input = safe_input(f"¿Ejecutar en modo simulación (dry run)? {Colors.YELLOW}*** NOTA: Esto no generará una lista ***{Colors.RESET} (s/n) [n]: ", default="n")
    dry_run = True if dry_run_input.lower() == 's' else False

    # Configuración de salida
    output_filename = None
    compress = False

    if not dry_run:
        output_filename = safe_input("\nIntroduce el nombre del archivo de salida (ej: wordlist.txt): ", allow_empty=False)
        if output_filename.endswith('.gz'):
            compress = True

        # Límite de seguridad
        limit = int(safe_input(f"Introduce límite máximo de contraseñas a generar (0 = sin límite) [{DEFAULT_OUTPUT_LIMIT}]: ") or DEFAULT_OUTPUT_LIMIT)
        if limit == 0:
            limit = None
    else:
        limit = DEFAULT_OUTPUT_LIMIT

    # Preparar datos para motores
    symbols = DEFAULT_SYMBOLS
    text_words = base_words
    numeric_words = generate_numeric_words(info)
    engines = selected

    # Inicializar estadísticas
    stats = {}
    total_written = 0

    if dry_run:
        print(f"\n{Colors.YELLOW}[ESTIMACIÓN]{Colors.RESET} Modo dry-run: calculando estimación rápida. Esto no escribirá archivos.")
    else:
        print(f"\n{Colors.GREEN}[+]{Colors.RESET} Salida a: {output_filename} {'(comprimido)' if compress else ''}")
        fh, writer, closer = open_output_file(output_filename, compress)

        # Si el archivo existe y no está vacío, cargamos un pequeño conjunto "seen" para evitar duplicados simples
        seen = set()
        if os.path.exists(output_filename) and os.path.getsize(output_filename) > 0:
            try:
                with (gzip.open(output_filename, 'rt', encoding='utf-8', errors='ignore') if compress else open(output_filename, 'r', encoding='utf-8', errors='ignore')) as r:
                    for i, line in enumerate(r):
                        if i > 10000:  # guardamos solo primeros 10k para acelerar reanudación
                            break
                        seen.add(line.strip())
            except Exception:
                seen = set()

    # Ejecutar motores uno por uno para controlar memoria y estadísticas
    start_all = time.time()

    for engine_id in engines:
        func = ENGINE_STREAMS.get(engine_id)
        if not func:
            continue

        print(f"\n{Colors.CYAN}->{Colors.RESET} Ejecutando motor {engine_id}: {ENGINE_DESCRIPTIONS.get(engine_id)}")
        t0 = time.time()
        gen = func(info, text_words, numeric_words, symbols)
        engine_stats = {'written': 0}

        if dry_run:
            # Contar sin escribir: limitamos muestras para estimación
            sample_count = 0
            for pwd in gen:
                if sample_count >= 100000:  # límite de muestreo
                    break
                if min_length <= len(pwd) <= max_length:
                    engine_stats['written'] += 1
                sample_count += 1

            engine_stats['time'] = time.time() - t0
            print(f"  {Colors.GREEN}[DRY]{Colors.RESET} Muestra procesada: {engine_stats['written']:,} candidatas válidas en {engine_stats['time']:.2f}s")
            stats[f"Motor {engine_id}"] = engine_stats
            total_written += engine_stats['written']
        else:
            # Stream write con filtro "seen"
            written = stream_generate_and_write(gen, writer, min_length, max_length, limit, seen, engine_stats)
            engine_stats['written'] = written
            engine_stats['time'] = time.time() - t0
            print(f"  {Colors.GREEN}[OK]{Colors.RESET} Escritas {written:,} contraseñas desde Motor {engine_id} en {engine_stats['time']:.2f}s")
            total_written += written

            # Detener si alcanzamos límite global
            if limit and total_written >= limit:
                print(f"{Colors.YELLOW}[LÍMITE]{Colors.RESET} Se alcanzó el límite global de {limit:,} contraseñas.")
                break

    end_all = time.time()

    # Cerrar archivo si corresponde
    if not dry_run:
        closer()

    # Mostrar estadísticas
    print(f"\n{Colors.CYAN}--- ESTADÍSTICAS DE GENERACIÓN ---{Colors.RESET}")
    for k, v in stats.items():
        print(f"  - {k}: {Colors.GREEN}{v.get('written',0):,}{Colors.RESET} candidatas en {v.get('time',0):.2f}s.")
    print("------------------------------------")
    print(f"{Colors.GREEN}[+]{Colors.RESET} Total generado/escrito: {total_written:,}")
    print(f"Tiempo total: {end_all - start_all:.2f} segundos.")

    if not dry_run:
        file_size = os.path.getsize(output_filename)
        print(f"Archivo final: {output_filename} (tamaño: {bytes_to_mb_str(file_size)})")
    else:
        print(f"{Colors.YELLOW}Dry run completado. Ningún archivo fue creado.{Colors.RESET}")
