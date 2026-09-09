"""
Sikhar Standard Library: std.math
"""

import math
from typing import Any, List
from ..interpreter.values import BuiltinFunction, SikharModule
from ..errors.error_types import SikharTypeError


def create_math_module() -> SikharModule:
    exports = {}

    def _sqrt(interp: Any, args: List[Any], line: int, col: int) -> float:
        if len(args) != 1:
            raise SikharTypeError("std.math.sqrt expects 1 argument", filename=interp.filename, line=line, column=col)
        return math.sqrt(args[0])

    def _pow(interp: Any, args: List[Any], line: int, col: int) -> float:
        if len(args) != 2:
            raise SikharTypeError("std.math.pow expects 2 arguments: (base, exp)", filename=interp.filename, line=line, column=col)
        return math.pow(args[0], args[1])

    def _abs(interp: Any, args: List[Any], line: int, col: int) -> float:
        if len(args) != 1:
            raise SikharTypeError("std.math.abs expects 1 argument", filename=interp.filename, line=line, column=col)
        return abs(args[0])

    def _sin(interp: Any, args: List[Any], line: int, col: int) -> float:
        if len(args) != 1:
            raise SikharTypeError("std.math.sin expects 1 argument", filename=interp.filename, line=line, column=col)
        return math.sin(args[0])

    def _cos(interp: Any, args: List[Any], line: int, col: int) -> float:
        if len(args) != 1:
            raise SikharTypeError("std.math.cos expects 1 argument", filename=interp.filename, line=line, column=col)
        return math.cos(args[0])

    def _tan(interp: Any, args: List[Any], line: int, col: int) -> float:
        if len(args) != 1:
            raise SikharTypeError("std.math.tan expects 1 argument", filename=interp.filename, line=line, column=col)
        return math.tan(args[0])

    def _floor(interp: Any, args: List[Any], line: int, col: int) -> int:
        if len(args) != 1:
            raise SikharTypeError("std.math.floor expects 1 argument", filename=interp.filename, line=line, column=col)
        return math.floor(args[0])

    def _ceil(interp: Any, args: List[Any], line: int, col: int) -> int:
        if len(args) != 1:
            raise SikharTypeError("std.math.ceil expects 1 argument", filename=interp.filename, line=line, column=col)
        return math.ceil(args[0])

    def _round(interp: Any, args: List[Any], line: int, col: int) -> Any:
        if len(args) == 1:
            return round(args[0])
        elif len(args) == 2:
            return round(args[0], args[1])
        raise SikharTypeError("std.math.round expects 1 or 2 arguments", filename=interp.filename, line=line, column=col)

    def _log(interp: Any, args: List[Any], line: int, col: int) -> float:
        if len(args) == 1:
            return math.log(args[0])
        elif len(args) == 2:
            return math.log(args[0], args[1])
        raise SikharTypeError("std.math.log expects 1 or 2 arguments", filename=interp.filename, line=line, column=col)

    exports["pi"] = math.pi
    exports["e"] = math.e
    exports["sqrt"] = BuiltinFunction("sqrt", _sqrt, arity=1)
    exports["pow"] = BuiltinFunction("pow", _pow, arity=2)
    exports["ghaat"] = exports["pow"]
    exports["abs"] = BuiltinFunction("abs", _abs, arity=1)
    exports["sin"] = BuiltinFunction("sin", _sin, arity=1)
    exports["cos"] = BuiltinFunction("cos", _cos, arity=1)
    exports["tan"] = BuiltinFunction("tan", _tan, arity=1)
    exports["floor"] = BuiltinFunction("floor", _floor, arity=1)
    exports["ceil"] = BuiltinFunction("ceil", _ceil, arity=1)
    exports["round"] = BuiltinFunction("round", _round, arity=None)
    exports["log"] = BuiltinFunction("log", _log, arity=None)
    exports["vargamul"] = exports["sqrt"]

    return SikharModule("std.math", exports)
