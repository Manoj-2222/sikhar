import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sikhar.lexer import Lexer
from sikhar.parser import Parser
from sikhar.vm import Compiler, OpCode, Disassembler


class TestCompiler(unittest.TestCase):
    def compile_source(self, code: str):
        tokens = Lexer(code, "test.sk").tokenize()
        ast = Parser(tokens, code, "test.sk").parse()
        return Compiler("test.sk").compile(ast)

    def test_compile_literals(self):
        code = """
        rakha x = 42
        rakha pi = 3.14
        rakha name = "Sikhar"
        rakha flag = sacho
        rakha none = khali
        """
        chunk = self.compile_source(code)
        self.assertGreater(chunk.count, 0)
        self.assertIn(42, chunk.constants)
        self.assertIn(3.14, chunk.constants)
        self.assertIn("Sikhar", chunk.constants)
        # sacho and khali use OP_TRUE / OP_NIL
        self.assertIn(OpCode.OP_TRUE, chunk.code)
        self.assertIn(OpCode.OP_NIL, chunk.code)

    def test_compile_arithmetic(self):
        code = "rakha result = 10 + 20 * 3"
        chunk = self.compile_source(code)
        self.assertIn(OpCode.OP_ADD, chunk.code)
        self.assertIn(OpCode.OP_MULTIPLY, chunk.code)

    def test_compile_function_and_call(self):
        code = """
        kaam add(a, b) {
            farka a + b
        }
        rakha sum = add(5, 7)
        """
        chunk = self.compile_source(code)
        self.assertIn(OpCode.OP_MAKE_FUNCTION, chunk.code)
        self.assertIn(OpCode.OP_CALL, chunk.code)

    def test_compile_loops(self):
        code = """
        rakha i = 0
        jaba i < 10 {
            yadi i == 5 {
                rok
            }
            badla i = i + 1
        }
        """
        chunk = self.compile_source(code)
        self.assertIn(OpCode.OP_LOOP, chunk.code)
        self.assertIn(OpCode.OP_JUMP, chunk.code)
        self.assertIn(OpCode.OP_JUMP_IF_FALSE, chunk.code)

    def test_compile_for_loop(self):
        code = """
        ko_lagi x ma [1, 2, 3] {
            dekha x
        }
        """
        chunk = self.compile_source(code)
        self.assertIn(OpCode.OP_GET_ITER, chunk.code)
        self.assertIn(OpCode.OP_FOR_ITER, chunk.code)

    def test_compile_try_catch(self):
        code = """
        koshish {
            fal "error"
        } samata e {
            dekha e
        }
        """
        chunk = self.compile_source(code)
        self.assertIn(OpCode.OP_PUSH_TRY, chunk.code)
        self.assertIn(OpCode.OP_POP_TRY, chunk.code)
        self.assertIn(OpCode.OP_THROW, chunk.code)

    def test_disassembler_output(self):
        code = """
        kaam square(n) {
            farka n * n
        }
        dekha square(4)
        """
        chunk = self.compile_source(code)
        dis_text = Disassembler.disassemble(chunk, "test")
        self.assertIn("Bytecode Disassembly", dis_text)
        self.assertIn("OP_MAKE_FUNCTION", dis_text)
        self.assertIn("OP_CALL", dis_text)
        self.assertIn("kaam square", dis_text)


if __name__ == "__main__":
    unittest.main()
