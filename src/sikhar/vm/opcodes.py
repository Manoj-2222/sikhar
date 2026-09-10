"""
Sikhar Virtual Machine OpCodes
Enumeration of all instruction bytecodes for the stack-based VM.
"""

from enum import IntEnum


class OpCode(IntEnum):
    # Stack manipulation & Literals
    OP_CONSTANT = 1
    OP_NIL = 2
    OP_TRUE = 3
    OP_FALSE = 4
    OP_POP = 5
    OP_DUP = 6

    # Unary operators
    OP_NEGATE = 10
    OP_NOT = 11

    # Binary arithmetic & string concatenation
    OP_ADD = 15
    OP_SUBTRACT = 16
    OP_MULTIPLY = 17
    OP_DIVIDE = 18
    OP_MODULO = 19

    # Comparisons
    OP_EQUAL = 25
    OP_NOT_EQUAL = 26
    OP_GREATER = 27
    OP_GREATER_EQUAL = 28
    OP_LESS = 29
    OP_LESS_EQUAL = 30

    # Variable & Constant Management
    OP_DEFINE_GLOBAL = 35
    OP_DEFINE_CONST = 36
    OP_GET_GLOBAL = 37
    OP_SET_GLOBAL = 38
    OP_GET_LOCAL = 39
    OP_SET_LOCAL = 40

    # Control Flow
    OP_JUMP = 45
    OP_JUMP_IF_FALSE = 46
    OP_LOOP = 47
    OP_GET_ITER = 48
    OP_FOR_ITER = 49

    # Data Structures & Member Access
    OP_BUILD_LIST = 55
    OP_BUILD_MAP = 56
    OP_INDEX_GET = 57
    OP_INDEX_SET = 58
    OP_GET_MEMBER = 59
    OP_SET_MEMBER = 60

    # Functions & Invocation
    OP_MAKE_FUNCTION = 65
    OP_CALL = 66
    OP_RETURN = 67

    # Modules & Builtins
    OP_IMPORT = 75
    OP_EXPORT = 76
    OP_PRINT = 77
    OP_FORMAT_STRING = 78

    # Assertions & Exceptions
    OP_ASSERT = 85
    OP_PUSH_TRY = 86
    OP_POP_TRY = 87
    OP_THROW = 88


OPCODE_NAMES = {op.value: op.name for op in OpCode}
