"""
Sikhar Abstract Syntax Tree (AST) Node Definitions
Clean, typed hierarchy for expressions and statements.
"""

from dataclasses import dataclass, field
from typing import Any, List, Optional, Tuple


@dataclass
class ASTNode:
    line: int = 1
    column: int = 1


# ==========================================
# Expressions
# ==========================================

class Expression(ASTNode):
    pass


@dataclass
class Literal(Expression):
    value: Any = None
    literal_type: str = "null"  # "number", "decimal", "text", "boolean", "null"


@dataclass
class Identifier(Expression):
    name: str = ""


@dataclass
class BinaryExpression(Expression):
    left: Expression = field(default_factory=Expression)
    operator: str = ""
    right: Expression = field(default_factory=Expression)


@dataclass
class UnaryExpression(Expression):
    operator: str = ""
    operand: Expression = field(default_factory=Expression)


@dataclass
class FunctionCall(Expression):
    callee: Expression = field(default_factory=Expression)
    arguments: List[Expression] = field(default_factory=list)


@dataclass
class ListLiteral(Expression):
    elements: List[Expression] = field(default_factory=list)


@dataclass
class MapLiteral(Expression):
    entries: List[Tuple[Expression, Expression]] = field(default_factory=list)


@dataclass
class IndexExpression(Expression):
    target: Expression = field(default_factory=Expression)
    index: Expression = field(default_factory=Expression)


# ==========================================
# Statements
# ==========================================

class Statement(ASTNode):
    pass


@dataclass
class Program(ASTNode):
    statements: List[Statement] = field(default_factory=list)


@dataclass
class Block(Statement):
    statements: List[Statement] = field(default_factory=list)


@dataclass
class VariableDeclaration(Statement):
    name: str = ""
    type_annotation: Optional[str] = None
    initializer: Optional[Expression] = None


@dataclass
class ConstantDeclaration(Statement):
    name: str = ""
    type_annotation: Optional[str] = None
    initializer: Expression = field(default_factory=Expression)


@dataclass
class Assignment(Statement):
    target: Expression = field(default_factory=Expression)
    value: Expression = field(default_factory=Expression)


@dataclass
class DekhaStatement(Statement):
    expression: Expression = field(default_factory=Expression)


@dataclass
class IfStatement(Statement):
    condition: Expression = field(default_factory=Expression)
    then_branch: Block = field(default_factory=Block)
    elif_branches: List[Tuple[Expression, Block]] = field(default_factory=list)
    else_branch: Optional[Block] = None


@dataclass
class WhileStatement(Statement):
    condition: Expression = field(default_factory=Expression)
    body: Block = field(default_factory=Block)


@dataclass
class ForStatement(Statement):
    var_name: str = ""
    iterable: Expression = field(default_factory=Expression)
    body: Block = field(default_factory=Block)


@dataclass
class BreakStatement(Statement):
    pass


@dataclass
class ContinueStatement(Statement):
    pass


@dataclass
class FunctionDeclaration(Statement):
    name: str = ""
    parameters: List[str] = field(default_factory=list)
    body: Block = field(default_factory=Block)


@dataclass
class ReturnStatement(Statement):
    value: Optional[Expression] = None


@dataclass
class TryStatement(Statement):
    try_block: Block = field(default_factory=Block)
    catch_var: Optional[str] = None
    catch_block: Block = field(default_factory=Block)


@dataclass
class ThrowStatement(Statement):
    expression: Expression = field(default_factory=Expression)


@dataclass
class ExpressionStatement(Statement):
    expression: Expression = field(default_factory=Expression)
