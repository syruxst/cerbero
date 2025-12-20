# coding: utf-8
"""
Cerbero v7.0 - Tests Unitarios del Módulo Core
Tests básicos para funciones principales
"""

import unittest
from core import (
    full_leetspeak,
    apply_variations,
    apply_mangling_rules,
    generate_usernames,
    normalize_string,
    estimate_entropy_bits,
    validate_strength
)


class TestGenerators(unittest.TestCase):
    """Tests para funciones de generación"""

    def test_full_leetspeak(self):
        """Test de conversión leetspeak completa"""
        result = full_leetspeak("hacker")
        # 'a' -> '4', 'e' -> '3'
        self.assertIn('4', result)  # 'a' -> '4'
        self.assertIn('3', result)  # 'e' -> '3'

    def test_apply_variations(self):
        """Test de variaciones de palabras"""
        variations = apply_variations("maria")
        # Debería retornar tupla con variaciones
        self.assertIsInstance(variations, tuple)
        self.assertGreater(len(variations), 0)
        self.assertIn("Maria", variations)  # Capitalize
        self.assertIn("MARIA", variations)  # Upper

    def test_apply_mangling_rules(self):
        """Test de reglas de mangling"""
        mangled = apply_mangling_rules("hola")
        self.assertIsInstance(mangled, list)
        self.assertGreater(len(mangled), 0)

    def test_generate_usernames(self):
        """Test de generación de usernames"""
        info = {
            'nombres': ['Juan'],
            'apellidos': ['Perez'],
            'sobrenombre': 'Juancho',
            'birth_year': '1990'
        }
        usernames = generate_usernames(info)
        self.assertIsInstance(usernames, list)
        self.assertGreater(len(usernames), 0)
        # Verificar que algunos patrones estén presentes
        self.assertIn('Juan', usernames)
        self.assertIn('Perez', usernames)

    def test_generate_usernames_missing_data(self):
        """Test de generación de usernames con datos faltantes"""
        info = {
            'nombres': [],
            'apellidos': [],
            'sobrenombre': '',
            'birth_year': ''
        }
        usernames = generate_usernames(info)
        # Debería retornar lista vacía si faltan datos críticos
        self.assertEqual(usernames, [])


class TestUtils(unittest.TestCase):
    """Tests para funciones de utilidades"""

    def test_normalize_string(self):
        """Test de normalización Unicode"""
        result = normalize_string("José Núñez")
        # normalize_string elimina acentos pero NO convierte a minúsculas
        self.assertEqual(result, "Jose Nunez")

        result = normalize_string("Ángel")
        self.assertEqual(result, "Angel")

    def test_estimate_entropy_bits(self):
        """Test de cálculo de entropía"""
        entropy = estimate_entropy_bits("password")
        self.assertIsInstance(entropy, float)
        self.assertGreater(entropy, 0)

        # Contraseña más compleja debería tener mayor entropía
        entropy_simple = estimate_entropy_bits("1234")
        entropy_complex = estimate_entropy_bits("P@ssw0rd!123")
        self.assertGreater(entropy_complex, entropy_simple)

    def test_validate_strength(self):
        """Test de validación de fortaleza"""
        # Contraseña débil
        weak = validate_strength("123456")
        self.assertIsInstance(weak, dict)
        self.assertIn('score', weak)
        self.assertIn('strength', weak)
        self.assertLess(weak['score'], 50)

        # Contraseña fuerte
        strong = validate_strength("MyStr0ng!P@ssw0rd2024")
        self.assertGreater(strong['score'], 70)


if __name__ == '__main__':
    unittest.main()
