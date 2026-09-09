"""
Sikhar Standard Library: std.map
"""

from typing import Any, List
from ..interpreter.values import BuiltinFunction, SikharModule
from ..errors.error_types import SikharTypeError


def create_map_module() -> SikharModule:
    exports = {}

    def _keys(interp: Any, args: List[Any], line: int, col: int) -> List[Any]:
        if len(args) != 1 or not isinstance(args[0], dict):
            raise SikharTypeError("std.map.keys expects a map", filename=interp.filename, line=line, column=col)
        return list(args[0].keys())

    def _values(interp: Any, args: List[Any], line: int, col: int) -> List[Any]:
        if len(args) != 1 or not isinstance(args[0], dict):
            raise SikharTypeError("std.map.values expects a map", filename=interp.filename, line=line, column=col)
        return list(args[0].values())

    def _entries(interp: Any, args: List[Any], line: int, col: int) -> List[List[Any]]:
        if len(args) != 1 or not isinstance(args[0], dict):
            raise SikharTypeError("std.map.entries expects a map", filename=interp.filename, line=line, column=col)
        return [[k, v] for k, v in args[0].items()]

    def _has(interp: Any, args: List[Any], line: int, col: int) -> bool:
        if len(args) != 2 or not isinstance(args[0], dict):
            raise SikharTypeError("std.map.has expects (map, key)", filename=interp.filename, line=line, column=col)
        return args[1] in args[0]

    def _merge(interp: Any, args: List[Any], line: int, col: int) -> dict:
        if len(args) != 2 or not isinstance(args[0], dict) or not isinstance(args[1], dict):
            raise SikharTypeError("std.map.merge expects (map1, map2)", filename=interp.filename, line=line, column=col)
        new_map = dict(args[0])
        new_map.update(args[1])
        return new_map

    exports["keys"] = BuiltinFunction("keys", _keys, arity=1)
    exports["kunji"] = exports["keys"]
    exports["values"] = BuiltinFunction("values", _values, arity=1)
    exports["man"] = exports["values"]
    exports["entries"] = BuiltinFunction("entries", _entries, arity=1)
    exports["has"] = BuiltinFunction("has", _has, arity=2)
    exports["cha"] = exports["has"]
    exports["merge"] = BuiltinFunction("merge", _merge, arity=2)
    exports["misa"] = exports["merge"]

    return SikharModule("std.map", exports)
