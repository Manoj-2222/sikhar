"""
Sikhar Module Loader
Loads local .sk files and standard library packages with caching and scope isolation.
"""

from pathlib import Path
from typing import Any, Dict, Optional

from ..interpreter.values import SikharModule
from ..std import get_std_module
from ..errors.error_types import SikharRuntimeError


class ModuleLoader:
    def __init__(self):
        self.cache: Dict[str, SikharModule] = {}

    def load_module(
        self,
        module_path: str,
        current_file: str = "<stdin>",
        line: int = 1,
        column: int = 1,
    ) -> SikharModule:
        # Check if standard library module
        std_mod = get_std_module(module_path)
        if std_mod is not None:
            return std_mod

        # Resolve local file path
        if current_file and current_file not in ("<stdin>", "<repl>"):
            base_dir = Path(current_file).resolve().parent
        else:
            base_dir = Path.cwd()

        target_path = base_dir / module_path
        # If no extension specified, try appending .sk
        if not target_path.exists() and not module_path.endswith(".sk"):
            target_path = base_dir / f"{module_path}.sk"

        canonical_path = str(target_path.resolve())

        if canonical_path in self.cache:
            return self.cache[canonical_path]

        if not target_path.exists():
            raise SikharRuntimeError(
                f"Cannot find module '{module_path}' (resolved to '{canonical_path}')",
                filename=current_file,
                line=line,
                column=column,
            )

        try:
            source = target_path.read_text(encoding="utf-8")
        except Exception as e:
            raise SikharRuntimeError(
                f"Error reading module file '{canonical_path}': {e}",
                filename=current_file,
                line=line,
                column=column,
            )

        from ..lexer.lexer import Lexer
        from ..parser.parser import Parser
        from ..interpreter.interpreter import Interpreter

        tokens = Lexer(source, canonical_path).tokenize()
        ast = Parser(tokens, source, canonical_path).parse()

        # Create isolated interpreter for module
        module_interp = Interpreter(source=source, filename=canonical_path)
        # Register module in cache before execution to prevent infinite recursion on circular imports
        mod_name = target_path.stem
        module_obj = SikharModule(mod_name, {})
        self.cache[canonical_path] = module_obj

        # Track exported symbols
        exported_symbols = set()
        from ..parser.ast_nodes import ExportStatement, VariableDeclaration, ConstantDeclaration, FunctionDeclaration

        for stmt in ast.statements:
            if isinstance(stmt, ExportStatement):
                if stmt.symbol_name:
                    exported_symbols.add(stmt.symbol_name)
                elif stmt.declaration:
                    if isinstance(stmt.declaration, (VariableDeclaration, ConstantDeclaration, FunctionDeclaration)):
                        exported_symbols.add(stmt.declaration.name)

        module_interp.interpret(ast)

        # Populate module exports
        if exported_symbols:
            for sym in exported_symbols:
                if sym in module_interp.globals.values:
                    module_obj.exports[sym] = module_interp.globals.values[sym]
        else:
            # If no explicit pathaau was used, export all non-builtin global symbols
            for k, v in module_interp.globals.values.items():
                if not hasattr(v, "_is_builtin"):
                    module_obj.exports[k] = v

        return module_obj


# Global loader instance
MODULE_LOADER = ModuleLoader()
