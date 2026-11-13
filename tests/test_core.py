import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.languages import LANGUAGES
from core.paradigms_data import PARADIGM_TOPICS
from core.memory_scenarios import MEMORY_SCENARIOS
from core.patterns_data import PATTERNS
from core.code_runner import CodeRunner

class TestPolyglotForge(unittest.TestCase):
    def test_languages_metadata(self):
        self.assertIn("rust", LANGUAGES)
        self.assertIn("go", LANGUAGES)
        self.assertIn("python", LANGUAGES)
        self.assertIn("typescript", LANGUAGES)
        self.assertEqual(LANGUAGES["rust"].extension, ".rs")

    def test_paradigm_topics(self):
        self.assertGreaterEqual(len(PARADIGM_TOPICS), 3)
        for topic in PARADIGM_TOPICS:
            self.assertIn("rust", topic.snippets)
            self.assertIn("go", topic.snippets)
            self.assertIn("typescript", topic.snippets)

    def test_memory_scenarios(self):
        self.assertGreaterEqual(len(MEMORY_SCENARIOS), 2)
        rust_sc = MEMORY_SCENARIOS[0]
        self.assertEqual(rust_sc.language, "rust")
        self.assertGreater(len(rust_sc.steps), 0)

    def test_patterns(self):
        self.assertGreaterEqual(len(PATTERNS), 2)
        circuit_breaker = PATTERNS[0]
        self.assertEqual(circuit_breaker.id, "circuit_breaker")
        self.assertIn("rust", circuit_breaker.code_implementations)

    def test_code_runner_python(self):
        output = CodeRunner.run("python", "print('TEST_OUTPUT_123')")
        self.assertEqual(output.exit_code, 0)
        self.assertIn("TEST_OUTPUT_123", output.stdout)

    def test_code_runner_simulated(self):
        output = CodeRunner.run("rust", "fn main() {}")
        self.assertEqual(output.exit_code, 0)
        self.assertTrue(output.is_simulated)

if __name__ == "__main__":
    unittest.main()
