import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sikhar.lexer import Lexer
from sikhar.parser import Parser
from sikhar.interpreter import Interpreter


class TestStringInterpolation(unittest.TestCase):
    def run_code(self, code: str) -> list[str]:
        output = []
        tokens = Lexer(code, "test.sk").tokenize()
        ast = Parser(tokens, code, "test.sk").parse()
        interp = Interpreter(code, "test.sk", output_fn=output.append)
        interp.interpret(ast)
        return output

    def test_variable_interpolation(self):
        code = """
        rakha name = "Manoj"
        dekha "Hello, {name}!"
        """
        output = self.run_code(code)
        self.assertEqual(output, ["Hello, Manoj!"])

    def test_expression_interpolation(self):
        code = """
        rakha x = 10
        rakha y = 20
        dekha "Total: {x + y}"
        """
        output = self.run_code(code)
        self.assertEqual(output, ["Total: 30"])

    def test_nested_interpolations_and_escapes(self):
        code = """
        rakha item = "book"
        rakha price = 25
        dekha "Item: {item}, Price: ${price}, Literal: \\{escaped\\}"
        """
        output = self.run_code(code)
        self.assertEqual(output, ["Item: book, Price: $25, Literal: {escaped}"])


if __name__ == "__main__":
    unittest.main()
