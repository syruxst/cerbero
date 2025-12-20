# coding: utf-8
"""
Cerbero v7.0 - Módulo de Salida
Funciones para escritura streaming de contraseñas
"""

from __future__ import annotations
import gzip
import time
from typing import Iterable, Callable, Optional, Set, Tuple
from .progress import ProgressBar


def open_output_file(path: str, compress: bool) -> Tuple[object, Callable[[str], None], Callable[[], None]]:
    """
    Abre archivo para escritura y devuelve funciones de write y close.

    Args:
        path: Ruta del archivo de salida
        compress: Si True, crea archivo .gz comprimido

    Returns:
        Tupla (file_handle, write_func, close_func)
    """
    if compress:
        gz = gzip.open(path, 'at', encoding='utf-8', errors='replace')

        def w(line: str):
            gz.write(line + '\n')

        def c():
            gz.close()

        return gz, w, c
    else:
        f = open(path, 'a', encoding='utf-8', errors='replace')

        def w(line: str):
            f.write(line + '\n')

        def c():
            f.close()

        return f, w, c


def stream_generate_and_write(generator: Iterable[str],
                              output_writer: Callable[[str], None],
                              min_len: int,
                              max_len: int,
                              limit: Optional[int] = None,
                              seen_filter: Optional[Set[str]] = None,
                              stats: Optional[dict] = None,
                              show_progress: bool = False,
                              progress_desc: str = "Generando") -> int:
    """
    Consume generador y escribe líneas válidas (entre min/max) al writer.

    Args:
        generator: Generador de contraseñas
        output_writer: Función para escribir cada línea
        min_len: Longitud mínima de contraseñas
        max_len: Longitud máxima de contraseñas
        limit: Límite máximo de contraseñas a escribir (None = sin límite)
        seen_filter: Conjunto para evitar duplicados (mejor si es BloomDeduplicator)
        stats: Diccionario donde acumular estadísticas
        show_progress: Si True, muestra barra de progreso
        progress_desc: Descripción para la barra de progreso

    Returns:
        Número de contraseñas escritas
    """
    written = 0
    t0 = time.time()

    # Inicializar barra de progreso si se solicita
    pbar = None
    if show_progress and limit:
        pbar = ProgressBar(limit, progress_desc)

    for pwd in generator:
        if not pwd:
            continue

        lp = len(pwd)
        if lp < min_len or lp > max_len:
            continue

        # Deduplicación
        if seen_filter is not None:
            # Soporta tanto set() como BloomDeduplicator (ambos con __contains__)
            if hasattr(seen_filter, 'add'):
                # BloomDeduplicator tiene método add() que retorna bool
                if callable(getattr(seen_filter, 'add')):
                    is_new = seen_filter.add(pwd)
                    if not is_new:
                        continue
                else:
                    # Set tradicional
                    if pwd in seen_filter:
                        continue
                    seen_filter.add(pwd)
            else:
                if pwd in seen_filter:
                    continue
                seen_filter.add(pwd)

        output_writer(pwd)
        written += 1

        # Actualizar progreso
        if pbar:
            pbar.update(1)

        # Estadísticas
        if stats is not None:
            stats['written'] = stats.get('written', 0) + 1

        # Límite de escritura
        if limit and written >= limit:
            break

    # Cerrar barra de progreso
    if pbar:
        pbar.close()

    if stats is not None:
        stats['time'] = time.time() - t0

    return written
