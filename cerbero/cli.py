#!/usr/bin/env python3
"""
Cerbero - Interfaz de línea de comandos.

Modos:
    cerbero                       Menú interactivo (por defecto).
    cerbero generate ...          Generación headless desde un perfil.
    cerbero audit ...             Auditar una contraseña contra una wordlist.
    cerbero merge ...             Unir y deduplicar varias wordlists.
    cerbero init-profile [ruta]   Escribir un perfil de ejemplo.
    cerbero version               Mostrar la versión.
"""
from __future__ import annotations

import argparse
import gzip
import os
import sys

from cerbero import __version__
from cerbero.core import (
    DEFAULT_MAX_LEN,
    DEFAULT_MIN_LEN,
    DEFAULT_OUTPUT_LIMIT,
    EXAMPLE_PROFILE_YAML,
    ProfileError,
    bytes_to_mb_str,
    console,
    err_console,
    load_profile,
    print_presentation,
    safe_input,
    setup_logging,
    validate_strength,
)
from cerbero.core.pipeline import run_generation
from cerbero.engines import ENGINE_DESCRIPTIONS
from cerbero.modes import (
    run_audit_mode_interactive,
    run_full_mode_interactive,
    run_merge_mode_interactive,
    run_numeric_mode_interactive,
    run_username_mode_interactive,
)


# --------------------------------------------------------------------------- #
# Subcomando: generate (headless)
# --------------------------------------------------------------------------- #
def cmd_generate(args: argparse.Namespace) -> int:
    """Generación headless de wordlist desde un perfil YAML/JSON."""
    try:
        info = load_profile(args.config)
    except ProfileError as exc:
        err_console.error(str(exc))
        return 2

    if not args.stdout and not args.dry_run and not args.output:
        err_console.error("Debes indicar --output ARCHIVO (o usar --stdout / --dry-run).")
        return 2

    def on_start(engine_id: str, desc: str) -> None:
        err_console.info(f"Motor {engine_id}: {desc}")

    def on_done(engine_id: str, written: int, dt: float) -> None:
        err_console.ok(f"Motor {engine_id}: {written:,} candidatas en {dt:.2f}s")

    limit = None if args.limit == 0 else args.limit

    try:
        result = run_generation(
            info,
            engines=args.engines,
            min_len=args.min_len,
            max_len=args.max_len,
            limit=limit,
            output_path=args.output,
            dry_run=args.dry_run,
            dedup=not args.no_dedup,
            to_stdout=args.stdout,
            on_engine_start=on_start if not args.stdout else None,
            on_engine_done=on_done if not args.stdout else None,
        )
    except (ValueError, OSError) as exc:
        err_console.error(f"Error de generación: {exc}")
        return 1

    _render_generation_summary(result, to_stdout=args.stdout)
    return 0


def _render_generation_summary(result, *, to_stdout: bool) -> None:
    """Imprime un resumen (tabla Rich si está disponible) por stderr."""
    out = err_console  # siempre stderr, no contamina la wordlist
    if result.dry_run:
        out.warn("DRY-RUN: no se escribió ningún archivo (estimación por muestreo).")

    rich = out.rich
    if rich is not None:
        from rich.table import Table

        table = Table(title="Resumen de generación", title_style="accent", header_style="bold")
        table.add_column("Motor", justify="right")
        table.add_column("Descripción")
        table.add_column("Generadas", justify="right")
        table.add_column("Tiempo", justify="right")
        for eid, count in sorted(result.by_engine.items(), key=lambda kv: int(kv[0])):
            table.add_row(
                eid,
                ENGINE_DESCRIPTIONS.get(eid, ""),
                f"{count:,}",
                f"{result.time_by_engine.get(eid, 0.0):.2f}s",
            )
        rich.print(table)
    else:
        for eid, count in sorted(result.by_engine.items(), key=lambda kv: int(kv[0])):
            out.print(f"  Motor {eid}: {count:,}")

    out.ok(f"Total: {result.total_written:,} contraseñas en {result.elapsed:.2f}s")
    if result.output_path:
        out.ok(f"Archivo: {result.output_path} ({bytes_to_mb_str(result.output_bytes)})")


