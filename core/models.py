# coding: utf-8
"""
Cerbero v7.0 - Módulo de Modelos de Datos
Estructuras de datos y clases para estadísticas
"""

from __future__ import annotations
from dataclasses import dataclass, field
from collections import defaultdict, Counter
from typing import Dict
from .utils import Colors, estimate_entropy_bits


@dataclass
class DetailedStats:
    """
    Estadísticas detalladas de generación de contraseñas.

    Atributos:
        by_engine: Diccionario con conteo por motor
        by_length: Diccionario con conteo por longitud
        by_entropy: Diccionario con conteo por rango de entropía
        total_time: Tiempo total de generación
        total_count: Contador total de contraseñas
    """
    by_engine: Dict[str, int] = field(default_factory=dict)
    by_length: Dict[int, int] = field(default_factory=lambda: defaultdict(int))
    by_entropy: Dict[int, int] = field(default_factory=lambda: defaultdict(int))
    total_time: float = 0.0
    total_count: int = 0

    def analyze_password(self, pwd: str, engine_id: str):
        """
        Analiza una contraseña y actualiza estadísticas.

        Args:
            pwd: Contraseña a analizar
            engine_id: ID del motor que generó la contraseña
        """
        # Por motor
        self.by_engine[engine_id] = self.by_engine.get(engine_id, 0) + 1

        # Por longitud
        self.by_length[len(pwd)] += 1

        # Por entropía (bins de 30 bits)
        entropy = estimate_entropy_bits(pwd)
        bin_range = int(entropy // 30) * 30
        self.by_entropy[bin_range] += 1

        self.total_count += 1

    def report(self):
        """Genera reporte visual de estadísticas en consola"""
        print(f"\n{Colors.CYAN}{'='*70}{Colors.RESET}")
        print(f"{Colors.CYAN}ESTADÍSTICAS DETALLADAS{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*70}{Colors.RESET}\n")

        # Por motor (tabla con barras)
        print(f"{Colors.YELLOW}Distribución por Motor:{Colors.RESET}")
        for engine_id, count in sorted(self.by_engine.items()):
            percent = (count / self.total_count) * 100
            bar = '█' * int(percent / 2)
            print(f"  Motor {engine_id:2s}: {count:>10,} ({percent:>5.1f}%) {bar}")

        # Por longitud (histograma)
        print(f"\n{Colors.YELLOW}Distribución por Longitud:{Colors.RESET}")
        for length in sorted(self.by_length.keys()):
            count = self.by_length[length]
            bar = '█' * min(50, count // max(1, self.total_count // 1000))
            print(f"  {length:2d} chars: {count:>10,} {bar}")

        # Por entropía
        print(f"\n{Colors.YELLOW}Distribución por Entropía:{Colors.RESET}")
        for entropy_range in sorted(self.by_entropy.keys()):
            count = self.by_entropy[entropy_range]
            label = f"{entropy_range}-{entropy_range+30} bits"
            percent = (count / self.total_count) * 100
            print(f"  {label:20s}: {count:>10,} ({percent:>5.1f}%)")

        # Recomendaciones
        if self.by_entropy:
            avg_entropy = sum(k*v for k, v in self.by_entropy.items()) / sum(self.by_entropy.values())
            print(f"\n{Colors.YELLOW}Insights:{Colors.RESET}")
            if avg_entropy < 40:
                print(f"  • Entropía promedio baja ({avg_entropy:.0f} bits). Considera Motor 6 (Mangler)")
            if self.by_entropy.get(60, 0) > self.total_count * 0.3:
                print(f"  • 30%+ de contraseñas con entropía alta (60-90 bits). ¡Excelente diversidad!")
