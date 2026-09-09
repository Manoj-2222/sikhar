import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from sikhar.formatter import Formatter


class TestFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = Formatter(indent_size=4)

    def test_format_if_statement(self):
        messy = 'yadi x>5{dekha "yes"}'
        formatted = self.formatter.format_code(messy)
        expected = 'yadi x > 5 {\n    dekha "yes"\n}\n'
        self.assertEqual(formatted, expected)

    def test_format_function_and_loop(self):
        messy = 'kaam add(a,b){farka a+b}\nrakha i=0\njaba i<5{badla i=i+1}'
        formatted = self.formatter.format_code(messy)
        expected = (
            'kaam add(a, b) {\n'
            '    farka a + b\n'
            '}\n'
            '\n'
            'rakha i = 0\n'
            'jaba i < 5 {\n'
            '    badla i = i + 1\n'
            '}\n'
        )
        self.assertEqual(formatted, expected)

    def test_format_is_idempotent(self):
        initial = 'yadi x > 5 {\n    dekha "yes"\n}\n'
        second_pass = self.formatter.format_code(initial)
        self.assertEqual(second_pass, initial)


if __name__ == "__main__":
    unittest.main()
