"""
Sikhar Command Line Interface (CLI)
Provides: run, check, test, format, init, repl, version, help
"""

import sys
import os
import argparse
from pathlib import Path
from typing import List, Optional

from .. import __version__
from ..lexer.lexer import Lexer
from ..parser.parser import Parser
from ..interpreter.interpreter import Interpreter
from ..formatter.formatter import Formatter
from ..errors.error_types import SikharError
from ..errors.reporter import print_error, format_error

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def run_file(file_path: str) -> int:
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File '{file_path}' does not exist.", file=sys.stderr)
        return 1

    try:
        source = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}", file=sys.stderr)
        return 1

    try:
        tokens = Lexer(source, str(path)).tokenize()
        ast = Parser(tokens, source, str(path)).parse()
        interpreter = Interpreter(source, str(path))
        interpreter.interpret(ast)
        return 0
    except SikharError as err:
        print_error(err, source)
        return 1
    except Exception as exc:
        print(f"Unexpected internal error: {exc}", file=sys.stderr)
        return 1


def check_file(file_path: str) -> int:
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File '{file_path}' does not exist.", file=sys.stderr)
        return 1

    try:
        source = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}", file=sys.stderr)
        return 1

    try:
        tokens = Lexer(source, str(path)).tokenize()
        Parser(tokens, source, str(path)).parse()
        print(f"Syntax OK: {file_path}")
        return 0
    except SikharError as err:
        print_error(err, source)
        return 1


def format_files(paths: List[str]) -> int:
    formatter = Formatter()
    if not paths:
        # Default to all .sk files in current directory tree
        paths = [str(p) for p in Path(".").glob("**/*.sk")]

    if not paths:
        print("No .sk files found to format.")
        return 0

    success = True
    for p_str in paths:
        p = Path(p_str)
        if not p.exists():
            print(f"Warning: File '{p_str}' not found.", file=sys.stderr)
            success = False
            continue
        try:
            source = p.read_text(encoding="utf-8")
            formatted = formatter.format_code(source, str(p))
            p.write_text(formatted, encoding="utf-8")
            print(f"Formatted: {p_str}")
        except SikharError as err:
            print_error(err, source)
            success = False
        except Exception as e:
            print(f"Error formatting '{p_str}': {e}", file=sys.stderr)
            success = False

    return 0 if success else 1


def init_project(project_name: str) -> int:
    target_dir = Path(project_name)
    if target_dir.exists():
        print(f"Error: Directory '{project_name}' already exists.", file=sys.stderr)
        return 1

    try:
        src_dir = target_dir / "src"
        tests_dir = target_dir / "tests"
        src_dir.mkdir(parents=True, exist_ok=True)
        tests_dir.mkdir(parents=True, exist_ok=True)

        # src/main.sk
        main_sk = (
            '# Sikhar Entry Point\n'
            'dekha "Namaste, Sikhar!"\n'
            '\n'
            'kaam abhivadan(naam) {\n'
            '    farka "Namaste, " + naam\n'
            '}\n'
            '\n'
            'dekha abhivadan("Sansar")\n'
        )
        (src_dir / "main.sk").write_text(main_sk, encoding="utf-8")

        # sikhar.toml
        sikhar_toml = (
            f'name = "{project_name}"\n'
            'version = "0.1.0"\n'
            'description = "A new Sikhar project"\n'
            'main = "src/main.sk"\n'
        )
        (target_dir / "sikhar.toml").write_text(sikhar_toml, encoding="utf-8")

        # README.md
        readme_md = (
            f'# {project_name}\n\n'
            'Built with [Sikhar](https://github.com/sikhar-lang/sikhar).\n\n'
            '## Running\n\n'
            '```bash\n'
            'sk run src/main.sk\n'
            '```\n'
        )
        (target_dir / "README.md").write_text(readme_md, encoding="utf-8")

        print(f"Initialized Sikhar project in '{project_name}':")
        print(f"  {project_name}/")
        print(f"  |-- src/")
        print(f"  |   \\-- main.sk")
        print(f"  |-- tests/")
        print(f"  |-- sikhar.toml")
        print(f"  \\-- README.md")
        return 0
    except Exception as e:
        print(f"Failed to initialize project: {e}", file=sys.stderr)
        return 1


