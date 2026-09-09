"""
Sikhar Environment (Lexical Scopes)
Manages variable bindings, constant enforcement, and lexical scoping.
"""

from typing import Any, Dict, Optional, Set
from ..errors.error_types import SikharNameError, SikharConstantMutationError


class Environment:
    def __init__(self, parent: Optional["Environment"] = None):
        self.parent: Optional["Environment"] = parent
        self.values: Dict[str, Any] = {}
        self.constants: Set[str] = set()

    def define(self, name: str, value: Any, is_constant: bool = False) -> None:
        """Define a new variable or constant in the current scope."""
        self.values[name] = value
        if is_constant:
            self.constants.add(name)

    def is_constant_in_hierarchy(self, name: str) -> bool:
        """Check if name is defined as a constant in this or any enclosing scope."""
        if name in self.constants:
            return True
        if self.parent is not None:
            return self.parent.is_constant_in_hierarchy(name)
        return False

    def assign(
        self,
        name: str,
        value: Any,
        filename: str = "<stdin>",
        line: int = 1,
        column: int = 1,
        source_line: Optional[str] = None,
    ) -> None:
        """Assign to an existing variable in the closest enclosing scope."""
        if name in self.values:
            if name in self.constants:
                raise SikharConstantMutationError(
                    f"Cannot modify constant '{name}' declared with 'sthayi'",
                    filename=filename,
                    line=line,
                    column=column,
                    source_line=source_line,
                )
            self.values[name] = value
            return

        if self.parent is not None:
            self.parent.assign(name, value, filename=filename, line=line, column=column, source_line=source_line)
            return

        raise SikharNameError(
            f"Variable '{name}' is not defined",
            filename=filename,
            line=line,
            column=column,
            source_line=source_line,
        )

    def get(
        self,
        name: str,
        filename: str = "<stdin>",
        line: int = 1,
        column: int = 1,
        source_line: Optional[str] = None,
    ) -> Any:
        """Retrieve value of a variable from the closest enclosing scope."""
        if name in self.values:
            return self.values[name]

        if self.parent is not None:
            return self.parent.get(name, filename=filename, line=line, column=column, source_line=source_line)

        raise SikharNameError(
            f"Variable '{name}' is not defined",
            filename=filename,
            line=line,
            column=column,
            source_line=source_line,
        )

    def contains(self, name: str) -> bool:
        """Check if name exists in current or any parent scope."""
        if name in self.values:
            return True
        if self.parent is not None:
            return self.parent.contains(name)
        return False
