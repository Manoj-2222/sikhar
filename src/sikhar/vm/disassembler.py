"""
Sikhar Bytecode Disassembler
Formats bytecode instructions into readable assembly listings.
"""

from typing import List, Tuple
from .chunk import Chunk, BytecodeFunction
from .opcodes import OpCode, OPCODE_NAMES


class Disassembler:
    @staticmethod
    def disassemble(chunk: Chunk, name: str = "main") -> str:
        lines: List[str] = []
        lines.append(f"== Bytecode Disassembly: {name} ({chunk.count} bytes) ==")

        nested_functions: List[BytecodeFunction] = []
        offset = 0
        last_line = -1

        while offset < chunk.count:
            line_str, new_offset, func_ref = Disassembler.disassemble_instruction(chunk, offset, last_line)
            lines.append(line_str)
            cur_line, _ = chunk.get_line_col(offset)
            last_line = cur_line
            offset = new_offset
            if func_ref is not None:
                nested_functions.append(func_ref)

        lines.append("")

        for fn in nested_functions:
            lines.append(Disassembler.disassemble(fn.chunk, f"kaam {fn.name}"))

        return "\n".join(lines)

    @staticmethod
    def disassemble_instruction(
        chunk: Chunk, offset: int, last_line: int = -1
    ) -> Tuple[str, int, BytecodeFunction | None]:
        if offset >= chunk.count:
            return f"{offset:04d}   <EOF>", offset + 1, None

        line, col = chunk.get_line_col(offset)
        line_prefix = f"{line:4d} " if line != last_line else "   | "

        byte_val = chunk.code[offset]
        op_name = OPCODE_NAMES.get(byte_val, f"UNKNOWN({byte_val})")

        func_ref: BytecodeFunction | None = None

        # 0-operand instructions (1 byte total)
        if byte_val in (
            OpCode.OP_NIL,
            OpCode.OP_TRUE,
            OpCode.OP_FALSE,
            OpCode.OP_POP,
            OpCode.OP_DUP,
            OpCode.OP_NEGATE,
            OpCode.OP_NOT,
            OpCode.OP_ADD,
            OpCode.OP_SUBTRACT,
            OpCode.OP_MULTIPLY,
            OpCode.OP_DIVIDE,
            OpCode.OP_MODULO,
            OpCode.OP_EQUAL,
            OpCode.OP_NOT_EQUAL,
            OpCode.OP_GREATER,
            OpCode.OP_GREATER_EQUAL,
            OpCode.OP_LESS,
            OpCode.OP_LESS_EQUAL,
            OpCode.OP_INDEX_GET,
            OpCode.OP_INDEX_SET,
            OpCode.OP_RETURN,
            OpCode.OP_POP_TRY,
            OpCode.OP_THROW,
            OpCode.OP_GET_ITER,
        ):
            return f"{offset:04d} {line_prefix} {op_name:<20}", offset + 1, None

        # 2-byte constant index operands
        if byte_val in (
            OpCode.OP_CONSTANT,
            OpCode.OP_DEFINE_GLOBAL,
            OpCode.OP_DEFINE_CONST,
            OpCode.OP_GET_GLOBAL,
            OpCode.OP_SET_GLOBAL,
            OpCode.OP_GET_MEMBER,
            OpCode.OP_SET_MEMBER,
            OpCode.OP_EXPORT,
        ):
            const_idx = chunk.read_short(offset + 1)
            val = chunk.constants[const_idx] if const_idx < len(chunk.constants) else "<out-of-bounds>"
            val_repr = repr(val)
            if len(val_repr) > 30:
                val_repr = val_repr[:27] + "..."
            return (
                f"{offset:04d} {line_prefix} {op_name:<20} {const_idx:4d} ({val_repr})",
                offset + 3,
                None,
            )

        # Local slot operands
        if byte_val in (OpCode.OP_GET_LOCAL, OpCode.OP_SET_LOCAL):
            slot = chunk.read_short(offset + 1)
            return f"{offset:04d} {line_prefix} {op_name:<20} slot={slot}", offset + 3, None

        # Jumps forward
        if byte_val in (OpCode.OP_JUMP, OpCode.OP_JUMP_IF_FALSE, OpCode.OP_FOR_ITER, OpCode.OP_PUSH_TRY):
            jump = chunk.read_short(offset + 1)
            target = offset + 3 + jump
            return f"{offset:04d} {line_prefix} {op_name:<20} +{jump} -> {target:04d}", offset + 3, None

        # Jumps backward (Loop)
        if byte_val == OpCode.OP_LOOP:
            jump = chunk.read_short(offset + 1)
            target = offset + 3 - jump
            return f"{offset:04d} {line_prefix} {op_name:<20} -{jump} -> {target:04d}", offset + 3, None

        # Counts
        if byte_val in (
            OpCode.OP_BUILD_LIST,
            OpCode.OP_BUILD_MAP,
            OpCode.OP_CALL,
            OpCode.OP_PRINT,
            OpCode.OP_FORMAT_STRING,
            OpCode.OP_ASSERT,
        ):
            count = chunk.read_short(offset + 1)
            return f"{offset:04d} {line_prefix} {op_name:<20} count={count}", offset + 3, None

        # OP_MAKE_FUNCTION
        if byte_val == OpCode.OP_MAKE_FUNCTION:
            const_idx = chunk.read_short(offset + 1)
            func_val = chunk.constants[const_idx] if const_idx < len(chunk.constants) else None
            if isinstance(func_val, BytecodeFunction):
                func_ref = func_val
            return (
                f"{offset:04d} {line_prefix} {op_name:<20} {const_idx:4d} ({repr(func_val)})",
                offset + 3,
                func_ref,
            )

        # OP_IMPORT
        if byte_val == OpCode.OP_IMPORT:
            const_idx = chunk.read_short(offset + 1)
            is_std = chunk.code[offset + 3] if offset + 3 < chunk.count else 0
            val = chunk.constants[const_idx] if const_idx < len(chunk.constants) else ""
            return (
                f"{offset:04d} {line_prefix} {op_name:<20} path={repr(val)} is_std={bool(is_std)}",
                offset + 4,
                None,
            )

        return f"{offset:04d} {line_prefix} {op_name}", offset + 1, None
