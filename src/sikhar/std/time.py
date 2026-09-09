"""
Sikhar Standard Library: std.time
"""

import time
from typing import Any, List
from ..interpreter.values import BuiltinFunction, SikharModule
from ..errors.error_types import SikharTypeError


def create_time_module() -> SikharModule:
    exports = {}

    def _now(interp: Any, args: List[Any], line: int, col: int) -> float:
        return time.time()

    def _sleep(interp: Any, args: List[Any], line: int, col: int) -> None:
        if len(args) != 1 or not isinstance(args[0], (int, float)):
            raise SikharTypeError("std.time.sleep expects seconds as a number", filename=interp.filename, line=line, column=col)
        time.sleep(args[0])
        return None

    def _format(interp: Any, args: List[Any], line: int, col: int) -> str:
        ts = args[0] if args else time.time()
        fmt = str(args[1]) if len(args) > 1 else "%Y-%m-%d %H:%M:%S"
        return time.strftime(fmt, time.localtime(ts))

    exports["now"] = BuiltinFunction("now", _now, arity=0)
    exports["sleep"] = BuiltinFunction("sleep", _sleep, arity=1)
    exports["format"] = BuiltinFunction("format", _format, arity=None)

    return SikharModule("std.time", exports)
