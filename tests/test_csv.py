import unittest
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sikhar.lexer import Lexer
from sikhar.parser import Parser
from sikhar.interpreter import Interpreter
from sikhar.vm.compiler import Compiler
from sikhar.vm.vm import VM


class TestCSV(unittest.TestCase):
    def run_code_ast(self, code: str) -> list[str]:
        output = []
        tokens = Lexer(code, "test.sk").tokenize()
        ast = Parser(tokens, code, "test.sk").parse()
        interp = Interpreter(code, "test.sk", output_fn=output.append)
        interp.interpret(ast)
        return output

    def run_code_vm(self, code: str) -> list[str]:
        output = []
        tokens = Lexer(code, "test.sk").tokenize()
        ast = Parser(tokens, code, "test.sk").parse()
        chunk = Compiler().compile(ast)
        vm = VM(filename="test.sk", output_fn=output.append)
        vm.run(chunk)
        return output

    def test_csv_parse_and_stringify(self):
        code = """
        aayaat std.csv
        rakha raw = "name,role,age\\nRam,Developer,28\\nSita,Designer,26"
        rakha rows = csv.parse(raw, sacho)
        dekha lamba(rows)
        dekha rows[0]["name"]
        dekha rows[1]["role"]

        rakha generated = csv.stringify(rows)
        dekha csv.parse(generated, sacho)[0]["name"]
        """
        ast_out = self.run_code_ast(code)
        self.assertEqual(ast_out, ["2", "Ram", "Designer", "Ram"])

        vm_out = self.run_code_vm(code)
        self.assertEqual(vm_out, ["2", "Ram", "Designer", "Ram"])

    def test_csv_file_io_and_custom_delimiter(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = str(Path(tmpdir) / "test_data.csv").replace("\\", "/")
            code = f"""
            aayaat std.csv
            rakha items = [
                {{"id": "1", "item": "pen", "cost": "10"}},
                {{"id": "2", "item": "book", "cost": "50"}}
            ]
            csv.lekh("{csv_path}", items, ";")

            rakha read_back = csv.padh("{csv_path}", sacho, ";")
            dekha lamba(read_back)
            dekha read_back[0]["item"]
            dekha read_back[1]["cost"]
            """
            ast_out = self.run_code_ast(code)
            self.assertEqual(ast_out, ["2", "pen", "50"])

            vm_out = self.run_code_vm(code)
            self.assertEqual(vm_out, ["2", "pen", "50"])


if __name__ == "__main__":
    unittest.main()
