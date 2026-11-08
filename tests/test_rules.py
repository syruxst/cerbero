"""Tests del motor de reglas estilo Hashcat (Motor 13)."""
from __future__ import annotations

import os
import tempfile
import unittest

from cerbero.engines import ENGINE_STREAMS
from cerbero.engines.rules import (
    DEFAULT_RULES,
    apply_rule,
    apply_rules,
    load_rules_file,
)


class TestApplyRule(unittest.TestCase):
    def test_passthrough(self):
        self.assertEqual(apply_rule("maria", ":"), "maria")

    def test_case_functions(self):
        self.assertEqual(apply_rule("maria", "u"), "MARIA")
        self.assertEqual(apply_rule("MARIA", "l"), "maria")
        self.assertEqual(apply_rule("maria", "c"), "Maria")
        self.assertEqual(apply_rule("MaRiA", "t"), "mArIa")

    def test_reverse_duplicate_reflect(self):
        self.assertEqual(apply_rule("abc", "r"), "cba")
        self.assertEqual(apply_rule("ab", "d"), "abab")
        self.assertEqual(apply_rule("ab", "f"), "abba")

    def test_append_prepend(self):
        self.assertEqual(apply_rule("maria", "$1"), "maria1")
        self.assertEqual(apply_rule("maria", "^!"), "!maria")
        self.assertEqual(apply_rule("maria", "$2$0$2$4"), "maria2024")

    def test_rotate_and_delete(self):
        self.assertEqual(apply_rule("abc", "{"), "bca")
        self.assertEqual(apply_rule("abc", "}"), "cab")
        self.assertEqual(apply_rule("abc", "["), "bc")
        self.assertEqual(apply_rule("abc", "]"), "ab")

    def test_substitute_leet(self):
        self.assertEqual(apply_rule("maria", "sa@"), "m@ri@")
        self.assertEqual(apply_rule("maria", "sa@si1"), "m@r1@")

    def test_toggle_position(self):
        self.assertEqual(apply_rule("maria", "T0"), "Maria")

    def test_combined_rule(self):
        # Capitaliza y añade 2024.
        self.assertEqual(apply_rule("maria", "c$2$0$2$4"), "Maria2024")

    def test_unknown_function_ignored(self):
        # 'z' no está soportada: se ignora, el resto se aplica.
        self.assertEqual(apply_rule("maria", "zu"), "MARIA")

    def test_empty_result_is_none(self):
        self.assertIsNone(apply_rule("a", "]"))

    def test_incomplete_rule_is_none(self):
        self.assertIsNone(apply_rule("maria", "$"))


class TestApplyRules(unittest.TestCase):
    def test_yields_non_empty(self):
        out = list(apply_rules("maria", [":", "u", "$1"]))
        self.assertEqual(out, ["maria", "MARIA", "maria1"])

    def test_default_rules_produce_many(self):
        out = list(apply_rules("maria", DEFAULT_RULES))
        self.assertGreater(len(out), 10)
        self.assertIn("Maria2024", out)


class TestLoadRulesFile(unittest.TestCase):
    def test_loads_and_skips_comments(self):
        with tempfile.NamedTemporaryFile("w", suffix=".rule", delete=False, encoding="utf-8") as fh:
            fh.write("# comentario\n\nu\n$1\n")
            path = fh.name
        try:
            rules = load_rules_file(path)
            self.assertEqual(rules, ["u", "$1"])
        finally:
            os.unlink(path)


class TestEngine13(unittest.TestCase):
    def test_registered_and_generates(self):
        self.assertIn("13", ENGINE_STREAMS)
        info = {"otros_datos": {}}
        gen = ENGINE_STREAMS["13"](info, ["maria", "juan"], [], [])
        out = list(gen)
        self.assertGreater(len(out), 0)
        self.assertIn("Maria2024", out)

    def test_uses_custom_rules_from_info(self):
        info = {"otros_datos": {"rules": ["u"]}}
        out = list(ENGINE_STREAMS["13"](info, ["maria"], [], []))
        self.assertEqual(out, ["MARIA"])

    def test_empty_words(self):
        self.assertEqual(list(ENGINE_STREAMS["13"]({"otros_datos": {}}, [], [], [])), [])

    def test_rules_do_not_leak_into_base_words(self):
        """Regresión: las reglas en info no deben extraerse como palabras base."""
        from cerbero.ioutils import generate_base_words, generate_numeric_words

        info = {
            "persona_principal": {"nombres": ["maria"], "apellidos": [], "sobrenombre": ""},
            "familia": {"pareja": {}, "hijos": []},
            "otros_datos": {"frases": [], "rules": ["c$2$0$2$5", "sa@se3", "r"]},
        }
        base = generate_base_words(info)
        nums = generate_numeric_words(info)
        self.assertNotIn("c$2$0$2$5", base)
        self.assertTrue(all("$" not in w for w in base))
        self.assertTrue(all("$" not in n for n in nums))


if __name__ == "__main__":
    unittest.main()