# --------------------------------------------------------------------------- #
# Subcomando: audit (headless)
# --------------------------------------------------------------------------- #
def cmd_audit(args: argparse.Namespace) -> int:
    """Audita una contraseña contra una wordlist y analiza su fortaleza."""
    file_path = args.wordlist
    password = args.password
    if not os.path.exists(file_path):
        err_console.error(f"No se encontró el archivo: {file_path}")
        return 1

    err_console.info(f"Buscando la contraseña en '{file_path}'...")
    found = False
    line_number = 0
    try:
        open_func = gzip.open if file_path.endswith(".gz") else open
        with open_func(file_path, "rt", encoding="utf-8", errors="ignore") as f:
            for idx, line in enumerate(f, 1):
                if line.strip() == password:
                    found, line_number = True, idx
                    break
    except OSError as exc:
        err_console.error(f"Error al leer el archivo: {exc}")
        return 1

    console.rule("Resultado de auditoría")
    if found:
        console.error(f"ALERTA: la contraseña FUE ENCONTRADA (línea {line_number:,}). Cámbiala ya.")
    else:
        console.ok("La contraseña NO fue encontrada en esta wordlist.")

    analysis = validate_strength(password)
    console.print(
        f"Score: {analysis['score']}/100 - {analysis['strength']} "
        f"| Entropía: {analysis['entropy']:.1f} bits"
    )
    if analysis["issues"]:
        console.warn("Problemas detectados:")
        for issue in analysis["issues"]:
            console.print(f"  - {issue}")
    return 0


# --------------------------------------------------------------------------- #
# Subcomando: merge (headless)
# --------------------------------------------------------------------------- #
def cmd_merge(args: argparse.Namespace) -> int:
    """Une varias wordlists en una sola, deduplicando."""
    file_paths = [p.strip() for p in args.input_files.split(",") if p.strip()]
    unique: set[str] = set()
    total_read = 0

    err_console.info("Procesando archivos...")
    for path in file_paths:
        if not os.path.exists(path):
            err_console.warn(f"'{path}' no existe, se omite.")
            continue
        try:
            open_func = gzip.open if path.endswith(".gz") else open
            with open_func(path, "rt", encoding="utf-8", errors="ignore") as f:
                lines = [ln.strip() for ln in f if ln.strip()]
                unique.update(lines)
                total_read += len(lines)
                err_console.ok(f"'{path}': {len(lines):,} líneas.")
        except OSError as exc:
            err_console.error(f"No se pudo leer '{path}': {exc}")

    err_console.ok(f"Líneas leídas: {total_read:,} | Únicas: {len(unique):,}")
    if not unique:
        err_console.warn("No hay contraseñas para guardar.")
        return 0

    compress = args.output.endswith(".gz")
    open_out = gzip.open if compress else open
    with open_out(args.output, "wt", encoding="utf-8", errors="replace") as out:
        for p in sorted(unique):
            out.write(p + "\n")
    err_console.ok(f"Lista unificada guardada en {args.output}")
    return 0


# --------------------------------------------------------------------------- #
# Subcomando: init-profile
# --------------------------------------------------------------------------- #
def cmd_init_profile(args: argparse.Namespace) -> int:
    """Escribe un perfil de ejemplo para el modo headless."""
    path = args.path or "perfil.yaml"
    if os.path.exists(path) and not args.force:
        err_console.error(f"'{path}' ya existe. Usa --force para sobrescribir.")
        return 1
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(EXAMPLE_PROFILE_YAML)
    console.ok(f"Perfil de ejemplo escrito en: {path}")
    console.info(f"Edítalo y luego: cerbero generate --config {path} --output wl.txt")
    return 0


