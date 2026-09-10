# Sikhar Bytecode Compiler & Virtual Machine (v0.3.0)

Sikhar `v0.3.0` introduces a high-performance **Bytecode Compiler**, a stack-based **Virtual Machine (VM)**, compiled binary serialization (`.skc`), and a bytecode disassembler (`sk dis`).

---

## 🏗️ Architecture Overview

```
Sikhar Source (.sk)
       │
       ▼
   Lexer & Parser
       │
       ▼
    Typed AST
   ┌───┴───────────────────────────────┐
   ▼                                   ▼
AST Interpreter (v0.1 - v0.2)     Bytecode Compiler (v0.3)
(Educational, tree-walking)            │
                                       ▼
                                Bytecode Chunk
                               ┌───────┴───────────────────────┐
                               ▼                               ▼
                      Bytecode Serializer                 Sikhar VM
                         (.skc binary)               (Stack execution)
                               │                               │
                               └───────────────────────────────┘
```

---

## ⚡ Key Features

1. **Stack-Based Execution**:
   Instructions operate on an evaluation value stack (`push`, `pop`, `peek`) with activation frames (`CallFrame`) tracking local variable slots and instruction pointers (`ip`).

2. **Dual-Engine Execution**:
   - `sk run script.sk` runs via the AST interpreter by default.
   - `sk run --vm script.sk` compiles in memory and runs directly on the high-performance VM.
   - `sk run script.skc` automatically loads and executes the compiled binary on the VM.

3. **Compiled Binary Format (`.skc`)**:
   Compiles Sikhar source into a portable binary format with magic header `b"SKC\x01"`, embedded version tag, constant pool, bytecode instruction stream, and source line-to-column debug tables.

4. **Built-in Disassembler**:
   Inspect human-readable instruction listings with line numbers, opcodes, jump targets, and constant pool references using `sk dis`.

---

## 🕹️ CLI Usage

### 1. Compile Source to Bytecode (`sk compile`)

```bash
# Compiles hello.sk to hello.skc
sk compile hello.sk

# Specify custom output path
sk compile src/main.sk -o dist/main.skc
```

### 2. Execute Bytecode or Run on VM (`sk run`)

```bash
# Run compiled bytecode binary
sk run hello.skc

# Run .sk source directly on VM
sk run --vm hello.sk
```

### 3. Disassemble to IR (`sk dis`)

```bash
# Disassemble source code
sk dis hello.sk

# Disassemble compiled binary
sk dis hello.skc
```

Example Disassembly Output:
```text
== Bytecode Disassembly: hello.sk (45 bytes) ==
0000    1  OP_CONSTANT             0 ('Namaste, Sansar!')
0003    |  OP_DEFINE_GLOBAL        1 ('sandesh')
0006    2  OP_GET_GLOBAL           1 ('sandesh')
0009    |  OP_PRINT             count=1
0012    3  OP_CONSTANT             2 (10)
0015    |  OP_DEFINE_GLOBAL        3 ('x')
0018    4  OP_GET_GLOBAL           3 ('x')
0021    |  OP_PRINT             count=1
0024    5  OP_GET_GLOBAL           3 ('x')
0027    |  OP_CONSTANT             4 (5)
0030    |  OP_GREATER          
0031    |  OP_JUMP_IF_FALSE     +9 -> 0043
0034    6  OP_CONSTANT             5 ('Thulo')
0037    |  OP_PRINT             count=1
0040    5  OP_JUMP              +0 -> 0043
0043    1  OP_NIL              
0044    |  OP_RETURN           
```

---

## 📋 Instruction Set Architecture (ISA)

| OpCode | Operand | Description |
| :--- | :--- | :--- |
| `OP_CONSTANT` | `uint16 const_idx` | Push constant from constant pool |
| `OP_NIL` | — | Push `khali` (`None`) |
| `OP_TRUE` / `OP_FALSE` | — | Push `sacho` / `jutho` |
| `OP_POP` / `OP_DUP` | — | Pop top of stack / duplicate top of stack |
| `OP_ADD` / `OP_SUBTRACT` | — | Binary addition/concatenation / subtraction |
| `OP_MULTIPLY` / `OP_DIVIDE` / `OP_MODULO` | — | Multiplication / division / modulo |
| `OP_NEGATE` / `OP_NOT` | — | Unary minus / logical inversion |
| `OP_EQUAL` / `OP_NOT_EQUAL` | — | Equality comparisons (`==`, `!=`) |
| `OP_GREATER` / `OP_GREATER_EQUAL` | — | Relational comparisons (`>`, `>=`) |
| `OP_LESS` / `OP_LESS_EQUAL` | — | Relational comparisons (`<`, `<=`) |
| `OP_DEFINE_GLOBAL` | `uint16 name_idx` | Define mutable global variable |
| `OP_DEFINE_CONST` | `uint16 name_idx` | Define immutable constant (`sthayi`) |
| `OP_GET_GLOBAL` / `OP_SET_GLOBAL` | `uint16 name_idx` | Read / write global variable |
| `OP_GET_LOCAL` / `OP_SET_LOCAL` | `uint16 slot` | Read / write fast stack slot |
| `OP_JUMP` | `uint16 offset` | Unconditional forward jump |
| `OP_JUMP_IF_FALSE` | `uint16 offset` | Jump forward if top of stack is falsy |
| `OP_LOOP` | `uint16 offset` | Unconditional backward jump to loop header |
| `OP_GET_ITER` / `OP_FOR_ITER` | `uint16 offset` | Setup iterator / advance iterator in `ko_lagi` |
| `OP_BUILD_LIST` | `uint16 count` | Build list from `count` stack elements |
| `OP_BUILD_MAP` | `uint16 pair_count` | Build map from `2 * pair_count` stack elements |
| `OP_INDEX_GET` / `OP_INDEX_SET` | — | Index access / index mutation (`target[idx]`) |
| `OP_GET_MEMBER` / `OP_SET_MEMBER` | `uint16 name_idx` | Property / module member access |
| `OP_MAKE_FUNCTION` | `uint16 func_idx` | Create function object bound to module globals |
| `OP_CALL` | `uint16 arity` | Call function with argument count |
| `OP_RETURN` | — | Return from current CallFrame |
| `OP_IMPORT` | `uint16 path_idx, uint8 is_std` | Import module or std package |
| `OP_EXPORT` | `uint16 name_idx` | Export symbol from module (`pathaau`) |
| `OP_PRINT` | `uint16 count` | Native `dekha` output formatting |
| `OP_FORMAT_STRING` | `uint16 count` | String interpolation concatenation |
| `OP_ASSERT` | `uint16 has_msg` | In-language assertion verification (`jaach`) |
| `OP_PUSH_TRY` / `OP_POP_TRY` | `uint16 offset` | Exception handler registration / deregistration |
| `OP_THROW` | — | Raise user exception (`fal`) |
