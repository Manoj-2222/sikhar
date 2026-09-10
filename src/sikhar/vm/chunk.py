"""
Sikhar Bytecode Chunk & Bytecode Function
Containers for bytecode instructions, constant pools, and debug metadata.
"""

from typing import Any, List, Tuple, Optional


class Chunk:
    def __init__(self, filename: str = "<stdin>"):
        self.filename: str = filename
        self.code: List[int] = []
        self.constants: List[Any] = []
        self.lines: List[Tuple[int, int]] = []  # (line, column) for each instruction byte

    @property
    def count(self) -> int:
        return len(self.code)

    def write_byte(self, byte_val: int, line: int = 1, column: int = 1) -> int:
        idx = len(self.code)
        self.code.append(byte_val & 0xFF)
        self.lines.append((line, column))
        return idx

    def write_short(self, short_val: int, line: int = 1, column: int = 1) -> int:
        idx = len(self.code)
        self.write_byte((short_val >> 8) & 0xFF, line, column)
        self.write_byte(short_val & 0xFF, line, column)
        return idx

    def patch_short(self, offset: int, short_val: int) -> None:
        self.code[offset] = (short_val >> 8) & 0xFF
        self.code[offset + 1] = short_val & 0xFF

    def read_short(self, offset: int) -> int:
        return (self.code[offset] << 8) | self.code[offset + 1]

    def add_constant(self, val: Any) -> int:
        # Deduplicate primitive constants
        if isinstance(val, (int, float, str, bool)) or val is None:
            for idx, existing in enumerate(self.constants):
                if type(existing) is type(val) and existing == val:
                    return idx

        self.constants.append(val)
        return len(self.constants) - 1

    def get_line_col(self, offset: int) -> Tuple[int, int]:
        if 0 <= offset < len(self.lines):
            return self.lines[offset]
        return (1, 1)


class BytecodeFunction:
    """Compiled function stored as a constant in a chunk."""

    def __init__(
        self,
        name: str,
        arity: int,
        param_names: Optional[List[str]] = None,
        chunk: Optional[Chunk] = None,
    ):
        self.name: str = name
        self.arity: int = arity
        self.param_names: List[str] = param_names or []
        self.chunk: Chunk = chunk if chunk is not None else Chunk()
        self.globals: Optional[dict[str, Any]] = None

    def __repr__(self) -> str:
        return f"<kaam {self.name} (bytecode, arity={self.arity})>"

