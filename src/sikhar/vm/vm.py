"""
Sikhar Stack-Based Virtual Machine (VM)
High-performance execution engine for Sikhar bytecode chunks.
"""

import sys
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from pathlib import Path

from .chunk import Chunk, BytecodeFunction
from .opcodes import OpCode
from ..interpreter.values import (
    BuiltinFunction,
    SikharCallable,
    SikharFunction,
    SikharModule,
    is_truthy,
    sikhar_stringify,
)
from ..runtime.builtins import register_builtins
from ..std import get_std_module
from ..errors.error_types import (
    SikharError,
    SikharRuntimeError,
    SikharTypeError,
    SikharIndexError,
    SikharKeyError,
    SikharDivisionByZeroError,
    SikharAssertionError,
    SikharConstantMutationError,
    SikharUserThrowError,
    SikharNameError,
)


class CallFrame:
    def __init__(self, function: BytecodeFunction, base_slot: int = 0, globals_dict: Optional[Dict[str, Any]] = None):
        self.function: BytecodeFunction = function
        self.ip: int = 0
        self.base_slot: int = base_slot
        self.globals: Dict[str, Any] = globals_dict if globals_dict is not None else {}
        self.try_stack: List[Tuple[int, int]] = []  # (catch_ip, saved_stack_depth)



