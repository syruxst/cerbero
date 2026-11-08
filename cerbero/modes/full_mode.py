"""
Cerbero - Modo Completo (interactivo).

Recopila datos del objetivo mediante el cuestionario y delega la generación
en el pipeline compartido (`cerbero.core.pipeline.run_generation`), de modo
que el comportamiento sea idéntico al modo headless.
"""
from __future__ import annotations

from cerbero.core import (
    BANNER,
    DEFAULT_MAX_LEN,
    DEFAULT_MIN_LEN,
    DEFAULT_OUTPUT_LIMIT,
    ETHICAL_DISCLAIMER,
    bytes_to_mb_str,
    console,
    safe_input,
)
from cerbero.core.pipeline import run_generation
from cerbero.engines import ENGINE_DESCRIPTIONS
from cerbero.ioutils import gather_smart_information, generate_base_words, generate_numeric_words


def run_full_mode_interactive():
    """
    Modo completo: generación avanzada de wordlists.

    - Selección de motores (1-12 o 'all').
    - Cuestionario inteligente de datos personales.
    - Dry-run para estimación.
    - Generación en streaming con estadísticas por motor (vía pipeline).
    """
    print(BANNER)
    print(ETHICAL_DISCLAIMER)
    console.rule("MODO COMPLETO: WORDLIST AVANZADA")

    console.print("Motores de Generación Disponibles:")
    for k, desc in ENGINE_DESCRIPTIONS.items():
        console.print(f"  {k}. {desc}")

    engines_input = safe_input(
        "¿Qué motores deseas ejecutar? (ej: 1,3,8 o 'all') [all]: ", default="all"
    )
    engines_to_run = [e.strip() for e in engines_input.lower().split(",")]
    all_selected = "all" in engines_to_run

    # Secciones del cuestionario según los motores elegidos.
    if all_selected:
        required_sections = {"principal", "pareja", "hijos", "otros", "mangle", "familia"}
    else:
        required_sections = {"principal"}

    info = gather_smart_information(required_sections)
    base_words = generate_base_words(info)
    console.ok(f"Se encontraron {len(base_words):,} palabras base.")
    console.ok(f"Se generaron {len(generate_numeric_words(info)):,} variantes numéricas.")

    # Longitudes
    try:
        min_length = int(safe_input(f"Longitud MÍNIMA [{DEFAULT_MIN_LEN}]: ") or DEFAULT_MIN_LEN)
        max_length = int(safe_input(f"Longitud MÁXIMA [{DEFAULT_MAX_LEN}]: ") or DEFAULT_MAX_LEN)
    except ValueError:
        min_length, max_length = DEFAULT_MIN_LEN, DEFAULT_MAX_LEN
        console.warn(f"Entrada inválida. Usando rango por defecto {min_length}-{max_length}.")

    dry_run = safe_input("¿Modo simulación (dry run)? (s/n) [n]: ", default="n").lower() == "s"

    output_filename = None
    limit: int | None = DEFAULT_OUTPUT_LIMIT
    if not dry_run:
        output_filename = safe_input(
            "\nArchivo de salida (ej: wordlist.txt, .gz para comprimir): ", allow_empty=False
        )
        limit = int(
            safe_input(f"Límite máximo (0 = sin límite) [{DEFAULT_OUTPUT_LIMIT}]: ")
            or DEFAULT_OUTPUT_LIMIT
        )
        if limit == 0:
            limit = None
        console.ok(f"Salida a: {output_filename}")

    def on_start(engine_id: str, desc: str) -> None:
        console.info(f"Motor {engine_id}: {desc}")

    def on_done(engine_id: str, written: int, dt: float) -> None:
        console.ok(f"Motor {engine_id}: {written:,} en {dt:.2f}s")

    result = run_generation(
        info,
        engines=engines_to_run,
        min_len=min_length,
        max_len=max_length,
        limit=limit,
        output_path=output_filename,
        dry_run=dry_run,
        on_engine_start=on_start,
        on_engine_done=on_done,
    )

    console.rule("ESTADÍSTICAS DE GENERACIÓN")
    console.ok(f"Total generado/escrito: {result.total_written:,}")
    console.print(f"Tiempo total: {result.elapsed:.2f}s")
    if dry_run:
        console.warn("Dry run completado. Ningún archivo fue creado.")
    elif result.output_path:
        console.ok(f"Archivo final: {result.output_path} ({bytes_to_mb_str(result.output_bytes)})")
