import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sikhar.lexer import Lexer
from sikhar.parser import Parser
from sikhar.interpreter import Interpreter
from sikhar.vm import Compiler, VM


class TestDB(unittest.TestCase):
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

    def test_database_sqlite_ast(self):
        code = """
        aayaat std.db

        rakha conn = db.connect(":memory:")
        conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, role TEXT)")
        conn.execute("INSERT INTO users (name, role) VALUES (?, ?)", ["Manoj", "Developer"])
        conn.execute("INSERT INTO users (name, role) VALUES (?, ?)", ["Aarav", "Designer"])

        rakha users = conn.query("SELECT * FROM users ORDER BY id ASC")
        dekha lamba(users)
        dekha users[0]["name"]
        dekha users[0]["role"]
        dekha users[1]["name"]

        rakha single = conn.query_one("SELECT * FROM users WHERE name = ?", ["Manoj"])
        dekha single["role"]

        conn.close()
        """
        out = self.run_ast(code)
        self.assertEqual(out, ["2", "Manoj", "Developer", "Aarav", "Developer"])

    def test_database_sqlite_vm(self):
        code = """
        aayaat std.db

        rakha conn = db.joda(":memory:")
        conn.chalaau("CREATE TABLE items (id INTEGER PRIMARY KEY, title TEXT)")
        conn.chalaau("INSERT INTO items (title) VALUES (?)", ["Everest"])

        rakha rows = conn.khoja("SELECT * FROM items")
        dekha rows[0]["title"]

        conn.banda()
        """
        out = self.run_vm(code)
        self.assertEqual(out, ["Everest"])


if __name__ == "__main__":
    unittest.main()
