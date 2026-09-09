"""
Sikhar Standard Library: std.text
"""

from typing import Any, List
from ..interpreter.values import BuiltinFunction, SikharModule, sikhar_stringify
from ..errors.error_types import SikharTypeError


def create_text_module() -> SikharModule:
    exports = {}

    def _upper(interp: Any, args: List[Any], line: int, col: int) -> str:
        if len(args) != 1:
            raise SikharTypeError("std.text.upper expects 1 argument", filename=interp.filename, line=line, column=col)
        return str(args[0]).upper()

    def _lower(interp: Any, args: List[Any], line: int, col: int) -> str:
        if len(args) != 1:
            raise SikharTypeError("std.text.lower expects 1 argument", filename=interp.filename, line=line, column=col)
        return str(args[0]).lower()

    def _trim(interp: Any, args: List[Any], line: int, col: int) -> str:
        if len(args) != 1:
            raise SikharTypeError("std.text.trim expects 1 argument", filename=interp.filename, line=line, column=col)
        return str(args[0]).strip()

    def _split(interp: Any, args: List[Any], line: int, col: int) -> List[str]:
        if len(args) == 1:
            return str(args[0]).split()
        elif len(args) == 2:
            return str(args[0]).split(str(args[1]))
        raise SikharTypeError("std.text.split expects 1 or 2 arguments", filename=interp.filename, line=line, column=col)

    def _join(interp: Any, args: List[Any], line: int, col: int) -> str:
        if len(args) != 2:
            raise SikharTypeError("std.text.join expects 2 arguments: (list, separator)", filename=interp.filename, line=line, column=col)
        lst, sep = args
        if not isinstance(lst, list):
            raise SikharTypeError("First argument to std.text.join must be a list", filename=interp.filename, line=line, column=col)
        return str(sep).join(sikhar_stringify(item) for item in lst)

    def _replace(interp: Any, args: List[Any], line: int, col: int) -> str:
        if len(args) != 3:
            raise SikharTypeError("std.text.replace expects 3 arguments: (text, old, new)", filename=interp.filename, line=line, column=col)
        return str(args[0]).replace(str(args[1]), str(args[2]))

    def _contains(interp: Any, args: List[Any], line: int, col: int) -> bool:
        if len(args) != 2:
            raise SikharTypeError("std.text.contains expects 2 arguments: (text, substring)", filename=interp.filename, line=line, column=col)
        return str(args[1]) in str(args[0])

    def _starts_with(interp: Any, args: List[Any], line: int, col: int) -> bool:
        if len(args) != 2:
            raise SikharTypeError("std.text.starts_with expects 2 arguments: (text, prefix)", filename=interp.filename, line=line, column=col)
        return str(args[0]).startswith(str(args[1]))

    def _ends_with(interp: Any, args: List[Any], line: int, col: int) -> bool:
        if len(args) != 2:
            raise SikharTypeError("std.text.ends_with expects 2 arguments: (text, suffix)", filename=interp.filename, line=line, column=col)
        return str(args[0]).endswith(str(args[1]))

    exports["upper"] = BuiltinFunction("upper", _upper, arity=1)
    exports["thulo"] = exports["upper"]
    exports["lower"] = BuiltinFunction("lower", _lower, arity=1)
    exports["sano"] = exports["lower"]
    exports["trim"] = BuiltinFunction("trim", _trim, arity=1)
    exports["split"] = BuiltinFunction("split", _split, arity=None)
    exports["tukra"] = exports["split"]
    exports["join"] = BuiltinFunction("join", _join, arity=2)
    exports["replace"] = BuiltinFunction("replace", _replace, arity=3)
    exports["contains"] = BuiltinFunction("contains", _contains, arity=2)
    exports["starts_with"] = BuiltinFunction("starts_with", _starts_with, arity=2)
    exports["ends_with"] = BuiltinFunction("ends_with", _ends_with, arity=2)

    return SikharModule("std.text", exports)
