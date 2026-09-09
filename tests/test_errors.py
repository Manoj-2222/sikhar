import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from sikhar.lexer import Lexer
from sikhar.parser import Parser
from sikhar.interpreter import Interpreter
from sikhar.errors.error_types import SikharNameError, SikharError
from sikhar.errors.reporter import format_error


class TestErrors(unittest.TestCase):
    def test_formatted_error_output_structure(self):
        code = "dekha not_defined"
        tokens = Lexer(code, "main.sk").tokenize()
        ast = Parser(tokens, code, "main.sk").parse()
        interp = Interpreter(code, "main.sk")
        try:
            interp.interpret(ast)
            self.fail("Should have raised an error")
        except SikharError as e:
            formatted = format_error(e, code)
            self.assertIn("Sikhar Error", formatted)
            self.assertIn("Type: UndefinedVariable", formatted)
            self.assertIn("Message: Variable 'not_defined' is not defined", formatted)
            self.assertIn("File: main.sk", formatted)
            self.assertIn("Line: 1", formatted)
            self.assertIn("Column: 7", formatted)
            self.assertIn("^", formatted)
            # Ensure no raw Python traceback string exists
            self.assertNotIn("Traceback (most recent call last)", formatted)

    def test_try_catch_user_throw(self):
        code = """
        rakha caught = ""
        koshish {
            fal "custom error message"
        } samata err {
            badla caught = err
        }
        dekha caught
        """
        output = []
        tokens = Lexer(code, "test.sk").tokenize()
        ast = Parser(tokens, code, "test.sk").parse()
        interp = Interpreter(code, "test.sk", output_fn=output.append)
        interp.interpret(ast)
        self.assertEqual(output, ["custom error message"])

    def test_try_catch_runtime_error(self):
        code = """
        rakha caught = ""
        koshish {
            rakha x = 10 / 0
        } samata err {
            badla caught = err
        }
        dekha caught
        """
        output = []
        tokens = Lexer(code, "test.sk").tokenize()
        ast = Parser(tokens, code, "test.sk").parse()
        interp = Interpreter(code, "test.sk", output_fn=output.append)
        interp.interpret(ast)
        self.assertEqual(output, ["Division by zero"])


if __name__ == "__main__":
    unittest.main()
