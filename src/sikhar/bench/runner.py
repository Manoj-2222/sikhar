"""
Sikhar Benchmarking Runner
Measures execution timing, ops/sec, and compares AST vs VM performance.
"""

import sys
import time
from pathlib import Path
from typing import List, Optional

from ..lexer.lexer import Lexer
from ..parser.parser import Parser
from ..interpreter.interpreter import Interpreter
from ..vm.compiler import Compiler
from ..vm.vm import VM


def run_benchmark(file_path: str, iterations: int = 5, compare: bool = True) -> int:
    path = Path(file_path)
    if not path.exists():
        print(f"Error: Benchmark file '{file_path}' does not exist.", file=sys.stderr)
        return 1

    source = path.read_text(encoding="utf-8")

    print(f"[*] Benchmarking: {path.name}")
    print(f"    Iterations: {iterations} runs (with 1 warmup)")
    print("")

    # Suppress normal dekha prints during benchmarking
    null_sink = lambda _msg: None

    # Compile for VM
    tokens = Lexer(source, path.name).tokenize()
    ast = Parser(tokens, source, path.name).parse()
    chunk = Compiler(path.name).compile(ast)

    # 1. Benchmark VM
    vm_times: List[float] = []
    # Warmup
    vm_warmup = VM(source=source, filename=path.name, output_fn=null_sink)
    vm_warmup.run(chunk)

    for _ in range(iterations):
        vm_inst = VM(source=source, filename=path.name, output_fn=null_sink)
        t0 = time.perf_counter()
        vm_inst.run(chunk)
        t1 = time.perf_counter()
        vm_times.append((t1 - t0) * 1000.0)

    avg_vm = sum(vm_times) / len(vm_times)
    min_vm = min(vm_times)
    max_vm = max(vm_times)

    print("+---------------------------+--------------+--------------+--------------+")
    print("| Engine                    | Avg (ms)     | Min (ms)     | Max (ms)     |")
    print("+---------------------------+--------------+--------------+--------------+")
    print(f"| Bytecode Virtual Machine  | {avg_vm:>10.3f}ms | {min_vm:>10.3f}ms | {max_vm:>10.3f}ms |")

    if compare:
        # 2. Benchmark AST Interpreter
        ast_times: List[float] = []
        # Warmup
        ast_warmup = Interpreter(filename=path.name, output_fn=null_sink)
        ast_warmup.interpret(ast)

        for _ in range(iterations):
            ast_inst = Interpreter(filename=path.name, output_fn=null_sink)
            t0 = time.perf_counter()
            ast_inst.interpret(ast)
            t1 = time.perf_counter()
            ast_times.append((t1 - t0) * 1000.0)

        avg_ast = sum(ast_times) / len(ast_times)
        min_ast = min(ast_times)
        max_ast = max(ast_times)

        print(f"| AST Tree-Walker           | {avg_ast:>10.3f}ms | {min_ast:>10.3f}ms | {max_ast:>10.3f}ms |")
        print("+---------------------------+--------------+--------------+--------------+")

        speedup = avg_ast / avg_vm if avg_vm > 0 else 1.0
        print(f"\n[>>] Bytecode VM is {speedup:.2f}x faster than AST interpreter.")
    else:
        print("+---------------------------+--------------+--------------+--------------+")

    return 0
