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
from ..vm import Compiler, VM, Disassembler, compile_file_to_skc, load_skc_file

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


def run_file(file_path: str, use_vm: bool = False) -> int:
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File '{file_path}' does not exist.", file=sys.stderr)
        return 1

    if path.suffix.lower() == ".skc":
        try:
            chunk = load_skc_file(str(path))
            vm = VM(filename=str(path))
            vm.run(chunk)
            return 0
        except SikharError as err:
            print_error(err, "")
            return 1
        except Exception as exc:
            print(f"VM execution error: {exc}", file=sys.stderr)
            return 1

    try:
        source = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}", file=sys.stderr)
        return 1

    try:
        tokens = Lexer(source, str(path)).tokenize()
        ast = Parser(tokens, source, str(path)).parse()

        if use_vm:
            chunk = Compiler(str(path)).compile(ast)
            vm = VM(source=source, filename=str(path))
            vm.run(chunk)
        else:
            interpreter = Interpreter(source, str(path))
            interpreter.interpret(ast)
        return 0
    except SikharError as err:
        print_error(err, source)
        return 1
    except Exception as exc:
        print(f"Unexpected internal error: {exc}", file=sys.stderr)
        return 1


def compile_file(file_path: str, output_path: Optional[str] = None) -> int:
    path = Path(file_path)
    if not path.exists():
        print(f"Error: Source file '{file_path}' does not exist.", file=sys.stderr)
        return 1

    try:
        out = compile_file_to_skc(file_path, output_path)
        print(f"Compiled: {file_path} -> {out}")
        return 0
    except SikharError as err:
        source = path.read_text(encoding="utf-8") if path.exists() else ""
        print_error(err, source)
        return 1
    except Exception as e:
        print(f"Compilation error: {e}", file=sys.stderr)
        return 1


def disassemble_file(file_path: str) -> int:
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File '{file_path}' does not exist.", file=sys.stderr)
        return 1

    try:
        if path.suffix.lower() == ".skc":
            chunk = load_skc_file(str(path))
        else:
            source = path.read_text(encoding="utf-8")
            tokens = Lexer(source, str(path)).tokenize()
            ast = Parser(tokens, source, str(path)).parse()
            chunk = Compiler(str(path)).compile(ast)

        output = Disassembler.disassemble(chunk, name=str(path))
        print(output)
        return 0
    except SikharError as err:
        source = path.read_text(encoding="utf-8") if path.exists() else ""
        print_error(err, source)
        return 1
    except Exception as e:
        print(f"Disassembly error: {e}", file=sys.stderr)
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


def serve_app(args: List[str]) -> int:
    port = 8000
    host = "127.0.0.1"
    target = None
    use_vm = False

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--vm":
            use_vm = True
            i += 1
        elif arg in ("-p", "--port") and i + 1 < len(args):
            try:
                port = int(args[i + 1])
            except ValueError:
                print(f"Error: Invalid port '{args[i + 1]}'", file=sys.stderr)
                return 1
            i += 2
        elif arg in ("-h", "--host") and i + 1 < len(args):
            host = args[i + 1]
            i += 2
        elif target is None:
            target = arg
            i += 1
        else:
            i += 1

    if target is None:
        if Path("src/main.sk").exists():
            target = "src/main.sk"
        elif Path("main.sk").exists():
            target = "main.sk"
        else:
            target = "."

    target_path = Path(target)
    if not target_path.exists():
        print(f"Error: Target '{target}' does not exist.", file=sys.stderr)
        return 1

    import os
    os.environ["SIKHAR_PORT"] = str(port)
    os.environ["SIKHAR_HOST"] = str(host)

    if target_path.is_file() and target_path.suffix.lower() in (".sk", ".skc"):
        print(f"🏔️  Sikhar v{__version__} serving '{target}' on http://{host}:{port} ({'VM' if use_vm else 'Interpreter'})")
        return run_file(str(target_path), use_vm=use_vm)
    else:
        from ..std.web import WebApp
        interp = Interpreter(filename="<serve>")
        app = WebApp(interp)
        app.static("/", str(target_path))
        print(f"🏔️  Sikhar v{__version__} serving directory '{target_path.resolve()}' on http://{host}:{port}")
        print("Press Ctrl+C to stop.")
        try:
            app.listen(port, host)
            return 0
        except KeyboardInterrupt:
            print("\nServer stopped. Dhanyabad!")
            return 0


