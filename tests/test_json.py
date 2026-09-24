import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sikhar.lexer import Lexer
from sikhar.parser import Parser
from sikhar.interpreter import Interpreter
from sikhar.vm import Compiler, VM
from sikhar.errors.error_types import SikharRuntimeError


class TestJSON(unittest.TestCase):
    def run_ast(self, code: str) -> list[str]:
        output = []
        tokens = Lexer(code, "test.sk").tokenize()
        ast = Parser(tokens, code, "test.sk").parse()
        interp = Interpreter(code, "test.sk", output_fn=output.append)
        interp.interpret(ast)
        return output

    def run_vm(self, code: str) -> list[str]:
        output = []
        tokens = Lexer(code, "test.sk").tokenize()
        ast = Parser(tokens, code, "test.sk").parse()
        chunk = Compiler("test.sk").compile(ast)
        vm = VM(source=code, filename="test.sk", output_fn=output.append)
        vm.run(chunk)
        return output

    def test_json_parse_and_stringify_ast(self):
        code = """
        aayaat std.json
        rakha raw = '{"name": "Sikhar", "version": "0.4.0", "active": true, "count": 42}'
        rakha parsed = json.parse(raw)
        dekha parsed["name"]
        dekha parsed["version"]
        dekha parsed["active"]
        dekha parsed["count"]

        rakha serialized = json.stringify(parsed)
        jaach json.valid(serialized) == sacho
        """
        out = self.run_ast(code)
        self.assertEqual(out, ["Sikhar", "0.4.0", "sacho", "42"])

    def test_json_parse_and_stringify_vm(self):
        code = """
        aayaat std.json
        rakha raw = '{"name": "Sikhar", "stars": 100}'
        rakha parsed = json.parse(raw)
        dekha parsed["name"]
        dekha parsed["stars"]

        rakha pretty = json.stringify(parsed, 2)
        dekha json.valid(pretty)
        """
        out = self.run_vm(code)
        self.assertEqual(out, ["Sikhar", "100", "sacho"])

    def test_nepali_aliases(self):
        code = """
        aayaat std.json
        rakha doc = json.padh('{"title": "Gorkha", "items": [1, 2]}')
        dekha doc["title"]
        dekha doc["items"][0]
        rakha out_str = json.rupantar(doc)
        dekha json.sacho(out_str)
        """
        out = self.run_ast(code)
        self.assertEqual(out, ["Gorkha", "1", "sacho"])

    def test_invalid_json(self):
        code = """
        aayaat std.json
        dekha json.valid("{bad json")
        """
        out = self.run_ast(code)
        self.assertEqual(out, ["jutho"])

    def test_parse_error(self):
        code = """
        aayaat std.json
        json.parse("not json")
        """
        with self.assertRaises(SikharRuntimeError):
            self.run_ast(code)


if __name__ == "__main__":
    unittest.main()
