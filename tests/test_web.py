import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sikhar.lexer import Lexer
from sikhar.parser import Parser
from sikhar.interpreter import Interpreter
from sikhar.vm import Compiler, VM


class TestWeb(unittest.TestCase):
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

    def test_web_routes_and_handle_ast(self):
        code = """
        aayaat std.web

        rakha app = web.app()

        app.get("/", kaam(req) {
            farka "Namaste Sansar"
        })

        app.get("/users/:id", kaam(req) {
            rakha user_id = req.params["id"]
            farka {"id": user_id, "role": "admin"}
        })

        app.post("/items", kaam(req) {
            farka {"status": 201, "body": "Created item"}
        })

        # Test GET /
        rakha r1 = app.handle({"method": "GET", "path": "/"})
        dekha r1.status
        dekha r1.body

        # Test GET /users/99
        rakha r2 = app.handle({"method": "GET", "path": "/users/99"})
        dekha r2.status
        dekha r2.body

        # Test POST /items
        rakha r3 = app.handle({"method": "POST", "path": "/items"})
        dekha r3.status
        dekha r3.body

        # Test 404
        rakha r4 = app.handle({"method": "GET", "path": "/missing"})
        dekha r4.status
        """
        out = self.run_ast(code)
        self.assertEqual(out, [
            "200",
            "Namaste Sansar",
            "200",
            '{"id": "99", "role": "admin"}',
            "201",
            "Created item",
            "404",
        ])

    def test_web_middleware_and_live_server_ast(self):
        code = """
        aayaat std.web
        aayaat std.http

        rakha app = web.app()

        # Middleware adding header or checking auth
        app.use(kaam(req) {
            yadi req.path == "/blocked" {
                farka {"status": 403, "body": "Blocked by middleware"}
            }
            farka khali
        })

        app.get("/allowed", kaam(req) {
            farka "Access granted"
        })

        rakha port = app.start(0)
        rakha base = "http://127.0.0.1:" + port

        rakha res1 = http.get(base + "/allowed")
        dekha res1.status
        dekha res1.body

        rakha res2 = http.get(base + "/blocked")
        dekha res2.status
        dekha res2.body

        app.stop()
        """
        out = self.run_ast(code)
        self.assertEqual(out, [
            "200",
            "Access granted",
            "403",
            "Blocked by middleware",
        ])

    def test_web_routes_vm(self):
        code = """
        aayaat std.web

        rakha app = web.app()

        app.get("/hello", kaam(req) {
            farka "Sikhar VM Web App"
        })

        rakha res = app.handle({"method": "GET", "path": "/hello"})
        dekha res.status
        dekha res.body
        """
        out = self.run_vm(code)
        self.assertEqual(out, ["200", "Sikhar VM Web App"])


if __name__ == "__main__":
    unittest.main()