class VM:
    def __init__(
        self,
        source: str = "",
        filename: str = "<stdin>",
        output_fn: Optional[Callable[[str], None]] = None,
        input_fn: Optional[Callable[[str], str]] = None,
    ):
        self.source: str = source
        self.filename: str = filename
        self.output_fn: Callable[[str], None] = output_fn if output_fn is not None else print
        self.input_fn: Callable[[str], str] = input_fn if input_fn is not None else input

        self.stack: List[Any] = []
        self.frames: List[CallFrame] = []
        self.globals: Dict[str, Any] = {}
        self.constants_set: Set[str] = set()
        self.exports: Dict[str, Any] = {}
        self.module_cache: Dict[str, SikharModule] = {}

        # Register standard builtins into VM globals
        register_builtins(self, self.output_fn, self.input_fn)

    def define(self, name: str, val: Any) -> None:
        """Helper for register_builtins compatibility."""
        self.globals[name] = val

    def _get_source_line(self, line_no: int) -> Optional[str]:
        if not self.source:
            return None
        lines = self.source.splitlines()
        if 1 <= line_no <= len(lines):
            return lines[line_no - 1]
        return None

    def push(self, val: Any) -> None:
        self.stack.append(val)

    def pop(self) -> Any:
        if not self.stack:
            raise SikharRuntimeError("VM stack underflow", filename=self.filename)
        return self.stack.pop()

    def peek(self, distance: int = 0) -> Any:
        idx = len(self.stack) - 1 - distance
        if idx < 0:
            raise SikharRuntimeError("VM stack peek underflow", filename=self.filename)
        return self.stack[idx]

    def run(self, chunk: Chunk) -> Any:
        top_fn = BytecodeFunction(name="<script>", arity=0, chunk=chunk)
        top_fn.globals = self.globals
        main_frame = CallFrame(top_fn, base_slot=0, globals_dict=self.globals)
        self.frames.append(main_frame)
        return self._execute()


    def _execute(self) -> Any:
        frames = self.frames
        stack = self.stack
        push = stack.append
        pop = stack.pop

        while frames:
            frame = frames[-1]
            code = frame.function.chunk.code
            constants = frame.function.chunk.constants

            if frame.ip >= len(code):
                frames.pop()
                if not frames:
                    return None
                continue

            op = code[frame.ip]
            line, col = frame.function.chunk.get_line_col(frame.ip)
            frame.ip += 1

            try:
                # ==========================================
                # Fast Path: Local Variables & Constants
                # ==========================================
                if op == OpCode.OP_GET_LOCAL:
                    slot = (code[frame.ip] << 8) | code[frame.ip + 1]
                    frame.ip += 2
                    push(stack[frame.base_slot + slot])

                elif op == OpCode.OP_SET_LOCAL:
                    slot = (code[frame.ip] << 8) | code[frame.ip + 1]
                    frame.ip += 2
                    stack[frame.base_slot + slot] = stack[-1]

                elif op == OpCode.OP_CONSTANT:
                    idx = (code[frame.ip] << 8) | code[frame.ip + 1]
                    frame.ip += 2
                    push(constants[idx])

                elif op == OpCode.OP_POP:
                    pop()

                elif op == OpCode.OP_DUP:
                    push(stack[-1])

                # ==========================================
                # Fast Path: Binary Arithmetic & Comparisons
                # ==========================================
                elif op == OpCode.OP_ADD:
                    b = pop()
                    a = pop()
                    if type(a) is int and type(b) is int:
                        push(a + b)
                    elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
                        push(a + b)
                    elif isinstance(a, str) or isinstance(b, str):
                        push(sikhar_stringify(a) + sikhar_stringify(b))
                    elif isinstance(a, list) and isinstance(b, list):
                        push(a + b)
                    else:
                        raise SikharTypeError(
                            f"Cannot add types '{type(a).__name__}' and '{type(b).__name__}'",
                            filename=self.filename,
                            line=line,
                            column=col,
                            source_line=self._get_source_line(line),
                        )

                elif op == OpCode.OP_SUBTRACT:
                    b = pop()
                    a = pop()
                    if type(a) is int and type(b) is int:
                        push(a - b)
                    elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
                        push(a - b)
                    else:
                        raise SikharTypeError(
                            f"Cannot subtract '{type(b).__name__}' from '{type(a).__name__}'",
                            filename=self.filename,
                            line=line,
                            column=col,
                            source_line=self._get_source_line(line),
                        )

                elif op == OpCode.OP_MULTIPLY:
                    b = pop()
                    a = pop()
                    if type(a) is int and type(b) is int:
                        push(a * b)
                    elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
                        push(a * b)
                    elif isinstance(a, str) and isinstance(b, int):
                        push(a * b)
                    elif isinstance(a, int) and isinstance(b, str):
                        push(b * a)
                    else:
                        raise SikharTypeError(
                            f"Cannot multiply '{type(a).__name__}' and '{type(b).__name__}'",
                            filename=self.filename,
                            line=line,
                            column=col,
                            source_line=self._get_source_line(line),
                        )

                elif op == OpCode.OP_LESS:
                    b = pop()
                    a = pop()
                    push(a < b)

                elif op == OpCode.OP_LESS_EQUAL:
                    b = pop()
                    a = pop()
                    push(a <= b)

                elif op == OpCode.OP_GREATER:
                    b = pop()
                    a = pop()
                    push(a > b)

                elif op == OpCode.OP_GREATER_EQUAL:
                    b = pop()
                    a = pop()
                    push(a >= b)

                elif op == OpCode.OP_EQUAL:
                    b = pop()
                    a = pop()
                    push(a == b)

                elif op == OpCode.OP_NOT_EQUAL:
                    b = pop()
                    a = pop()
                    push(a != b)

                # ==========================================
                # Fast Path: Control Flow
                # ==========================================
                elif op == OpCode.OP_LOOP:
                    offset = (code[frame.ip] << 8) | code[frame.ip + 1]
                    frame.ip += 2
                    frame.ip -= offset

                elif op == OpCode.OP_JUMP_IF_FALSE:
                    offset = (code[frame.ip] << 8) | code[frame.ip + 1]
                    frame.ip += 2
                    cond = pop()
                    if not is_truthy(cond):
                        frame.ip += offset

                elif op == OpCode.OP_JUMP:
                    offset = (code[frame.ip] << 8) | code[frame.ip + 1]
                    frame.ip += 2 + offset

                elif op == OpCode.OP_NIL:
                    push(None)

                elif op == OpCode.OP_TRUE:
                    push(True)

                elif op == OpCode.OP_FALSE:
                    push(False)


                # ==========================================
                # Unary Operators
                # ==========================================
                elif op == OpCode.OP_NEGATE:
                    val = pop()
                    if not isinstance(val, (int, float)):
                        raise SikharTypeError(
                            f"Operand for '-' must be a number, got '{type(val).__name__}'",
                            filename=self.filename,
                            line=line,
                            column=col,
                            source_line=self._get_source_line(line),
                        )
                    push(-val)

                elif op == OpCode.OP_NOT:
                    val = pop()
                    push(not is_truthy(val))

                elif op == OpCode.OP_DIVIDE:
                    b = pop()
                    a = pop()
                    if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
                        raise SikharTypeError(
                            f"Cannot divide '{type(a).__name__}' by '{type(b).__name__}'",
                            filename=self.filename,
                            line=line,
                            column=col,
                            source_line=self._get_source_line(line),
                        )
                    if b == 0:
                        raise SikharDivisionByZeroError(
                            "Division by zero ('sunya le bhag')",
                            filename=self.filename,
                            line=line,
                            column=col,
                            source_line=self._get_source_line(line),
                        )
                    res = a / b
                    if isinstance(a, int) and isinstance(b, int) and a % b == 0:
                        res = int(res)
                    push(res)

                elif op == OpCode.OP_MODULO:
                    b = pop()
                    a = pop()
                    if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
                        raise SikharTypeError(
                            f"Cannot modulo '{type(a).__name__}' and '{type(b).__name__}'",
                            filename=self.filename,
                            line=line,
                            column=col,
                            source_line=self._get_source_line(line),
                        )
                    if b == 0:
                        raise SikharDivisionByZeroError(
                            "Modulo by zero ('sunya le bhag')",
                            filename=self.filename,
                            line=line,
                            column=col,
                            source_line=self._get_source_line(line),
                        )
                    push(a % b)


                # ==========================================
                # Variables & Constants
                # ==========================================
                elif op == OpCode.OP_DEFINE_GLOBAL:
                    idx = (code[frame.ip] << 8) | code[frame.ip + 1]
                    frame.ip += 2
                    name = constants[idx]
                    val = self.pop()
                    frame.globals[name] = val

                elif op == OpCode.OP_DEFINE_CONST:
                    idx = (code[frame.ip] << 8) | code[frame.ip + 1]
                    frame.ip += 2
                    name = constants[idx]
                    val = self.pop()
                    frame.globals[name] = val
                    self.constants_set.add(name)

                elif op == OpCode.OP_GET_GLOBAL:
                    idx = (code[frame.ip] << 8) | code[frame.ip + 1]
                    frame.ip += 2
                    name = constants[idx]
                    if name in frame.globals:
                        self.push(frame.globals[name])
                    elif name in self.globals:
                        self.push(self.globals[name])
                    else:
                        raise SikharNameError(
                            f"Undefined variable '{name}'",
                            filename=self.filename,
                            line=line,
                            column=col,
                            source_line=self._get_source_line(line),
                        )

                elif op == OpCode.OP_SET_GLOBAL:
                    idx = (code[frame.ip] << 8) | code[frame.ip + 1]
                    frame.ip += 2
                    name = constants[idx]
                    if name in self.constants_set:
                        raise SikharConstantMutationError(
                            f"Cannot modify constant '{name}' declared with 'sthayi'",
                            filename=self.filename,
                            line=line,
                            column=col,
                            source_line=self._get_source_line(line),
                        )
                    val = self.peek()
                    frame.globals[name] = val


                elif op == OpCode.OP_GET_ITER:
                    val = self.pop()
                    if isinstance(val, (list, tuple)):
                        self.push(iter(val))
                    elif isinstance(val, str):
                        self.push(iter(val))
                    elif isinstance(val, dict):
                        self.push(iter(val.keys()))
                    else:
                        raise SikharTypeError(
                            f"Type '{type(val).__name__}' is not iterable in loop ('ko_lagi')",
                            filename=self.filename,
                            line=line,
                            column=col,
                            source_line=self._get_source_line(line),
                        )

                elif op == OpCode.OP_FOR_ITER:
                    offset = (code[frame.ip] << 8) | code[frame.ip + 1]
                    frame.ip += 2
                    iterator = self.peek()
                    try:
                        next_item = next(iterator)
                        self.push(next_item)
                    except StopIteration:
                        # Loop finished: pop iterator and jump past loop body
                        self.pop()
                        frame.ip += offset

                # ==========================================
                # Data Structures & Member Access
                # ==========================================
                elif op == OpCode.OP_BUILD_LIST:
                    count = (code[frame.ip] << 8) | code[frame.ip + 1]
                    frame.ip += 2
                    if count == 0:
                        self.push([])
                    else:
                        elements = self.stack[-count:]
                        del self.stack[-count:]
                        self.push(elements)

                elif op == OpCode.OP_BUILD_MAP:
                    pair_count = (code[frame.ip] << 8) | code[frame.ip + 1]
                    frame.ip += 2
                    items_count = pair_count * 2
                    if items_count == 0:
                        self.push({})
                    else:
                        raw = self.stack[-items_count:]
                        del self.stack[-items_count:]
                        mp = {}
                        for i in range(0, items_count, 2):
                            mp[raw[i]] = raw[i + 1]
                        self.push(mp)

                elif op == OpCode.OP_INDEX_GET:
                    index = self.pop()
                    target = self.pop()
                    if isinstance(target, list):
                        if not isinstance(index, int):
                            raise SikharTypeError("List index must be an integer", filename=self.filename, line=line, column=col)
                        if index < 0 or index >= len(target):
                            raise SikharIndexError(f"List index out of range: {index}", filename=self.filename, line=line, column=col)
                        self.push(target[index])
                    elif isinstance(target, str):
                        if not isinstance(index, int):
                            raise SikharTypeError("String index must be an integer", filename=self.filename, line=line, column=col)
                        if index < 0 or index >= len(target):
                            raise SikharIndexError(f"String index out of range: {index}", filename=self.filename, line=line, column=col)
                        self.push(target[index])
                    elif isinstance(target, dict):
                        if index not in target:
                            raise SikharKeyError(f"Key not found in map: '{index}'", filename=self.filename, line=line, column=col)
                        self.push(target[index])
                    else:
                        raise SikharTypeError(
                            f"Cannot index into type '{type(target).__name__}'",
                            filename=self.filename,
                            line=line,
                            column=col,
                        )

                elif op == OpCode.OP_INDEX_SET:
                    val = self.pop()
                    index = self.pop()
                    target = self.pop()
                    if isinstance(target, list):
                        if not isinstance(index, int):
                            raise SikharTypeError("List index must be an integer", filename=self.filename, line=line, column=col)
                        if index < 0 or index >= len(target):
                            raise SikharIndexError(f"List index out of range: {index}", filename=self.filename, line=line, column=col)
                        target[index] = val
                        self.push(val)
                    elif isinstance(target, dict):
                        target[index] = val
                        self.push(val)
                    else:
                        raise SikharTypeError(
                            f"Cannot assign by index to type '{type(target).__name__}'",
                            filename=self.filename,
                            line=line,
                            column=col,
                        )

                elif op == OpCode.OP_GET_MEMBER:
                    idx = (code[frame.ip] << 8) | code[frame.ip + 1]
                    frame.ip += 2
                    prop = constants[idx]
                    target = self.pop()
                    if isinstance(target, SikharModule):
                        self.push(target.get_member(prop, line=line, col=col, filename=self.filename))
                    elif isinstance(target, dict):
                        if prop in target:
                            self.push(target[prop])
                        else:
                            raise SikharKeyError(f"Key '{prop}' not found in map", filename=self.filename, line=line, column=col)
                    elif hasattr(target, prop):
                        self.push(getattr(target, prop))
                    else:
                        raise SikharTypeError(
                            f"Cannot access property '{prop}' on type '{type(target).__name__}'",
                            filename=self.filename,
                            line=line,
                            column=col,
                        )

                elif op == OpCode.OP_SET_MEMBER:
                    idx = (code[frame.ip] << 8) | code[frame.ip + 1]
                    frame.ip += 2
                    prop = constants[idx]
                    val = self.pop()
                    target = self.pop()
                    if isinstance(target, SikharModule):
                        target.set_member(prop, val)
                        self.push(val)
                    elif isinstance(target, dict):
                        target[prop] = val
                        self.push(val)
                    elif hasattr(target, prop):
                        setattr(target, prop, val)
                        self.push(val)
                    else:
                        raise SikharTypeError(
                            f"Cannot set property '{prop}' on type '{type(target).__name__}'",
                            filename=self.filename,
                            line=line,
                            column=col,
                        )

                # ==========================================
                # Functions & Calls
                # ==========================================
                elif op == OpCode.OP_MAKE_FUNCTION:
                    idx = (code[frame.ip] << 8) | code[frame.ip + 1]
                    frame.ip += 2
                    func_template = constants[idx]
                    func_obj = BytecodeFunction(
                        name=func_template.name,
                        arity=func_template.arity,
                        param_names=func_template.param_names,
                        chunk=func_template.chunk,
                    )
                    func_obj.globals = frame.globals
                    self.push(func_obj)

                elif op == OpCode.OP_CALL:
                    arg_count = (code[frame.ip] << 8) | code[frame.ip + 1]
                    frame.ip += 2

                    callee = self.peek(arg_count)

                    if isinstance(callee, BytecodeFunction):
                        if arg_count != callee.arity:
                            raise SikharTypeError(
                                f"Function '{callee.name}' expects {callee.arity} arguments, got {arg_count}",
                                filename=self.filename,
                                line=line,
                                column=col,
                            )
                        # The function itself is at stack index: len(stack) - 1 - arg_count
                        # Its arguments start at slot: len(stack) - arg_count
                        base_slot = len(self.stack) - arg_count
                        fn_globals = callee.globals if callee.globals is not None else frame.globals
                        new_frame = CallFrame(callee, base_slot=base_slot, globals_dict=fn_globals)
                        self.frames.append(new_frame)


                    elif isinstance(callee, BuiltinFunction):
                        args = self.stack[len(self.stack) - arg_count :] if arg_count > 0 else []
                        # Pop args and callee
                        del self.stack[len(self.stack) - (arg_count + 1) :]
                        res = callee.call(self, args, line=line, column=col)
                        self.push(res)

                    elif isinstance(callee, SikharCallable):
                        args = self.stack[len(self.stack) - arg_count :] if arg_count > 0 else []
                        del self.stack[len(self.stack) - (arg_count + 1) :]
                        res = callee.call(self, args, line=line, column=col)
                        self.push(res)

                    elif callable(callee):
                        args = self.stack[len(self.stack) - arg_count :] if arg_count > 0 else []
                        del self.stack[len(self.stack) - (arg_count + 1) :]
                        res = callee(*args)
                        self.push(res)

                    else:
                        raise SikharTypeError(
                            f"Value of type '{type(callee).__name__}' is not callable",
                            filename=self.filename,
                            line=line,
                            column=col,
                        )

                elif op == OpCode.OP_RETURN:
                    ret_val = self.pop()
                    finished_frame = self.frames.pop()
                    # Clean up local variables and callee function from stack
                    cleanup_to = finished_frame.base_slot - 1
                    if cleanup_to >= 0:
                        del self.stack[cleanup_to:]

                    if not self.frames:
                        return ret_val

                    self.push(ret_val)

                # ==========================================
                # Modules & I/O
                # ==========================================
                elif op == OpCode.OP_IMPORT:
                    idx = (code[frame.ip] << 8) | code[frame.ip + 1]
                    is_std = bool(code[frame.ip + 2])
                    frame.ip += 3
                    mod_path = constants[idx]
                    mod = self._load_module(mod_path, is_std, line, col)
                    self.push(mod)

                elif op == OpCode.OP_EXPORT:
                    idx = (code[frame.ip] << 8) | code[frame.ip + 1]
                    frame.ip += 2
                    sym_name = constants[idx]
                    if sym_name in frame.globals:
                        self.exports[sym_name] = frame.globals[sym_name]
                    elif sym_name in self.globals:
                        self.exports[sym_name] = self.globals[sym_name]


                elif op == OpCode.OP_PRINT:
                    arg_count = (code[frame.ip] << 8) | code[frame.ip + 1]
                    frame.ip += 2
                    if arg_count == 0:
                        self.output_fn("")
                    else:
                        items = self.stack[-arg_count:]
                        del self.stack[-arg_count:]
                        self.output_fn(" ".join(sikhar_stringify(x) for x in items))

                elif op == OpCode.OP_FORMAT_STRING:
                    count = (code[frame.ip] << 8) | code[frame.ip + 1]
                    frame.ip += 2
                    if count == 0:
                        self.push("")
                    else:
                        items = self.stack[-count:]
                        del self.stack[-count:]
                        self.push("".join(sikhar_stringify(x) for x in items))

                # ==========================================
                # Assertions & Exceptions
                # ==========================================
                elif op == OpCode.OP_ASSERT:
                    has_msg = bool((code[frame.ip] << 8) | code[frame.ip + 1])
                    frame.ip += 2
                    msg = "Assertion failed ('jaach')"
                    if has_msg:
                        msg = sikhar_stringify(self.pop())
                    cond = self.pop()
                    if not is_truthy(cond):
                        raise SikharAssertionError(
                            msg,
                            filename=self.filename,
                            line=line,
                            column=col,
                            source_line=self._get_source_line(line),
                        )

                elif op == OpCode.OP_PUSH_TRY:
                    offset = (code[frame.ip] << 8) | code[frame.ip + 1]
                    frame.ip += 2
                    catch_ip = frame.ip + offset
                    frame.try_stack.append((catch_ip, len(self.stack)))

                elif op == OpCode.OP_POP_TRY:
                    if frame.try_stack:
                        frame.try_stack.pop()

                elif op == OpCode.OP_THROW:
                    val = self.pop()
                    raise SikharUserThrowError(
                        val,
                        filename=self.filename,
                        line=line,
                        column=col,
                        source_line=self._get_source_line(line),
                    )

            except Exception as exc:
                # Check if caught by try-catch handler in call stack
                handled = False
                while self.frames:
                    cur_f = self.frames[-1]
                    if cur_f.try_stack:
                        catch_ip, saved_stack_depth = cur_f.try_stack.pop()
                        # Unwind stack
                        if len(self.stack) > saved_stack_depth:
                            del self.stack[saved_stack_depth:]
                        # Push thrown value or error message
                        thrown_val = exc.thrown_value if isinstance(exc, SikharUserThrowError) else str(exc)
                        self.push(thrown_val)
                        cur_f.ip = catch_ip
                        handled = True
                        break
                    else:
                        self.frames.pop()

                if not handled:
                    raise exc

        return None

    def _load_module(self, module_path: str, is_std: bool, line: int, col: int) -> SikharModule:
        # Check if standard library module
        std_mod = get_std_module(module_path)
        if std_mod is not None:
            return std_mod

        # Resolve local module
        if self.filename and self.filename not in ("<stdin>", "<repl>"):
            base_dir = Path(self.filename).resolve().parent
        else:
            base_dir = Path.cwd()

        target_path = base_dir / module_path
        if not target_path.exists() and not module_path.endswith(".sk"):
            target_path = base_dir / f"{module_path}.sk"

        canonical_path = str(target_path.resolve())
        if canonical_path in self.module_cache:
            return self.module_cache[canonical_path]

        if not target_path.exists():
            raise SikharRuntimeError(
                f"Cannot find module '{module_path}' (resolved to '{canonical_path}')",
                filename=self.filename,
                line=line,
                column=col,
            )

        source = target_path.read_text(encoding="utf-8")

        from ..lexer.lexer import Lexer
        from ..parser.parser import Parser
        from .compiler import Compiler

        tokens = Lexer(source, canonical_path).tokenize()
        ast = Parser(tokens, source, canonical_path).parse()
        module_chunk = Compiler(canonical_path).compile(ast)

        module_vm = VM(source=source, filename=canonical_path)
        mod_name = target_path.stem
        module_obj = SikharModule(mod_name, {})
        self.module_cache[canonical_path] = module_obj

        module_vm.run(module_chunk)

        # Exported symbols
        if module_vm.exports:
            module_obj.exports.update(module_vm.exports)
        else:
            for k, v in module_vm.globals.items():
                if not hasattr(v, "_is_builtin"):
                    module_obj.exports[k] = v

        return module_obj
