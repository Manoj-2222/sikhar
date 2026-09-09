"""
Sikhar Standard Library: std.file
Safe, structured file I/O operations.
"""

from pathlib import Path
from typing import Any, List
from ..interpreter.values import BuiltinFunction, SikharModule, sikhar_stringify
from ..errors.error_types import SikharTypeError, SikharRuntimeError


def create_file_module() -> SikharModule:
    exports = {}

    def _read(interp: Any, args: List[Any], line: int, col: int) -> str:
        if len(args) != 1:
            raise SikharTypeError("std.file.read expects 1 argument (path)", filename=interp.filename, line=line, column=col)
        path = Path(str(args[0]))
        if not path.exists():
            raise SikharRuntimeError(f"File not found: '{path}'", filename=interp.filename, line=line, column=col)
        try:
            return path.read_text(encoding="utf-8")
        except Exception as e:
            raise SikharRuntimeError(f"Error reading file '{path}': {e}", filename=interp.filename, line=line, column=col)

    def _write(interp: Any, args: List[Any], line: int, col: int) -> int:
        if len(args) != 2:
            raise SikharTypeError("std.file.write expects 2 arguments: (path, content)", filename=interp.filename, line=line, column=col)
        path = Path(str(args[0]))
        content = sikhar_stringify(args[1])
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return len(content)
        except Exception as e:
            raise SikharRuntimeError(f"Error writing to file '{path}': {e}", filename=interp.filename, line=line, column=col)

    def _append(interp: Any, args: List[Any], line: int, col: int) -> int:
        if len(args) != 2:
            raise SikharTypeError("std.file.append expects 2 arguments: (path, content)", filename=interp.filename, line=line, column=col)
        path = Path(str(args[0]))
        content = sikhar_stringify(args[1])
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "a", encoding="utf-8") as f:
                f.write(content)
            return len(content)
        except Exception as e:
            raise SikharRuntimeError(f"Error appending to file '{path}': {e}", filename=interp.filename, line=line, column=col)

    def _exists(interp: Any, args: List[Any], line: int, col: int) -> bool:
        if len(args) != 1:
            raise SikharTypeError("std.file.exists expects 1 argument (path)", filename=interp.filename, line=line, column=col)
        return Path(str(args[0])).exists()

    def _remove(interp: Any, args: List[Any], line: int, col: int) -> bool:
        if len(args) != 1:
            raise SikharTypeError("std.file.remove expects 1 argument (path)", filename=interp.filename, line=line, column=col)
        path = Path(str(args[0]))
        if not path.exists():
            return False
        try:
            path.unlink()
            return True
        except Exception as e:
            raise SikharRuntimeError(f"Error removing file '{path}': {e}", filename=interp.filename, line=line, column=col)

    exports["read"] = BuiltinFunction("read", _read, arity=1)
    exports["padh"] = exports["read"]
    exports["write"] = BuiltinFunction("write", _write, arity=2)
    exports["lekh"] = exports["write"]
    exports["append"] = BuiltinFunction("append", _append, arity=2)
    exports["thap"] = exports["append"]
    exports["exists"] = BuiltinFunction("exists", _exists, arity=1)
    exports["cha"] = exports["exists"]
    exports["remove"] = BuiltinFunction("remove", _remove, arity=1)
    exports["hatau"] = exports["remove"]

    return SikharModule("std.file", exports)
