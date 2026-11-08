"""Tests de la CLI (parser y subcomandos headless)."""
from __future__ import annotations

import os
import tempfile
import unittest

from cerbero.cli import build_parser, main
from cerbero.core.profile import EXAMPLE_PROFILE_YAML


class TestParser(unittest.TestCase):
    def test_subcommands_exist(self):
        parser = build_parser()
        args = parser.parse_args(["generate", "--config", "p.yaml", "--output", "o.txt"])
        self.assertEqual(args.command, "generate")
        self.assertEqual(args.engines, "all")

    def test_no_command_defaults_none(self):
        args = build_parser().parse_args([])
        self.assertIsNone(args.command)


class TestHeadlessGenerate(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.profile = os.path.join(self.tmpdir, "perfil.yaml")
        with open(self.profile, "w", encoding="utf-8") as fh:
            fh.write(EXAMPLE_PROFILE_YAML)

    def tearDown(self):
        for f in os.listdir(self.tmpdir):
            os.unlink(os.path.join(self.tmpdir, f))
        os.rmdir(self.tmpdir)

    def test_generate_creates_output(self):
        out = os.path.join(self.tmpdir, "wl.txt")
        rc = main(
            ["generate", "--config", self.profile, "--engines", "1,3",
             "--limit", "500", "--output", out]
        )
        self.assertEqual(rc, 0)
        self.assertTrue(os.path.exists(out))
        self.assertGreater(os.path.getsize(out), 0)

    def test_generate_missing_output_errors(self):
        rc = main(["generate", "--config", self.profile, "--engines", "1"])
        self.assertEqual(rc, 2)

    def test_generate_bad_profile_errors(self):
        rc = main(["generate", "--config", "/no/existe.yaml", "--output", "x.txt"])
        self.assertEqual(rc, 2)

    def test_init_profile(self):
        dest = os.path.join(self.tmpdir, "nuevo.yaml")
        rc = main(["init-profile", dest])
        self.assertEqual(rc, 0)
        self.assertTrue(os.path.exists(dest))


if __name__ == "__main__":
    unittest.main()
