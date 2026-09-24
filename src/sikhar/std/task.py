"""
Sikhar Standard Library: std.task
Concurrency, asynchronous task spawning, and thread workers.
"""

import threading
import time
from typing import Any, Dict, List, Optional

from ..interpreter.values import BuiltinFunction, SikharModule
from ..errors.error_types import SikharTypeError, SikharRuntimeError


class TaskHandle:
    def __init__(self, task_id: int, fn: Any, args: List[Any], interp: Any):
        self.task_id = task_id
        self.fn = fn
        self.args = args
        self.interp = interp
        self.result: Any = None
        self.error: Optional[Exception] = None
        self.done = threading.Event()
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def _worker(self) -> None:
        try:
            worker_interp = self.interp
            if hasattr(self.interp, "call_function"):
                # VM instance: create an isolated VM thread runner to avoid stack corruption
                from ..vm.vm import VM
                worker_vm = VM(
                    filename=getattr(self.interp, "filename", "<task>"),
                    source=getattr(self.interp, "source", None),
                    output_fn=getattr(self.interp, "output_fn", print),
                    input_fn=getattr(self.interp, "input_fn", input),
                )
                if hasattr(self.interp, "globals") and isinstance(self.interp.globals, dict):
                    worker_vm.globals = dict(self.interp.globals)
                if hasattr(self.interp, "module_cache") and isinstance(self.interp.module_cache, dict):
                    worker_vm.module_cache = dict(self.interp.module_cache)
                worker_interp = worker_vm
            elif hasattr(self.interp, "execute_block"):
                # Interpreter instance: create an isolated Interpreter runner to avoid current_env races
                from ..interpreter.interpreter import Interpreter
                worker_interp = Interpreter(
                    source=getattr(self.interp, "source", ""),
                    filename=getattr(self.interp, "filename", "<task>"),
                    output_fn=getattr(self.interp, "output_fn", print),
                    input_fn=getattr(self.interp, "input_fn", input),
                )
                worker_interp.globals = self.interp.globals
                worker_interp.current_env = self.interp.current_env
                if hasattr(self.interp, "module_cache"):
                    worker_interp.module_cache = dict(self.interp.module_cache)

            if hasattr(self.fn, "call"):
                self.result = self.fn.call(worker_interp, self.args, 1, 1)
            elif callable(self.fn):
                self.result = self.fn(*self.args)
            else:
                self.error = SikharRuntimeError("Task target is not callable")
        except Exception as e:
            self.error = e
        finally:
            self.done.set()

    def wait(self, timeout: Optional[float] = None) -> Any:
        finished = self.done.wait(timeout=timeout)
        if not finished:
            raise SikharRuntimeError(f"Task {self.task_id} timed out after {timeout} seconds")
        if self.error:
            raise SikharRuntimeError(f"Task {self.task_id} failed: {self.error}")
        return self.result

    def is_done(self) -> bool:
        return self.done.is_set()


_NEXT_TASK_ID = 1
_TASK_LOCK = threading.Lock()


def _get_next_id() -> int:
    global _NEXT_TASK_ID
    with _TASK_LOCK:
        tid = _NEXT_TASK_ID
        _NEXT_TASK_ID += 1
        return tid


def create_task_module() -> SikharModule:
    exports = {}

    def _spawn(interp: Any, args: List[Any], line: int, col: int) -> Dict[str, Any]:
        if not args or len(args) > 2:
            raise SikharTypeError("std.task.spawn expects (function, [arguments_list])", filename=interp.filename, line=line, column=col)
        fn = args[0]
        fn_args = args[1] if len(args) == 2 and isinstance(args[1], list) else []

        tid = _get_next_id()
        handle = TaskHandle(tid, fn, fn_args, interp)

        return {
            "id": tid,
            "wait": BuiltinFunction("wait", lambda _i, a, l, c: handle.wait(float(a[0]) if a else None)),
            "is_done": BuiltinFunction("is_done", lambda _i, a, l, c: handle.is_done()),
        }

    def _wait(interp: Any, args: List[Any], line: int, col: int) -> Any:
        if not args or len(args) > 2 or not isinstance(args[0], dict) or "wait" not in args[0]:
            raise SikharTypeError("std.task.wait expects (task_handle, [timeout])", filename=interp.filename, line=line, column=col)
        handle_dict = args[0]
        timeout = float(args[1]) if len(args) == 2 and args[1] is not None else None
        wait_fn = handle_dict["wait"]
        if hasattr(wait_fn, "call"):
            return wait_fn.call(interp, [timeout] if timeout is not None else [], line, col)
        elif callable(wait_fn):
            return wait_fn([timeout] if timeout is not None else [])
        raise SikharRuntimeError("Invalid task handle", filename=interp.filename, line=line, column=col)

    def _sleep(interp: Any, args: List[Any], line: int, col: int) -> None:
        if not args or not isinstance(args[0], (int, float)):
            raise SikharTypeError("std.task.sleep expects 1 number (seconds)", filename=interp.filename, line=line, column=col)
        time.sleep(float(args[0]))
        return None

    exports["spawn"] = BuiltinFunction("spawn", _spawn, arity=None)
    exports["suru"] = exports["spawn"]

    exports["wait"] = BuiltinFunction("wait", _wait, arity=None)
    exports["parkha"] = exports["wait"]

    exports["sleep"] = BuiltinFunction("sleep", _sleep, arity=1)
    exports["suta"] = exports["sleep"]

    return SikharModule("std.task", exports)
