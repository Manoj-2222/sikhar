"""
Sikhar Bytecode Compiler
Compiles Sikhar AST nodes into Bytecode Chunks with lexical scoping and jump resolution.
"""

from typing import Any, List, Optional, Tuple, Dict
from ..parser.ast_nodes import (
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
    AssertStatement,
    ExportStatement,
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
)
from .chunk import Chunk, BytecodeFunction
from .opcodes import OpCode
from ..errors.error_types import SikharCompileError


class Local:
    def __init__(self, name: str, depth: int, is_const: bool = False):
        self.name: str = name
        self.depth: int = depth
        self.is_const: bool = is_const


class LoopContext:
    def __init__(self, start_offset: int, scope_depth: int):
        self.start_offset: int = start_offset
        self.continue_target: int = start_offset
        self.scope_depth: int = scope_depth
        self.break_jumps: List[int] = []


class Compiler:
    def __init__(
        self,
        filename: str = "<stdin>",
        parent: Optional["Compiler"] = None,
        function_name: Optional[str] = None,
    ):
        self.filename: str = filename
        self.parent: Optional[Compiler] = parent
        self.function_name: Optional[str] = function_name
        self.chunk: Chunk = Chunk(filename)
        self.locals: List[Local] = []
        self.scope_depth: int = 0
        self.loop_stack: List[LoopContext] = []

    def compile(self, program: Program) -> Chunk:
        for stmt in program.statements:
            self.compile_statement(stmt)
        # Top-level script implicitly returns nil
        self.emit_byte(OpCode.OP_NIL, 1, 1)
        self.emit_byte(OpCode.OP_RETURN, 1, 1)
        return self.chunk

    # ==========================================
    # Bytecode Emission Helpers
    # ==========================================

    def emit_byte(self, byte_val: int, line: int = 1, column: int = 1) -> int:
        return self.chunk.write_byte(int(byte_val), line, column)

    def emit_short(self, short_val: int, line: int = 1, column: int = 1) -> int:
        return self.chunk.write_short(short_val, line, column)

    def emit_op_short(self, opcode: OpCode, operand: int, line: int = 1, column: int = 1) -> int:
        pos = self.emit_byte(opcode, line, column)
        self.emit_short(operand, line, column)
        return pos

    def emit_constant(self, val: Any, line: int = 1, column: int = 1) -> None:
        idx = self.chunk.add_constant(val)
        self.emit_op_short(OpCode.OP_CONSTANT, idx, line, column)

    def emit_jump(self, opcode: OpCode, line: int = 1, column: int = 1) -> int:
        """Emit jump instruction with 2-byte dummy offset and return offset to patch."""
        self.emit_byte(opcode, line, column)
        return self.emit_short(0xFFFF, line, column)

    def patch_jump(self, offset: int) -> None:
        """Patch a forward jump offset (offset points to the 2-byte operand)."""
        jump = self.chunk.count - (offset + 2)
        if jump > 0xFFFF:
            raise SikharCompileError("Jump offset too large (exceeds 65535 bytes)", filename=self.filename)
        self.chunk.patch_short(offset, jump)

    def emit_loop(self, loop_start: int, line: int = 1, column: int = 1) -> None:
        """Emit backward jump to loop_start."""
        self.emit_byte(OpCode.OP_LOOP, line, column)
        offset = self.chunk.count + 2 - loop_start
        if offset > 0xFFFF:
            raise SikharCompileError("Loop jump backward too large", filename=self.filename)
        self.emit_short(offset, line, column)

    # ==========================================
    # Scoping & Symbol Resolution
    # ==========================================

    def begin_scope(self) -> None:
        self.scope_depth += 1

    def end_scope(self, line: int = 1, column: int = 1) -> None:
        self.scope_depth -= 1
        # Pop all locals belonging to the finished scope
        while self.locals and self.locals[-1].depth > self.scope_depth:
            self.emit_byte(OpCode.OP_POP, line, column)
            self.locals.pop()

    def resolve_local(self, name: str) -> Optional[int]:
        for idx in range(len(self.locals) - 1, -1, -1):
            if self.locals[idx].name == name:
                return idx
        return None

    def add_local(self, name: str, is_const: bool = False, line: int = 1, column: int = 1) -> int:
        # Check if already declared in same scope
        for local in reversed(self.locals):
            if local.depth < self.scope_depth:
                break
            if local.name == name:
                raise SikharCompileError(
                    f"Variable '{name}' is already declared in this scope",
                    filename=self.filename,
                    line=line,
                    column=column,
                )
        self.locals.append(Local(name, self.scope_depth, is_const))
        return len(self.locals) - 1

    # ==========================================
    # Statement Compilation
    # ==========================================

    def compile_statement(self, stmt: Statement) -> None:
        if isinstance(stmt, VariableDeclaration):
            self._compile_var_decl(stmt)
        elif isinstance(stmt, ConstantDeclaration):
            self._compile_const_decl(stmt)
        elif isinstance(stmt, Assignment):
            self._compile_assignment(stmt)
        elif isinstance(stmt, DekhaStatement):
            self._compile_dekha(stmt)
        elif isinstance(stmt, IfStatement):
            self._compile_if(stmt)
        elif isinstance(stmt, WhileStatement):
            self._compile_while(stmt)
        elif isinstance(stmt, ForStatement):
            self._compile_for(stmt)
        elif isinstance(stmt, BreakStatement):
            self._compile_break(stmt)
        elif isinstance(stmt, ContinueStatement):
            self._compile_continue(stmt)
        elif isinstance(stmt, FunctionDeclaration):
            self._compile_function_decl(stmt)
        elif isinstance(stmt, ReturnStatement):
            self._compile_return(stmt)
        elif isinstance(stmt, TryStatement):
            self._compile_try(stmt)
        elif isinstance(stmt, ThrowStatement):
            self._compile_throw(stmt)
        elif isinstance(stmt, AssertStatement):
            self._compile_assert(stmt)
        elif isinstance(stmt, ExportStatement):
            self._compile_export(stmt)
        elif isinstance(stmt, ExpressionStatement):
            if isinstance(stmt.expression, ImportExpression):
                self.compile_expression(stmt.expression)
                from pathlib import Path
                mod_path = stmt.expression.module_path
                if mod_path.endswith(".sk"):
                    clean_name = Path(mod_path).stem
                else:
                    clean_name = mod_path.split(".")[-1]
                if self.scope_depth > 0:
                    self.add_local(clean_name, is_const=False, line=stmt.line, column=stmt.column)
                else:
                    idx = self.chunk.add_constant(clean_name)
                    self.emit_op_short(OpCode.OP_DEFINE_GLOBAL, idx, stmt.line, stmt.column)

            else:
                self.compile_expression(stmt.expression)
                self.emit_byte(OpCode.OP_POP, stmt.line, stmt.column)
        elif isinstance(stmt, Block):
            self.begin_scope()
            for s in stmt.statements:
                self.compile_statement(s)
            self.end_scope(stmt.line, stmt.column)

    def _compile_var_decl(self, stmt: VariableDeclaration) -> None:
        if stmt.initializer is not None:
            self.compile_expression(stmt.initializer)
        else:
            self.emit_byte(OpCode.OP_NIL, stmt.line, stmt.column)

        if self.scope_depth > 0:
            self.add_local(stmt.name, is_const=False, line=stmt.line, column=stmt.column)
        else:
            idx = self.chunk.add_constant(stmt.name)
            self.emit_op_short(OpCode.OP_DEFINE_GLOBAL, idx, stmt.line, stmt.column)

    def _compile_const_decl(self, stmt: ConstantDeclaration) -> None:
        self.compile_expression(stmt.initializer)
        if self.scope_depth > 0:
            self.add_local(stmt.name, is_const=True, line=stmt.line, column=stmt.column)
        else:
            idx = self.chunk.add_constant(stmt.name)
            self.emit_op_short(OpCode.OP_DEFINE_CONST, idx, stmt.line, stmt.column)

    def _compile_assignment(self, stmt: Assignment) -> None:
        if isinstance(stmt.target, Identifier):
            name = stmt.target.name
            local_slot = self.resolve_local(name)
            if local_slot is not None:
                if self.locals[local_slot].is_const:
                    raise SikharCompileError(
                        f"Cannot modify constant '{name}' declared with 'sthayi'",
                        filename=self.filename,
                        line=stmt.line,
                        column=stmt.column,
                    )
                self.compile_expression(stmt.value)
                self.emit_op_short(OpCode.OP_SET_LOCAL, local_slot, stmt.line, stmt.column)
                self.emit_byte(OpCode.OP_POP, stmt.line, stmt.column)
            else:
                self.compile_expression(stmt.value)
                idx = self.chunk.add_constant(name)
                self.emit_op_short(OpCode.OP_SET_GLOBAL, idx, stmt.line, stmt.column)
                self.emit_byte(OpCode.OP_POP, stmt.line, stmt.column)

        elif isinstance(stmt.target, IndexExpression):
            self.compile_expression(stmt.target.target)
            self.compile_expression(stmt.target.index)
            self.compile_expression(stmt.value)
            self.emit_byte(OpCode.OP_INDEX_SET, stmt.line, stmt.column)
            self.emit_byte(OpCode.OP_POP, stmt.line, stmt.column)

        elif isinstance(stmt.target, MemberExpression):
            self.compile_expression(stmt.target.target)
            self.compile_expression(stmt.value)
            idx = self.chunk.add_constant(stmt.target.property_name)
            self.emit_op_short(OpCode.OP_SET_MEMBER, idx, stmt.line, stmt.column)
            self.emit_byte(OpCode.OP_POP, stmt.line, stmt.column)
        else:
            raise SikharCompileError("Invalid assignment target", filename=self.filename, line=stmt.line, column=stmt.column)

    def _compile_dekha(self, stmt: DekhaStatement) -> None:
        self.compile_expression(stmt.expression)
        self.emit_op_short(OpCode.OP_PRINT, 1, stmt.line, stmt.column)

    def _compile_if(self, stmt: IfStatement) -> None:
        exit_jumps: List[int] = []

        # If branch
        self.compile_expression(stmt.condition)
        false_jump = self.emit_jump(OpCode.OP_JUMP_IF_FALSE, stmt.line, stmt.column)

        self.begin_scope()
        for s in stmt.then_branch.statements:
            self.compile_statement(s)
        self.end_scope(stmt.line, stmt.column)

        exit_jumps.append(self.emit_jump(OpCode.OP_JUMP, stmt.line, stmt.column))
        self.patch_jump(false_jump)

        # Elif branches
        for elif_cond, elif_body in stmt.elif_branches:
            self.compile_expression(elif_cond)
            elif_false_jump = self.emit_jump(OpCode.OP_JUMP_IF_FALSE, elif_cond.line, elif_cond.column)

            self.begin_scope()
            for s in elif_body.statements:
                self.compile_statement(s)
            self.end_scope(elif_cond.line, elif_cond.column)

            exit_jumps.append(self.emit_jump(OpCode.OP_JUMP, elif_cond.line, elif_cond.column))
            self.patch_jump(elif_false_jump)

        # Else branch
        if stmt.else_branch is not None:
            self.begin_scope()
            for s in stmt.else_branch.statements:
                self.compile_statement(s)
            self.end_scope(stmt.line, stmt.column)

        for j in exit_jumps:
            self.patch_jump(j)

    def _compile_while(self, stmt: WhileStatement) -> None:
        loop_start = self.chunk.count
        loop_ctx = LoopContext(loop_start, self.scope_depth)
        self.loop_stack.append(loop_ctx)

        self.compile_expression(stmt.condition)
        exit_jump = self.emit_jump(OpCode.OP_JUMP_IF_FALSE, stmt.line, stmt.column)

        self.begin_scope()
        for s in stmt.body.statements:
            self.compile_statement(s)
        self.end_scope(stmt.line, stmt.column)

        self.emit_loop(loop_start, stmt.line, stmt.column)
        self.patch_jump(exit_jump)

        for brk in loop_ctx.break_jumps:
            self.patch_jump(brk)
        self.loop_stack.pop()

    def _compile_for(self, stmt: ForStatement) -> None:
        # Evaluate iterable
        self.compile_expression(stmt.iterable)
        self.emit_byte(OpCode.OP_GET_ITER, stmt.line, stmt.column)

        self.begin_scope()
        iter_slot = self.add_local("(iter)", is_const=True, line=stmt.line, column=stmt.column)

        loop_start = self.chunk.count
        loop_ctx = LoopContext(loop_start, self.scope_depth)
        loop_ctx.continue_target = loop_start
        self.loop_stack.append(loop_ctx)

        # OP_FOR_ITER peeks at iterator (iter_slot) and pushes next item onto stack (var_slot)
        exit_jump = self.emit_jump(OpCode.OP_FOR_ITER, stmt.line, stmt.column)

        # Add loop variable to locals in current scope
        var_slot = self.add_local(stmt.var_name, is_const=False, line=stmt.line, column=stmt.column)

        for s in stmt.body.statements:
            self.compile_statement(s)

        # Pop loop variable at end of iteration before next iteration
        self.emit_byte(OpCode.OP_POP, stmt.line, stmt.column)
        self.locals.pop()

        self.emit_loop(loop_start, stmt.line, stmt.column)
        self.patch_jump(exit_jump)

        for brk in loop_ctx.break_jumps:
            self.patch_jump(brk)
        self.loop_stack.pop()

        # Iterator was popped by OP_FOR_ITER on StopIteration
        self.locals.pop()
        self.scope_depth -= 1

    def _compile_break(self, stmt: BreakStatement) -> None:
        if not self.loop_stack:
            raise SikharCompileError("Cannot use 'rok' (break) outside a loop", filename=self.filename, line=stmt.line, column=stmt.column)
        loop_ctx = self.loop_stack[-1]
        # Pop locals down to loop scope depth (plus iterator if in for loop)
        for _ in range(len(self.locals) - loop_ctx.scope_depth):
            self.emit_byte(OpCode.OP_POP, stmt.line, stmt.column)
        # Pop the loop iterator if innermost loop is a for-loop
        if self.locals and self.locals[loop_ctx.scope_depth - 1].name == "(iter)":
            self.emit_byte(OpCode.OP_POP, stmt.line, stmt.column)

        j = self.emit_jump(OpCode.OP_JUMP, stmt.line, stmt.column)
        loop_ctx.break_jumps.append(j)

    def _compile_continue(self, stmt: ContinueStatement) -> None:
        if not self.loop_stack:
            raise SikharCompileError("Cannot use 'jaari' (continue) outside a loop", filename=self.filename, line=stmt.line, column=stmt.column)
        loop_ctx = self.loop_stack[-1]
        # For a for-loop, pop down to iterator (pop inner locals and loop variable)
        if self.locals and self.locals[loop_ctx.scope_depth - 1].name == "(iter)":
            for _ in range(len(self.locals) - loop_ctx.scope_depth):
                self.emit_byte(OpCode.OP_POP, stmt.line, stmt.column)
        else:
            for _ in range(len(self.locals) - loop_ctx.scope_depth):
                self.emit_byte(OpCode.OP_POP, stmt.line, stmt.column)
        self.emit_loop(loop_ctx.continue_target, stmt.line, stmt.column)


    def _compile_function_decl(self, stmt: FunctionDeclaration) -> None:
        func_compiler = Compiler(filename=self.filename, parent=self, function_name=stmt.name)
        func_compiler.scope_depth = 1

        # Parameter slots inside function call frame
        for param in stmt.parameters:
            func_compiler.locals.append(Local(param, depth=1, is_const=False))

        for s in stmt.body.statements:
            func_compiler.compile_statement(s)

        # Implicit return nil at end of function
        func_compiler.emit_byte(OpCode.OP_NIL, stmt.line, stmt.column)
        func_compiler.emit_byte(OpCode.OP_RETURN, stmt.line, stmt.column)

        func_obj = BytecodeFunction(
            name=stmt.name,
            arity=len(stmt.parameters),
            param_names=list(stmt.parameters),
            chunk=func_compiler.chunk,
        )

        const_idx = self.chunk.add_constant(func_obj)
        self.emit_op_short(OpCode.OP_MAKE_FUNCTION, const_idx, stmt.line, stmt.column)

        if self.scope_depth > 0:
            self.add_local(stmt.name, is_const=False, line=stmt.line, column=stmt.column)
        else:
            name_idx = self.chunk.add_constant(stmt.name)
            self.emit_op_short(OpCode.OP_DEFINE_GLOBAL, name_idx, stmt.line, stmt.column)

    def _compile_return(self, stmt: ReturnStatement) -> None:
        if stmt.value is not None:
            self.compile_expression(stmt.value)
        else:
            self.emit_byte(OpCode.OP_NIL, stmt.line, stmt.column)
        self.emit_byte(OpCode.OP_RETURN, stmt.line, stmt.column)

    def _compile_try(self, stmt: TryStatement) -> None:
        # OP_PUSH_TRY with jump offset to catch block
        try_jump = self.emit_jump(OpCode.OP_PUSH_TRY, stmt.line, stmt.column)

        self.begin_scope()
        for s in stmt.try_block.statements:
            self.compile_statement(s)
        self.end_scope(stmt.line, stmt.column)

        self.emit_byte(OpCode.OP_POP_TRY, stmt.line, stmt.column)
        skip_catch = self.emit_jump(OpCode.OP_JUMP, stmt.line, stmt.column)

        # Catch handler begins
        self.patch_jump(try_jump)
        self.begin_scope()
        if stmt.catch_var:
            self.add_local(stmt.catch_var, is_const=False, line=stmt.line, column=stmt.column)
        else:
            self.emit_byte(OpCode.OP_POP, stmt.line, stmt.column)

        for s in stmt.catch_block.statements:
            self.compile_statement(s)
        self.end_scope(stmt.line, stmt.column)

        self.patch_jump(skip_catch)

    def _compile_throw(self, stmt: ThrowStatement) -> None:
        self.compile_expression(stmt.expression)
        self.emit_byte(OpCode.OP_THROW, stmt.line, stmt.column)

    def _compile_assert(self, stmt: AssertStatement) -> None:
        self.compile_expression(stmt.condition)
        if stmt.message is not None:
            self.compile_expression(stmt.message)
            self.emit_op_short(OpCode.OP_ASSERT, 1, stmt.line, stmt.column)
        else:
            self.emit_op_short(OpCode.OP_ASSERT, 0, stmt.line, stmt.column)

    def _compile_export(self, stmt: ExportStatement) -> None:
        if stmt.declaration is not None:
            self.compile_statement(stmt.declaration)
            name = getattr(stmt.declaration, "name", None)
            if name:
                idx = self.chunk.add_constant(name)
                self.emit_op_short(OpCode.OP_EXPORT, idx, stmt.line, stmt.column)
        elif stmt.symbol_name:
            idx = self.chunk.add_constant(stmt.symbol_name)
            self.emit_op_short(OpCode.OP_EXPORT, idx, stmt.line, stmt.column)

    # ==========================================
    # Expression Compilation
    # ==========================================

    def compile_expression(self, expr: Expression) -> None:
        if isinstance(expr, Literal):
            self._compile_literal(expr)
        elif isinstance(expr, Identifier):
            self._compile_identifier(expr)
        elif isinstance(expr, BinaryExpression):
            self._compile_binary(expr)
        elif isinstance(expr, UnaryExpression):
            self._compile_unary(expr)
        elif isinstance(expr, FunctionCall):
            self._compile_call(expr)
        elif isinstance(expr, ListLiteral):
            self._compile_list(expr)
        elif isinstance(expr, MapLiteral):
            self._compile_map(expr)
        elif isinstance(expr, IndexExpression):
            self._compile_index(expr)
        elif isinstance(expr, MemberExpression):
            self._compile_member(expr)
        elif isinstance(expr, ImportExpression):
            self._compile_import(expr)
        else:
            raise SikharCompileError(
                f"Unknown expression type: {type(expr).__name__}",
                filename=self.filename,
                line=expr.line,
                column=expr.column,
            )

    def _compile_literal(self, expr: Literal) -> None:
        if expr.value is None:
            self.emit_byte(OpCode.OP_NIL, expr.line, expr.column)
        elif isinstance(expr.value, bool):
            if expr.value:
                self.emit_byte(OpCode.OP_TRUE, expr.line, expr.column)
            else:
                self.emit_byte(OpCode.OP_FALSE, expr.line, expr.column)
        elif isinstance(expr.value, str):
            if "{" in expr.value or "\0" in expr.value:
                self._compile_interpolated_string(expr.value, expr.line, expr.column)
            else:
                self.emit_constant(expr.value, expr.line, expr.column)
        else:
            self.emit_constant(expr.value, expr.line, expr.column)

    def _compile_interpolated_string(self, text: str, line: int, col: int) -> None:
        parts_count = 0
        i = 0
        n = len(text)

        while i < n:
            if text[i] == "\0" and i + 1 < n and text[i + 1] in ("{", "}"):
                self.emit_constant(text[i + 1], line, col)
                parts_count += 1
                i += 2
            elif text[i] == "{":
                depth = 1
                start = i + 1
                j = start
                in_str = False
                while j < n and depth > 0:
                    if text[j] == '"' and (j == 0 or text[j - 1] != "\\"):
                        in_str = not in_str
                    elif not in_str:
                        if text[j] == "{":
                            depth += 1
                        elif text[j] == "}":
                            depth -= 1
                    j += 1
                if depth > 0:
                    self.emit_constant(text[i], line, col)
                    parts_count += 1
                    i += 1
                else:
                    expr_text = text[start:j - 1].strip()
                    if expr_text:
                        from ..lexer.lexer import Lexer
                        from ..parser.parser import Parser

                        tokens = Lexer(expr_text, self.filename).tokenize()
                        parsed = Parser(tokens, expr_text, self.filename)._parse_expression()
                        self.compile_expression(parsed)
                        parts_count += 1
                    i = j
            else:
                # Accumulate plain literal run
                run_start = i
                while i < n and text[i] not in ("{", "\0"):
                    i += 1
                run_str = text[run_start:i]
                if run_str:
                    self.emit_constant(run_str, line, col)
                    parts_count += 1

        self.emit_op_short(OpCode.OP_FORMAT_STRING, parts_count, line, col)

    def _compile_identifier(self, expr: Identifier) -> None:
        slot = self.resolve_local(expr.name)
        if slot is not None:
            self.emit_op_short(OpCode.OP_GET_LOCAL, slot, expr.line, expr.column)
        else:
            idx = self.chunk.add_constant(expr.name)
            self.emit_op_short(OpCode.OP_GET_GLOBAL, idx, expr.line, expr.column)

    def _compile_binary(self, expr: BinaryExpression) -> None:
        op = expr.operator

        # Short-circuiting logical AND ('ra' / 'and')
        if op in ("ra", "and"):
            self.compile_expression(expr.left)
            self.emit_byte(OpCode.OP_DUP, expr.line, expr.column)
            end_jump = self.emit_jump(OpCode.OP_JUMP_IF_FALSE, expr.line, expr.column)
            self.emit_byte(OpCode.OP_POP, expr.line, expr.column)
            self.compile_expression(expr.right)
            self.patch_jump(end_jump)
            return

        # Short-circuiting logical OR ('wa' / 'or')
        if op in ("wa", "or"):
            self.compile_expression(expr.left)
            self.emit_byte(OpCode.OP_DUP, expr.line, expr.column)
            # If truthy, skip right operand
            eval_right_jump = self.emit_jump(OpCode.OP_JUMP_IF_FALSE, expr.line, expr.column)
            end_jump = self.emit_jump(OpCode.OP_JUMP, expr.line, expr.column)
            self.patch_jump(eval_right_jump)
            self.emit_byte(OpCode.OP_POP, expr.line, expr.column)
            self.compile_expression(expr.right)
            self.patch_jump(end_jump)
            return

        self.compile_expression(expr.left)
        self.compile_expression(expr.right)

        op_map = {
            "+": OpCode.OP_ADD,
            "-": OpCode.OP_SUBTRACT,
            "*": OpCode.OP_MULTIPLY,
            "/": OpCode.OP_DIVIDE,
            "%": OpCode.OP_MODULO,
            "==": OpCode.OP_EQUAL,
            "!=": OpCode.OP_NOT_EQUAL,
            ">": OpCode.OP_GREATER,
            ">=": OpCode.OP_GREATER_EQUAL,
            "<": OpCode.OP_LESS,
            "<=": OpCode.OP_LESS_EQUAL,
        }

        if op in op_map:
            self.emit_byte(op_map[op], expr.line, expr.column)
        else:
            raise SikharCompileError(f"Unsupported binary operator '{op}'", filename=self.filename, line=expr.line, column=expr.column)

    def _compile_unary(self, expr: UnaryExpression) -> None:
        self.compile_expression(expr.operand)
        if expr.operator == "-":
            self.emit_byte(OpCode.OP_NEGATE, expr.line, expr.column)
        elif expr.operator in ("!", "chaina", "not"):
            self.emit_byte(OpCode.OP_NOT, expr.line, expr.column)
        else:
            raise SikharCompileError(f"Unsupported unary operator '{expr.operator}'", filename=self.filename, line=expr.line, column=expr.column)


    def _compile_call(self, expr: FunctionCall) -> None:
        self.compile_expression(expr.callee)
        for arg in expr.arguments:
            self.compile_expression(arg)
        self.emit_op_short(OpCode.OP_CALL, len(expr.arguments), expr.line, expr.column)

    def _compile_list(self, expr: ListLiteral) -> None:
        for elem in expr.elements:
            self.compile_expression(elem)
        self.emit_op_short(OpCode.OP_BUILD_LIST, len(expr.elements), expr.line, expr.column)

    def _compile_map(self, expr: MapLiteral) -> None:
        for key, val in expr.entries:
            self.compile_expression(key)
            self.compile_expression(val)
        self.emit_op_short(OpCode.OP_BUILD_MAP, len(expr.entries), expr.line, expr.column)

    def _compile_index(self, expr: IndexExpression) -> None:
        self.compile_expression(expr.target)
        self.compile_expression(expr.index)
        self.emit_byte(OpCode.OP_INDEX_GET, expr.line, expr.column)

    def _compile_member(self, expr: MemberExpression) -> None:
        self.compile_expression(expr.target)
        idx = self.chunk.add_constant(expr.property_name)
        self.emit_op_short(OpCode.OP_GET_MEMBER, idx, expr.line, expr.column)

    def _compile_import(self, expr: ImportExpression) -> None:
        idx = self.chunk.add_constant(expr.module_path)
        pos = self.emit_byte(OpCode.OP_IMPORT, expr.line, expr.column)
        self.emit_short(idx, expr.line, expr.column)
        self.emit_byte(1 if expr.is_std else 0, expr.line, expr.column)
