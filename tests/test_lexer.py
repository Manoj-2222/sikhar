import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from sikhar.lexer import Lexer, TokenType, Token
from sikhar.errors.error_types import SikharSyntaxError


class TestLexer(unittest.TestCase):
    def test_numbers_and_decimals(self):
        lexer = Lexer("10 99.50 0 123.456")
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].value, 10)
        self.assertEqual(tokens[1].type, TokenType.DECIMAL)
        self.assertEqual(tokens[1].value, 99.50)
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[2].value, 0)
        self.assertEqual(tokens[3].type, TokenType.DECIMAL)
        self.assertEqual(tokens[3].value, 123.456)

    def test_strings_and_escapes(self):
        lexer = Lexer(r'"Hello\nWorld\t\"Sikhar\"\\"')
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.TEXT)
        self.assertEqual(tokens[0].value, 'Hello\nWorld\t"Sikhar"\\')

    def test_unterminated_string_raises_syntax_error(self):
        lexer = Lexer('"Unclosed string')
        with self.assertRaises(SikharSyntaxError):
            lexer.tokenize()

    def test_keywords_and_booleans(self):
        src = "rakha badla sthayi sacho jutho khali yadi athawa natra jaba ko_lagi ma rok jaari kaam farka koshish samata fal"
        tokens = Lexer(src).tokenize()
        expected = [
            TokenType.RAKHA, TokenType.BADLA, TokenType.STHAYI,
            TokenType.BOOLEAN, TokenType.BOOLEAN, TokenType.NULL,
            TokenType.YADI, TokenType.ATHAWA, TokenType.NATRA,
            TokenType.JABA, TokenType.KO_LAGI, TokenType.MA,
            TokenType.ROK, TokenType.JAARI, TokenType.KAAM, TokenType.FARKA,
            TokenType.KOSHISH, TokenType.SAMATA, TokenType.FAL,
        ]
        actual = [t.type for t in tokens if t.type != TokenType.EOF]
        self.assertEqual(actual, expected)
        # Check boolean & null values
        self.assertEqual(tokens[3].value, True)
        self.assertEqual(tokens[4].value, False)
        self.assertIsNone(tokens[5].value)

    def test_operators(self):
        src = "+ - * / % == != < <= > >= = and or not"
        tokens = Lexer(src).tokenize()
        expected = [
            TokenType.PLUS, TokenType.MINUS, TokenType.STAR, TokenType.SLASH, TokenType.PERCENT,
            TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL,
            TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.EQUAL,
            TokenType.AND, TokenType.OR, TokenType.NOT,
        ]
        actual = [t.type for t in tokens if t.type != TokenType.EOF]
        self.assertEqual(actual, expected)

    def test_comments_ignored(self):
        src = "# This is a comment\nrakha x = 10 # Another comment\n"
        tokens = Lexer(src).tokenize()
        types = [t.type for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.EOF)]
        self.assertEqual(types, [TokenType.RAKHA, TokenType.IDENTIFIER, TokenType.EQUAL, TokenType.NUMBER])

    def test_line_and_column_tracking(self):
        src = "rakha\n  x = 10"
        tokens = Lexer(src).tokenize()
        tok_rakha = tokens[0]
        self.assertEqual(tok_rakha.line, 1)
        self.assertEqual(tok_rakha.column, 1)

        tok_x = tokens[2]  # tokens[1] is NEWLINE
        self.assertEqual(tok_x.line, 2)
        self.assertEqual(tok_x.column, 3)

    def test_unexpected_character(self):
        with self.assertRaises(SikharSyntaxError):
            Lexer("@").tokenize()


if __name__ == "__main__":
    unittest.main()
