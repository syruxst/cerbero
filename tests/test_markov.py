"""Tests del modelo de Markov y el Motor 14."""
from __future__ import annotations

import unittest

from cerbero.engines import ENGINE_STREAMS
from cerbero.engines.markov import MarkovModel

WORDS = ["juan", "maria", "perez", "mariana", "juana", "pereira"]


class TestMarkovModel(unittest.TestCase):
    def test_untrained_generates_nothing(self):
        self.assertEqual(MarkovModel().generate(), [])

    def test_generates_tokens(self):
        model = MarkovModel(order=2).train(WORDS)
        out = model.generate(max_results=50, min_len=4, max_len=12)
        self.assertGreater(len(out), 0)
        self.assertTrue(all(4 <= len(w) <= 12 for w in out))
        self.assertTrue(all(w.isalpha() for w in out))

    def test_deterministic(self):
        a = MarkovModel(order=2).train(WORDS).generate(max_results=30)
        b = MarkovModel(order=2).train(WORDS).generate(max_results=30)
        self.assertEqual(a, b)

    def test_unique_results(self):
        out = MarkovModel(order=2).train(WORDS).generate(max_results=100)
        self.assertEqual(len(out), len(set(out)))


class TestEngine14(unittest.TestCase):
    def test_registered_and_generates(self):
        self.assertIn("14", ENGINE_STREAMS)
        info = {"otros_datos": {}}
        out = list(ENGINE_STREAMS["14"](info, WORDS, ["1990", "2024"], []))
        self.assertGreater(len(out), 0)
        # Debe producir variantes capitalizadas y con año.
        self.assertTrue(any(w[0].isupper() for w in out))
        self.assertTrue(any(w.endswith("2024") for w in out))

    def test_needs_minimum_words(self):
        self.assertEqual(list(ENGINE_STREAMS["14"]({"otros_datos": {}}, ["solo"], [], [])), [])


if __name__ == "__main__":
    unittest.main()
