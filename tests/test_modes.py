# coding: utf-8
"""
Cerbero v7.0 - Tests Unitarios de Modos
Validación de importación y estructura de modos
"""

import unittest
from modes import (
    run_full_mode_interactive,
    run_numeric_mode_interactive,
    run_username_mode_interactive,
    run_merge_mode_interactive,
    run_audit_mode_interactive
)


class TestModes(unittest.TestCase):
    """Tests para validar que los modos existen y son importables"""

    def test_full_mode_exists(self):
        """Verificar que el modo full existe"""
        self.assertTrue(callable(run_full_mode_interactive))

    def test_numeric_mode_exists(self):
        """Verificar que el modo numeric existe"""
        self.assertTrue(callable(run_numeric_mode_interactive))

    def test_username_mode_exists(self):
        """Verificar que el modo username existe"""
        self.assertTrue(callable(run_username_mode_interactive))

    def test_merge_mode_exists(self):
        """Verificar que el modo merge existe"""
        self.assertTrue(callable(run_merge_mode_interactive))

    def test_audit_mode_exists(self):
        """Verificar que el modo audit existe"""
        self.assertTrue(callable(run_audit_mode_interactive))

    def test_all_modes_have_docstrings(self):
        """Verificar que todos los modos tienen documentación"""
        modes = [
            run_full_mode_interactive,
            run_numeric_mode_interactive,
            run_username_mode_interactive,
            run_merge_mode_interactive,
            run_audit_mode_interactive
        ]

        for mode in modes:
            self.assertIsNotNone(mode.__doc__)
            self.assertGreater(len(mode.__doc__.strip()), 0)


if __name__ == '__main__':
    unittest.main()
