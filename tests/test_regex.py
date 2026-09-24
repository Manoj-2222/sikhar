import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sikhar.lexer import Lexer
from sikhar.parser import Parser
from sikhar.interpreter import Interpreter
from sikhar.vm.compiler import Compiler
from sikhar.vm.vm import VM


class TestRegex(unittest.TestCase):
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

    def test_regex_matching_and_finding(self):
        code = """
        aayaat std.regex
        rakha text = "Order #12345 placed on 2026-09-24 for $99.99"
        
        # Test match
        dekha regex.match("^Order", text)
        dekha regex.match("^Invoice", text)

        # Test find_all
        rakha digits = regex.find_all("\\\\d+", text)
        dekha digits[0]
        dekha digits[1]
        dekha digits[2]
        """
        ast_out = self.run_code_ast(code)
        self.assertEqual(ast_out, ["sacho", "jutho", "12345", "2026", "09"])

        vm_out = self.run_code_vm(code)
        self.assertEqual(vm_out, ["sacho", "jutho", "12345", "2026", "09"])

    def test_regex_replace_split_and_aliases(self):
        code = """
        aayaat std.regex
        # Test replace / badla: (pattern, replacement, text)
        rakha clean = regex.badla("\\\\s+", " ", "hello    world  sikhar")
        dekha clean

        # Test split
        rakha parts = regex.split("[,;:]\\\\s*", "apple, banana; orange: grape")
        dekha lamba(parts)
        dekha parts[0]
        dekha parts[3]

        # Test Nepali alias milcha and khoja
        dekha regex.milcha(".*sikhar.*", "hello sikhar world")
        rakha found = regex.khoja("[a-z]+", "foo 123 bar")
        dekha found[0]
        dekha found[1]
        """
        ast_out = self.run_code_ast(code)
        self.assertEqual(ast_out, ["hello world sikhar", "4", "apple", "grape", "sacho", "foo", "bar"])

        vm_out = self.run_code_vm(code)
        self.assertEqual(vm_out, ["hello world sikhar", "4", "apple", "grape", "sacho", "foo", "bar"])


if __name__ == "__main__":
    unittest.main()
