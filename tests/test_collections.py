import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from sikhar.lexer import Lexer
from sikhar.parser import Parser
from sikhar.interpreter import Interpreter
from sikhar.errors.error_types import SikharIndexError, SikharKeyError


class TestCollections(unittest.TestCase):
    def run_code(self, code: str) -> list[str]:
        output = []
        tokens = Lexer(code, "test.sk").tokenize()
        ast = Parser(tokens, code, "test.sk").parse()
        interp = Interpreter(code, "test.sk", output_fn=output.append)
        interp.interpret(ast)
        return output

    def test_list_indexing_and_mutation(self):
        code = """
        rakha arr = [10, 20, 30]
        dekha arr[0]
        dekha arr[2]
        badla arr[1] = 99
        dekha arr[1]
        """
        output = self.run_code(code)
        self.assertEqual(output, ["10", "30", "99"])

    def test_list_out_of_bounds(self):
        code = """
        rakha arr = [1, 2]
        dekha arr[5]
        """
        with self.assertRaises(SikharIndexError):
            self.run_code(code)

    def test_list_builtins(self):
        code = """
        rakha arr = [1, 2]
        dekha lamba(arr)
        jod_suchi(arr, 3)
        dekha arr
        dekha lamba(arr)
        rakha removed = hatau_suchi(arr, 0)
        dekha removed
        dekha arr
        dekha khoj_suchi(arr, 3)
        """
        output = self.run_code(code)
        self.assertEqual(output, [
            "2",
            "[1, 2, 3]",
            "3",
            "1",
            "[2, 3]",
            "1",
        ])

    def test_map_operations(self):
        code = """
        rakha person = {"name": "Manoj", "age": 20}
        dekha person["name"]
        dekha person["age"]
        badla person["age"] = 21
        dekha person["age"]
        badla person["city"] = "Pokhara"
        dekha person["city"]
        """
        output = self.run_code(code)
        self.assertEqual(output, ["Manoj", "20", "21", "Pokhara"])

    def test_map_missing_key_error(self):
        code = """
        rakha m = {"a": 1}
        dekha m["b"]
        """
        with self.assertRaises(SikharKeyError):
            self.run_code(code)

    def test_map_key_iteration(self):
        code = """
        rakha m = {"k1": "v1"}
        ko_lagi key ma m {
            dekha key
            dekha m[key]
        }
        """
        output = self.run_code(code)
        self.assertEqual(output, ["k1", "v1"])


if __name__ == "__main__":
    unittest.main()
