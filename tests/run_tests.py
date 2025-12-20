#!/usr/bin/env python3
# coding: utf-8
"""
Cerbero v7.0 - Ejecutor de Tests
Script para ejecutar todos los tests unitarios
"""

import unittest
import sys
import os

# Añadir el directorio padre al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Descubrir y ejecutar todos los tests
if __name__ == '__main__':
    # Descubrir tests en el directorio actual
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')

    # Ejecutar tests con verbosidad
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Salir con código de error si hubo fallos
    sys.exit(not result.wasSuccessful())
