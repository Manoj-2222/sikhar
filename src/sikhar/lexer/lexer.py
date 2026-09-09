"""
Sikhar Lexer
Transforms source code into a stream of tokens with accurate line/column tracking.
"""

from typing import List, Optional
from .token_type import TokenType, KEYWORDS
from .token import Token
from ..errors.error_types import SikharSyntaxError


class Lexer:
    def __init__(self, source: str, filename: str = "<stdin>"):
        self.source = source
        self.filename = filename
        self.length = len(source)
        self.index = 0
        self.line = 1
        self.column = 1

    def _peek(self, offset: int = 0) -> Optional[str]:
        pos = self.index + offset
        if pos < self.length:
            return self.source[pos]
        return None

    def _advance(self) -> Optional[str]:
        if self.index >= self.length:
            return None
        ch = self.source[self.index]
        self.index += 1
        if ch == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []

        while self.index < self.length:
            ch = self._peek()

            # Skip spaces, tabs, carriage returns
            if ch in (' ', '\t', '\r'):
                self._advance()
                continue

            # Skip comments (# ...)
            if ch == '#':
                while self._peek() is not None and self._peek() != '\n':
                    self._advance()
                continue

            # Handle newlines
            if ch == '\n':
                line = self.line
                col = self.column
                self._advance()
                # Deduplicate consecutive newlines
                if tokens and tokens[-1].type == TokenType.NEWLINE:
                    continue
                tokens.append(Token(TokenType.NEWLINE, '\n', line, col, 1, self.filename))
                continue

            # Track start position for token
            start_line = self.line
            start_col = self.column
            start_index = self.index

            # Numbers (integer and decimal)
            if ch.isdigit():
                tokens.append(self._lex_number(start_line, start_col))
                continue

            # Strings
            if ch == '"':
                tokens.append(self._lex_string(start_line, start_col))
                continue

            # Identifiers and keywords
            if ch.isalpha() or ch == '_' or ord(ch) > 127:
                tokens.append(self._lex_identifier(start_line, start_col))
                continue

            # Two-character operators
            next_ch = self._peek(1)
            two_char = ch + (next_ch if next_ch else "")

            if two_char == "==":
                self._advance()
                self._advance()
                tokens.append(Token(TokenType.EQUAL_EQUAL, "==", start_line, start_col, 2, self.filename))
                continue
            elif two_char == "!=":
                self._advance()
                self._advance()
                tokens.append(Token(TokenType.BANG_EQUAL, "!=", start_line, start_col, 2, self.filename))
                continue
            elif two_char == "<=":
                self._advance()
                self._advance()
                tokens.append(Token(TokenType.LESS_EQUAL, "<=", start_line, start_col, 2, self.filename))
                continue
            elif two_char == ">=":
                self._advance()
                self._advance()
                tokens.append(Token(TokenType.GREATER_EQUAL, ">=", start_line, start_col, 2, self.filename))
                continue

            # Single-character tokens
            single_map = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.STAR,
                '/': TokenType.SLASH,
                '%': TokenType.PERCENT,
                '=': TokenType.EQUAL,
                '<': TokenType.LESS,
                '>': TokenType.GREATER,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                ',': TokenType.COMMA,
                ':': TokenType.COLON,
                ';': TokenType.SEMICOLON,
                '.': TokenType.DOT,
            }

            if ch in single_map:
                self._advance()
                tokens.append(Token(single_map[ch], ch, start_line, start_col, 1, self.filename))
                continue

            # Unexpected character
            line_content = self.source.splitlines()[start_line - 1] if self.source.splitlines() else ch
            raise SikharSyntaxError(
                f"Unexpected character '{ch}'",
                filename=self.filename,
                line=start_line,
                column=start_col,
                source_line=line_content,
            )

        tokens.append(Token(TokenType.EOF, "", self.line, self.column, 0, self.filename))
        return tokens

    def _lex_number(self, start_line: int, start_col: int) -> Token:
        chars = []
        is_decimal = False

        while self._peek() is not None and self._peek().isdigit():
            chars.append(self._advance())

        if self._peek() == '.' and self._peek(1) is not None and self._peek(1).isdigit():
            is_decimal = True
            chars.append(self._advance())  # Consume '.'
            while self._peek() is not None and self._peek().isdigit():
                chars.append(self._advance())

        num_str = "".join(chars)
        length = len(num_str)
        if is_decimal:
            return Token(TokenType.DECIMAL, float(num_str), start_line, start_col, length, self.filename)
        return Token(TokenType.NUMBER, int(num_str), start_line, start_col, length, self.filename)

    def _lex_string(self, start_line: int, start_col: int) -> Token:
        self._advance()  # Skip opening quote "
        chars = []

        while self._peek() is not None and self._peek() != '"':
            ch = self._advance()
            if ch == '\\':
                escape_ch = self._advance()
                if escape_ch is None:
                    break
                if escape_ch == 'n':
                    chars.append('\n')
                elif escape_ch == 't':
                    chars.append('\t')
                elif escape_ch == 'r':
                    chars.append('\r')
                elif escape_ch == '"':
                    chars.append('"')
                elif escape_ch == '\\':
                    chars.append('\\')
                else:
                    chars.append(escape_ch)
            elif ch == '\n':
                # Unterminated string on current line
                line_content = self.source.splitlines()[start_line - 1]
                raise SikharSyntaxError(
                    "Unterminated string literal",
                    filename=self.filename,
                    line=start_line,
                    column=start_col,
                    source_line=line_content,
                )
            else:
                chars.append(ch)

        if self._peek() != '"':
            line_content = self.source.splitlines()[start_line - 1] if self.source.splitlines() else ""
            raise SikharSyntaxError(
                "Unterminated string literal at end of input",
                filename=self.filename,
                line=start_line,
                column=start_col,
                source_line=line_content,
            )

        self._advance()  # Skip closing quote "
        str_val = "".join(chars)
        # Length including quotes
        length = len(str_val) + 2
        return Token(TokenType.TEXT, str_val, start_line, start_col, length, self.filename)

    def _lex_identifier(self, start_line: int, start_col: int) -> Token:
        chars = []
        while self._peek() is not None:
            ch = self._peek()
            if ch.isalnum() or ch == '_' or ord(ch) > 127:
                chars.append(self._advance())
            else:
                break

        word = "".join(chars)
        length = len(word)

        if word in KEYWORDS:
            tok_type = KEYWORDS[word]
            if tok_type == TokenType.SACHO:
                return Token(TokenType.BOOLEAN, True, start_line, start_col, length, self.filename)
            elif tok_type == TokenType.JUTHO:
                return Token(TokenType.BOOLEAN, False, start_line, start_col, length, self.filename)
            elif tok_type == TokenType.KHALI:
                return Token(TokenType.NULL, None, start_line, start_col, length, self.filename)
            return Token(tok_type, word, start_line, start_col, length, self.filename)

        return Token(TokenType.IDENTIFIER, word, start_line, start_col, length, self.filename)
