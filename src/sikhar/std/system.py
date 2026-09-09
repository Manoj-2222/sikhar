"""
Sikhar Standard Library: std.system
"""

import sys
import os
import platform
from typing import Any, List
from ..interpreter.values import BuiltinFunction, SikharModule
from ..errors.error_types import SikharTypeError


def create_system_module() -> SikharModule:
    exports = {}

    def _args(interp: Any, args: List[Any], line: int, col: int) -> List[str]:
        return list(sys.argv)

    def _env(interp: Any, args: List[Any], line: int, col: int) -> Any:
        if len(args) == 1:
            return os.environ.get(str(args[0]), None)
        elif len(args) == 2:
            return os.environ.get(str(args[0]), args[1])
        raise SikharTypeError("std.system.env expects 1 or 2 arguments", filename=interp.filename, line=line, column=col)

    def _os_name(interp: Any, args: List[Any], line: int, col: int) -> str:
        return platform.system().lower()

    def _exit(interp: Any, args: List[Any], line: int, col: int) -> None:
        code = int(args[0]) if args else 0
        sys.exit(code)

    exports["args"] = BuiltinFunction("args", _args, arity=0)
    exports["env"] = BuiltinFunction("env", _env, arity=None)
    exports["os_name"] = BuiltinFunction("os_name", _os_name, arity=0)
    exports["exit"] = BuiltinFunction("exit", _exit, arity=None)

    return SikharModule("std.system", exports)
