"""
Sikhar Standard Library: std.list
"""

from typing import Any, List
from ..interpreter.values import BuiltinFunction, SikharModule, SikharCallable, is_truthy
from ..errors.error_types import SikharTypeError


def create_list_module() -> SikharModule:
    exports = {}

    def _reverse(interp: Any, args: List[Any], line: int, col: int) -> List[Any]:
        if len(args) != 1 or not isinstance(args[0], list):
            raise SikharTypeError("std.list.reverse expects a list", filename=interp.filename, line=line, column=col)
        return list(reversed(args[0]))

    def _sort(interp: Any, args: List[Any], line: int, col: int) -> List[Any]:
        if len(args) != 1 or not isinstance(args[0], list):
            raise SikharTypeError("std.list.sort expects a list", filename=interp.filename, line=line, column=col)
        return sorted(args[0])

    def _slice(interp: Any, args: List[Any], line: int, col: int) -> List[Any]:
        if len(args) not in (2, 3) or not isinstance(args[0], list):
            raise SikharTypeError("std.list.slice expects (list, start, [end])", filename=interp.filename, line=line, column=col)
        lst = args[0]
        start = args[1]
        end = args[2] if len(args) == 3 else len(lst)
        return lst[start:end]

    def _filter(interp: Any, args: List[Any], line: int, col: int) -> List[Any]:
        if len(args) != 2 or not isinstance(args[0], list) or not isinstance(args[1], SikharCallable):
            raise SikharTypeError("std.list.filter expects (list, predicate_fn)", filename=interp.filename, line=line, column=col)
        lst, fn = args[0], args[1]
        res = []
        for item in lst:
            if is_truthy(fn.call(interp, [item], line, col)):
                res.append(item)
        return res

    def _map(interp: Any, args: List[Any], line: int, col: int) -> List[Any]:
        if len(args) != 2 or not isinstance(args[0], list) or not isinstance(args[1], SikharCallable):
            raise SikharTypeError("std.list.map expects (list, transform_fn)", filename=interp.filename, line=line, column=col)
        lst, fn = args[0], args[1]
        return [fn.call(interp, [item], line, col) for item in lst]

    def _sum(interp: Any, args: List[Any], line: int, col: int) -> Any:
        if len(args) != 1 or not isinstance(args[0], list):
            raise SikharTypeError("std.list.sum expects a list of numbers", filename=interp.filename, line=line, column=col)
        return sum(args[0])

    def _min(interp: Any, args: List[Any], line: int, col: int) -> Any:
        if len(args) != 1 or not isinstance(args[0], list) or not args[0]:
            raise SikharTypeError("std.list.min expects a non-empty list", filename=interp.filename, line=line, column=col)
        return min(args[0])

    def _max(interp: Any, args: List[Any], line: int, col: int) -> Any:
        if len(args) != 1 or not isinstance(args[0], list) or not args[0]:
            raise SikharTypeError("std.list.max expects a non-empty list", filename=interp.filename, line=line, column=col)
        return max(args[0])

    def _contains(interp: Any, args: List[Any], line: int, col: int) -> bool:
        if len(args) != 2 or not isinstance(args[0], list):
            raise SikharTypeError("std.list.contains expects (list, item)", filename=interp.filename, line=line, column=col)
        return args[1] in args[0]

    exports["reverse"] = BuiltinFunction("reverse", _reverse, arity=1)
    exports["ulta"] = exports["reverse"]
    exports["sort"] = BuiltinFunction("sort", _sort, arity=1)
    exports["kram"] = exports["sort"]
    exports["slice"] = BuiltinFunction("slice", _slice, arity=None)
    exports["tukra"] = exports["slice"]
    exports["filter"] = BuiltinFunction("filter", _filter, arity=2)
    exports["map"] = BuiltinFunction("map", _map, arity=2)
    exports["sum"] = BuiltinFunction("sum", _sum, arity=1)
    exports["jamma"] = exports["sum"]
    exports["min"] = BuiltinFunction("min", _min, arity=1)
    exports["max"] = BuiltinFunction("max", _max, arity=1)
    exports["contains"] = BuiltinFunction("contains", _contains, arity=2)

    return SikharModule("std.list", exports)
