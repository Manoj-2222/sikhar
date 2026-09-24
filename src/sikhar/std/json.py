"""
Sikhar Standard Library: std.json
JSON serialization, deserialization, and validation.
"""

import json
from typing import Any, List
from ..interpreter.values import BuiltinFunction, SikharModule
from ..errors.error_types import SikharTypeError, SikharRuntimeError


def _to_json_compatible(val: Any) -> Any:
    """Recursively ensure Sikhar objects can be safely converted to JSON."""
    if val is None or isinstance(val, (int, float, str, bool)):
        return val
    elif isinstance(val, list):
        return [_to_json_compatible(x) for x in val]
    elif isinstance(val, dict):
        return {str(k): _to_json_compatible(v) for k, v in val.items()}
    elif isinstance(val, SikharModule):
        return {str(k): _to_json_compatible(v) for k, v in val.exports.items()}
    return str(val)


def create_json_module() -> SikharModule:
    exports = {}

    def _parse(interp: Any, args: List[Any], line: int, col: int) -> Any:
        if len(args) != 1 or not isinstance(args[0], str):
            raise SikharTypeError("std.json.parse expects 1 string argument", filename=interp.filename, line=line, column=col)
        text = args[0]
        try:
            return json.loads(text)
        except Exception as e:
            raise SikharRuntimeError(f"JSON parse error: {e}", filename=interp.filename, line=line, column=col)

    def _stringify(interp: Any, args: List[Any], line: int, col: int) -> str:
        if len(args) not in (1, 2):
            raise SikharTypeError("std.json.stringify expects 1 or 2 arguments: (value, [indent])", filename=interp.filename, line=line, column=col)
        val = args[0]
        indent = None
        if len(args) == 2:
            if isinstance(args[1], int) and args[1] >= 0:
                indent = args[1]
            elif args[1] is not None:
                raise SikharTypeError("std.json.stringify indent must be an integer", filename=interp.filename, line=line, column=col)

        try:
            cleaned = _to_json_compatible(val)
            return json.dumps(cleaned, indent=indent, ensure_ascii=False)
        except Exception as e:
            raise SikharRuntimeError(f"JSON stringify error: {e}", filename=interp.filename, line=line, column=col)

    def _valid(interp: Any, args: List[Any], line: int, col: int) -> bool:
        if len(args) != 1 or not isinstance(args[0], str):
            return False
        try:
            json.loads(args[0])
            return True
        except Exception:
            return False

    exports["parse"] = BuiltinFunction("parse", _parse, arity=1)
    exports["padh"] = exports["parse"]
    exports["chin"] = exports["parse"]

    exports["stringify"] = BuiltinFunction("stringify", _stringify, arity=None)
    exports["rupantar"] = exports["stringify"]
    exports["lekh"] = exports["stringify"]

    exports["valid"] = BuiltinFunction("valid", _valid, arity=1)
    exports["sacho"] = exports["valid"]

    return SikharModule("std.json", exports)
