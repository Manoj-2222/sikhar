"""
Sikhar Error Reporter
Formats errors in a clean, developer-friendly manner with exact source location.
Never exposes raw Python stack traces.
"""

from typing import Optional
from .error_types import SikharError


def format_error(error: SikharError, source_code: Optional[str] = None) -> str:
    """Format a SikharError into a beautiful terminal message."""
    output = []
    output.append("Sikhar Error")
    output.append("")
    output.append(f"Type: {error.error_type_name}")
    output.append(f"Message: {error.message}")
    output.append("")
    output.append(f"File: {error.filename}")
    output.append(f"Line: {error.line}")
    output.append(f"Column: {error.column}")

    # Extract source line for visual pointer if available
    line_content = error.source_line
    if line_content is None and source_code:
        lines = source_code.splitlines()
        if 1 <= error.line <= len(lines):
            line_content = lines[error.line - 1]

    if line_content is not None:
        output.append("")
        line_num_str = f"{error.line:4d} | "
        output.append(f"{line_num_str}{line_content}")
        # Pointer alignment: offset column by margin
        pointer_indent = " " * (len(line_num_str) + max(0, error.column - 1))
        output.append(f"{pointer_indent}^")

    if error.call_stack:
        output.append("")
        output.append("Call Stack:")
        for frame in reversed(error.call_stack):
            output.append(f"  at {frame}")

    return "\n".join(output)


def print_error(error: SikharError, source_code: Optional[str] = None) -> None:
    """Print formatted error to stderr or stdout."""
    import sys
    print(format_error(error, source_code), file=sys.stderr)
