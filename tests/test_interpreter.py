import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from sikhar.lexer import Lexer
from sikhar.parser import Parser
from sikhar.interpreter import Interpreter
from sikhar.errors.error_types import (
    SikharNameError,
    SikharConstantMutationError,
    SikharDivisionByZeroError,
)


class TestInterpreter(unittest.TestCase):
    def run_code(self, code: str) -> list[str]:
        output = []
        tokens = Lexer(code, "test.sk").tokenize()
        ast = Parser(tokens, code, "test.sk").parse()
        interp = Interpreter(code, "test.sk", output_fn=output.append)
        interp.interpret(ast)
        return output

    def test_variables_and_mutation(self):
        code = """
        rakha x = 10
        dekha x
        badla x = 25
        dekha x
        """
        output = self.run_code(code)
        self.assertEqual(output, ["10", "25"])

    def test_constant_declaration_and_mutation_error(self):
        code = """
        sthayi pi = 3.14
        dekha pi
        badla pi = 4.0
        """
        with self.assertRaises(SikharConstantMutationError):
            self.run_code(code)

    def test_undefined_variable_error(self):
        code = "dekha undefined_var"
        with self.assertRaises(SikharNameError):
            self.run_code(code)

    def test_arithmetic_operations(self):
        code = """
        dekha 10 + 20
        dekha 50 - 15
        dekha 6 * 7
        dekha 40 / 4
        dekha 17 % 5
        """
        output = self.run_code(code)
        self.assertEqual(output, ["30", "35", "42", "10", "2"])

    def test_division_by_zero(self):
        code = "rakha a = 10 / 0"
        with self.assertRaises(SikharDivisionByZeroError):
            self.run_code(code)

    def test_string_concatenation(self):
        code = """
        rakha name = "Sikhar"
        dekha "Hello, " + name + "!"
        """
        output = self.run_code(code)
        self.assertEqual(output, ["Hello, Sikhar!"])

    def test_comparison_and_logic(self):
        code = """
        dekha 10 > 5
        dekha 5 >= 5
        dekha 3 < 2
        dekha 4 <= 4
        dekha 10 == 10
        dekha 10 != 5
        dekha sacho and jutho
        dekha sacho or jutho
        dekha not jutho
        """
        output = self.run_code(code)
        self.assertEqual(output, [
            "sacho", "sacho", "jutho", "sacho", "sacho", "sacho",
            "jutho", "sacho", "sacho",
        ])

    def test_if_athawa_natra_execution(self):
        code = """
        kaam check(val) {
            yadi val > 10 {
                farka "greater"
            } athawa val == 10 {
                farka "equal"
            } natra {
                farka "lesser"
            }
        }
        dekha check(15)
        dekha check(10)
        dekha check(5)
        """
        output = self.run_code(code)
        self.assertEqual(output, ["greater", "equal", "lesser"])

    def test_while_loop(self):
        code = """
        rakha count = 0
        rakha i = 1
        jaba i <= 4 {
            badla count = count + i
            badla i = i + 1
        }
        dekha count
        """
        output = self.run_code(code)
        self.assertEqual(output, ["10"])

    def test_for_loop_and_break_continue(self):
        code = """
        rakha nums = [1, 2, 3, 4, 5]
        ko_lagi n ma nums {
            yadi n == 2 {
                jaari
            }
            yadi n == 4 {
                rok
            }
            dekha n
        }
        """
        output = self.run_code(code)
        self.assertEqual(output, ["1", "3"])


if __name__ == "__main__":
    unittest.main()