def build_bundle(args: List[str]) -> int:
    if not args:
        print("Error: Missing file argument for 'build'. Usage: sk build <file.sk|file.skc> [-o <out.pyz>] [--ast] [--no-wrapper]", file=sys.stderr)
        return 1

    target_file = None
    output_path = None
    use_vm = True
    create_wrapper = True

    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("-o", "--output") and i + 1 < len(args):
            output_path = args[i + 1]
            i += 2
        elif arg == "--ast":
            use_vm = False
            i += 1
        elif arg == "--vm":
            use_vm = True
            i += 1
        elif arg == "--no-wrapper":
            create_wrapper = False
            i += 1
        elif target_file is None:
            target_file = arg
            i += 1
        else:
            i += 1

    if not target_file:
        print("Error: Missing file argument for 'build'. Usage: sk build <file.sk|file.skc> [-o <out.pyz>]", file=sys.stderr)
        return 1

    if not Path(target_file).exists():
        print(f"Error: Target file '{target_file}' does not exist.", file=sys.stderr)
        return 1

    try:
        from ..builder.bundle import build_standalone
        pyz_file, bat_file = build_standalone(
            entry_file=target_file,
            output_path=output_path,
            use_vm=use_vm,
            create_wrapper=create_wrapper,
        )
        print(f"📦 Successfully built standalone executable:")
        print(f"  - Bundle:  {pyz_file}")
        if bat_file and bat_file.exists():
            print(f"  - Launcher: {bat_file}")
        print(f"  Engine:   {'Bytecode VM' if use_vm else 'AST Interpreter'}")
        return 0
    except Exception as e:
        print(f"Build failed: {e}", file=sys.stderr)
        return 1


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

    if command == "build":
        return build_bundle(args[1:])

    if command == "serve":
        return serve_app(args[1:])

    if command == "bench":
        if len(args) < 2:
            print("Error: Missing file argument for 'bench'. Usage: sk bench <file.sk> [--iterations <N>]", file=sys.stderr)
            return 1
        iterations = 5
        file_arg = args[1]
        if len(args) >= 4 and args[2] in ("-i", "--iterations"):
            try:
                iterations = int(args[3])
            except ValueError:
                pass
        from ..bench.runner import run_benchmark
        return run_benchmark(file_arg, iterations=iterations)

    if command == "lsp":
        from ..lsp.server import start_lsp_server
        return start_lsp_server()

    if command == "add":
        if len(args) < 2:
            print("Error: Missing package name. Usage: sk add <package> [--version <ver>]", file=sys.stderr)
            return 1
        pkg_name = args[1]
        ver = "*"
        if len(args) >= 4 and args[2] in ("-v", "--version"):
            ver = args[3]
        from ..pkg.manager import add_dependency
        return add_dependency(pkg_name, ver)

    if command == "install":
        from ..pkg.manager import install_dependencies
        return install_dependencies()

    if command == "publish":
        from ..pkg.manager import publish_package
        return publish_package()

    if command == "run":
        if len(args) < 2:
            print("Error: Missing file argument for 'run'. Usage: sk run [--vm] <file.sk|file.skc>", file=sys.stderr)
            return 1
        use_vm = False
        target_file = None
        for arg in args[1:]:
            if arg == "--vm":
                use_vm = True
            elif target_file is None:
                target_file = arg

        if not target_file:
            print("Error: Missing file argument for 'run'. Usage: sk run [--vm] <file.sk|file.skc>", file=sys.stderr)
            return 1
        return run_file(target_file, use_vm=use_vm)

    if command == "compile":
        if len(args) < 2:
            print("Error: Missing source file. Usage: sk compile <file.sk> [-o <file.skc>]", file=sys.stderr)
            return 1
        src_file = args[1]
        out_file = None
        if len(args) >= 4 and args[2] == "-o":
            out_file = args[3]
        return compile_file(src_file, out_file)

    if command == "dis":
        if len(args) < 2:
            print("Error: Missing file argument for 'dis'. Usage: sk dis <file.sk|file.skc>", file=sys.stderr)
            return 1
        return disassemble_file(args[1])

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

    # If argument ends with .sk or .skc, treat as run
    if command.endswith(".sk") or command.endswith(".skc"):
        return run_file(command)

    print(f"Unknown command: '{command}'")
    print_help()
    return 1


def print_help() -> None:
    print(f"""Sikhar Programming Language v{__version__}
Usage:
  sk [command] [options]
  sk <file.sk|file.skc>

Commands:
  run [--vm] <file>       Execute a Sikhar source (.sk) or bytecode (.skc) file
  build <file> [opt]      Build a standalone executable bundle (.pyz, .bat)
  serve [file|dir] [opt]  Serve a Sikhar web app or static directory (--port, --host, --vm)
  bench <file.sk> [opt]   Benchmark execution speed (AST vs VM comparison)
  compile <file.sk>       Compile Sikhar source to binary bytecode (.skc)
  dis <file>              Disassemble source or bytecode to human-readable IR
  check <file.sk>         Check syntax and parse without running
  format [file.sk]        Format source files deterministically
  init <project>          Create a new Sikhar project scaffold
  add <package>           Add a dependency to sikhar.toml
  install                 Install dependencies declared in sikhar.toml
  publish                 Package and prepare project for distribution
  test                    Run automated test suite
  lsp                     Start Language Server Protocol (JSON-RPC)
  repl                    Start interactive Sikhar session
  version                 Display current version
  help                    Show this help message
""")


if __name__ == "__main__":
    sys.exit(main())

