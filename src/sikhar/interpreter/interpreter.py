"""
Sikhar AST Tree-Walking Interpreter
Executes Sikhar AST nodes with full environment and error handling.
"""

from typing import Any, Callable, List, Optional
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
)
from .environment import Environment
from .values import (
    SikharCallable,
    SikharFunction,
    ReturnSignal,
    BreakSignal,
    ContinueSignal,
    is_truthy,
    sikhar_stringify,
)
from ..runtime.builtins import register_builtins
from ..errors.error_types import (
    SikharRuntimeError,
    SikharTypeError,
    SikharIndexError,
    SikharKeyError,
    SikharDivisionByZeroError,
    SikharUserThrowError,
)


class Interpreter:
    def __init__(
        self,
        source: str = "",
        filename: str = "<stdin>",
        output_fn: Optional[Callable[[str], None]] = None,
        input_fn: Optional[Callable[[str], str]] = None,
    ):
        self.source = source
        self.filename = filename
        self.output_fn = output_fn if output_fn is not None else print
        self.input_fn = input_fn if input_fn is not None else input

        # Global scope initialization
        self.globals = Environment()
        register_builtins(self.globals, self.output_fn, self.input_fn)
        self.current_env = self.globals
        self.call_stack: List[str] = []

    def _get_source_line(self, line_no: int) -> Optional[str]:
        if not self.source:
            return None
        lines = self.source.splitlines()
        if 1 <= line_no <= len(lines):
            return lines[line_no - 1]
        return None

    def interpret(self, program: Program) -> Any:
        """Interpret an entire Sikhar program."""
        result = None
        for stmt in program.statements:
            result = self.execute(stmt)
        return result

    def execute(self, stmt: Statement) -> Any:
        """Execute a single statement."""
        if isinstance(stmt, VariableDeclaration):
            return self._execute_var_decl(stmt)
        elif isinstance(stmt, ConstantDeclaration):
            return self._execute_const_decl(stmt)
        elif isinstance(stmt, Assignment):
            return self._execute_assignment(stmt)
        elif isinstance(stmt, DekhaStatement):
            return self._execute_dekha(stmt)
        elif isinstance(stmt, IfStatement):
            return self._execute_if(stmt)
        elif isinstance(stmt, WhileStatement):
            return self._execute_while(stmt)
        elif isinstance(stmt, ForStatement):
            return self._execute_for(stmt)
        elif isinstance(stmt, BreakStatement):
            raise BreakSignal()
        elif isinstance(stmt, ContinueStatement):
            raise ContinueSignal()
        elif isinstance(stmt, FunctionDeclaration):
            return self._execute_function_decl(stmt)
        elif isinstance(stmt, ReturnStatement):
            return self._execute_return(stmt)
        elif isinstance(stmt, TryStatement):
            return self._execute_try_catch(stmt)
        elif isinstance(stmt, ThrowStatement):
            return self._execute_throw(stmt)
        elif isinstance(stmt, ExpressionStatement):
            return self.evaluate(stmt.expression)
        elif isinstance(stmt, Block):
            return self.execute_block(stmt)
        else:
            raise SikharRuntimeError(
                f"Unknown statement type: {type(stmt).__name__}",
                filename=self.filename,
                line=stmt.line,
                column=stmt.column,
                source_line=self._get_source_line(stmt.line),
            )

    def execute_block(self, block: Block, env: Optional[Environment] = None) -> Any:
        """Execute a block of statements in a scoped environment."""
        previous_env = self.current_env
        self.current_env = env if env is not None else Environment(parent=previous_env)
        try:
            res = None
            for stmt in block.statements:
                res = self.execute(stmt)
            return res
        finally:
            self.current_env = previous_env

    def _execute_var_decl(self, stmt: VariableDeclaration) -> None:
        val = None
        if stmt.initializer is not None:
            val = self.evaluate(stmt.initializer)
        self.current_env.define(stmt.name, val, is_constant=False)

    def _execute_const_decl(self, stmt: ConstantDeclaration) -> None:
        val = self.evaluate(stmt.initializer)
        self.current_env.define(stmt.name, val, is_constant=True)

    def _execute_assignment(self, stmt: Assignment) -> Any:
        val = self.evaluate(stmt.value)
        source_line = self._get_source_line(stmt.line)

        if isinstance(stmt.target, Identifier):
            self.current_env.assign(
                stmt.target.name,
                val,
                filename=self.filename,
                line=stmt.line,
                column=stmt.column,
                source_line=source_line,
            )
            return val
        elif isinstance(stmt.target, IndexExpression):
            target_obj = self.evaluate(stmt.target.target)
            idx_val = self.evaluate(stmt.target.index)

            if isinstance(target_obj, list):
                if not isinstance(idx_val, int):
                    raise SikharTypeError(
                        f"List indices must be integers, got '{type(idx_val).__name__}'",
                        filename=self.filename,
                        line=stmt.line,
                        column=stmt.column,
                        source_line=source_line,
                    )
                if idx_val < 0 or idx_val >= len(target_obj):
                    raise SikharIndexError(
                        f"List index out of range: {idx_val} (size {len(target_obj)})",
                        filename=self.filename,
                        line=stmt.line,
                        column=stmt.column,
                        source_line=source_line,
                    )
                target_obj[idx_val] = val
                return val
            elif isinstance(target_obj, dict):
                target_obj[idx_val] = val
                return val
            else:
                raise SikharTypeError(
                    f"Cannot assign by index to type '{type(target_obj).__name__}'",
                    filename=self.filename,
                    line=stmt.line,
                    column=stmt.column,
                    source_line=source_line,
                )

        raise SikharRuntimeError(
            "Invalid assignment target",
            filename=self.filename,
            line=stmt.line,
            column=stmt.column,
            source_line=source_line,
        )

    def _execute_dekha(self, stmt: DekhaStatement) -> None:
        val = self.evaluate(stmt.expression)
        self.output_fn(sikhar_stringify(val))

    def _execute_if(self, stmt: IfStatement) -> Any:
        cond_val = self.evaluate(stmt.condition)
        if is_truthy(cond_val):
            return self.execute_block(stmt.then_branch)

        for elif_cond, elif_block in stmt.elif_branches:
            if is_truthy(self.evaluate(elif_cond)):
                return self.execute_block(elif_block)

        if stmt.else_branch is not None:
            return self.execute_block(stmt.else_branch)

        return None

    def _execute_while(self, stmt: WhileStatement) -> None:
        while is_truthy(self.evaluate(stmt.condition)):
            try:
                self.execute_block(stmt.body)
            except BreakSignal:
                break
            except ContinueSignal:
                continue

    def _execute_for(self, stmt: ForStatement) -> None:
        iterable = self.evaluate(stmt.iterable)
        source_line = self._get_source_line(stmt.line)

        items = []
        if isinstance(iterable, (list, tuple)):
            items = iterable
        elif isinstance(iterable, dict):
            items = list(iterable.keys())
        elif isinstance(iterable, str):
            items = list(iterable)
        else:
            raise SikharTypeError(
                f"Type '{type(iterable).__name__}' is not iterable in 'ko_lagi'",
                filename=self.filename,
                line=stmt.line,
                column=stmt.column,
                source_line=source_line,
            )

        for item in items:
            loop_env = Environment(parent=self.current_env)
            loop_env.define(stmt.var_name, item)
            try:
                self.execute_block(stmt.body, loop_env)
            except BreakSignal:
                break
            except ContinueSignal:
                continue

    def _execute_function_decl(self, stmt: FunctionDeclaration) -> None:
        func = SikharFunction(stmt, self.current_env)
        self.current_env.define(stmt.name, func)

    def _execute_return(self, stmt: ReturnStatement) -> None:
        val = None
        if stmt.value is not None:
            val = self.evaluate(stmt.value)
        raise ReturnSignal(val)

    def _execute_try_catch(self, stmt: TryStatement) -> Any:
        try:
            return self.execute_block(stmt.try_block)
        except SikharUserThrowError as err:
            catch_env = Environment(parent=self.current_env)
            if stmt.catch_var:
                catch_env.define(stmt.catch_var, err.thrown_value)
            return self.execute_block(stmt.catch_block, catch_env)
        except SikharRuntimeError as err:
            catch_env = Environment(parent=self.current_env)
            if stmt.catch_var:
                catch_env.define(stmt.catch_var, err.message)
            return self.execute_block(stmt.catch_block, catch_env)

    def _execute_throw(self, stmt: ThrowStatement) -> None:
        val = self.evaluate(stmt.expression)
        raise SikharUserThrowError(
            val,
            filename=self.filename,
            line=stmt.line,
            column=stmt.column,
            source_line=self._get_source_line(stmt.line),
            call_stack=list(self.call_stack),
        )

    # ==========================================
    # Expression Evaluation
    # ==========================================

    def evaluate(self, expr: Expression) -> Any:
        """Evaluate an expression node."""
        source_line = self._get_source_line(expr.line)

        if isinstance(expr, Literal):
            return expr.value

        elif isinstance(expr, Identifier):
            return self.current_env.get(
                expr.name,
                filename=self.filename,
                line=expr.line,
                column=expr.column,
                source_line=source_line,
            )

        elif isinstance(expr, BinaryExpression):
            return self._eval_binary(expr)

        elif isinstance(expr, UnaryExpression):
            return self._eval_unary(expr)

        elif isinstance(expr, FunctionCall):
            return self._eval_call(expr)

        elif isinstance(expr, ListLiteral):
            return [self.evaluate(elem) for elem in expr.elements]

        elif isinstance(expr, MapLiteral):
            m = {}
            for k_expr, v_expr in expr.entries:
                key = self.evaluate(k_expr)
                val = self.evaluate(v_expr)
                m[key] = val
            return m

        elif isinstance(expr, IndexExpression):
            target = self.evaluate(expr.target)
            idx = self.evaluate(expr.index)

            if isinstance(target, list):
                if not isinstance(idx, int):
                    raise SikharTypeError(
                        f"List index must be an integer, got '{type(idx).__name__}'",
                        filename=self.filename,
                        line=expr.line,
                        column=expr.column,
                        source_line=source_line,
                    )
                if idx < 0 or idx >= len(target):
                    raise SikharIndexError(
                        f"List index out of range: {idx} (size {len(target)})",
                        filename=self.filename,
                        line=expr.line,
                        column=expr.column,
                        source_line=source_line,
                    )
                return target[idx]

            elif isinstance(target, dict):
                if idx not in target:
                    raise SikharKeyError(
                        f"Key '{idx}' not found in map",
                        filename=self.filename,
                        line=expr.line,
                        column=expr.column,
                        source_line=source_line,
                    )
                return target[idx]

            elif isinstance(target, str):
                if not isinstance(idx, int):
                    raise SikharTypeError(
                        f"String index must be an integer, got '{type(idx).__name__}'",
                        filename=self.filename,
                        line=expr.line,
                        column=expr.column,
                        source_line=source_line,
                    )
                if idx < 0 or idx >= len(target):
                    raise SikharIndexError(
                        f"String index out of range: {idx} (size {len(target)})",
                        filename=self.filename,
                        line=expr.line,
                        column=expr.column,
                        source_line=source_line,
                    )
                return target[idx]

            else:
                raise SikharTypeError(
                    f"Type '{type(target).__name__}' cannot be indexed",
                    filename=self.filename,
                    line=expr.line,
                    column=expr.column,
                    source_line=source_line,
                )

        raise SikharRuntimeError(
            f"Unknown expression type: {type(expr).__name__}",
            filename=self.filename,
            line=expr.line,
            column=expr.column,
            source_line=source_line,
        )

    def _eval_binary(self, expr: BinaryExpression) -> Any:
        op = expr.operator
        source_line = self._get_source_line(expr.line)

        # Short-circuit logical operators
        if op == "or":
            left_val = self.evaluate(expr.left)
            if is_truthy(left_val):
                return left_val
            return self.evaluate(expr.right)

        if op == "and":
            left_val = self.evaluate(expr.left)
            if not is_truthy(left_val):
                return left_val
            return self.evaluate(expr.right)

        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if op == "+":
            if isinstance(left, str) or isinstance(right, str):
                return sikhar_stringify(left) + sikhar_stringify(right)
            if isinstance(left, list) and isinstance(right, list):
                return left + right
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            raise SikharTypeError(
                f"Unsupported operand types for '+': '{type(left).__name__}' and '{type(right).__name__}'",
                filename=self.filename,
                line=expr.line,
                column=expr.column,
                source_line=source_line,
            )

        if op == "-":
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left - right
            raise SikharTypeError(
                f"Unsupported operand types for '-': '{type(left).__name__}' and '{type(right).__name__}'",
                filename=self.filename,
                line=expr.line,
                column=expr.column,
                source_line=source_line,
            )

        if op == "*":
            if isinstance(left, str) and isinstance(right, int):
                return left * right
            if isinstance(left, list) and isinstance(right, int):
                return left * right
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left * right
            raise SikharTypeError(
                f"Unsupported operand types for '*': '{type(left).__name__}' and '{type(right).__name__}'",
                filename=self.filename,
                line=expr.line,
                column=expr.column,
                source_line=source_line,
            )

        if op == "/":
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                if right == 0:
                    raise SikharDivisionByZeroError(
                        "Division by zero",
                        filename=self.filename,
                        line=expr.line,
                        column=expr.column,
                        source_line=source_line,
                    )
                val = left / right
                # Return clean int if exact
                if val.is_integer() and isinstance(left, int) and isinstance(right, int):
                    return int(val)
                return val
            raise SikharTypeError(
                f"Unsupported operand types for '/': '{type(left).__name__}' and '{type(right).__name__}'",
                filename=self.filename,
                line=expr.line,
                column=expr.column,
                source_line=source_line,
            )

        if op == "%":
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                if right == 0:
                    raise SikharDivisionByZeroError(
                        "Modulo by zero",
                        filename=self.filename,
                        line=expr.line,
                        column=expr.column,
                        source_line=source_line,
                    )
                return left % right
            raise SikharTypeError(
                f"Unsupported operand types for '%': '{type(left).__name__}' and '{type(right).__name__}'",
                filename=self.filename,
                line=expr.line,
                column=expr.column,
                source_line=source_line,
            )

        if op == "==":
            return left == right

        if op == "!=":
            return left != right

        if op in ("<", "<=", ">", ">="):
            if type(left) != type(right) and not (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                raise SikharTypeError(
                    f"Cannot compare different types with '{op}': '{type(left).__name__}' and '{type(right).__name__}'",
                    filename=self.filename,
                    line=expr.line,
                    column=expr.column,
                    source_line=source_line,
                )
            if op == "<":
                return left < right
            elif op == "<=":
                return left <= right
            elif op == ">":
                return left > right
            elif op == ">=":
                return left >= right

        raise SikharRuntimeError(
            f"Unknown operator: '{op}'",
            filename=self.filename,
            line=expr.line,
            column=expr.column,
            source_line=source_line,
        )

    def _eval_unary(self, expr: UnaryExpression) -> Any:
        operand = self.evaluate(expr.operand)
        source_line = self._get_source_line(expr.line)

        if expr.operator == "not":
            return not is_truthy(operand)

        if expr.operator == "-":
            if isinstance(operand, (int, float)):
                return -operand
            raise SikharTypeError(
                f"Unary '-' cannot be applied to type '{type(operand).__name__}'",
                filename=self.filename,
                line=expr.line,
                column=expr.column,
                source_line=source_line,
            )

        raise SikharRuntimeError(
            f"Unknown unary operator: '{expr.operator}'",
            filename=self.filename,
            line=expr.line,
            column=expr.column,
            source_line=source_line,
        )

    def _eval_call(self, expr: FunctionCall) -> Any:
        callee = self.evaluate(expr.callee)
        args = [self.evaluate(arg) for arg in expr.arguments]
        source_line = self._get_source_line(expr.line)

        if not isinstance(callee, SikharCallable):
            name = getattr(expr.callee, "name", str(expr.callee))
            raise SikharTypeError(
                f"'{name}' is not callable",
                filename=self.filename,
                line=expr.line,
                column=expr.column,
                source_line=source_line,
            )

        if callee.arity != -1 and len(args) != callee.arity:
            raise SikharTypeError(
                f"Function '{getattr(callee, 'name', 'kaam')}' expects {callee.arity} arguments, but got {len(args)}",
                filename=self.filename,
                line=expr.line,
                column=expr.column,
                source_line=source_line,
            )

        fn_name = getattr(callee, "name", "kaam")
        frame_desc = f"{fn_name}() at {self.filename}:{expr.line}:{expr.column}"
        self.call_stack.append(frame_desc)

        try:
            return callee.call(self, args, expr.line, expr.column)
        finally:
            self.call_stack.pop()
