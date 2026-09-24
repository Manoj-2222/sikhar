# Sikhar CLI Tool (`sk`)

The `sk` command-line tool provides a unified interface for running, checking, formatting, testing, and managing Sikhar projects.

## Commands Overview

| Command | Usage | Description |
| :--- | :--- | :--- |
| `run` | `sk run [--vm] <file.sk\|file.skc>` | Execute a source file or compiled binary |
| `build` | `sk build <file.sk\|file.skc> [options]` | Build a standalone executable bundle (`.pyz`, `.bat`) |
| `serve` | `sk serve [file\|dir] [options]` | Serve a Sikhar web app or static asset directory |
| `bench` | `sk bench <file.sk> [--runs N]` | Benchmark execution speed comparing AST vs VM |
| `compile` | `sk compile <file.sk> [-o <out.skc>]` | Compile source to binary bytecode (`.skc`) |
| `dis` | `sk dis <file.sk\|file.skc>` | Disassemble bytecode to human-readable IR |
| `check` | `sk check <file.sk>` | Parse and validate syntax without executing |
| `format` | `sk format [file.sk]` | Deterministically format source code |
| `init` | `sk init <project-name>` | Scaffold a new Sikhar project |
| `add` | `sk add <package> [version]` | Add dependency to `sikhar.toml` |
| `install` | `sk install` | Install dependencies from `sikhar.toml` |
| `publish` | `sk publish` | Package and validate project for publication |
| `lsp` | `sk lsp` | Start JSON-RPC 2.0 Language Server on stdio |
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

### 2. `sk build`

Compiles and packages a Sikhar program into a self-contained, standalone executable bundle (`.pyz` and companion `.bat` launcher on Windows) with zero third-party dependencies:

```bash
# Build standalone executable bundle for an application
sk build src/main.sk

# Specify custom output bundle path
sk build src/main.sk -o dist/my_app.pyz

# Build with AST interpreter instead of Bytecode VM
sk build src/main.sk --ast

# Run the generated bundle directly without installing Sikhar:
python dist/my_app.pyz
# Or run the companion launcher on Windows:
.\dist\my_app.bat
```

### 3. `sk serve`

Serves a Sikhar web application script or static files directory:

```bash
# Serve default web app (src/main.sk or main.sk) on http://127.0.0.1:8000
sk serve

# Serve a specific Sikhar script
sk serve app.sk

# Specify custom port and host
sk serve app.sk --port 3000 --host 0.0.0.0

# Run using the Bytecode Virtual Machine
sk serve app.sk --vm --port 8080

# Serve static directory (HTML, CSS, JS)
sk serve ./dist --port 5000
```

### 3. `sk compile`

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
Sikhar Programming Language v1.0.0
Type 'exit' or 'samapta' to quit. Press Ctrl+C to cancel line.

sikhar> rakha x = 42
sikhar> dekha x * 2
84
sikhar> exit
Dhanyabad!
```

### 7. `sk bench`

Benchmarks program execution comparing the Bytecode VM against the AST interpreter:

```bash
sk bench examples/08_algorithms.sk --runs 5
```

### 8. Package Management (`sk add`, `sk install`, `sk publish`)

Manage dependencies and packages declared in `sikhar.toml`:

```bash
# Add a dependency
sk add nepal_utils ^1.2.0

# Install dependencies into .sikhar/packages/
sk install

# Package project for distribution
sk publish
```

### 9. Language Server Protocol (`sk lsp`)

Starts the JSON-RPC 2.0 Language Server on stdio for IDE integration (VS Code, Neovim, Zed):

```bash
sk lsp
```
