# Sikhar Programming Language

<div align="center">

```
  ____  _ _    _                 
 / ___|(_) | _| |__   __ _ _ __  
 \___ \| | |/ / '_ \ / _` | '__| 
  ___) | |   <| | | | (_| | |    
 |____/|_|_|\_\_| |_|\__,_|_|    
```

**Sikhar (`v0.1.0`)** — A modern, expressive, and beginner-friendly programming language with Nepali-inspired keywords, clean grammar, and pinpoint diagnostics.

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/sikhar-lang/sikhar)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)](https://www.python.org/)

</div>

---

## 🏔️ Core Identity

* **Language Name**: Sikhar
* **Current Version**: v0.1.0
* **Source Extension**: `.sk`
* **CLI Command**: `sk`
* **Execution Model**: Pure AST Tree-Walking Interpreter
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

---

## 🛠️ CLI Commands (`sk`)

```bash
sk run <file.sk>       # Execute a Sikhar source file
sk check <file.sk>     # Parse and validate syntax without execution
sk format [file.sk]    # Deterministically format source code
sk test                # Run the automated test suite
sk init <project>      # Scaffold a new project
sk repl                # Start interactive REPL
sk version             # Display current version
sk help                # Show help message
```

---

## 📂 Repository Structure

```text
sikhar/
├── src/
│   └── sikhar/
│       ├── __init__.py
│       ├── __main__.py
│       ├── lexer/             # Character scanner & token definitions
│       │   ├── token_type.py
│       │   ├── token.py
│       │   └── lexer.py
│       ├── parser/            # Recursive descent parser & AST
│       │   ├── ast_nodes.py
│       │   └── parser.py
│       ├── interpreter/       # AST tree-walking interpreter & scopes
│       │   ├── environment.py
│       │   ├── values.py
│       │   └── interpreter.py
│       ├── runtime/           # Built-in functions (dekha, sodha, lamba...)
│       │   └── builtins.py
│       ├── errors/            # Native Sikhar diagnostics & formatting
│       │   ├── error_types.py
│       │   └── reporter.py
│       ├── formatter/         # Canonical deterministic AST formatter
│       │   └── formatter.py
│       └── cli/               # CLI commands and REPL
│           └── main.py
├── bin/
│   ├── sk.bat                 # Windows CLI launcher
│   └── sk                     # POSIX shell launcher
├── tests/                     # Automated unit test suite (49 tests)
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_interpreter.py
│   ├── test_functions.py
│   ├── test_collections.py
│   ├── test_errors.py
│   ├── test_formatter.py
│   └── test_cli.py
├── examples/                  # 8 runnable demonstration scripts
│   ├── 01_hello.sk
│   ├── 02_variables.sk
│   ├── 03_conditions.sk
│   ├── 04_loops.sk
│   ├── 05_functions.sk
│   ├── 06_collections.sk
│   ├── 07_error_handling.sk
│   └── 08_algorithms.sk
├── docs/                      # 15 detailed documentation guides
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
│   ├── cli.md
│   └── roadmap.md
├── vscode-extension/          # Official VS Code syntax highlighting
│   ├── package.json
│   ├── language-configuration.json
│   └── syntaxes/
│       └── sikhar.tmLanguage.json
├── pyproject.toml
├── sikhar.toml
├── LICENSE
└── README.md
```

---

## 🧪 Running Automated Tests

Run the full test suite with either command:

```bash
sk test
```
or
```bash
python -m unittest discover -s tests -p "test_*.py"
```

Result:
```text
Ran 49 tests in 0.010s
OK
```

---

## 🗺️ Roadmap Ahead

* **v0.2.0**: Modules (`aayaat`, `pathaau`), Standard Library (`std.*`), File I/O (`khola`, `padh`, `lekh`, `banda`).
* **v0.3.0**: Bytecode Compiler & Virtual Machine.
* **v0.4.0**: Networking & Sikhar Web framework.
* **v0.5.0**: Language Server Protocol (LSP) & Package Manager.
* **v1.0.0**: Production-grade Compiler (Native/Wasm) and standardized ecosystem.

---

## 📜 License

Licensed under the [MIT License](LICENSE).
