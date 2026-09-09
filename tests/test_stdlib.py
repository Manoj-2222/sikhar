import unittest
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sikhar.lexer import Lexer
from sikhar.parser import Parser
from sikhar.interpreter import Interpreter


class TestStdLib(unittest.TestCase):
    def run_code(self, code: str) -> list[str]:
        output = []
        tokens = Lexer(code, "test.sk").tokenize()
        ast = Parser(tokens, code, "test.sk").parse()
        interp = Interpreter(code, "test.sk", output_fn=output.append)
        interp.interpret(ast)
        return output

    def test_std_math(self):
        code = """
        rakha math = aayaat std.math
        dekha math.floor(3.7)
        dekha math.ceil(3.2)
        dekha math.pow(2, 3)
        dekha math.abs(-15)
        """
        output = self.run_code(code)
        self.assertEqual(output, ["3", "4", "8.0", "15"])

    def test_std_text(self):
        code = """
        rakha text = aayaat std.text
        dekha text.lower("HELLO")
        dekha text.trim("   spaces   ")
        dekha text.replace("cat and dog", "cat", "fox")
        dekha text.contains("Sikhar Language", "Sikhar")
        dekha text.starts_with("compiler", "comp")
        dekha text.ends_with("compiler", "ler")
        """
        output = self.run_code(code)
        self.assertEqual(output, [
            "hello",
            "spaces",
            "fox and dog",
            "sacho",
            "sacho",
            "sacho",
        ])

    def test_std_list(self):
        code = """
        rakha list_mod = aayaat std.list
        rakha arr = [3, 1, 4, 1, 5]
        dekha list_mod.sort(arr)
        dekha list_mod.reverse(arr)
        dekha list_mod.sum([10, 20, 30])
        dekha list_mod.min([4, 2, 8])
        dekha list_mod.max([4, 2, 8])
        dekha list_mod.slice([10, 20, 30, 40], 1, 3)
        """
        output = self.run_code(code)
        self.assertEqual(output, [
            "[1, 1, 3, 4, 5]",
            "[5, 1, 4, 1, 3]",
            "60",
            "2",
            "8",
            "[20, 30]",
        ])

    def test_std_map(self):
        code = """
        rakha map_mod = aayaat std.map
        rakha m1 = {"a": 1, "b": 2}
        dekha map_mod.has(m1, "a")
        dekha map_mod.has(m1, "z")
        rakha m2 = {"c": 3}
        rakha merged = map_mod.merge(m1, m2)
        dekha map_mod.has(merged, "c")
        """
        output = self.run_code(code)
        self.assertEqual(output, ["sacho", "jutho", "sacho"])

    def test_std_file_and_file_builtins(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            fpath = (Path(tmp_dir) / "test_file.txt").as_posix()
            code = f"""
            rakha file_mod = aayaat std.file
            file_mod.write("{fpath}", "Hello Sikhar File!")
            dekha file_mod.exists("{fpath}")
            dekha file_mod.read("{fpath}")
            file_mod.append("{fpath}", " Extra")
            dekha file_mod.read("{fpath}")

            # Test direct builtins padh and lekh
            lekh("{fpath}", "Overwritten with lekh")
            dekha padh("{fpath}")
            """
            output = self.run_code(code)
            self.assertEqual(output, [
                "sacho",
                "Hello Sikhar File!",
                "Hello Sikhar File! Extra",
                "Overwritten with lekh",
            ])


if __name__ == "__main__":
    unittest.main()
