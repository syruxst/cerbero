# coding: utf-8
"""
Cerbero v7.0 - Módulo de Deduplicación
Implementación de Bloom Filter para deduplicación escalable
"""

from __future__ import annotations
from typing import Optional


# Intentar importar pybloom-live, con fallback a set()
try:
    from pybloom_live import ScalableBloomFilter
    BLOOM_AVAILABLE = True
except ImportError:
    BLOOM_AVAILABLE = False


class BloomDeduplicator:
    """
    Deduplicador escalable usando Bloom Filter.

    Usa pybloom-live si está disponible, fallback a set() si no.
    Soporta millones de contraseñas con memoria constante.
    """

    def __init__(self, capacity: int = 10_000_000, error_rate: float = 0.001):
        """
        Inicializa el deduplicador.

        Args:
            capacity: Capacidad inicial estimada (para Bloom Filter)
            error_rate: Tasa de falsos positivos aceptable (default: 0.1%)
        """
        self.seen_count = 0
        self.using_bloom = BLOOM_AVAILABLE

        if BLOOM_AVAILABLE:
            # Usar Bloom Filter escalable
            self.bloom = ScalableBloomFilter(
                mode=ScalableBloomFilter.SMALL_SET_GROWTH,
                initial_capacity=capacity,
                error_rate=error_rate
            )
            self.fallback_set = None
        else:
            # Fallback a set tradicional
            self.bloom = None
            self.fallback_set = set()
            print("[AVISO] pybloom-live no disponible. Usando set() (menor escalabilidad).")
            print("        Instala con: pip install pybloom-live")

    def add(self, password: str) -> bool:
        """
        Añade una contraseña al deduplicador.

        Args:
            password: Contraseña a añadir

        Returns:
            True si es nueva, False si es duplicada
        """
        if self.using_bloom:
            # Usar Bloom Filter
            if password in self.bloom:
                return False  # Ya existe (o falso positivo ~0.1%)
            self.bloom.add(password)
            self.seen_count += 1
            return True
        else:
            # Usar set tradicional
            if password in self.fallback_set:
                return False
            self.fallback_set.add(password)
            self.seen_count += 1
            return True

    def __len__(self) -> int:
        """Retorna el número de elementos añadidos"""
        return self.seen_count

    def __contains__(self, password: str) -> bool:
        """Verifica si una contraseña está en el deduplicador"""
        if self.using_bloom:
            return password in self.bloom
        else:
            return password in self.fallback_set


def create_deduplicator(capacity: int = 10_000_000,
                       error_rate: float = 0.001) -> BloomDeduplicator:
    """
    Factory function para crear un deduplicador.

    Args:
        capacity: Capacidad inicial estimada
        error_rate: Tasa de falsos positivos

    Returns:
        Instancia de BloomDeduplicator configurada
    """
    return BloomDeduplicator(capacity=capacity, error_rate=error_rate)
