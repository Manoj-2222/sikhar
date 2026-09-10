"""
Sikhar Bytecode Serializer & Deserializer
Encodes and decodes compiled Chunks to/from binary .skc files.
"""

import marshal
from pathlib import Path
from typing import Any, List, Optional, Tuple

from .. import __version__
from .chunk import Chunk, BytecodeFunction
from ..errors.error_types import SikharCompileError

MAGIC_HEADER = b"SKC\x01"


def _constant_to_serializable(val: Any) -> Any:
    if isinstance(val, BytecodeFunction):
        return (
            "__sk_fn__",
            val.name,
            val.arity,
            val.param_names,
            val.chunk.code,
            [_constant_to_serializable(c) for c in val.chunk.constants],
            val.chunk.lines,
        )
    return val


def _serializable_to_constant(val: Any, filename: str = "<stdin>") -> Any:
    if isinstance(val, tuple) and len(val) == 7 and val[0] == "__sk_fn__":
        _, name, arity, param_names, code, constants, lines = val
        inner_chunk = Chunk(filename)
        inner_chunk.code = list(code)
        inner_chunk.constants = [_serializable_to_constant(c, filename) for c in constants]
        inner_chunk.lines = list(lines)
        return BytecodeFunction(name=name, arity=arity, param_names=list(param_names), chunk=inner_chunk)
    return val


def serialize_chunk(chunk: Chunk) -> bytes:
    """Serialize a Chunk into binary .skc bytes."""
    constants_data = [_constant_to_serializable(c) for c in chunk.constants]
    payload_obj = {
        "version": __version__,
        "code": chunk.code,
        "constants": constants_data,
        "lines": chunk.lines,
    }
    payload_bytes = marshal.dumps(payload_obj)

    version_bytes = __version__.encode("utf-8")
    header = MAGIC_HEADER + len(version_bytes).to_bytes(2, "big") + version_bytes
    return header + payload_bytes


def deserialize_chunk(data: bytes, filename: str = "<stdin>") -> Chunk:
    """Deserialize binary .skc bytes back into a Chunk."""
    if not data.startswith(MAGIC_HEADER):
        raise SikharCompileError(f"Invalid .skc file: missing magic header", filename=filename)

    offset = len(MAGIC_HEADER)
    version_len = int.from_bytes(data[offset : offset + 2], "big")
    offset += 2
    version_str = data[offset : offset + version_len].decode("utf-8")
    offset += version_len

    payload_data = data[offset:]
    try:
        obj = marshal.loads(payload_data)
    except Exception as e:
        raise SikharCompileError(f"Corrupt .skc bytecode file: {e}", filename=filename)

    chunk = Chunk(filename)
    chunk.code = list(obj["code"])
    chunk.constants = [_serializable_to_constant(c, filename) for c in obj["constants"]]
    chunk.lines = list(obj["lines"])
    return chunk


def compile_file_to_skc(source_path: str, output_path: Optional[str] = None) -> str:
    """Compile a .sk source file into a binary .skc file."""
    src = Path(source_path)
    if not src.exists():
        raise FileNotFoundError(f"Source file '{source_path}' does not exist.")

    if output_path is None:
        out = src.with_suffix(".skc")
    else:
        out = Path(output_path)

    source_text = src.read_text(encoding="utf-8")

    from ..lexer.lexer import Lexer
    from ..parser.parser import Parser
    from .compiler import Compiler

    tokens = Lexer(source_text, str(src)).tokenize()
    ast = Parser(tokens, source_text, str(src)).parse()
    chunk = Compiler(str(src)).compile(ast)

    binary_data = serialize_chunk(chunk)
    out.write_bytes(binary_data)
    return str(out)


def load_skc_file(file_path: str) -> Chunk:
    """Load and deserialize a .skc file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Compiled file '{file_path}' does not exist.")
    return deserialize_chunk(path.read_bytes(), filename=str(path))
