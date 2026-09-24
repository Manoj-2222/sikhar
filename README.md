# Sikhar Programming Language

<div align="center">

```
  ____  _ _    _                 
 / ___|(_) | _| |__   __ _ _ __  
 \___ \| | |/ / '_ \ / _` | '__| 
  ___) | |   <| | | | (_| | |    
 |____/|_|_|\_\_| |_|\__,_|_|    
```

**Sikhar (`v1.0.0`)** — A modern, expressive, and beginner-friendly programming language with Nepali-inspired keywords, clean grammar, pinpoint diagnostics, and production-ready toolchain.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Manoj-2222/sikhar)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)](https://www.python.org/)

</div>

---

## 🏔️ Core Identity

* **Language Name**: Sikhar
* **Current Version**: v1.0.0 (Production-Ready)
* **Source Extension**: `.sk`
* **Bytecode Extension**: `.skc`
* **CLI Command**: `sk`
* **Execution Model**: Dual-Engine (AST Tree-Walking Interpreter + Stack-Based Bytecode VM)
* **Dependencies**: Zero external dependencies (Pure Python 3.10+ Standard Library)


---

## 🚀 Quick Start

### 1. The Hello World Program

Create `hello.sk`:

```sk
rakha sandesh = "Namaste, Sansar!"
dekha sandesh

rakha x = 10
dekha x

yadi x > 5 {
    dekha "Thulo"
}
```

### 2. Running with CLI

On Windows:
```cmd
.\sk.bat run hello.sk
```

On Linux / macOS:
```bash
./bin/sk run hello.sk
```

Or directly via Python:
```bash
python -m sikhar run hello.sk
```

Output:
```text
Namaste, Sansar!
10
Thulo
```

---

## 📖 Language Syntax & Features

### 1. Variables and Constants

```sk
# Mutable variable
rakha naam = "Manoj"
rakha age = 20

# Intentional mutation using 'badla'
badla age = 21

# Immutable constant using 'sthayi'
sthayi pi = 3.14159
```

Attempting to modify a constant produces a native Sikhar error:
```text
Sikhar Error

Type: ConstantMutation
Message: Cannot modify constant 'pi' declared with 'sthayi'

File: main.sk
Line: 8
Column: 1

   8 | badla pi = 3.0
       ^
```

### 2. Data Types

| Type | Literal Example |
| :--- | :--- |
| `number` | `10`, `-42`, `0` |
| `decimal` | `3.14159`, `99.50` |
| `text` | `"Sikhar Language"` |
| `boolean` | `sacho` (true), `jutho` (false) |
| `null` | `khali` |
| `list` | `[10, 20, 30]` |
| `map` | `{"name": "Manoj", "age": 20}` |

### 3. Conditions: `yadi` - `athawa` - `natra`

```sk
rakha marks = 85

yadi marks >= 90 {
    dekha "Grade: A"
} athawa marks >= 80 {
    dekha "Grade: B"
} natra {
    dekha "Grade: C"
}
```

### 4. Loops: `jaba` and `ko_lagi ... ma ...`

```sk
# While loop
rakha i = 1
jaba i <= 3 {
    dekha i
    badla i = i + 1
}

# Collection iteration
rakha fruits = ["Aam", "Kera", "Suntala"]
ko_lagi fruit ma fruits {
    dekha fruit
}

# Break ('rok') and Continue ('jaari')
ko_lagi x ma [1, 2, 3, 4, 5] {
    yadi x == 2 {
        jaari
    }
    yadi x == 4 {
        rok
    }
    dekha x
}
```

### 5. Functions: `kaam` and `farka`

```sk
kaam jod(a, b) {
    farka a + b
}

rakha sum = jod(15, 25)
dekha sum # 40

# Recursion
kaam factorial(n) {
    yadi n <= 1 {
        farka 1
    }
    farka n * factorial(n - 1)
}

dekha factorial(5) # 120
```

### 6. Collections: Lists and Maps

```sk
# Lists
rakha numbers = [10, 20, 30]
dekha numbers[0]       # 10
badla numbers[1] = 99  # Update in place
jod_suchi(numbers, 40) # Append
dekha lamba(numbers)   # 4

# Maps
rakha user = {
    "name": "Manoj",
    "role": "Engineer"
}
dekha user["name"]
badla user["city"] = "Kathmandu"
```

### 7. Error Handling: `koshish`, `samata`, `fal`

```sk
koshish {
    fal "Something went wrong"
} samata error {
    dekha "Caught: " + error
}
```

### 8. Modules & Standard Library: `aayaat`, `pathaau`

Export public symbols from files with `pathaau`:
```sk
# math_utils.sk
pathaau sthayi PI = 3.14159
pathaau kaam barga(n) { farka n * n }
```

Import local files or standard modules with `aayaat`:
```sk
aayaat "math_utils.sk"
aayaat std.math
aayaat std.text

dekha math_utils.barga(6)    # 36
dekha math.sqrt(64)          # 8.0
dekha text.thulo("sikhar")   # SIKHAR
```

### 9. String Interpolation

Embed variables and expressions seamlessly in text:
```sk
rakha user = "Manoj"
rakha score = 95
dekha "Player {user} scored {score + 5} points!"
# Literal braces can be escaped with \{ and \}
dekha "Format: \{not_interpolated\}"
```

### 10. In-Language Assertions: `jaach`

Write self-testing scripts and assertions natively:
```sk
jaach 10 + 20 == 30, "Math sanity check"
jaach text.contains("hello world", "world")
```

### 11. Bytecode Compiler & Virtual Machine (`.skc`)

Compile any Sikhar script to portable binary bytecode for execution on the stack-based VM:

```bash
# Compile to binary bytecode (.skc)
sk compile examples/01_hello.sk -o hello.skc

# Run on the Virtual Machine
sk run --vm examples/01_hello.sk
sk run hello.skc

# Disassemble into human-readable IR
sk dis examples/01_hello.sk
```

### 12. Web Framework, Networking & Databases (`std.web`, `std.http`, `std.json`, `std.db`)

Build web applications, microservices, and persistent database-backed APIs with zero external dependencies:

```sk
aayaat std.web
aayaat std.db
aayaat std.json

rakha app = web.app()
rakha conn = db.connect(":memory:")
conn.execute("CREATE TABLE visitors (id INTEGER PRIMARY KEY, name TEXT)")

app.get("/", kaam(req) {
    farka "Welcome to Sikhar Web Framework!"
})

app.get("/visitors/:name", kaam(req) {
    rakha guest = req.params["name"]
    conn.execute("INSERT INTO visitors (name) VALUES (?)", [guest])
    farka {"status": 200, "body": {"greeting": "Namaste, " + guest + "!"}}
})

app.listen(8000)
```

Run with the CLI server:
```bash
sk serve app.sk --port 8000
```

### 13. Standalone Executable Bundler (`sk build`)

Compile and bundle any Sikhar application into a self-contained, standalone executable archive (`.pyz` and companion `.bat` launcher on Windows) with zero third-party dependencies:

```bash
# Build standalone executable bundle
sk build src/main.sk

# Specify custom output path
sk build src/main.sk -o dist/my_app.pyz

# Run anywhere with Python without installing Sikhar:
python dist/my_app.pyz
# Or run the companion launcher on Windows:
.\dist\my_app.bat
```

---

## 🛠️ CLI Commands (`sk`)

```bash
sk run [--vm] <file>       # Execute source (.sk) or compiled bytecode (.skc)
sk build <file> [opt]      # Build standalone executable bundle (.pyz, .bat)
sk serve [file|dir] [opt]  # Serve web app or static directory (--port, --host, --vm)
sk bench <file.sk> [opt]   # Benchmark execution speed (AST vs VM comparison)
sk compile <file.sk>       # Compile source to binary bytecode (.skc)
sk dis <file>              # Disassemble source or bytecode to human-readable IR
sk check <file.sk>         # Parse and validate syntax without execution
sk format [file.sk]        # Deterministically format source code
sk add <pkg> [ver]         # Add dependency to sikhar.toml
sk install                 # Install dependencies from sikhar.toml
sk publish                 # Package project for distribution
sk lsp                     # Start JSON-RPC 2.0 Language Server on stdio
sk test                    # Run test suite (Python + Native .sk tests)
sk init <project>          # Scaffold a new project
sk repl                    # Start interactive REPL
sk version                 # Display current version
sk help                    # Show help message
```

---

## 📂 Repository Structure

```text
sikhar/
├── src/
│   └── sikhar/
│       ├── __init__.py
│       ├── __main__.py
│       ├── lexer/             # Scanner, tokens & Unicode support
│       │   ├── token_type.py
│       │   ├── token.py
│       │   └── lexer.py
│       ├── parser/            # Recursive descent parser & AST
│       │   ├── ast_nodes.py
│       │   └── parser.py
│       ├── interpreter/       # AST interpreter, environments & values
│       │   ├── environment.py
│       │   ├── values.py
│       │   └── interpreter.py
│       ├── vm/                # Stack-based Bytecode Virtual Machine
│       │   ├── opcodes.py     # Instruction set & OpCodes
│       │   ├── chunk.py       # Instruction & constant chunk containers
│       │   ├── compiler.py    # AST-to-Bytecode compiler & scope resolver
│       │   ├── vm.py          # High-performance stack VM & CallFrames
│       │   ├── disassembler.py# Bytecode disassembler
│       │   └── serializer.py  # .skc binary serialization & loader
│       ├── runtime/           # Builtins & ModuleLoader
│       │   ├── builtins.py
│       │   └── module_loader.py
│       ├── std/               # Standard Library
│       │   ├── math.py        # std.math
│       │   ├── text.py        # std.text
│       │   ├── list.py        # std.list
│       │   ├── map.py         # std.map
│       │   ├── time.py        # std.time
│       │   ├── file.py        # std.file
│       │   ├── system.py      # std.system
│       │   ├── json.py        # std.json
│       │   ├── http.py        # std.http
│       │   ├── web.py         # std.web framework
│       │   ├── db.py          # std.db SQLite driver
│       │   ├── crypto.py      # std.crypto
│       │   ├── csv.py         # std.csv
│       │   ├── regex.py       # std.regex
│       │   ├── process.py     # std.process
│       │   └── task.py        # std.task
│       ├── lsp/               # Language Server Protocol (LSP)
│       │   └── server.py
│       ├── pkg/               # Package manager
│       │   └── manager.py
│       ├── bench/             # Benchmarking runner
│       │   └── runner.py
│       ├── builder/           # Standalone executable bundler
│       │   └── bundle.py
│       ├── errors/            # Native diagnostics & formatting
│       ├── formatter/         # Canonical AST formatter
│       └── cli/               # CLI commands and REPL
├── tests/                     # Comprehensive test suite (120+ tests)
├── examples/                  # 20 runnable example scripts
├── docs/                      # 23 documentation guides & specifications
├── pyproject.toml
├── sikhar.toml
├── LICENSE
└── README.md
```

---

## 🧪 Running Automated Tests

Run the full dual-engine test suite:

```bash
sk test
```
or
```bash
python -m unittest discover -s tests -p "test_*.py"
```

Result:
```text
Ran 123 tests in 2.2s
OK
=== Running Sikhar Python Test Suite ===

=== Running Native Sikhar (.sk) Test Suite ===
Testing tests\test_v020_features.sk ... PASSED
Testing tests\test_v040_features.sk ... PASSED
Testing tests\test_v100_features.sk ... PASSED
```

---

## 🗺️ Roadmap & Release Milestones

* [x] **v0.1.0**: Core Language Foundation (Lexer, Parser, Interpreter, REPL, CLI, Formatter).
* [x] **v0.2.0**: Modules (`aayaat`, `pathaau`), Standard Library (`std.*`), File I/O, String Interpolation, Assertions (`jaach`).
* [x] **v0.3.0**: Bytecode Compiler & Virtual Machine (`.skc`), Disassembler (`sk dis`).
* [x] **v0.4.0**: Networking & Sikhar Web framework (`std.web`, `std.http`, `std.json`, `std.db`, `sk serve`).
* [x] **v0.5.0**: Developer Tooling, Language Server Protocol (`sk lsp`), Benchmarking (`sk bench`).
* [x] **v0.6.0**: Concurrency (`std.task`) & System Subprocesses (`std.process`).
* [x] **v0.7.0**: Cryptography & Security (`std.crypto`).
* [x] **v0.8.0**: Package Manager & Manifests (`sikhar.toml`, `sk add`, `sk install`, `sk publish`).
* [x] **v0.9.0**: Structured Data & Text Processing (`std.csv`, `std.regex`).
* [x] **v1.0.0**: **Production-Ready Sikhar** (Unified standard, standalone bundler `sk build`, dual-engine parity, 120+ tests).
* [ ] **Post-1.0**: LLVM / WebAssembly AOT backend and Interactive Debugger (DAP).

---

## 📜 License

Licensed under the [MIT License](LICENSE).
