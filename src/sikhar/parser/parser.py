"""
Sikhar Parser
Parses a list of tokens into an Abstract Syntax Tree (AST).
"""

from typing import List, Optional, Tuple
from ..lexer.token import Token
from ..lexer.token_type import TokenType, RESERVED_FUTURE_KEYWORDS, KEYWORDS
from ..errors.error_types import SikharSyntaxError
from .ast_nodes import (
    Program,
    Statement,
    Expression,
    Block,
    VariableDeclaration,
    ConstantDeclaration,
    Assignment,
    DekhaStatement,
    IfStatement,
    WhileStatement,
    ForStatement,
    BreakStatement,
    ContinueStatement,
    FunctionDeclaration,
    ReturnStatement,
    TryStatement,
    ThrowStatement,
    ExpressionStatement,
    Literal,
    Identifier,
    BinaryExpression,
    UnaryExpression,
    FunctionCall,
    ListLiteral,
    MapLiteral,
    IndexExpression,
    MemberExpression,
    ImportExpression,
    ExportStatement,
    AssertStatement,
)


class Parser:
    def __init__(self, tokens: List[Token], source: str = "", filename: str = "<stdin>"):
        self.tokens = tokens
        self.source = source
        self.filename = filename
        self.pos = 0

    def _current(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def _peek(self, offset: int = 1) -> Token:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]

    def _is_at_end(self) -> bool:
        return self._current().type == TokenType.EOF

    def _advance(self) -> Token:
        tok = self._current()
        if not self._is_at_end():
            self.pos += 1
        return tok

    def _check(self, tok_type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._current().type == tok_type

    def _match(self, *tok_types: TokenType) -> bool:
        for t in tok_types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _consume(self, tok_type: TokenType, error_msg: str) -> Token:
        if self._check(tok_type):
            return self._advance()
        curr = self._current()
        line_content = self._get_source_line(curr.line)
        raise SikharSyntaxError(
            error_msg,
            filename=self.filename,
            line=curr.line,
            column=curr.column,
            source_line=line_content,
        )

    def _get_source_line(self, line_no: int) -> Optional[str]:
        if not self.source:
            return None
        lines = self.source.splitlines()
        if 1 <= line_no <= len(lines):
            return lines[line_no - 1]
        return None

    def _skip_newlines(self) -> None:
        while self._check(TokenType.NEWLINE):
            self._advance()

    def parse(self) -> Program:
        statements: List[Statement] = []
        self._skip_newlines()

        while not self._is_at_end():
            stmt = self._parse_statement()
            if stmt is not None:
                statements.append(stmt)
            self._skip_newlines()

        return Program(
            line=1 if not statements else statements[0].line,
            column=1 if not statements else statements[0].column,
            statements=statements,
        )

    def _parse_statement(self) -> Statement:
        self._skip_newlines()
        curr = self._current()

        # Check for reserved keywords and provide helpful error
        if curr.type in RESERVED_FUTURE_KEYWORDS:
            explanation = RESERVED_FUTURE_KEYWORDS[curr.type]
            line_content = self._get_source_line(curr.line)
            raise SikharSyntaxError(
                f"Keyword '{curr.value}' is reserved. {explanation}",
                filename=self.filename,
                line=curr.line,
                column=curr.column,
                source_line=line_content,
            )

        if curr.type == TokenType.RAKHA:
            return self._parse_var_declaration()
        elif curr.type == TokenType.STHAYI:
            return self._parse_const_declaration()
        elif curr.type == TokenType.BADLA:
            return self._parse_badla_assignment()
        elif curr.type == TokenType.DEKHA:
            return self._parse_dekha_statement()
        elif curr.type == TokenType.YADI:
            return self._parse_if_statement()
        elif curr.type == TokenType.JABA:
            return self._parse_while_statement()
        elif curr.type == TokenType.KO_LAGI:
            return self._parse_for_statement()
        elif curr.type == TokenType.ROK:
            self._advance()
            return BreakStatement(line=curr.line, column=curr.column)
        elif curr.type == TokenType.JAARI:
            self._advance()
            return ContinueStatement(line=curr.line, column=curr.column)
        elif curr.type == TokenType.KAAM:
            return self._parse_function_declaration()
        elif curr.type == TokenType.FARKA:
            return self._parse_return_statement()
        elif curr.type == TokenType.KOSHISH:
            return self._parse_try_catch_statement()
        elif curr.type == TokenType.FAL:
            return self._parse_throw_statement()
        elif curr.type == TokenType.PATHAAU:
            return self._parse_export_statement()
        elif curr.type == TokenType.JAACH:
            return self._parse_assert_statement()
        else:
            return self._parse_expression_or_assignment()

    def _parse_var_declaration(self) -> VariableDeclaration:
        tok = self._advance()  # Consume 'rakha'
        name_tok = self._consume(TokenType.IDENTIFIER, "Expected variable name after 'rakha'")
        type_annot = None

        if self._match(TokenType.COLON):
            type_tok = self._consume(TokenType.IDENTIFIER, "Expected type name after ':'")
            type_annot = str(type_tok.value)

        initializer = None
        if self._match(TokenType.EQUAL):
            initializer = self._parse_expression()

        return VariableDeclaration(
            line=tok.line,
            column=tok.column,
            name=str(name_tok.value),
            type_annotation=type_annot,
            initializer=initializer,
        )

    def _parse_const_declaration(self) -> ConstantDeclaration:
        tok = self._advance()  # Consume 'sthayi'
        name_tok = self._consume(TokenType.IDENTIFIER, "Expected constant name after 'sthayi'")
        type_annot = None

        if self._match(TokenType.COLON):
            type_tok = self._consume(TokenType.IDENTIFIER, "Expected type name after ':'")
            type_annot = str(type_tok.value)

        self._consume(TokenType.EQUAL, "Constant declaration requires an initializer '='")
        initializer = self._parse_expression()

        return ConstantDeclaration(
            line=tok.line,
            column=tok.column,
            name=str(name_tok.value),
            type_annotation=type_annot,
            initializer=initializer,
        )

    def _parse_badla_assignment(self) -> Assignment:
        tok = self._advance()  # Consume 'badla'
        target = self._parse_postfix()
        self._consume(TokenType.EQUAL, "Expected '=' in assignment")
        val = self._parse_expression()
        return Assignment(line=tok.line, column=tok.column, target=target, value=val)

    def _parse_export_statement(self) -> ExportStatement:
        tok = self._advance()  # Consume 'pathaau'
        curr = self._current()
        if curr.type in (TokenType.KAAM, TokenType.RAKHA, TokenType.STHAYI):
            decl = self._parse_statement()
            return ExportStatement(line=tok.line, column=tok.column, declaration=decl)
        elif curr.type == TokenType.IDENTIFIER:
            id_tok = self._advance()
            return ExportStatement(line=tok.line, column=tok.column, symbol_name=str(id_tok.value))
        else:
            line_content = self._get_source_line(tok.line)
            raise SikharSyntaxError(
                "Expected declaration or identifier after 'pathaau'",
                filename=self.filename,
                line=tok.line,
                column=tok.column,
                source_line=line_content,
            )

    def _parse_assert_statement(self) -> AssertStatement:
        tok = self._advance()  # Consume 'jaach'
        cond = self._parse_expression()
        msg = None
        if self._match(TokenType.COMMA):
            msg = self._parse_expression()
        return AssertStatement(line=tok.line, column=tok.column, condition=cond, message=msg)

    def _parse_import_expression(self) -> ImportExpression:
        tok = self.tokens[self.pos - 1]  # 'aayaat' token
        if self._check(TokenType.TEXT):
            path_tok = self._advance()
            return ImportExpression(line=tok.line, column=tok.column, module_path=str(path_tok.value), is_std=False)
        elif self._check(TokenType.IDENTIFIER):
            parts = [str(self._advance().value)]
            while self._match(TokenType.DOT):
                id_tok = self._consume(TokenType.IDENTIFIER, "Expected identifier after '.' in module path")
                parts.append(str(id_tok.value))
            path_str = ".".join(parts)
            is_std = path_str.startswith("std.") or path_str == "std"
            return ImportExpression(line=tok.line, column=tok.column, module_path=path_str, is_std=is_std)
        else:
            line_content = self._get_source_line(tok.line)
            raise SikharSyntaxError(
                "Expected module string or dot-path after 'aayaat'",
                filename=self.filename,
                line=tok.line,
                column=tok.column,
                source_line=line_content,
            )

    def _parse_dekha_statement(self) -> DekhaStatement:
        tok = self._advance()  # Consume 'dekha'
        expr = self._parse_expression()
        return DekhaStatement(line=tok.line, column=tok.column, expression=expr)

    def _parse_if_statement(self) -> IfStatement:
        tok = self._advance()  # Consume 'yadi'
        condition = self._parse_expression()
        then_block = self._parse_block()

        elif_branches: List[Tuple[Expression, Block]] = []
        else_block = None

        # Optional newlines before athawa / natra
        self._skip_newlines()

        while self._check(TokenType.ATHAWA):
            self._advance()  # Consume 'athawa'
            elif_cond = self._parse_expression()
            elif_body = self._parse_block()
            elif_branches.append((elif_cond, elif_body))
            self._skip_newlines()

        if self._check(TokenType.NATRA):
            self._advance()  # Consume 'natra'
            else_block = self._parse_block()

        return IfStatement(
            line=tok.line,
            column=tok.column,
            condition=condition,
            then_branch=then_block,
            elif_branches=elif_branches,
            else_branch=else_block,
        )

    def _parse_while_statement(self) -> WhileStatement:
        tok = self._advance()  # Consume 'jaba'
        cond = self._parse_expression()
        body = self._parse_block()
        return WhileStatement(line=tok.line, column=tok.column, condition=cond, body=body)

    def _parse_for_statement(self) -> ForStatement:
        tok = self._advance()  # Consume 'ko_lagi'
        var_tok = self._consume(TokenType.IDENTIFIER, "Expected loop variable after 'ko_lagi'")
        self._consume(TokenType.MA, "Expected 'ma' after loop variable in 'ko_lagi'")
        iterable = self._parse_expression()
        body = self._parse_block()
        return ForStatement(
            line=tok.line,
            column=tok.column,
            var_name=str(var_tok.value),
            iterable=iterable,
            body=body,
        )

    def _parse_function_declaration(self) -> FunctionDeclaration:
        tok = self._advance()  # Consume 'kaam'
        name_tok = self._consume(TokenType.IDENTIFIER, "Expected function name after 'kaam'")
        self._consume(TokenType.LPAREN, "Expected '(' after function name")
        params: List[str] = []

        if not self._check(TokenType.RPAREN):
            param_tok = self._consume(TokenType.IDENTIFIER, "Expected parameter name")
            params.append(str(param_tok.value))
            while self._match(TokenType.COMMA):
                param_tok = self._consume(TokenType.IDENTIFIER, "Expected parameter name after ','")
                params.append(str(param_tok.value))

        self._consume(TokenType.RPAREN, "Expected ')' after parameters")
        body = self._parse_block()

        return FunctionDeclaration(
            line=tok.line,
            column=tok.column,
            name=str(name_tok.value),
            parameters=params,
            body=body,
        )

    def _parse_return_statement(self) -> ReturnStatement:
        tok = self._advance()  # Consume 'farka'
        val = None
        if not self._check(TokenType.NEWLINE) and not self._check(TokenType.RBRACE) and not self._is_at_end():
            val = self._parse_expression()
        return ReturnStatement(line=tok.line, column=tok.column, value=val)

    def _parse_try_catch_statement(self) -> TryStatement:
        tok = self._advance()  # Consume 'koshish'
        try_block = self._parse_block()
        self._skip_newlines()
        self._consume(TokenType.SAMATA, "Expected 'samata' after try block")

        catch_var = None
        if self._check(TokenType.IDENTIFIER):
            catch_var = str(self._advance().value)

        catch_block = self._parse_block()
        return TryStatement(
            line=tok.line,
            column=tok.column,
            try_block=try_block,
            catch_var=catch_var,
            catch_block=catch_block,
        )

    def _parse_throw_statement(self) -> ThrowStatement:
        tok = self._advance()  # Consume 'fal'
        expr = self._parse_expression()
        return ThrowStatement(line=tok.line, column=tok.column, expression=expr)

    def _parse_expression_or_assignment(self) -> Statement:
        expr = self._parse_expression()
        # Check if direct assignment: target = val
        if self._match(TokenType.EQUAL):
            val = self._parse_expression()
            return Assignment(line=expr.line, column=expr.column, target=expr, value=val)
        return ExpressionStatement(line=expr.line, column=expr.column, expression=expr)

    def _parse_block(self) -> Block:
        self._skip_newlines()
        start_tok = self._consume(TokenType.LBRACE, "Expected '{' to start block")
        stmts: List[Statement] = []
        self._skip_newlines()

        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt is not None:
                stmts.append(stmt)
            self._skip_newlines()

        self._consume(TokenType.RBRACE, "Expected '}' to close block")
        return Block(line=start_tok.line, column=start_tok.column, statements=stmts)

    # ==========================================
    # Expression Parsing (Precedence hierarchy)
    # ==========================================

    def _parse_expression(self) -> Expression:
        return self._parse_logical_or()

    def _parse_logical_or(self) -> Expression:
        expr = self._parse_logical_and()
        while self._match(TokenType.OR):
            op = "or"
            right = self._parse_logical_and()
            expr = BinaryExpression(line=expr.line, column=expr.column, left=expr, operator=op, right=right)
        return expr

    def _parse_logical_and(self) -> Expression:
        expr = self._parse_equality()
        while self._match(TokenType.AND):
            op = "and"
            right = self._parse_equality()
            expr = BinaryExpression(line=expr.line, column=expr.column, left=expr, operator=op, right=right)
        return expr

    def _parse_equality(self) -> Expression:
        expr = self._parse_comparison()
        while self._match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            prev = self.tokens[self.pos - 1]
            right = self._parse_comparison()
            expr = BinaryExpression(line=expr.line, column=expr.column, left=expr, operator=str(prev.value), right=right)
        return expr

    def _parse_comparison(self) -> Expression:
        expr = self._parse_term()
        while self._match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            prev = self.tokens[self.pos - 1]
            right = self._parse_term()
            expr = BinaryExpression(line=expr.line, column=expr.column, left=expr, operator=str(prev.value), right=right)
        return expr

    def _parse_term(self) -> Expression:
        expr = self._parse_factor()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            prev = self.tokens[self.pos - 1]
            right = self._parse_factor()
            expr = BinaryExpression(line=expr.line, column=expr.column, left=expr, operator=str(prev.value), right=right)
        return expr

    def _parse_factor(self) -> Expression:
        expr = self._parse_unary()
        while self._match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            prev = self.tokens[self.pos - 1]
            right = self._parse_unary()
            expr = BinaryExpression(line=expr.line, column=expr.column, left=expr, operator=str(prev.value), right=right)
        return expr

    def _parse_unary(self) -> Expression:
        if self._match(TokenType.NOT, TokenType.MINUS):
            tok = self.tokens[self.pos - 1]
            op = "not" if tok.type == TokenType.NOT else "-"
            operand = self._parse_unary()
            return UnaryExpression(line=tok.line, column=tok.column, operator=op, operand=operand)
        return self._parse_postfix()

    def _parse_postfix(self) -> Expression:
        expr = self._parse_primary()

        while True:
            if self._match(TokenType.LPAREN):
                # Function call
                args: List[Expression] = []
                if not self._check(TokenType.RPAREN):
                    args.append(self._parse_expression())
                    while self._match(TokenType.COMMA):
                        args.append(self._parse_expression())
                rparen = self._consume(TokenType.RPAREN, "Expected ')' after arguments")
                expr = FunctionCall(line=expr.line, column=expr.column, callee=expr, arguments=args)
            elif self._match(TokenType.LBRACKET):
                # Indexing
                idx = self._parse_expression()
                self._consume(TokenType.RBRACKET, "Expected ']' after index")
                expr = IndexExpression(line=expr.line, column=expr.column, target=expr, index=idx)
            elif self._match(TokenType.DOT):
                # Member access e.g. math.sqrt or file.hatau
                curr = self._current()
                if curr.type == TokenType.IDENTIFIER or curr.type in KEYWORDS.values():
                    prop_tok = self._advance()
                else:
                    prop_tok = self._consume(TokenType.IDENTIFIER, "Expected property name after '.'")
                expr = MemberExpression(line=expr.line, column=expr.column, target=expr, property_name=str(prop_tok.value))
            else:
                break

        return expr

    def _parse_primary(self) -> Expression:
        curr = self._current()

        if self._match(TokenType.NUMBER):
            return Literal(line=curr.line, column=curr.column, value=curr.value, literal_type="number")

        if self._match(TokenType.DECIMAL):
            return Literal(line=curr.line, column=curr.column, value=curr.value, literal_type="decimal")

        if self._match(TokenType.TEXT):
            return Literal(line=curr.line, column=curr.column, value=curr.value, literal_type="text")

        if self._match(TokenType.BOOLEAN):
            return Literal(line=curr.line, column=curr.column, value=curr.value, literal_type="boolean")

        if self._match(TokenType.NULL):
            return Literal(line=curr.line, column=curr.column, value=None, literal_type="null")

        if self._match(TokenType.IDENTIFIER):
            return Identifier(line=curr.line, column=curr.column, name=str(curr.value))

        if self._match(TokenType.SODHA):
            # Builtin sodha keyword used as expression/callee
            return Identifier(line=curr.line, column=curr.column, name="sodha")

        if self._match(TokenType.DEKHA):
            # Builtin dekha keyword used as expression/callee
            return Identifier(line=curr.line, column=curr.column, name="dekha")

        if self._match(TokenType.AAYAAT):
            return self._parse_import_expression()

        if self._match(TokenType.LPAREN):
            expr = self._parse_expression()
            self._consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr

        if self._match(TokenType.LBRACKET):
            # List literal [elem1, elem2]
            elements: List[Expression] = []
            self._skip_newlines()
            if not self._check(TokenType.RBRACKET):
                elements.append(self._parse_expression())
                self._skip_newlines()
                while self._match(TokenType.COMMA):
                    self._skip_newlines()
                    if self._check(TokenType.RBRACKET):
                        break
                    elements.append(self._parse_expression())
                    self._skip_newlines()
            self._consume(TokenType.RBRACKET, "Expected ']' after list elements")
            return ListLiteral(line=curr.line, column=curr.column, elements=elements)

        if self._match(TokenType.LBRACE):
            # Map literal {"key": val, ...}
            entries: List[Tuple[Expression, Expression]] = []
            self._skip_newlines()
            if not self._check(TokenType.RBRACE):
                key = self._parse_expression()
                self._consume(TokenType.COLON, "Expected ':' after map key")
                val = self._parse_expression()
                entries.append((key, val))
                self._skip_newlines()
                while self._match(TokenType.COMMA):
                    self._skip_newlines()
                    if self._check(TokenType.RBRACE):
                        break
                    key = self._parse_expression()
                    self._consume(TokenType.COLON, "Expected ':' after map key")
                    val = self._parse_expression()
                    entries.append((key, val))
                    self._skip_newlines()
            self._consume(TokenType.RBRACE, "Expected '}' after map entries")
            return MapLiteral(line=curr.line, column=curr.column, entries=entries)

        line_content = self._get_source_line(curr.line)
        raise SikharSyntaxError(
            f"Unexpected token '{curr.value}'",
            filename=self.filename,
            line=curr.line,
            column=curr.column,
            source_line=line_content,
        )
