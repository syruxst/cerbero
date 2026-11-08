"""Tests del pipeline de generación."""
from __future__ import annotations

import os
import tempfile
import unittest

from cerbero.core.pipeline import GenerationResult, resolve_engines, run_generation
from cerbero.core.profile import build_info

SAMPLE = build_info(
    {
        "persona_principal": {
            "nombres": ["Juan"],
            "apellidos": ["Perez"],
            "fecha_nacimiento": "1990-05-12",
            "sobrenombre": "Juancho",
        },
        "pareja": {"nombres": ["Maria"], "fecha_nacimiento": "1988-03-02"},
        "hijos": [{"nombres": ["Benja"], "fecha_nacimiento": "2012-09-01"}],
        "otros": {"frases": ["Red Segura"], "mangle_phrases": ["Red Segura"]},
    }
)


class TestResolveEngines(unittest.TestCase):
    def test_all(self):
        self.assertEqual(len(resolve_engines("all")), 14)
        self.assertEqual(len(resolve_engines(None)), 14)

    def test_subset_string_and_list(self):
        self.assertEqual(resolve_engines("1,3,10"), ["1", "3", "10"])
        self.assertEqual(resolve_engines([1, 3]), ["1", "3"])

    def test_unknown_ignored(self):
        self.assertEqual(resolve_engines("1,99,abc"), ["1"])


class TestRunGeneration(unittest.TestCase):
    def _tmp(self) -> str:
        fd, path = tempfile.mkstemp(suffix=".txt")
        os.close(fd)
        return path

    def test_writes_file(self):
        path = self._tmp()
        try:
            res = run_generation(
                SAMPLE, engines="1,3", min_len=6, max_len=16, limit=1000, output_path=path
            )
            self.assertIsInstance(res, GenerationResult)
            self.assertGreater(res.total_written, 0)
            with open(path, encoding="utf-8") as fh:
                lines = [ln.strip() for ln in fh if ln.strip()]
            self.assertEqual(len(lines), res.total_written)
            # Longitudes respetadas.
            self.assertTrue(all(6 <= len(line) <= 16 for line in lines))
        finally:
            os.unlink(path)

    def test_global_limit_respected(self):
        path = self._tmp()
        try:
            res = run_generation(
                SAMPLE, engines="all", min_len=1, max_len=40, limit=50, output_path=path
            )
            self.assertLessEqual(res.total_written, 50)
        finally:
            os.unlink(path)

    def test_dedup_no_duplicates(self):
        path = self._tmp()
        try:
            run_generation(
                SAMPLE, engines="all", min_len=1, max_len=40, limit=5000, output_path=path
            )
            with open(path, encoding="utf-8") as fh:
                lines = [ln.strip() for ln in fh if ln.strip()]
            self.assertEqual(len(lines), len(set(lines)))
        finally:
            os.unlink(path)

    def test_dry_run_writes_nothing(self):
        res = run_generation(SAMPLE, engines="1", min_len=1, max_len=40, dry_run=True)
        self.assertTrue(res.dry_run)
        self.assertIsNone(res.output_path)
        self.assertGreater(res.total_written, 0)  # estimación por muestreo

    def test_no_valid_engine_raises(self):
        with self.assertRaises(ValueError):
            run_generation(SAMPLE, engines="99", min_len=1, max_len=40, dry_run=True)


if __name__ == "__main__":
    unittest.main()
