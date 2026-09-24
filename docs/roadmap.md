# Sikhar Language Roadmap

Sikhar follows an incremental, deliberate release roadmap.

---

## v0.1.0 — Initial Release (Core Language Foundation)

* [x] Lexer with full Nepali-inspired keywords & Unicode support
* [x] Parser producing structured, typed AST
* [x] Tree-walking interpreter with clean environments
* [x] Variables (`rakha`), mutations (`badla`), constants (`sthayi`)
* [x] Primitive types: `number`, `decimal`, `text`, `boolean`, `null`
* [x] Collections: `list`, `map` with indexing & mutations
* [x] Control flow: `yadi` / `athawa` / `natra`
* [x] Loops: `jaba`, `ko_lagi ... ma ...`, `rok`, `jaari`
* [x] Functions: `kaam`, `farka`, recursion, closures
* [x] Native error handling: `koshish`, `samata`, `fal`
* [x] Developer-friendly diagnostics without raw Python stack traces
* [x] Unified CLI (`sk run`, `sk check`, `sk format`, `sk test`, `sk init`, `sk repl`)
* [x] Deterministic AST-based code formatter
* [x] VS Code syntax extension

---

## v0.2.0 — Modules & Standard Library

* [x] Module imports and exports (`aayaat`, `pathaau`) with file isolation & caching
* [x] Structured Standard Library namespaces (`std.math`, `std.text`, `std.list`, `std.map`, `std.time`, `std.file`, `std.system`)
* [x] File I/O operations and builtins (`khola`, `banda`, `padh`, `lekh`)
* [x] Native string interpolation (`dekha "Hello, {name}"`) with brace escaping
* [x] In-language test assertions (`jaach <condition> [, <message>]`)
* [x] Dual-engine test runner (`sk test` running unit tests & native `.sk` tests)

---

## v0.3.0 — Bytecode Compiler & Virtual Machine

* [x] Sikhar Bytecode specification & IR (`OpCode` enum & instruction set)
* [x] Stack-based Bytecode compiler (`Compiler` with lexical scoping and jump patching)
* [x] High-performance stack-based Virtual Machine (`VM` with CallFrames)
* [x] Binary bytecode serialization & deserialization (`.skc` format)
* [x] Built-in Bytecode Disassembler (`sk dis`)
* [x] CLI enhancements: `sk compile`, `sk dis`, `sk run --vm`, and direct `.skc` execution
* [x] Performance benchmarks comparing AST tree-walker vs Virtual Machine

---

## v0.4.0 — Web Framework & Networking

* [x] Native HTTP client and standalone HTTP server (`std.http`)
* [x] Official Sikhar Web framework (`std.web`) with routing, parameterized paths, and middleware
* [x] Fast JSON serialization, deserialization & validation (`std.json`)
* [x] Embedded SQLite database driver (`std.db`) with parameterized queries and transactions
* [x] Reentrant VM callbacks and first-class anonymous function expressions (`kaam(...) { ... }`)
* [x] CLI web server command (`sk serve`) with live reloading and static asset hosting
* [x] Zero external dependencies maintained across both AST interpreter and Bytecode VM

---

## v0.5.0 — Developer Tooling & LSP
* [x] Standard JSON-RPC 2.0 Language Server (`sk lsp`) with diagnostics, hover, symbols, and completion
* [x] Automated benchmarking engine (`sk bench`) comparing AST vs Bytecode VM

---

## v0.6.0 — Concurrency & System Processes
* [x] Asynchronous multi-threaded worker tasks (`std.task`) with thread-isolated execution
* [x] Child process execution, pipes, and environment variables (`std.process`)

---

## v0.7.0 — Cryptography & Security
* [x] Secure hashing algorithms (`std.crypto`: SHA-256, SHA-512, MD5)
* [x] Keyed HMAC message authentication and Base64 encode/decode
* [x] Cryptographically secure random tokens and nonces

---

## v0.8.0 — Package Management & Manifests
* [x] Project manifest format (`sikhar.toml`) with root and dependency sections
* [x] Dependency management CLI: `sk add` and `sk install`
* [x] Standalone distribution packager: `sk publish`

---

## v0.9.0 — Structured Data & Text Processing
* [x] Built-in CSV parser, generator, and file I/O (`std.csv`) with custom delimiters
* [x] Regular expression pattern matching, search, and substitution (`std.regex`)

---

## v1.0.0 — Production-Ready Release (Unified Standard)
* [x] Standalone executable and binary bundler (`sk build`) producing zero-dependency `.pyz` and `.bat` executables
* [x] Formal frozen language specification (`docs/language-specification-v1.0.md`) guaranteeing syntax and bytecode stability
* [x] Official distribution packages (`sikhar-1.0.0-py3-none-any.whl` and `sikhar-1.0.0.tar.gz`)
* [x] Dual-engine execution parity across AST Tree-Walker and Bytecode Virtual Machine
* [x] Full test suite with 120+ automated unit tests and native `.sk` test runners
* [x] Zero external dependencies across core engine, stdlib, web framework, LSP, and package manager

---

## Post-1.0 — Future Horizons
* [ ] LLVM / WebAssembly AOT backend for direct native machine code generation
* [ ] Interactive Step Debugger (DAP protocol)
* [ ] Cloud package registry portal
