# Sikhar Language Roadmap

Sikhar follows an incremental, deliberate release roadmap.

---

## v0.1.0 — Current Release (Core Language Foundation)

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

* [ ] Module imports and exports (`aayaat`, `pathaau`)
* [ ] Structured Standard Library namespaces (`std.io`, `std.math`, `std.file`, `std.time`)
* [ ] File operations (`khola`, `banda`, `padh`, `lekh`)
* [ ] Static type checker using explicit type annotations (`rakha x: number = 10`)
* [ ] Native string interpolation (`dekha "Hello, {name}"`)
* [ ] In-language test runner syntax (`jaach`)

---

## v0.3.0 — Bytecode Compiler & Virtual Machine

* [ ] Sikhar Bytecode specification & IR
* [ ] Bytecode compiler
* [ ] Stack-based Sikhar Virtual Machine (VM)
* [ ] Bytecode serialization (`.skc` files)
* [ ] Significant performance benchmarks

---

## v0.4.0 — Web Framework & Networking

* [ ] Native HTTP client and server
* [ ] Official Sikhar Web framework
* [ ] JSON serialization & deserialization
* [ ] REST API routing & middleware
* [ ] Database driver interfaces

---

## v0.5.0 — Developer Tooling & Ecosystem

* [ ] Sikhar Language Server Protocol (LSP) implementation
* [ ] Full VS Code language server extension (diagnostics, autocomplete, go-to-def)
* [ ] Interactive debugger (DAP)
* [ ] Package manager (`sk add`, `sk install`, `sk publish`)
* [ ] Official documentation portal

---

## v1.0.0 — Production-Ready Sikhar

* [ ] Frozen, standardized language specification
* [ ] AOT compiler (LLVM backend / WebAssembly)
* [ ] Native cross-platform binary generation
* [ ] Production web & desktop ecosystem
