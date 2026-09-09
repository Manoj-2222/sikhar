import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from sikhar.lexer import Lexer
from sikhar.parser import Parser
from sikhar.interpreter import Interpreter
from sikhar.errors.error_types import SikharTypeError


class TestFunctions(unittest.TestCase):
    def run_code(self, code: str) -> list[str]:
        output = []
        tokens = Lexer(code, "test.sk").tokenize()
        ast = Parser(tokens, code, "test.sk").parse()
        interp = Interpreter(code, "test.sk", output_fn=output.append)
        interp.interpret(ast)
        return output

    def test_basic_function(self):
        code = """
        kaam jod(a, b) {
            farka a + b
        }
        rakha result = jod(10, 20)
        dekha result
        """
        output = self.run_code(code)
        self.assertEqual(output, ["30"])

    def test_local_scope_isolation(self):
        code = """
        rakha x = "global"
        kaam shadow() {
            rakha x = "local"
            farka x
        }
        dekha shadow()
        dekha x
        """
        output = self.run_code(code)
        self.assertEqual(output, ["local", "global"])

    def test_recursion_factorial(self):
        code = """
        kaam fact(n) {
            yadi n <= 1 {
                farka 1
            }
            farka n * fact(n - 1)
        }
        dekha fact(6)
        """
        output = self.run_code(code)
        self.assertEqual(output, ["720"])

    def test_recursion_fibonacci(self):
        code = """
        kaam fib(n) {
            yadi n <= 0 {
                farka 0
            }
            yadi n == 1 {
                farka 1
            }
            farka fib(n - 1) + fib(n - 2)
        }
        dekha fib(8)
        """
        output = self.run_code(code)
        self.assertEqual(output, ["21"])

    def test_arity_mismatch(self):
        code = """
        kaam greet(a, b) {
            farka a + b
        }
        greet(1)
        """
        with self.assertRaises(SikharTypeError):
            self.run_code(code)

    def test_calling_non_callable(self):
        code = """
        rakha not_func = 42
        not_func()
        """
        with self.assertRaises(SikharTypeError):
            self.run_code(code)


if __name__ == "__main__":
    unittest.main()
