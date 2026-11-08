"""Tests del cargador de perfiles headless."""
from __future__ import annotations

import json
import os
import tempfile
import unittest
from datetime import datetime

from cerbero.core.profile import (
    EXAMPLE_PROFILE_YAML,
    ProfileError,
    build_info,
    load_profile,
    parse_date,
)


class TestParseDate(unittest.TestCase):
    def test_formats(self):
        self.assertEqual(parse_date("12/07/1985"), datetime(1985, 7, 12))
        self.assertEqual(parse_date("1985-07-12"), datetime(1985, 7, 12))

    def test_none_and_empty(self):
        self.assertIsNone(parse_date(None))
        self.assertIsNone(parse_date(""))

    def test_invalid(self):
        with self.assertRaises(ProfileError):
            parse_date("no-es-fecha")


class TestBuildInfo(unittest.TestCase):
    def test_minimal(self):
        info = build_info({"persona_principal": {"nombres": ["José"], "apellidos": ["Núñez"]}})
        # Normalización de acentos aplicada.
        self.assertEqual(info["persona_principal"]["nombres"], ["Jose"])
        self.assertEqual(info["persona_principal"]["apellidos"], ["Nunez"])
        self.assertIn("familia", info)
        self.assertIn("otros_datos", info)

    def test_full_structure(self):
        info = build_info(
            {
                "persona_principal": {
                    "nombres": ["Juan"],
                    "fecha_nacimiento": "1990-01-02",
                    "sobrenombre": "Juancho",
                },
                "pareja": {"nombres": ["Maria"]},
                "hijos": [{"nombres": ["Benja"], "fecha_nacimiento": "2012-09-01"}],
                "otros": {"frases": ["Red Segura"], "numeros_importantes": ["1234"]},
            }
        )
        self.assertEqual(info["persona_principal"]["fecha_nacimiento"], datetime(1990, 1, 2))
        self.assertEqual(len(info["familia"]["hijos"]), 1)
        self.assertEqual(info["otros_datos"]["numeros_importantes"], ["1234"])

    def test_empty_profile_raises(self):
        with self.assertRaises(ProfileError):
            build_info({})

    def test_bad_hijos_type(self):
        with self.assertRaises(ProfileError):
            build_info({"persona_principal": {"nombres": ["X"]}, "hijos": "no-lista"})


class TestLoadProfile(unittest.TestCase):
    def test_load_json(self):
        data = {"persona_principal": {"nombres": ["Ana"], "apellidos": ["Soto"]}}
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh:
            json.dump(data, fh)
            path = fh.name
        try:
            info = load_profile(path)
            self.assertEqual(info["persona_principal"]["nombres"], ["Ana"])
        finally:
            os.unlink(path)

    def test_example_yaml_is_loadable(self):
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8") as fh:
            fh.write(EXAMPLE_PROFILE_YAML)
            path = fh.name
        try:
            info = load_profile(path)
            self.assertTrue(info["persona_principal"]["nombres"])
        finally:
            os.unlink(path)

    def test_missing_file(self):
        with self.assertRaises(ProfileError):
            load_profile("/ruta/que/no/existe.yaml")


if __name__ == "__main__":
    unittest.main()
