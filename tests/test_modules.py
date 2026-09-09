import unittest
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sikhar.lexer import Lexer
from sikhar.parser import Parser
from sikhar.interpreter import Interpreter
from sikhar.errors.error_types import SikharNameError


class TestModules(unittest.TestCase):
    def test_import_std_math(self):
        code = """
        rakha math = aayaat std.math
        dekha math.sqrt(49)
        dekha math.pi > 3
        """
        output = []
        tokens = Lexer(code, "test.sk").tokenize()
        ast = Parser(tokens, code, "test.sk").parse()
        interp = Interpreter(code, "test.sk", output_fn=output.append)
        interp.interpret(ast)
        self.assertEqual(output, ["7.0", "sacho"])

    def test_import_std_statement_syntax(self):
        code = """
        aayaat std.text
        dekha text.upper("nepal")
        """
        output = []
        tokens = Lexer(code, "test.sk").tokenize()
        ast = Parser(tokens, code, "test.sk").parse()
        interp = Interpreter(code, "test.sk", output_fn=output.append)
        interp.interpret(ast)
        self.assertEqual(output, ["NEPAL"])

    def test_local_module_export_and_import(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            mod_path = Path(tmp_dir) / "calc.sk"
            mod_path.write_text("""
            pathaau kaam jod(a, b) {
                farka a + b
            }
            pathaau sthayi VERSION = 2
            rakha secret = "invisible"
            """, encoding="utf-8")

            main_code = f"""
            rakha calc = aayaat "{mod_path.as_posix()}"
            dekha calc.jod(10, 5)
            dekha calc.VERSION
            """
            output = []
            tokens = Lexer(main_code, "main.sk").tokenize()
            ast = Parser(tokens, main_code, "main.sk").parse()
            interp = Interpreter(main_code, "main.sk", output_fn=output.append)
            interp.interpret(ast)
            self.assertEqual(output, ["15", "2"])

            # Verify unexported variable is not accessible
            err_code = f"""
            rakha calc = aayaat "{mod_path.as_posix()}"
            dekha calc.secret
            """
            tokens = Lexer(err_code, "main.sk").tokenize()
            ast = Parser(tokens, err_code, "main.sk").parse()
            with self.assertRaises(SikharNameError):
                Interpreter(err_code, "main.sk").interpret(ast)


if __name__ == "__main__":
    unittest.main()
