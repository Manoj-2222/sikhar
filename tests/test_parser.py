import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from sikhar.lexer import Lexer
from sikhar.parser import (
    Parser,
    Program,
    VariableDeclaration,
    ConstantDeclaration,
    Assignment,
    IfStatement,
    WhileStatement,
    ForStatement,
    FunctionDeclaration,
    ReturnStatement,
    TryStatement,
    ThrowStatement,
    BinaryExpression,
    UnaryExpression,
    Literal,
    Identifier,
    ListLiteral,
    MapLiteral,
    IndexExpression,
)
from sikhar.errors.error_types import SikharSyntaxError


class TestParser(unittest.TestCase):
    def parse_snippet(self, code: str) -> Program:
        tokens = Lexer(code, "test.sk").tokenize()
        return Parser(tokens, code, "test.sk").parse()

    def test_variable_and_constant_declarations(self):
        prog = self.parse_snippet("rakha a = 10\nsthayi b: number = 20")
        self.assertEqual(len(prog.statements), 2)

        v_decl = prog.statements[0]
        self.assertIsInstance(v_decl, VariableDeclaration)
        self.assertEqual(v_decl.name, "a")
        self.assertIsNone(v_decl.type_annotation)
        self.assertEqual(v_decl.initializer.value, 10)

        c_decl = prog.statements[1]
        self.assertIsInstance(c_decl, ConstantDeclaration)
        self.assertEqual(c_decl.name, "b")
        self.assertEqual(c_decl.type_annotation, "number")
        self.assertEqual(c_decl.initializer.value, 20)

    def test_operator_precedence(self):
        # 2 + 3 * 4 -> 2 + (3 * 4)
        prog = self.parse_snippet("rakha res = 2 + 3 * 4")
        decl = prog.statements[0]
        bin_expr = decl.initializer
        self.assertIsInstance(bin_expr, BinaryExpression)
        self.assertEqual(bin_expr.operator, "+")
        self.assertEqual(bin_expr.left.value, 2)
        self.assertEqual(bin_expr.right.operator, "*")

    def test_if_athawa_natra(self):
        code = """
        yadi x > 10 {
            dekha "big"
        } athawa x > 5 {
            dekha "medium"
        } natra {
            dekha "small"
        }
        """
        prog = self.parse_snippet(code)
        if_stmt = prog.statements[0]
        self.assertIsInstance(if_stmt, IfStatement)
        self.assertEqual(len(if_stmt.elif_branches), 1)
        self.assertIsNotNone(if_stmt.else_branch)

    def test_loops(self):
        code = """
        jaba i < 10 {
            badla i = i + 1
        }
        ko_lagi x ma items {
            rok
            jaari
        }
        """
        prog = self.parse_snippet(code)
        self.assertIsInstance(prog.statements[0], WhileStatement)
        self.assertIsInstance(prog.statements[1], ForStatement)
        self.assertEqual(prog.statements[1].var_name, "x")

    def test_functions_and_returns(self):
        code = "kaam add(x, y) { farka x + y }"
        prog = self.parse_snippet(code)
        fn_decl = prog.statements[0]
        self.assertIsInstance(fn_decl, FunctionDeclaration)
        self.assertEqual(fn_decl.name, "add")
        self.assertEqual(fn_decl.parameters, ["x", "y"])
        self.assertIsInstance(fn_decl.body.statements[0], ReturnStatement)

    def test_collections_parsing(self):
        code = """
        rakha lst = [1, "two", sacho]
        rakha mp = {"key": 42}
        rakha elem = lst[0]
        """
        prog = self.parse_snippet(code)
        self.assertIsInstance(prog.statements[0].initializer, ListLiteral)
        self.assertIsInstance(prog.statements[1].initializer, MapLiteral)
        self.assertIsInstance(prog.statements[2].initializer, IndexExpression)

    def test_try_catch_and_throw(self):
        code = """
        koshish {
            fal "err"
        } samata e {
            dekha e
        }
        """
        prog = self.parse_snippet(code)
        try_stmt = prog.statements[0]
        self.assertIsInstance(try_stmt, TryStatement)
        self.assertEqual(try_stmt.catch_var, "e")
        self.assertIsInstance(try_stmt.try_block.statements[0], ThrowStatement)

    def test_reserved_future_keyword_syntax_error(self):
        code = "varg Animal {}"
        with self.assertRaises(SikharSyntaxError) as ctx:
            self.parse_snippet(code)
        self.assertIn("reserved", str(ctx.exception).lower())


if __name__ == "__main__":
    unittest.main()
