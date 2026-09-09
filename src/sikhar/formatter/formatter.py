"""
Sikhar Code Formatter
Deterministic AST pretty-printer for Sikhar source code.
"""

from typing import Any, List, Optional
from ..parser.ast_nodes import (
    ASTNode,
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
from ..lexer.lexer import Lexer
from ..parser.parser import Parser


class Formatter:
    def __init__(self, indent_size: int = 4):
        self.indent_size = indent_size

    def format_code(self, source: str, filename: str = "<stdin>") -> str:
        """Parse and re-format source code deterministically."""
        tokens = Lexer(source, filename).tokenize()
        program = Parser(tokens, source, filename).parse()
        return self.format_ast(program)

    def format_ast(self, program: Program) -> str:
        lines: List[str] = []
        for i, stmt in enumerate(program.statements):
            # Extra blank line before function declarations
            if i > 0 and isinstance(stmt, FunctionDeclaration):
                lines.append("")
            lines.append(self._format_statement(stmt, 0))
            if isinstance(stmt, FunctionDeclaration) and i < len(program.statements) - 1:
                lines.append("")
        # Remove consecutive blank lines
        cleaned: List[str] = []
        for line in lines:
            if not line.strip() and cleaned and not cleaned[-1].strip():
                continue
            cleaned.append(line)
        return "\n".join(cleaned) + "\n"

    def _indent(self, level: int) -> str:
        return " " * (self.indent_size * level)

    def _format_statement(self, stmt: Statement, level: int) -> str:
        indent = self._indent(level)

        if isinstance(stmt, VariableDeclaration):
            annot = f": {stmt.type_annotation}" if stmt.type_annotation else ""
            if stmt.initializer is not None:
                init_str = self._format_expression(stmt.initializer)
                return f"{indent}rakha {stmt.name}{annot} = {init_str}"
            return f"{indent}rakha {stmt.name}{annot}"

        elif isinstance(stmt, ConstantDeclaration):
            annot = f": {stmt.type_annotation}" if stmt.type_annotation else ""
            init_str = self._format_expression(stmt.initializer)
            return f"{indent}sthayi {stmt.name}{annot} = {init_str}"

        elif isinstance(stmt, Assignment):
            target_str = self._format_expression(stmt.target)
            val_str = self._format_expression(stmt.value)
            return f"{indent}badla {target_str} = {val_str}"

        elif isinstance(stmt, DekhaStatement):
            expr_str = self._format_expression(stmt.expression)
            return f"{indent}dekha {expr_str}"

        elif isinstance(stmt, IfStatement):
            cond_str = self._format_expression(stmt.condition)
            lines = [f"{indent}yadi {cond_str} {{"]
            lines.extend(self._format_block_lines(stmt.then_branch, level + 1))

            for elif_cond, elif_block in stmt.elif_branches:
                elif_cond_str = self._format_expression(elif_cond)
                lines.append(f"{indent}}} athawa {elif_cond_str} {{")
                lines.extend(self._format_block_lines(elif_block, level + 1))

            if stmt.else_branch is not None:
                lines.append(f"{indent}}} natra {{")
                lines.extend(self._format_block_lines(stmt.else_branch, level + 1))

            lines.append(f"{indent}}}")
            return "\n".join(lines)

        elif isinstance(stmt, WhileStatement):
            cond_str = self._format_expression(stmt.condition)
            lines = [f"{indent}jaba {cond_str} {{"]
            lines.extend(self._format_block_lines(stmt.body, level + 1))
            lines.append(f"{indent}}}")
            return "\n".join(lines)

        elif isinstance(stmt, ForStatement):
            iter_str = self._format_expression(stmt.iterable)
            lines = [f"{indent}ko_lagi {stmt.var_name} ma {iter_str} {{"]
            lines.extend(self._format_block_lines(stmt.body, level + 1))
            lines.append(f"{indent}}}")
            return "\n".join(lines)

        elif isinstance(stmt, BreakStatement):
            return f"{indent}rok"

        elif isinstance(stmt, ContinueStatement):
            return f"{indent}jaari"

        elif isinstance(stmt, FunctionDeclaration):
            params_str = ", ".join(stmt.parameters)
            lines = [f"{indent}kaam {stmt.name}({params_str}) {{"]
            lines.extend(self._format_block_lines(stmt.body, level + 1))
            lines.append(f"{indent}}}")
            return "\n".join(lines)

        elif isinstance(stmt, ReturnStatement):
            if stmt.value is not None:
                return f"{indent}farka {self._format_expression(stmt.value)}"
            return f"{indent}farka"

        elif isinstance(stmt, TryStatement):
            lines = [f"{indent}koshish {{"]
            lines.extend(self._format_block_lines(stmt.try_block, level + 1))
            catch_var_str = f" {stmt.catch_var}" if stmt.catch_var else ""
            lines.append(f"{indent}}} samata{catch_var_str} {{")
            lines.extend(self._format_block_lines(stmt.catch_block, level + 1))
            lines.append(f"{indent}}}")
            return "\n".join(lines)

        elif isinstance(stmt, ThrowStatement):
            return f"{indent}fal {self._format_expression(stmt.expression)}"

        elif isinstance(stmt, ExportStatement):
            if stmt.declaration:
                decl_str = self._format_statement(stmt.declaration, level)
                return f"{indent}pathaau {decl_str.lstrip()}"
            elif stmt.symbol_name:
                return f"{indent}pathaau {stmt.symbol_name}"
            return f"{indent}pathaau"

        elif isinstance(stmt, AssertStatement):
            cond_str = self._format_expression(stmt.condition)
            if stmt.message is not None:
                msg_str = self._format_expression(stmt.message)
                return f"{indent}jaach {cond_str}, {msg_str}"
            return f"{indent}jaach {cond_str}"

        elif isinstance(stmt, ExpressionStatement):
            return f"{indent}{self._format_expression(stmt.expression)}"

        return f"{indent}# {type(stmt).__name__}"

    def _format_block_lines(self, block: Block, level: int) -> List[str]:
        lines = []
        for stmt in block.statements:
            lines.append(self._format_statement(stmt, level))
        return lines

    def _format_expression(self, expr: Expression) -> str:
        if isinstance(expr, Literal):
            if expr.literal_type == "text":
                # Escape quotes
                val = str(expr.value).replace('"', '\\"')
                return f'"{val}"'
            if expr.literal_type == "boolean":
                return "sacho" if expr.value else "jutho"
            if expr.literal_type == "null":
                return "khali"
            return str(expr.value)

        elif isinstance(expr, Identifier):
            return expr.name

        elif isinstance(expr, BinaryExpression):
            left_str = self._format_expression(expr.left)
            right_str = self._format_expression(expr.right)
            # Add parens for nested binary expressions with lower precedence if needed
            return f"{left_str} {expr.operator} {right_str}"

        elif isinstance(expr, UnaryExpression):
            op = expr.operator
            operand_str = self._format_expression(expr.operand)
            if op == "not":
                return f"not {operand_str}"
            return f"{op}{operand_str}"

        elif isinstance(expr, FunctionCall):
            callee_str = self._format_expression(expr.callee)
            args_str = ", ".join(self._format_expression(arg) for arg in expr.arguments)
            return f"{callee_str}({args_str})"

        elif isinstance(expr, ListLiteral):
            elems = ", ".join(self._format_expression(e) for e in expr.elements)
            return f"[{elems}]"

        elif isinstance(expr, MapLiteral):
            entries = ", ".join(f"{self._format_expression(k)}: {self._format_expression(v)}" for k, v in expr.entries)
            return f"{{{entries}}}"

        elif isinstance(expr, IndexExpression):
            target_str = self._format_expression(expr.target)
            idx_str = self._format_expression(expr.index)
            return f"{target_str}[{idx_str}]"

        elif isinstance(expr, MemberExpression):
            target_str = self._format_expression(expr.target)
            return f"{target_str}.{expr.property_name}"

        elif isinstance(expr, ImportExpression):
            if expr.is_std or not expr.module_path.startswith((".", "/")):
                return f"aayaat {expr.module_path}"
            return f'aayaat "{expr.module_path}"'

        return str(expr)
