# Sikhar CLI Tool (`sk`)

The `sk` command-line tool provides a unified interface for running, checking, formatting, testing, and managing Sikhar projects.

## Commands Overview

| Command | Usage | Description |
| :--- | :--- | :--- |
| `run` | `sk run [--vm] <file.sk\|file.skc>` | Execute a source file or compiled binary |
| `compile` | `sk compile <file.sk> [-o <out.skc>]` | Compile source to binary bytecode (`.skc`) |
| `dis` | `sk dis <file.sk\|file.skc>` | Disassemble bytecode to human-readable IR |
| `check` | `sk check <file.sk>` | Parse and validate syntax without executing |
| `format` | `sk format [file.sk]` | Deterministically format source code |
| `init` | `sk init <project-name>` | Scaffold a new Sikhar project |
| `test` | `sk test` | Run project unit test suite |
| `repl` | `sk repl` (or `sk`) | Start interactive REPL session |
| `version` | `sk version` | Print current Sikhar version |
| `help` | `sk help` | Display CLI help message |

---

## Detailed Command Usage

### 1. `sk run`

Executes any `.sk` file directly using either the AST tree-walking interpreter (default) or the stack-based VM:

```bash
# Run with AST interpreter
sk run examples/01_hello.sk

# Run on the bytecode VM
sk run --vm examples/01_hello.sk

# Run compiled bytecode binary directly
sk run hello.skc
```

### 2. `sk compile`

Compiles a `.sk` source file into a portable `.skc` binary:

```bash
sk compile examples/01_hello.sk -o hello.skc
```

### 3. `sk dis`

Disassembles either a `.sk` source file or a compiled `.skc` binary into human-readable bytecode instructions:

```bash
sk dis examples/01_hello.sk
```


### 2. `sk check`

Quickly checks syntax without running code or performing side effects:

```bash
sk check src/main.sk
```

Output:
```text
Syntax OK: src/main.sk
```

### 3. `sk format`

Deterministically formats one or more files in place:

```bash
sk format src/main.sk
```

### 4. `sk init`

Creates a modern project structure:

```bash
sk init my-app
```

Generated directory tree:

```text
my-app/
├── src/
│   └── main.sk
├── tests/
├── sikhar.toml
└── README.md
```

### 5. `sk test`

Discovers and runs test files in the `tests/` directory:

```bash
sk test
```

### 6. `sk repl`

Launches the interactive Read-Eval-Print Loop:

```bash
sk repl
```

```text
Sikhar Programming Language v0.1.0
Type 'exit' or 'samapta' to quit. Press Ctrl+C to cancel line.

sikhar> rakha x = 42
sikhar> dekha x * 2
84
sikhar> exit
Dhanyabad!
```
