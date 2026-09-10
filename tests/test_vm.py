import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sikhar.lexer import Lexer
from sikhar.parser import Parser
from sikhar.vm import Compiler, VM
from sikhar.errors.error_types import (
    SikharAssertionError,
    SikharConstantMutationError,
    SikharDivisionByZeroError,
    SikharIndexError,
    SikharKeyError,
)


class TestVM(unittest.TestCase):
    def run_code(self, code: str) -> list[str]:
        output = []
        tokens = Lexer(code, "test.sk").tokenize()
        ast = Parser(tokens, code, "test.sk").parse()
        chunk = Compiler("test.sk").compile(ast)
        vm = VM(source=code, filename="test.sk", output_fn=output.append)
        vm.run(chunk)
        return output

    def test_arithmetic_and_precedence(self):
        code = """
        rakha a = 10 + 5 * 2
        rakha b = (10 + 5) * 2
        rakha c = 20 / 4
        rakha d = 17 % 5
        dekha a
        dekha b
        dekha c
        dekha d
        """
        out = self.run_code(code)
        self.assertEqual(out, ["20", "30", "5", "2"])

    def test_conditions_and_logic(self):
        code = """
        rakha x = 15
        yadi x > 20 {
            dekha "too big"
        } athawa x > 10 and x < 20 {
            dekha "just right"
        } natra {
            dekha "too small"
        }
        """
        out = self.run_code(code)
        self.assertEqual(out, ["just right"])

    def test_while_and_for_loops(self):
        code = """
        rakha total = 0
        ko_lagi n ma [1, 2, 3, 4] {
            badla total = total + n
        }
        dekha total
        """
        out = self.run_code(code)
        self.assertEqual(out, ["10"])

    def test_recursion_factorial(self):
        code = """
        kaam fact(n) {
            yadi n <= 1 {
                farka 1
            }
            farka n * fact(n - 1)
        }
        dekha fact(5)
        """
        out = self.run_code(code)
        self.assertEqual(out, ["120"])

    def test_fibonacci(self):
        code = """
        kaam fib(n) {
            yadi n <= 1 {
                farka n
            }
            farka fib(n - 1) + fib(n - 2)
        }
        dekha fib(7)
        """
        out = self.run_code(code)
        self.assertEqual(out, ["13"])

    def test_collections_and_maps(self):
        code = """
        rakha lst = [10, 20]
        jod_suchi(lst, 30)
        badla lst[0] = 99
        dekha lst[0]
        dekha lamba(lst)

        rakha user = {"name": "Manoj"}
        badla user["city"] = "Kathmandu"
        dekha user["name"]
        dekha user["city"]
        """
        out = self.run_code(code)
        self.assertEqual(out, ["99", "3", "Manoj", "Kathmandu"])

    def test_constant_mutation_error(self):
        code = """
        sthayi pi = 3.14
        badla pi = 3.0
        """
        with self.assertRaises(SikharConstantMutationError):
            self.run_code(code)

    def test_division_by_zero_error(self):
        code = "rakha bad = 10 / 0"
        with self.assertRaises(SikharDivisionByZeroError):
            self.run_code(code)

    def test_try_catch(self):
        code = """
        rakha caught = ""
        koshish {
            fal "custom error"
        } samata err {
            badla caught = err
        }
        dekha caught
        """
        out = self.run_code(code)
        self.assertEqual(out, ["custom error"])

    def test_assertion(self):
        code = """
        jaach 10 + 20 == 30, "Sanity check"
        dekha "assert passed"
        """
        out = self.run_code(code)
        self.assertEqual(out, ["assert passed"])

    def test_assertion_failure(self):
        code = 'jaach 2 + 2 == 5, "Math broke"'
        with self.assertRaises(SikharAssertionError):
            self.run_code(code)

    def test_string_interpolation(self):
        code = """
        rakha name = "Sikhar"
        rakha version = "0.3.0"
        dekha "Running {name} v{version}!"
        """
        out = self.run_code(code)
        self.assertEqual(out, ["Running Sikhar v0.3.0!"])


if __name__ == "__main__":
    unittest.main()