# --------------------------------------------------------------------------- #
# Modo interactivo
# --------------------------------------------------------------------------- #
def run_interactive() -> int:
    """Menú interactivo clásico."""
    print_presentation()
    try:
        while True:
            console.rule("Menú principal")
            console.print("  1. Modo Completo (Wordlist Avanzada)")
            console.print("  2. Modo Numérico (PINs / Códigos)")
            console.print("  3. Modo Nombres de Usuario (Userlist)")
            console.print("  4. Modo Auditoría (Buscar contraseña + análisis)")
            console.print("  5. Modo Unir Wordlists")
            console.print("  6. Salir")
            choice = safe_input("Opción: ")

            if choice == "1":
                run_full_mode_interactive()
            elif choice == "2":
                run_numeric_mode_interactive()
            elif choice == "3":
                run_username_mode_interactive()
            elif choice == "4":
                run_audit_mode_interactive()
            elif choice == "5":
                run_merge_mode_interactive()
            elif choice == "6":
                console.info("Saliendo de Cerbero. ¡Hasta la próxima!")
                return 0
            else:
                console.warn("Opción no válida.")

            if choice in ["1", "2", "3", "4", "5"]:
                _ = safe_input("\nPresiona Enter para volver al menú...")
    except KeyboardInterrupt:
        console.info("\nSalida solicitada por el usuario. ¡Gracias por usar Cerbero!")
        return 0


# --------------------------------------------------------------------------- #
# Parser
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cerbero",
        description=f"Cerbero v{__version__} - Suite de perfilado de credenciales.",
        epilog="Uso ético exclusivamente: pentesting autorizado y auditorías propias.",
    )
    parser.add_argument("--version", action="version", version=f"cerbero {__version__}")
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="Aumenta el detalle de logging (-v info, -vv debug).")

    sub = parser.add_subparsers(dest="command")

    # generate
    g = sub.add_parser("generate", help="Generar wordlist desde un perfil (headless).")
    g.add_argument("--config", required=True, help="Perfil de objetivo (.yaml/.json).")
    g.add_argument("--engines", default="all", help="Motores: 'all' o '1,3,8'.")
    g.add_argument("--output", help="Archivo de salida (.gz para comprimir).")
    g.add_argument("--min-len", type=int, default=DEFAULT_MIN_LEN)
    g.add_argument("--max-len", type=int, default=DEFAULT_MAX_LEN)
    g.add_argument("--limit", type=int, default=DEFAULT_OUTPUT_LIMIT,
                   help="Tope global de contraseñas (0 = sin tope).")
    g.add_argument("--stdout", action="store_true",
                   help="Emitir a stdout (para pipe a hashcat/john).")
    g.add_argument("--no-dedup", action="store_true", help="Desactivar deduplicación.")
    g.add_argument("--dry-run", action="store_true", help="Estimar sin escribir.")
    g.set_defaults(func=cmd_generate)

    # audit
    a = sub.add_parser("audit", help="Auditar una contraseña contra una wordlist.")
    a.add_argument("--wordlist", required=True, help="Ruta de la wordlist.")
    a.add_argument("--password", required=True, help="Contraseña a verificar.")
    a.set_defaults(func=cmd_audit)

    # merge
    m = sub.add_parser("merge", help="Unir y deduplicar varias wordlists.")
    m.add_argument("--input-files", required=True, help="Rutas separadas por comas.")
    m.add_argument("--output", required=True, help="Archivo de salida (.gz para comprimir).")
    m.set_defaults(func=cmd_merge)

    # init-profile
    ip = sub.add_parser("init-profile", help="Escribir un perfil de ejemplo.")
    ip.add_argument("path", nargs="?", help="Ruta destino (default: perfil.yaml).")
    ip.add_argument("--force", action="store_true", help="Sobrescribir si existe.")
    ip.set_defaults(func=cmd_init_profile)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    setup_logging(getattr(args, "verbose", 0))

    if not args.command:
        return run_interactive()
    return int(args.func(args) or 0)


if __name__ == "__main__":
    sys.exit(main())
