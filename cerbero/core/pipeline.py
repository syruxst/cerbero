"""
Cerbero - Pipeline de generación.

Núcleo único y reutilizable de generación de wordlists. Tanto el modo
interactivo como el headless llaman aquí, de modo que el límite global,
la deduplicación y las estadísticas se comporten igual en ambos.
"""
from __future__ import annotations

import os
import sys
import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from cerbero.core.config import DEFAULT_SYMBOLS
from cerbero.core.logging_config import get_logger
from cerbero.engines import ENGINE_DESCRIPTIONS, ENGINE_STREAMS
from cerbero.ioutils import (
    generate_base_words,
    generate_numeric_words,
    open_output_file,
    stream_generate_and_write,
)

log = get_logger()


@dataclass
class GenerationResult:
    """Resultado agregado de una corrida de generación."""

    total_written: int = 0
    elapsed: float = 0.0
    by_engine: Dict[str, int] = field(default_factory=dict)
    time_by_engine: Dict[str, float] = field(default_factory=dict)
    output_path: Optional[str] = None
    output_bytes: int = 0
    dry_run: bool = False


def resolve_engines(spec: object) -> List[str]:
    """
    Normaliza una especificación de motores a una lista de IDs válidos.

    Acepta 'all', 'all'/None, 'ALL', una cadena '1,3,8' o una lista.
    """
    available = list(ENGINE_STREAMS.keys())
    all_aliases = {"all", "todos", "*", ""}
    if spec is None:
        return available
    if isinstance(spec, str):
        tokens = [t.strip().lower() for t in spec.split(",")]
    elif isinstance(spec, (list, tuple)):
        tokens = [str(t).strip().lower() for t in spec]
    else:
        raise ValueError(f"Especificación de motores no válida: {spec!r}")

    # 'all' (u otros alias) en cualquier posición selecciona todos los motores,
    # tanto si viene como cadena ("all") como dentro de una lista (["all"]).
    if any(t in all_aliases for t in tokens):
        return available

    selected = [t for t in tokens if t in ENGINE_STREAMS]
    unknown = [t for t in tokens if t and t not in ENGINE_STREAMS]
    if unknown:
        log.warning("Motores ignorados (no existen): %s", ", ".join(unknown))
    return selected


def _make_deduplicator(dedup: bool):
    """Devuelve un deduplicador (Bloom si está, set si no) o None."""
    if not dedup:
        return None
    try:
        from cerbero.optimizations.dedup import create_deduplicator

        return create_deduplicator()
    except Exception:  # pragma: no cover
        return set()


def run_generation(
    info: dict,
    *,
    engines: object = None,
    min_len: int,
    max_len: int,
    limit: Optional[int] = None,
    output_path: Optional[str] = None,
    compress: Optional[bool] = None,
    dry_run: bool = False,
    dedup: bool = True,
    to_stdout: bool = False,
    on_engine_start=None,
    on_engine_done=None,
) -> GenerationResult:
    """
    Ejecuta los motores seleccionados y escribe el resultado.

    Args:
        info: Diccionario de datos del objetivo.
        engines: 'all', '1,3,8' o lista de IDs (None = todos).
        min_len / max_len: filtro de longitud.
        limit: tope GLOBAL de contraseñas escritas (None = sin tope).
        output_path: archivo de salida (ignorado si to_stdout o dry_run).
        compress: forzar gzip; si None se infiere por extensión .gz.
        dry_run: no escribe, solo estima (muestra hasta 100k por motor).
        dedup: deduplicar salida (Bloom filter si está disponible).
        to_stdout: escribir las contraseñas a stdout (para pipe a hashcat/john).
        on_engine_start / on_engine_done: callbacks opcionales de progreso.

    Returns:
        GenerationResult con totales y estadísticas por motor.
    """
    selected = resolve_engines(engines)
    if not selected:
        raise ValueError("No se seleccionó ningún motor válido.")

    text_words = generate_base_words(info)
    numeric_words = generate_numeric_words(info)
    symbols = DEFAULT_SYMBOLS

    result = GenerationResult(output_path=None if (dry_run or to_stdout) else output_path,
                              dry_run=dry_run)

    # Preparar el escritor de salida.
    writer: Optional[Callable[[str], None]] = None
    closer: Optional[Callable[[], None]] = None
    if dry_run:
        pass
    elif to_stdout:
        def _stdout_writer(line: str) -> None:
            sys.stdout.write(line + "\n")

        def _stdout_closer() -> None:
            sys.stdout.flush()

        writer, closer = _stdout_writer, _stdout_closer
    else:
        if not output_path:
            raise ValueError("Se requiere output_path cuando no es dry_run ni to_stdout.")
        if compress is None:
            compress = output_path.endswith(".gz")
        _fh, writer, closer = open_output_file(output_path, compress)

    seen = _make_deduplicator(dedup)
    start_all = time.time()

    try:
        for engine_id in selected:
            func = ENGINE_STREAMS.get(engine_id)
            if not func:
                continue
            desc = ENGINE_DESCRIPTIONS.get(engine_id, "")
            if on_engine_start:
                on_engine_start(engine_id, desc)

            t0 = time.time()
            gen: Iterable[str] = func(info, text_words, numeric_words, symbols)

            if dry_run:
                written = 0
                for i, pwd in enumerate(gen):
                    if i >= 100_000:  # muestreo para estimación
                        break
                    if pwd and min_len <= len(pwd) <= max_len:
                        written += 1
            else:
                remaining = (limit - result.total_written) if limit else None
                if remaining is not None and remaining <= 0:
                    break
                assert writer is not None  # garantizado cuando no es dry_run
                written = stream_generate_and_write(
                    gen, writer, min_len, max_len, remaining, seen
                )

            dt = time.time() - t0
            result.by_engine[engine_id] = written
            result.time_by_engine[engine_id] = dt
            result.total_written += written
            if on_engine_done:
                on_engine_done(engine_id, written, dt)

            if limit and result.total_written >= limit and not dry_run:
                break
    finally:
        if closer is not None:
            closer()

    result.elapsed = time.time() - start_all
    if result.output_path and os.path.exists(result.output_path):
        result.output_bytes = os.path.getsize(result.output_path)
    return result
