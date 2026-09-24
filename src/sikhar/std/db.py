"""
Sikhar Standard Library: std.db
Database driver interface and embedded SQLite engine.
"""

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..interpreter.values import BuiltinFunction, SikharModule
from ..errors.error_types import SikharTypeError, SikharRuntimeError


def _convert_param(p: Any) -> Any:
    """Convert Sikhar values into SQLite-friendly types."""
    if p is None or isinstance(p, (int, float, str, bytes, bool)):
        return p
    return str(p)


def _prepare_params(params_arg: Any) -> Any:
    if params_arg is None:
        return ()
    if isinstance(params_arg, list):
        return [_convert_param(x) for x in params_arg]
    if isinstance(params_arg, dict):
        return {str(k): _convert_param(v) for k, v in params_arg.items()}
    return (_convert_param(params_arg),)


class SikharDBConnection:
    """Active SQLite database connection handle."""

    def __init__(self, db_path: str, interp: Any):
        self.db_path = db_path
        self.interp = interp
        try:
            if db_path != ":memory:":
                Path(db_path).parent.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(db_path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
        except Exception as e:
            raise SikharRuntimeError(f"Failed to connect to database '{db_path}': {e}", filename=interp.filename)

    def execute(self, sql: str, params: Any = None) -> Dict[str, Any]:
        try:
            cur = self._conn.cursor()
            prepared = _prepare_params(params)
            cur.execute(sql, prepared)
            self._conn.commit()
            return {
                "rows_affected": cur.rowcount if cur.rowcount >= 0 else 0,
                "last_id": cur.lastrowid if cur.lastrowid is not None else 0,
            }
        except Exception as e:
            raise SikharRuntimeError(f"Database execute error: {e}", filename=self.interp.filename)

    def query(self, sql: str, params: Any = None) -> List[Dict[str, Any]]:
        try:
            cur = self._conn.cursor()
            prepared = _prepare_params(params)
            cur.execute(sql, prepared)
            rows = cur.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            raise SikharRuntimeError(f"Database query error: {e}", filename=self.interp.filename)

    def query_one(self, sql: str, params: Any = None) -> Optional[Dict[str, Any]]:
        try:
            cur = self._conn.cursor()
            prepared = _prepare_params(params)
            cur.execute(sql, prepared)
            row = cur.fetchone()
            return dict(row) if row is not None else None
        except Exception as e:
            raise SikharRuntimeError(f"Database query_one error: {e}", filename=self.interp.filename)

    def commit(self) -> None:
        try:
            self._conn.commit()
        except Exception as e:
            raise SikharRuntimeError(f"Database commit error: {e}", filename=self.interp.filename)

    def rollback(self) -> None:
        try:
            self._conn.rollback()
        except Exception as e:
            raise SikharRuntimeError(f"Database rollback error: {e}", filename=self.interp.filename)

    def close(self) -> None:
        try:
            self._conn.close()
        except Exception:
            pass


def create_db_module() -> SikharModule:
    exports = {}

    def _connect(interp: Any, args: List[Any], line: int, col: int) -> Dict[str, Any]:
        if len(args) != 1 or not isinstance(args[0], str):
            raise SikharTypeError("std.db.connect expects 1 database path argument (e.g. ':memory:' or file path)", filename=interp.filename, line=line, column=col)
        path_str = args[0]
        conn = SikharDBConnection(path_str, interp)

        def _execute(_i: Any, a: List[Any], l: int, c: int) -> Dict[str, Any]:
            if not a or len(a) > 2:
                raise SikharTypeError("conn.execute expects (sql, [params])", filename=interp.filename, line=l, column=c)
            params = a[1] if len(a) == 2 else None
            return conn.execute(str(a[0]), params)

        def _query(_i: Any, a: List[Any], l: int, c: int) -> List[Dict[str, Any]]:
            if not a or len(a) > 2:
                raise SikharTypeError("conn.query expects (sql, [params])", filename=interp.filename, line=l, column=c)
            params = a[1] if len(a) == 2 else None
            return conn.query(str(a[0]), params)

        def _query_one(_i: Any, a: List[Any], l: int, c: int) -> Optional[Dict[str, Any]]:
            if not a or len(a) > 2:
                raise SikharTypeError("conn.query_one expects (sql, [params])", filename=interp.filename, line=l, column=c)
            params = a[1] if len(a) == 2 else None
            return conn.query_one(str(a[0]), params)

        def _commit(_i: Any, a: List[Any], l: int, c: int) -> None:
            conn.commit()
            return None

        def _rollback(_i: Any, a: List[Any], l: int, c: int) -> None:
            conn.rollback()
            return None

        def _close(_i: Any, a: List[Any], l: int, c: int) -> None:
            conn.close()
            return None

        return {
            "execute": BuiltinFunction("execute", _execute, arity=None),
            "chalaau": BuiltinFunction("chalaau", _execute, arity=None),
            "query": BuiltinFunction("query", _query, arity=None),
            "khoja": BuiltinFunction("khoja", _query, arity=None),
            "query_one": BuiltinFunction("query_one", _query_one, arity=None),
            "commit": BuiltinFunction("commit", _commit, arity=0),
            "rollback": BuiltinFunction("rollback", _rollback, arity=0),
            "close": BuiltinFunction("close", _close, arity=0),
            "banda": BuiltinFunction("banda", _close, arity=0),
        }

    exports["connect"] = BuiltinFunction("connect", _connect, arity=1)
    exports["joda"] = exports["connect"]

    return SikharModule("std.db", exports)
