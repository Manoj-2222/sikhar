"""
Sikhar Token Representation
"""

from dataclasses import dataclass
from typing import Any
from .token_type import TokenType


@dataclass(frozen=True)
class Token:
    type: TokenType
    value: Any
    line: int
    column: int
    length: int = 1
    filename: str = "<stdin>"

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, L{self.line}:C{self.column})"
