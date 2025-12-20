# coding: utf-8
"""
Cerbero v7.0 - Tests Unitarios de Motores
Validación básica de que todos los motores funcionan
"""

import unittest
from engines import ENGINE_STREAMS, ENGINE_DESCRIPTIONS


class TestEngines(unittest.TestCase):
    """Tests para validar motores de generación"""

    def setUp(self):
        """Configuración de datos de prueba"""
        self.test_info = {
            'persona_principal': {
                'nombres': ['Juan'],
                'apellidos': ['Perez'],
                'sobrenombre': 'Juancho'
            },
            'familia': {
                'pareja': {'nombres': ['Maria'], 'apellidos': ['Lopez']},
                'hijos': []
            },
            'otros_datos': {
                'mascota': 'Firulais',
                'frases': ['Red Segura'],
                'numeros_importantes': ['123'],
                'mangle_phrases': ['Mi Casa']
            }
        }
        self.test_text_words = ['juan', 'perez', 'maria', 'lopez']
        self.test_numeric_words = ['1990', '1995', '2024']
        self.test_symbols = ['!', '#', '$', '@', '*']

    def test_all_engines_registered(self):
        """Verificar que todos los 12 motores estén registrados"""
        expected_engines = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        for engine_id in expected_engines:
            self.assertIn(engine_id, ENGINE_STREAMS)
            self.assertIn(engine_id, ENGINE_DESCRIPTIONS)

    def test_engine_1_simple_combinations(self):
        """Test Motor 1: Combinaciones simples"""
        engine = ENGINE_STREAMS['1']
        gen = engine(self.test_info, self.test_text_words, self.test_numeric_words, self.test_symbols)

        # Tomar primeras 10 contraseñas
        passwords = [pwd for _, pwd in zip(range(10), gen)]

        self.assertGreater(len(passwords), 0)
        # Verificar que genera algo
        self.assertTrue(all(isinstance(pwd, str) for pwd in passwords))

    def test_engine_2_complex_patterns(self):
        """Test Motor 2: Patrones complejos"""
        engine = ENGINE_STREAMS['2']
        gen = engine(self.test_info, self.test_text_words, self.test_numeric_words, self.test_symbols)

        passwords = [pwd for _, pwd in zip(range(10), gen)]
        self.assertGreater(len(passwords), 0)

    def test_engine_3_leetspeak(self):
        """Test Motor 3: Leetspeak moderno"""
        engine = ENGINE_STREAMS['3']
        gen = engine(self.test_info, self.test_text_words, self.test_numeric_words, self.test_symbols)

        passwords = [pwd for _, pwd in zip(range(10), gen)]
        self.assertGreater(len(passwords), 0)

    def test_engine_10_pcfg(self):
        """Test Motor 10: PCFG - Verificar que está completo"""
        engine = ENGINE_STREAMS['10']
        gen = engine(self.test_info, self.test_text_words, self.test_numeric_words, self.test_symbols)

        # Generar más contraseñas para asegurar que todas las estructuras funcionan
        passwords = [pwd for _, pwd in zip(range(100), gen)]
        self.assertGreater(len(passwords), 0)

    def test_engine_9_prince(self):
        """Test Motor 9: PRINCE (nuevo en v7.0)"""
        engine = ENGINE_STREAMS['9']
        gen = engine(self.test_info, self.test_text_words, self.test_numeric_words, self.test_symbols)

        passwords = [pwd for _, pwd in zip(range(10), gen)]
        self.assertGreater(len(passwords), 0)

    def test_engine_11_keyboard_walk(self):
        """Test Motor 11: Keyboard Walk (nuevo en v7.0)"""
        engine = ENGINE_STREAMS['11']
        gen = engine(self.test_info, self.test_text_words, self.test_numeric_words, self.test_symbols)

        passwords = [pwd for _, pwd in zip(range(10), gen)]
        self.assertGreater(len(passwords), 0)

    def test_engine_12_ml_patterns(self):
        """Test Motor 12: ML-Patterns (nuevo en v7.0)"""
        engine = ENGINE_STREAMS['12']
        gen = engine(self.test_info, self.test_text_words, self.test_numeric_words, self.test_symbols)

        passwords = [pwd for _, pwd in zip(range(10), gen)]
        self.assertGreater(len(passwords), 0)

    def test_engines_return_generators(self):
        """Verificar que todos los motores retornen generadores"""
        for engine_id, engine_func in ENGINE_STREAMS.items():
            gen = engine_func(self.test_info, self.test_text_words, self.test_numeric_words, self.test_symbols)
            # Verificar que es un generador
            self.assertTrue(hasattr(gen, '__iter__'))
            self.assertTrue(hasattr(gen, '__next__'))


if __name__ == '__main__':
    unittest.main()
