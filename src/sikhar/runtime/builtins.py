"""
Sikhar Built-in Functions
Provides foundational operations for I/O, collections, types, and math.
"""

from typing import Any, List, Dict
from ..errors.error_types import SikharTypeError, SikharIndexError
from ..interpreter.values import BuiltinFunction, sikhar_stringify


def register_builtins(global_env: Any, output_fn: Any = print, input_fn: Any = input) -> None:
    """Register all built-in functions into the global environment."""

    def _builtin_dekha(interpreter: Any, args: List[Any], line: int, col: int) -> None:
        text = " ".join(sikhar_stringify(arg) for arg in args)
        output_fn(text)
        return None

    def _builtin_sodha(interpreter: Any, args: List[Any], line: int, col: int) -> str:
        prompt_text = ""
        if args:
            prompt_text = sikhar_stringify(args[0])
        try:
            return input_fn(prompt_text)
        except EOFError:
            return ""

    def _builtin_lamba(interpreter: Any, args: List[Any], line: int, col: int) -> int:
        if len(args) != 1:
            raise SikharTypeError("Function 'lamba' expects exactly 1 argument", filename=interpreter.filename, line=line, column=col)
        target = args[0]
        if isinstance(target, (str, list, dict)):
            return len(target)
        raise SikharTypeError(
            f"Cannot determine length ('lamba') of type '{type(target).__name__}'",
            filename=interpreter.filename,
            line=line,
            column=col,
        )

    def _builtin_prakaar(interpreter: Any, args: List[Any], line: int, col: int) -> str:
        if len(args) != 1:
            raise SikharTypeError("Function 'prakaar' expects exactly 1 argument", filename=interpreter.filename, line=line, column=col)
        target = args[0]
        if target is None:
            return "khali"
        if isinstance(target, bool):
            return "boolean"
        if isinstance(target, int):
            return "number"
        if isinstance(target, float):
            return "decimal"
        if isinstance(target, str):
            return "text"
        if isinstance(target, list):
            return "list"
        if isinstance(target, dict):
            return "map"
        return "kaam"

    def _builtin_jod_suchi(interpreter: Any, args: List[Any], line: int, col: int) -> List[Any]:
        if len(args) != 2:
            raise SikharTypeError("Function 'jod_suchi' expects 2 arguments: (list, item)", filename=interpreter.filename, line=line, column=col)
        lst, item = args
        if not isinstance(lst, list):
            raise SikharTypeError("First argument to 'jod_suchi' must be a list", filename=interpreter.filename, line=line, column=col)
        lst.append(item)
        return lst

    def _builtin_hatau_suchi(interpreter: Any, args: List[Any], line: int, col: int) -> Any:
        if len(args) != 2:
            raise SikharTypeError("Function 'hatau_suchi' expects 2 arguments: (list, index)", filename=interpreter.filename, line=line, column=col)
        lst, idx = args
        if not isinstance(lst, list):
            raise SikharTypeError("First argument to 'hatau_suchi' must be a list", filename=interpreter.filename, line=line, column=col)
        if not isinstance(idx, int):
            raise SikharTypeError("Index for 'hatau_suchi' must be an integer", filename=interpreter.filename, line=line, column=col)
        if idx < 0 or idx >= len(lst):
            raise SikharIndexError(f"List index out of range: {idx}", filename=interpreter.filename, line=line, column=col)
        return lst.pop(idx)

    def _builtin_khoj_suchi(interpreter: Any, args: List[Any], line: int, col: int) -> int:
        if len(args) != 2:
            raise SikharTypeError("Function 'khoj_suchi' expects 2 arguments: (list, item)", filename=interpreter.filename, line=line, column=col)
        lst, item = args
        if not isinstance(lst, list):
            raise SikharTypeError("First argument to 'khoj_suchi' must be a list", filename=interpreter.filename, line=line, column=col)
        try:
            return lst.index(item)
        except ValueError:
            return -1

    def _builtin_thulo(interpreter: Any, args: List[Any], line: int, col: int) -> Any:
        if len(args) < 2:
            raise SikharTypeError("Function 'thulo' expects at least 2 arguments", filename=interpreter.filename, line=line, column=col)
        return max(args)

    def _builtin_sano(interpreter: Any, args: List[Any], line: int, col: int) -> Any:
        if len(args) < 2:
            raise SikharTypeError("Function 'sano' expects at least 2 arguments", filename=interpreter.filename, line=line, column=col)
        return min(args)

    def _builtin_ghat(interpreter: Any, args: List[Any], line: int, col: int) -> Any:
        if len(args) != 1:
            raise SikharTypeError("Function 'ghat' expects 1 argument", filename=interpreter.filename, line=line, column=col)
        if not isinstance(args[0], (int, float)):
            raise SikharTypeError("Argument to 'ghat' must be a number", filename=interpreter.filename, line=line, column=col)
        return abs(args[0])

    builtins_map = {
        "dekha": BuiltinFunction("dekha", _builtin_dekha, arity=None),
        "sodha": BuiltinFunction("sodha", _builtin_sodha, arity=None),
        "lamba": BuiltinFunction("lamba", _builtin_lamba, arity=1),
        "lambai": BuiltinFunction("lambai", _builtin_lamba, arity=1),
        "prakaar": BuiltinFunction("prakaar", _builtin_prakaar, arity=1),
        "jod_suchi": BuiltinFunction("jod_suchi", _builtin_jod_suchi, arity=2),
        "hatau_suchi": BuiltinFunction("hatau_suchi", _builtin_hatau_suchi, arity=2),
        "khoj_suchi": BuiltinFunction("khoj_suchi", _builtin_khoj_suchi, arity=2),
        "thulo": BuiltinFunction("thulo", _builtin_thulo, arity=None),
        "sano": BuiltinFunction("sano", _builtin_sano, arity=None),
        "ghat": BuiltinFunction("ghat", _builtin_ghat, arity=1),
    }

    for name, fn in builtins_map.items():
        global_env.define(name, fn)