def run_tests() -> int:
    import unittest
    loader = unittest.TestLoader()
    start_dir = "tests"
    if not Path(start_dir).exists():
        print("No 'tests' directory found.")
        return 1

    print("=== Running Sikhar Python Test Suite ===")
    suite = loader.discover(start_dir, pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    py_result = runner.run(suite)

    # Discover and run .sk test files
    sk_tests = list(Path(start_dir).glob("**/*.sk"))
    sk_success = True
    if sk_tests:
        print("\n=== Running Native Sikhar (.sk) Test Suite ===")
        for sk_file in sk_tests:
            print(f"Testing {sk_file} ... ", end="")
            code = run_file(str(sk_file))
            if code == 0:
                print("PASSED")
            else:
                print("FAILED")
                sk_success = False

    return 0 if py_result.wasSuccessful() and sk_success else 1


def repl() -> int:
    print(f"Sikhar Programming Language v{__version__}")
    print("Type 'exit' or 'samapta' to quit. Press Ctrl+C to cancel line.")
    print("")

    interpreter = Interpreter(filename="<repl>")
    buffer = []

    while True:
        try:
            prompt = "sikhar> " if not buffer else "  ...   "
            line = input(prompt)
            if not buffer and line.strip() in ("exit", "samapta", "quit"):
                print("Dhanyabad!")
                break

            buffer.append(line)
            combined = "\n".join(buffer)

            # Check if braces or brackets are unclosed
            open_braces = combined.count("{") - combined.count("}")
            if open_braces > 0:
                continue

            # Process combined input
            try:
                tokens = Lexer(combined, "<repl>").tokenize()
                ast = Parser(tokens, combined, "<repl>").parse()
                res = interpreter.interpret(ast)
                if res is not None:
                    print(res)
            except SikharError as err:
                print_error(err, combined)
            finally:
                buffer = []

        except (KeyboardInterrupt, EOFError):
            print("\nDhanyabad!")
            break
        except Exception as e:
            print(f"REPL Error: {e}", file=sys.stderr)
            buffer = []

    return 0


def main(args: Optional[List[str]] = None) -> int:
    if args is None:
        args = sys.argv[1:]

    if not args:
        return repl()

    command = args[0]

    if command in ("-v", "--version", "version"):
        print(f"Sikhar v{__version__}")
        return 0

    if command in ("-h", "--help", "help"):
        print_help()
        return 0

    if command == "run":
        if len(args) < 2:
            print("Error: Missing file argument for 'run'. Usage: sk run <file.sk>", file=sys.stderr)
            return 1
        return run_file(args[1])

    if command == "check":
        if len(args) < 2:
            print("Error: Missing file argument for 'check'. Usage: sk check <file.sk>", file=sys.stderr)
            return 1
        return check_file(args[1])

    if command == "format":
        files = args[1:]
        return format_files(files)

    if command == "init":
        if len(args) < 2:
            print("Error: Missing project name. Usage: sk init <project-name>", file=sys.stderr)
            return 1
        return init_project(args[1])

    if command == "test":
        return run_tests()

    if command == "repl":
        return repl()

    # If argument ends with .sk, treat as run
    if command.endswith(".sk"):
        return run_file(command)

    print(f"Unknown command: '{command}'")
    print_help()
    return 1


def print_help() -> None:
    print(f"""Sikhar Programming Language v{__version__}
Usage:
  sk [command] [options]
  sk <file.sk>

Commands:
  run <file.sk>       Execute a Sikhar source file
  check <file.sk>     Check syntax and parse without running
  format [file.sk]    Format source files deterministically
  init <project>      Create a new Sikhar project scaffold
  test                Run automated test suite
  repl                Start interactive Sikhar session
  version             Display current version
  help                Show this help message
""")


if __name__ == "__main__":
    sys.exit(main())
