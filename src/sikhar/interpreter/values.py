"""
Sikhar Runtime Values & Signals
Defines how values behave and how control flow signals propagate.
"""

from typing import Any, Callable, List, Optional
from ..parser.ast_nodes import FunctionDeclaration
from .environment import Environment


class ReturnSignal(Exception):
    """Signal used by 'farka' to unwind call stack with return value."""
    def __init__(self, value: Any):
        self.value = value


class BreakSignal(Exception):
    """Signal used by 'rok' to exit loops."""
    pass


class ContinueSignal(Exception):
    """Signal used by 'jaari' to proceed to next loop iteration."""
    pass


class SikharCallable:
    """Base interface for callable objects in Sikhar."""
    def call(self, interpreter: Any, arguments: List[Any], line: int, column: int) -> Any:
        raise NotImplementedError

    @property
    def arity(self) -> int:
        return 0


class SikharFunction(SikharCallable):
    """User-defined Sikhar function."""
    def __init__(self, declaration: FunctionDeclaration, closure: Environment):
        self.declaration = declaration
        self.closure = closure

    @property
    def name(self) -> str:
        return self.declaration.name

    @property
    def arity(self) -> int:
        return len(self.declaration.parameters)

    def call(self, interpreter: Any, arguments: List[Any], line: int, column: int) -> Any:
        func_env = Environment(parent=self.closure)
        for param, arg in zip(self.declaration.parameters, arguments):
            func_env.define(param, arg)

        try:
            interpreter.execute_block(self.declaration.body, func_env)
        except ReturnSignal as ret:
            return ret.value

        return None

    def __repr__(self) -> str:
        return f"<kaam {self.declaration.name}>"


class BuiltinFunction(SikharCallable):
    """Built-in function implemented in Python."""
    def __init__(self, name: str, fn: Callable[..., Any], arity: Optional[int] = None):
        self._name = name
        self._fn = fn
        self._arity = arity

    @property
    def name(self) -> str:
        return self._name

    @property
    def arity(self) -> int:
        return self._arity if self._arity is not None else -1

    def call(self, interpreter: Any, arguments: List[Any], line: int, column: int) -> Any:
        return self._fn(interpreter, arguments, line, column)

    def __repr__(self) -> str:
        return f"<built-in kaam {self._name}>"


class SikharModule:
    """A module containing exported functions, variables, and constants."""
    def __init__(self, name: str, exports: dict[str, Any]):
        self.name = name
        self.exports = exports

    def get_member(self, member_name: str, line: int = 1, col: int = 1, filename: str = "<stdin>") -> Any:
        if member_name in self.exports:
            return self.exports[member_name]
        from ..errors.error_types import SikharNameError
        raise SikharNameError(
            f"Module '{self.name}' has no member named '{member_name}'",
            filename=filename,
            line=line,
            column=col,
        )

    def set_member(self, member_name: str, val: Any) -> None:
        self.exports[member_name] = val

    def __getitem__(self, key: str) -> Any:
        return self.exports[key]

    def __contains__(self, key: str) -> bool:
        return key in self.exports

    def __repr__(self) -> str:
        return f"<module '{self.name}'>"


def is_truthy(val: Any) -> bool:
    """Determine truthiness in Sikhar."""
    if val is None:
        return False
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        return val != 0
    if isinstance(val, str):
        return len(val) > 0
    if isinstance(val, (list, dict)):
        return len(val) > 0
    return True


def sikhar_stringify(val: Any, in_collection: bool = False) -> str:
    """Format any Sikhar value for display."""
    if val is None:
        return "khali"
    if isinstance(val, bool):
        return "sacho" if val else "jutho"
    if isinstance(val, float):
        # Clean display for integer floats e.g. 5.0 -> 5.0, 99.5
        s = str(val)
        return s
    if isinstance(val, int):
        return str(val)
    if isinstance(val, str):
        if in_collection:
            return f'"{val}"'
        return val
    if isinstance(val, list):
        items = [sikhar_stringify(item, in_collection=True) for item in val]
        return "[" + ", ".join(items) + "]"
    if isinstance(val, dict):
        pairs = [f'{sikhar_stringify(k, in_collection=True)}: {sikhar_stringify(v, in_collection=True)}' for k, v in val.items()]
        return "{" + ", ".join(pairs) + "}"
    if isinstance(val, SikharCallable):
        return repr(val)
    if isinstance(val, SikharModule):
        return repr(val)
    return str(val)
