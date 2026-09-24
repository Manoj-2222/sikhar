"""
Sikhar Standard Library: std.process
Child process execution, system commands, environment variables, and CLI arguments.
"""

import os
import subprocess
import sys
from typing import Any, Dict, List, Optional

from ..interpreter.values import BuiltinFunction, SikharModule
from ..errors.error_types import SikharTypeError, SikharRuntimeError


def create_process_module() -> SikharModule:
    exports = {}

    def _exec(interp: Any, args: List[Any], line: int, col: int) -> Dict[str, Any]:
        if not args or len(args) > 2:
            raise SikharTypeError("std.process.exec expects (command, [timeout_seconds=30])", filename=interp.filename, line=line, column=col)
        command = str(args[0])
        timeout = float(args[1]) if len(args) == 2 else 30.0

        try:
            res = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return {
                "stdout": res.stdout,
                "stderr": res.stderr,
                "code": res.returncode,
                "ok": res.returncode == 0,
            }
        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds",
                "code": -1,
                "ok": False,
            }
        except Exception as e:
            raise SikharRuntimeError(f"Process execution failed: {e}", filename=interp.filename, line=line, column=col)

    def _env(interp: Any, args: List[Any], line: int, col: int) -> Optional[str]:
        if not args or len(args) > 2:
            raise SikharTypeError("std.process.env expects (key, [default])", filename=interp.filename, line=line, column=col)
        key = str(args[0])
        default = str(args[1]) if len(args) == 2 else None
        return os.environ.get(key, default)

    def _set_env(interp: Any, args: List[Any], line: int, col: int) -> None:
        if len(args) != 2:
            raise SikharTypeError("std.process.set_env expects (key, value)", filename=interp.filename, line=line, column=col)
        os.environ[str(args[0])] = str(args[1])
        return None

    def _args(interp: Any, args: List[Any], line: int, col: int) -> List[str]:
        return list(sys.argv[1:])

    def _cwd(interp: Any, args: List[Any], line: int, col: int) -> str:
        return os.getcwd()

    exports["exec"] = BuiltinFunction("exec", _exec, arity=None)
    exports["chalaau"] = exports["exec"]

    exports["env"] = BuiltinFunction("env", _env, arity=None)
    exports["set_env"] = BuiltinFunction("set_env", _set_env, arity=2)
    exports["args"] = BuiltinFunction("args", _args, arity=0)
    exports["cwd"] = BuiltinFunction("cwd", _cwd, arity=0)

    return SikharModule("std.process", exports)
