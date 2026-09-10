# Sikhar Programming Language

<div align="center">

```
  ____  _ _    _                 
 / ___|(_) | _| |__   __ _ _ __  
 \___ \| | |/ / '_ \ / _` | '__| 
  ___) | |   <| | | | (_| | |    
 |____/|_|_|\_\_| |_|\__,_|_|    
```

**Sikhar (`v0.3.0`)** — A modern, expressive, and beginner-friendly programming language with Nepali-inspired keywords, clean grammar, and pinpoint diagnostics.

[![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)](https://github.com/Manoj-2222/sikhar)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)](https://www.python.org/)

</div>

---

## 🏔️ Core Identity

* **Language Name**: Sikhar
* **Current Version**: v0.3.0
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

---

## 🛠️ CLI Commands (`sk`)

```bash
sk run [--vm] <file>  # Execute source (.sk) or compiled bytecode (.skc)
sk compile <file.sk>  # Compile source to binary bytecode (.skc)
sk dis <file>         # Disassemble source or bytecode to human-readable IR
sk check <file.sk>    # Parse and validate syntax without execution
sk format [file.sk]   # Deterministically format source code
sk test               # Run test suite (Python + Native .sk tests)
sk init <project>     # Scaffold a new project
sk repl               # Start interactive REPL
sk version            # Display current version
sk help               # Show help message
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
│       ├── vm/                # Stack-based Bytecode Virtual Machine (v0.3.0)
│       │   ├── __init__.py
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
│       │   ├── __init__.py
│       │   ├── math.py        # std.math
│       │   ├── text.py        # std.text
│       │   ├── list.py        # std.list
│       │   ├── map.py         # std.map
│       │   ├── time.py        # std.time
│       │   ├── file.py        # std.file
│       │   └── system.py      # std.system
│       ├── errors/            # Native diagnostics & formatting
│       │   ├── error_types.py
│       │   └── reporter.py
│       ├── formatter/         # Canonical AST formatter
│       │   └── formatter.py
│       └── cli/               # CLI commands and REPL
│           └── main.py
├── bin/
│   ├── sk.bat                 # Windows CLI launcher
│   └── sk                     # POSIX shell launcher
├── benchmarks/                # Performance benchmarks
│   └── run_benchmarks.py
├── tests/                     # Test suite (Python + Native .sk)
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_interpreter.py
│   ├── test_functions.py
│   ├── test_collections.py
│   ├── test_errors.py
│   ├── test_formatter.py
│   ├── test_cli.py
│   ├── test_modules.py
│   ├── test_stdlib.py
│   ├── test_interpolation.py
│   ├── test_assert.py
│   ├── test_compiler.py       # Compiler & disassembler unit tests
│   ├── test_vm.py             # VM execution unit tests
│   ├── test_skc.py            # .skc serialization tests
│   └── test_v020_features.sk  # Native .sk test suite
├── examples/                  # 13 runnable example scripts
├── docs/                      # 16 detailed documentation guides
│   ├── introduction.md
│   ├── installation.md
│   ├── syntax.md
│   ├── variables.md
│   ├── types.md
│   ├── operators.md
│   ├── conditions.md
│   ├── loops.md
│   ├── functions.md
│   ├── collections.md
│   ├── errors.md
│   ├── modules.md
│   ├── standard-library.md
│   ├── bytecode-vm.md         # VM architecture & instruction set guide
│   ├── cli.md
│   └── roadmap.md
├── vscode-extension/          # Official VS Code syntax highlighting
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
Ran 87 tests in 0.029s
OK
=== Running Sikhar Python Test Suite ===

=== Running Native Sikhar (.sk) Test Suite ===
Testing tests\test_v020_features.sk ... PASSED
```

---

## 🗺️ Roadmap Ahead

* [x] **v0.1.0**: Core Language Foundation (Lexer, Parser, Interpreter, REPL, CLI, Formatter).
* [x] **v0.2.0**: Modules (`aayaat`, `pathaau`), Standard Library (`std.*`), File I/O, String Interpolation, Assertions (`jaach`).
* [x] **v0.3.0**: Bytecode Compiler & Virtual Machine (`.skc`), Disassembler (`sk dis`).
* [ ] **v0.4.0**: Networking & Sikhar Web framework.
* [ ] **v0.5.0**: Language Server Protocol (LSP) & Package Manager.
* [ ] **v1.0.0**: Production-grade Compiler (Native/Wasm) and standardized ecosystem.

---

## 📜 License

Licensed under the [MIT License](LICENSE).

