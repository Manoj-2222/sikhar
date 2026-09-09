"""
Sikhar Error Types
Clean, native Sikhar exception hierarchy.
"""

from typing import Optional, List


class SikharError(Exception):
    """Base class for all Sikhar errors."""
    def __init__(
        self,
        message: str,
        filename: str = "<stdin>",
        line: int = 1,
        column: int = 1,
        source_line: Optional[str] = None,
        call_stack: Optional[List[str]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.filename = filename
        self.line = line
        self.column = column
        self.source_line = source_line
        self.call_stack = call_stack or []

    @property
    def error_type_name(self) -> str:
        return self.__class__.__name__.replace("Sikhar", "")


class SikharSyntaxError(SikharError):
    """Raised during lexical analysis or parsing."""
    @property
    def error_type_name(self) -> str:
        return "SyntaxError"


class SikharRuntimeError(SikharError):
    """Generic runtime error during execution."""
    @property
    def error_type_name(self) -> str:
        return "RuntimeError"


class SikharNameError(SikharRuntimeError):
    """Raised when an identifier is referenced before definition."""
    @property
    def error_type_name(self) -> str:
        return "UndefinedVariable"


class SikharTypeError(SikharRuntimeError):
    """Raised when an operation is performed on incompatible types."""
    @property
    def error_type_name(self) -> str:
        return "TypeError"


class SikharConstantMutationError(SikharRuntimeError):
    """Raised when attempting to modify a constant declared with 'sthayi'."""
    @property
    def error_type_name(self) -> str:
        return "ConstantMutation"


class SikharIndexError(SikharRuntimeError):
    """Raised when a list index is out of bounds."""
    pass


class SikharKeyError(SikharRuntimeError):
    """Raised when a map key does not exist."""
    pass


class SikharDivisionByZeroError(SikharRuntimeError):
    """Raised when dividing or modulo by zero."""
    pass


class SikharUserThrowError(SikharRuntimeError):
    """Raised explicitly by the user using 'fal'."""
    def __init__(
        self,
        value: str,
        filename: str = "<stdin>",
        line: int = 1,
        column: int = 1,
        source_line: Optional[str] = None,
        call_stack: Optional[List[str]] = None,
    ):
        super().__init__(
            message=str(value),
            filename=filename,
            line=line,
            column=column,
            source_line=source_line,
            call_stack=call_stack,
        )
        self.thrown_value = value
