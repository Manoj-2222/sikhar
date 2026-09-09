import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sikhar.lexer import Lexer
from sikhar.parser import Parser
from sikhar.interpreter import Interpreter
from sikhar.errors.error_types import SikharAssertionError


class TestAssertions(unittest.TestCase):
    def test_assertion_passes(self):
        code = """
        jaach 10 > 5
        jaach "abc" != "xyz"
        jaach sacho
        """
        output = []
        tokens = Lexer(code, "test.sk").tokenize()
        ast = Parser(tokens, code, "test.sk").parse()
        interp = Interpreter(code, "test.sk", output_fn=output.append)
        interp.interpret(ast)

    def test_assertion_fails_default_message(self):
        code = "jaach 5 > 10"
        tokens = Lexer(code, "test.sk").tokenize()
        ast = Parser(tokens, code, "test.sk").parse()
        interp = Interpreter(code, "test.sk")
        with self.assertRaises(SikharAssertionError) as ctx:
            interp.interpret(ast)
        self.assertIn("Assertion failed", str(ctx.exception))

    def test_assertion_fails_custom_message(self):
        code = 'jaach 2 + 2 == 5, "Math is broken"'
        tokens = Lexer(code, "test.sk").tokenize()
        ast = Parser(tokens, code, "test.sk").parse()
        interp = Interpreter(code, "test.sk")
        with self.assertRaises(SikharAssertionError) as ctx:
            interp.interpret(ast)
        self.assertIn("Math is broken", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
