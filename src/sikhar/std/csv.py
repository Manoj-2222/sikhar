"""
Sikhar Standard Library: std.csv
CSV parsing, serialization, and file I/O operations.
"""

import csv
import io
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..interpreter.values import BuiltinFunction, SikharModule
from ..errors.error_types import SikharTypeError, SikharRuntimeError


def _parse_csv_string(text: str, has_headers: bool = True, delimiter: str = ",") -> List[Any]:
    f = io.StringIO(text.strip())
    if has_headers:
        reader = csv.DictReader(f, delimiter=delimiter)
        return [dict(row) for row in reader]
    else:
        reader = csv.reader(f, delimiter=delimiter)
        return [list(row) for row in reader]


def _stringify_csv_data(rows: List[Any], headers: Optional[List[str]] = None, delimiter: str = ",") -> str:
    out = io.StringIO()
    if not rows:
        return ""

    if isinstance(rows[0], dict):
        fieldnames = headers or list(rows[0].keys())
        writer = csv.DictWriter(out, fieldnames=fieldnames, delimiter=delimiter, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            clean_row = {k: str(row.get(k, "")) for k in fieldnames}
            writer.writerow(clean_row)
    elif isinstance(rows[0], list):
        writer = csv.writer(out, delimiter=delimiter, lineterminator="\n")
        if headers:
            writer.writerow(headers)
        for row in rows:
            writer.writerow([str(x) for x in row])
    else:
        writer = csv.writer(out, delimiter=delimiter, lineterminator="\n")
        for row in rows:
            writer.writerow([str(row)])

    return out.getvalue()


def create_csv_module() -> SikharModule:
    exports = {}

    def _parse(interp: Any, args: List[Any], line: int, col: int) -> List[Any]:
        if not args or len(args) > 3 or not isinstance(args[0], str):
            raise SikharTypeError("std.csv.parse expects (csv_text, [has_headers=true], [delimiter=','])", filename=interp.filename, line=line, column=col)
        text = args[0]
        has_headers = bool(args[1]) if len(args) >= 2 else True
        delimiter = str(args[2]) if len(args) >= 3 else ","
        try:
            return _parse_csv_string(text, has_headers=has_headers, delimiter=delimiter)
        except Exception as e:
            raise SikharRuntimeError(f"CSV parse error: {e}", filename=interp.filename, line=line, column=col)

    def _stringify(interp: Any, args: List[Any], line: int, col: int) -> str:
        if not args or len(args) > 3 or not isinstance(args[0], list):
            raise SikharTypeError("std.csv.stringify expects (rows_list, [headers_list], [delimiter=','])", filename=interp.filename, line=line, column=col)
        rows = args[0]
        headers = None
        delimiter = ","
        if len(args) == 2:
            if isinstance(args[1], str):
                delimiter = args[1]
            elif isinstance(args[1], list):
                headers = args[1]
        elif len(args) >= 3:
            headers = args[1] if isinstance(args[1], list) else None
            delimiter = str(args[2])
        try:
            return _stringify_csv_data(rows, headers=headers, delimiter=delimiter)
        except Exception as e:
            raise SikharRuntimeError(f"CSV stringify error: {e}", filename=interp.filename, line=line, column=col)

    def _read(interp: Any, args: List[Any], line: int, col: int) -> List[Any]:
        if not args or len(args) > 3 or not isinstance(args[0], str):
            raise SikharTypeError("std.csv.read expects (file_path, [has_headers=true], [delimiter=','])", filename=interp.filename, line=line, column=col)
        path = Path(args[0])
        has_headers = bool(args[1]) if len(args) >= 2 else True
        delimiter = str(args[2]) if len(args) >= 3 else ","
        if not path.exists():
            raise SikharRuntimeError(f"File not found: '{args[0]}'", filename=interp.filename, line=line, column=col)
        try:
            content = path.read_text(encoding="utf-8")
            return _parse_csv_string(content, has_headers=has_headers, delimiter=delimiter)
        except Exception as e:
            raise SikharRuntimeError(f"CSV read error: {e}", filename=interp.filename, line=line, column=col)

    def _write(interp: Any, args: List[Any], line: int, col: int) -> bool:
        if len(args) < 2 or len(args) > 4:
            raise SikharTypeError("std.csv.write expects (file_path, rows, [headers], [delimiter=','])", filename=interp.filename, line=line, column=col)
        path = Path(args[0])
        rows = args[1]
        headers = None
        delimiter = ","
        if len(args) == 3:
            if isinstance(args[2], str):
                delimiter = args[2]
            elif isinstance(args[2], list):
                headers = args[2]
        elif len(args) >= 4:
            headers = args[2] if isinstance(args[2], list) else None
            delimiter = str(args[3])
        try:
            content = _stringify_csv_data(rows, headers=headers, delimiter=delimiter)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return True
        except Exception as e:
            raise SikharRuntimeError(f"CSV write error: {e}", filename=interp.filename, line=line, column=col)

    exports["parse"] = BuiltinFunction("parse", _parse, arity=None)
    exports["stringify"] = BuiltinFunction("stringify", _stringify, arity=None)
    exports["read"] = BuiltinFunction("read", _read, arity=None)
    exports["write"] = BuiltinFunction("write", _write, arity=None)

    # Nepali aliases
    exports["padh"] = exports["read"]
    exports["lekh"] = exports["write"]

    return SikharModule("std.csv", exports)
