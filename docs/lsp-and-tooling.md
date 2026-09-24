# Developer Tooling & Language Server Protocol (LSP)

Sikhar provides first-class developer tooling directly in the standard distribution, including an LSP server for modern code editors (VS Code, Neovim, Zed, Helix), code formatters, and a benchmarking engine.

---

## Language Server Protocol (`sk lsp`)

Sikhar implements a standard **JSON-RPC 2.0** Language Server listening on standard I/O (`stdio`).

### Capabilities
- **Live Diagnostics**: Parses code on document open and edit, reporting syntax errors with exact line, column, and error messages.
- **Hover Documentation**: Detailed Markdown explanation and code examples when hovering over keywords (`rakha`, `kaam`, `yadi`, etc.).
- **Symbol Outline**: Hierarchical outline of functions (`kaam`) and variables declared in the document for breadcrumbs and symbol finders.
- **IntelliSense Autocompletion**: Auto-completes keywords, built-in functions, and standard library module namespaces (`std.crypto`, `std.csv`, etc.).

### Starting the Server
```bash
sk lsp
```
The server reads headers and JSON payloads from standard input and streams formatted JSON-RPC responses to standard output:
```
Content-Length: 142

{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": { ... }}
```

### Editor Configuration (e.g. Neovim)
```lua
vim.lsp.start({
  name = 'sikhar-lsp',
  cmd = {'sk', 'lsp'},
  root_dir = vim.fs.dirname(vim.fs.find({'sikhar.toml', '.git'}, { upward = true })[1]),
})
```

---

## Benchmarking Engine (`sk bench`)

Compare the execution speed between the AST Tree-Walker and Bytecode Virtual Machine across multiple warmup and measured runs:

```bash
sk bench examples/08_algorithms.sk --runs 5
```

Output:
```
[*] Benchmarking: 08_algorithms.sk
    Iterations: 5 runs (with 1 warmup)

+---------------------------+--------------+--------------+--------------+
| Engine                    | Avg (ms)     | Min (ms)     | Max (ms)     |
+---------------------------+--------------+--------------+--------------+
| Bytecode Virtual Machine  |      0.592ms |      0.588ms |      0.601ms |
| AST Tree-Walker           |      0.222ms |      0.209ms |      0.261ms |
+---------------------------+--------------+--------------+--------------+

[>>] Bytecode VM is 0.38x faster than AST interpreter.
```

---

## Deterministic Code Formatter (`sk format`)

Format Sikhar source files with canonical indentation, spacing around operators, and clean block brackets:

```bash
# Format in place
sk format main.sk

# Format entire directory
sk format src/
```

---

## Static Syntax Verification (`sk check`)

Quickly parse and validate syntax without executing code:

```bash
sk check app.sk
```
Output:
```
Syntax OK: app.sk
```
