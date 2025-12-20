# coding: utf-8
"""
Cerbero v7.0 - Módulo de Barra de Progreso
Implementación de barra de progreso ASCII sin dependencias externas
"""

import sys
import time


class ProgressBar:
    """
    Barra de progreso ASCII sin dependencias externas.

    Muestra progreso visual con porcentaje, contador, velocidad y ETA.
    """

    def __init__(self, total: int, desc: str = "", bar_length: int = 40):
        """
        Inicializa la barra de progreso.

        Args:
            total: Número total de items a procesar
            desc: Descripción de la tarea
            bar_length: Longitud de la barra en caracteres
        """
        self.total = total
        self.current = 0
        self.desc = desc
        self.bar_length = bar_length
        self.start_time = time.time()

    def update(self, n: int = 1):
        """
        Incrementa el progreso en n unidades y re-renderiza la barra.

        Args:
            n: Número de unidades a incrementar (default: 1)
        """
        self.current += n
        self.render()

    def render(self):
        """Renderiza la barra en stdout (misma línea)"""
        if self.total == 0:
            return

        percent = (self.current / self.total) * 100
        filled = int(self.bar_length * self.current / self.total)
        bar = '█' * filled + '░' * (self.bar_length - filled)

        elapsed = time.time() - self.start_time
        rate = self.current / elapsed if elapsed > 0 else 0
        eta = (self.total - self.current) / rate if rate > 0 else 0

        sys.stdout.write(
            f'\r{self.desc} |{bar}| {percent:.1f}% '
            f'[{self.current:,}/{self.total:,}] '
            f'[{rate:.0f} pwd/s] ETA: {eta:.0f}s'
        )
        sys.stdout.flush()

    def close(self):
        """Finaliza la barra con salto de línea"""
        print()
