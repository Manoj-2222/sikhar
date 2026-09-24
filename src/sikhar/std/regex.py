"""
Sikhar Standard Library: std.regex
Regular expression pattern matching, searches, substitutions, and splitting.
"""

import re
from typing import Any, List

from ..interpreter.values import BuiltinFunction, SikharModule
from ..errors.error_types import SikharTypeError, SikharRuntimeError


def create_regex_module() -> SikharModule:
    exports = {}

    def _match(interp: Any, args: List[Any], line: int, col: int) -> bool:
        if len(args) != 2:
            raise SikharTypeError("std.regex.match expects (pattern, text)", filename=interp.filename, line=line, column=col)
        pattern = str(args[0])
        text = str(args[1])
        try:
            return bool(re.search(pattern, text))
        except Exception as e:
            raise SikharRuntimeError(f"Regex match error: {e}", filename=interp.filename, line=line, column=col)

    def _find_all(interp: Any, args: List[Any], line: int, col: int) -> List[str]:
        if len(args) != 2:
            raise SikharTypeError("std.regex.find_all expects (pattern, text)", filename=interp.filename, line=line, column=col)
        pattern = str(args[0])
        text = str(args[1])
        try:
            matches = re.findall(pattern, text)
            if matches and isinstance(matches[0], tuple):
                return ["".join(m) if isinstance(m, tuple) else str(m) for m in matches]
            return [str(m) for m in matches]
        except Exception as e:
            raise SikharRuntimeError(f"Regex find_all error: {e}", filename=interp.filename, line=line, column=col)

    def _replace(interp: Any, args: List[Any], line: int, col: int) -> str:
        if len(args) != 3:
            raise SikharTypeError("std.regex.replace expects (pattern, replacement, text)", filename=interp.filename, line=line, column=col)
        pattern = str(args[0])
        replacement = str(args[1])
        text = str(args[2])
        try:
            return re.sub(pattern, replacement, text)
        except Exception as e:
            raise SikharRuntimeError(f"Regex replace error: {e}", filename=interp.filename, line=line, column=col)

    def _split(interp: Any, args: List[Any], line: int, col: int) -> List[str]:
        if len(args) != 2:
            raise SikharTypeError("std.regex.split expects (pattern, text)", filename=interp.filename, line=line, column=col)
        pattern = str(args[0])
        text = str(args[1])
        try:
            return re.split(pattern, text)
        except Exception as e:
            raise SikharRuntimeError(f"Regex split error: {e}", filename=interp.filename, line=line, column=col)

    exports["match"] = BuiltinFunction("match", _match, arity=2)
    exports["find_all"] = BuiltinFunction("find_all", _find_all, arity=2)
    exports["replace"] = BuiltinFunction("replace", _replace, arity=3)
    exports["split"] = BuiltinFunction("split", _split, arity=2)

    # Nepali aliases
    exports["milcha"] = exports["match"]
    exports["khoja"] = exports["find_all"]
    exports["badla"] = exports["replace"]

    return SikharModule("std.regex", exports)
