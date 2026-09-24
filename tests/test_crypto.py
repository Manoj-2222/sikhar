import unittest
import sys
import hashlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sikhar.lexer import Lexer
from sikhar.parser import Parser
from sikhar.interpreter import Interpreter
from sikhar.vm.compiler import Compiler
from sikhar.vm.vm import VM


class TestCrypto(unittest.TestCase):
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

    def test_hashing_ast_and_vm(self):
        code = """
        aayaat std.crypto
        dekha crypto.sha256("sikhar")
        dekha crypto.md5("sikhar")
        dekha crypto.sha512("sikhar")
        """
        expected_sha256 = hashlib.sha256(b"sikhar").hexdigest()
        expected_md5 = hashlib.md5(b"sikhar").hexdigest()
        expected_sha512 = hashlib.sha512(b"sikhar").hexdigest()

        ast_out = self.run_code_ast(code)
        self.assertEqual(ast_out, [expected_sha256, expected_md5, expected_sha512])

        vm_out = self.run_code_vm(code)
        self.assertEqual(vm_out, [expected_sha256, expected_md5, expected_sha512])

    def test_hmac_and_base64(self):
        code = """
        aayaat std.crypto
        rakha sig = crypto.hmac_sha256("secret_key", "payload_data")
        dekha sig
        rakha b64 = crypto.base64_encode("hello world")
        dekha b64
        rakha orig = crypto.base64_decode(b64)
        dekha orig
        """
        ast_out = self.run_code_ast(code)
        self.assertEqual(ast_out[1], "aGVsbG8gd29ybGQ=")
        self.assertEqual(ast_out[2], "hello world")

        vm_out = self.run_code_vm(code)
        self.assertEqual(vm_out, ast_out)

    def test_random_token_and_nepali_aliases(self):
        code = """
        aayaat std.crypto
        rakha hex_bytes = crypto.random_bytes(8)
        dekha lamba(hex_bytes)
        dekha crypto.hashing("hello") == crypto.sha256("hello")
        dekha crypto.gupta("key", "msg") == crypto.hmac_sha256("key", "msg")
        """
        ast_out = self.run_code_ast(code)
        self.assertEqual(ast_out, ["16", "sacho", "sacho"])

        vm_out = self.run_code_vm(code)
        self.assertEqual(vm_out, ["16", "sacho", "sacho"])


if __name__ == "__main__":
    unittest.main()
