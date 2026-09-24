"""
Sikhar Token Representation
"""

from dataclasses import dataclass
from typing import Any, Optional
from .token_type import TokenType


@dataclass(frozen=True)
class Token:
    type: TokenType
    value: Any
    line: int
    column: int
    length: int = 1
    filename: str = "<stdin>"
    quote_char: Optional[str] = None

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, L{self.line}:C{self.column})"
