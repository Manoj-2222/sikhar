import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sikhar.lexer import Lexer
from sikhar.parser import Parser
from sikhar.interpreter import Interpreter
from sikhar.vm import Compiler, VM


class TestHTTP(unittest.TestCase):
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

    def test_http_server_and_client_ast(self):
        code = """
        aayaat std.http
        aayaat std.json

        kaam api_handler(req) {
            yadi req.path == "/ping" {
                farka "pong"
            }
            yadi req.path == "/echo" {
                rakha data = json.parse(req.body)
                farka {"echo": data["message"]}
            }
            farka {"status": 404, "body": "Not Found"}
        }

        rakha srv = http.server(0, api_handler)
        srv.start()

        rakha base = "http://127.0.0.1:" + srv.port

        # Test GET /ping
        rakha res1 = http.get(base + "/ping")
        dekha res1.status
        dekha res1.body
        dekha res1.ok

        # Test POST /echo
        rakha payload = '{"message": "Namaste"}'
        rakha res2 = http.post(base + "/echo", payload)
        dekha res2.status
        rakha res2_json = json.parse(res2.body)
        dekha res2_json["echo"]

        srv.stop()
        """
        out = self.run_ast(code)
        self.assertEqual(out, ["200", "pong", "sacho", "200", "Namaste"])

    def test_http_server_and_client_vm(self):
        code = """
        aayaat std.http

        kaam handle(req) {
            farka "Hello from VM Server"
        }

        rakha srv = http.server(0, handle)
        srv.start()

        rakha url = "http://127.0.0.1:" + srv.port + "/hello"
        rakha res = http.lyaau(url)
        dekha res.status
        dekha res.body

        srv.stop()
        """
        out = self.run_vm(code)
        self.assertEqual(out, ["200", "Hello from VM Server"])


if __name__ == "__main__":
    unittest.main()
