import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sikhar.lexer import Lexer
from sikhar.parser import Parser
from sikhar.interpreter import Interpreter
from sikhar.vm.compiler import Compiler
from sikhar.vm.vm import VM


class TestProcessAndTask(unittest.TestCase):
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

    def test_task_concurrency_ast_and_vm(self):
        code = """
        aayaat std.task
        kaam add_ten(x) {
            task.sleep(0.01)
            farka x + 10
        }
        rakha t1 = task.spawn(add_ten, [5])
        rakha t2 = task.spawn(add_ten, [20])
        
        rakha r1 = task.wait(t1)
        rakha r2 = task.wait(t2)
        dekha r1
        dekha r2
        """
        ast_out = self.run_code_ast(code)
        self.assertEqual(ast_out, ["15", "30"])

        vm_out = self.run_code_vm(code)
        self.assertEqual(vm_out, ["15", "30"])

    def test_process_exec_and_env_ast_and_vm(self):
        code = """
        aayaat std.process
        aayaat std.text
        process.set_env("TEST_SIKHAR_VAR", "nepal_himalaya")
        dekha process.env("TEST_SIKHAR_VAR")

        rakha cmd = process.exec("echo v1.0.0-verified")
        dekha cmd["ok"]
        dekha cmd["code"]
        dekha text.trim(cmd["stdout"])
        """
        ast_out = self.run_code_ast(code)
        self.assertEqual(ast_out, ["nepal_himalaya", "sacho", "0", "v1.0.0-verified"])

        vm_out = self.run_code_vm(code)
        self.assertEqual(vm_out, ["nepal_himalaya", "sacho", "0", "v1.0.0-verified"])


if __name__ == "__main__":
    unittest.main()
