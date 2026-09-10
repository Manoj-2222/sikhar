"""
Sikhar Performance Benchmarks
Compares AST Tree-Walking Interpreter vs Bytecode Virtual Machine (VM).
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sikhar.lexer import Lexer
from sikhar.parser import Parser
from sikhar.interpreter import Interpreter
from sikhar.vm import Compiler, VM


def benchmark_snippet(name: str, code: str, iterations: int = 5):
    # Prepare AST
    tokens = Lexer(code, "<benchmark>").tokenize()
    ast = Parser(tokens, code, "<benchmark>").parse()

    # Prepare Bytecode Chunk
    chunk = Compiler("<benchmark>").compile(ast)

    # Warmup
    interp_warmup = Interpreter(output_fn=lambda x: None)
    interp_warmup.interpret(ast)

    vm_warmup = VM(output_fn=lambda x: None)
    vm_warmup.run(chunk)

    # Benchmark AST Interpreter
    interp_times = []
    for _ in range(iterations):
        interp = Interpreter(output_fn=lambda x: None)
        t0 = time.perf_counter()
        interp.interpret(ast)
        t1 = time.perf_counter()
        interp_times.append(t1 - t0)
    avg_interp = sum(interp_times) / len(interp_times)

    # Benchmark Bytecode VM
    vm_times = []
    for _ in range(iterations):
        vm = VM(output_fn=lambda x: None)
        t0 = time.perf_counter()
        vm.run(chunk)
        t1 = time.perf_counter()
        vm_times.append(t1 - t0)
    avg_vm = sum(vm_times) / len(vm_times)

    speedup = avg_interp / avg_vm if avg_vm > 0 else 1.0

    print(f"| {name:<30} | {avg_interp*1000:>10.2f} ms | {avg_vm*1000:>10.2f} ms | {speedup:>8.2f}x |")


def main():
    print("==========================================================================")
    print("       Sikhar v0.3.0 Benchmark: AST Interpreter vs Bytecode VM           ")
    print("==========================================================================")
    print(f"| {'Benchmark Name':<30} | {'AST Interp':>10} | {'Bytecode VM':>10} | {'Speedup':>8} |")
    print("|" + "-" * 32 + "|" + "-" * 13 + "|" + "-" * 13 + "|" + "-" * 10 + "|")

    # 1. Fibonacci recursion
    fib_code = """
    kaam fib(n) {
        yadi n <= 1 {
            farka n
        }
        farka fib(n - 1) + fib(n - 2)
    }
    rakha res = fib(18)
    """
    benchmark_snippet("Recursive Fibonacci (n=18)", fib_code, iterations=5)

    # 2. Tight loop summation
    loop_code = """
    rakha sum = 0
    rakha i = 1
    jaba i <= 10000 {
        badla sum = sum + i
        badla i = i + 1
    }
    """
    benchmark_snippet("Tight Loop Sum (10,000 iters)", loop_code, iterations=5)

    # 3. List construction & mutation
    list_code = """
    rakha lst = []
    rakha i = 0
    jaba i < 2000 {
        jod_suchi(lst, i * 2)
        badla i = i + 1
    }
    """
    benchmark_snippet("List Append (2,000 items)", list_code, iterations=5)

    # 4. Function call overhead
    func_code = """
    kaam compute(a, b) {
        farka (a * 3) + (b * 2)
    }
    rakha total = 0
    rakha i = 0
    jaba i < 5000 {
        badla total = total + compute(i, 2)
        badla i = i + 1
    }
    """
    benchmark_snippet("Function Calls (5,000 iters)", func_code, iterations=5)

    print("==========================================================================")


if __name__ == "__main__":
    main()
