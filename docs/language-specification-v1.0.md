# Sikhar Language Specification — v1.0.0 (Frozen Standard)

**Status:** Official Frozen Standard  
**Version:** 1.0.0  
**Compatibility:** Backward-compatible across all 1.x releases  

---

## 1. Introduction & Conformance

Sikhar is a dynamically-typed, general-purpose programming language featuring readable, expressive Nepali-inspired keywords, first-class functions and closures, native collections, robust error handling, a stack-based Bytecode Virtual Machine, and an integrated standard library for web development and system scripting with zero third-party dependencies.

This document defines the formal language specification for Sikhar v1.0.0. Conforming implementations must adhere to the syntax, semantics, standard library interfaces, and bytecode behavior detailed herein.

---

## 2. Lexical Structure

### 2.1 Character Encoding & Source Text
- Source files are encoded in **UTF-8**.
- Line terminators: `\n` (LF) or `\r\n` (CRLF).
- Indentation is whitespace-agnostic; statement blocks are explicitly delimited by braces `{ ... }`.

### 2.2 Comments
- **Single-line comments**: Begin with `#` and extend to the end of the line.
```sk
# This is a comment in Sikhar
```

### 2.3 Identifiers
An identifier begins with an ASCII letter (`a`-`z`, `A`-`Z`) or an underscore `_`, followed by any sequence of alphanumeric characters or underscores. Identifiers are case-sensitive.

### 2.4 Keywords
The following tokens are reserved keywords:

| English Equivalent | Sikhar Keyword | Description |
| :--- | :--- | :--- |
| `let` / `var` | `rakha` | Mutable variable declaration |
| `const` | `sthayi` | Immutable constant declaration |
| `set` / `mutate` | `badla` | Variable or index reassignment |
| `if` | `yadi` | Conditional branch |
| `elif` / `else if` | `athawa` | Alternative conditional branch |
| `else` | `natra` | Fallback branch |
| `while` | `jaba` | Conditional loop |
| `for` | `ko_lagi` | For-in loop initiator |
| `in` | `ma` | Collection traversal connector |
| `break` | `rok` | Terminate loop execution |
| `continue` | `jaari` | Advance to next loop iteration |
| `function` | `kaam` | Function declaration or lambda |
| `return` | `farka` | Return value from function |
| `try` | `koshish` | Exception handling block |
| `catch` | `samata` | Exception interception block |
| `throw` | `fal` | Raise an exception |
| `import` | `aayaat` | Import module or namespace |
| `export` | `pathaau` | Export declaration or symbol |
| `assert` | `jaach` | In-language test assertion |
| `print` | `dekha` | Standard output statement |
| `true` | `sacho` | Boolean true literal |
| `false` | `jutho` | Boolean false literal |
| `null` | `khali` | Null value literal |
| `and` | `ra` | Logical conjunction |
| `or` | `wa` | Logical disjunction |
| `not` | `hoina` | Logical negation |

### 2.5 Literals
- **Integers**: `42`, `-10`, `0`
- **Decimals**: `3.14159`, `0.005`, `-1.5`
- **Strings**:
  - Double quotes `"..."`: Evaluates string interpolation `{expr}` unless escaped `\{expr\}`.
  - Single quotes `'...'`: Raw strings with literal evaluation (ideal for JSON, regex, SQL).
- **Booleans**: `sacho` (true), `jutho` (false)
- **Null**: `khali` (represents absence of value)

### 2.6 Operators

| Type | Operators | Precedence (High to Low) |
| :--- | :--- | :--- |
| Primary | Member access `.`, Indexing `[]`, Call `()` | 8 |
| Unary | `-`, `hoina`, `not`, `!` | 7 |
| Multiplicative | `*`, `/`, `%` | 6 |
| Additive | `+`, `-` | 5 |
| Relational | `<`, `<=`, `>`, `>=` | 4 |
| Equality | `==`, `!=` | 3 |
| Logical AND | `ra`, `and`, `&&` | 2 |
| Logical OR | `wa`, `or`, `\|\|` | 1 |

---

## 3. Formal Grammar (EBNF)

```ebnf
Program         ::= Statement* EOF ;

Statement       ::= VarDecl
                  | ConstDecl
                  | Assignment
                  | IfStmt
                  | WhileStmt
                  | ForStmt
                  | FunctionDecl
                  | ReturnStmt
                  | TryStmt
                  | ThrowStmt
                  | ImportStmt
                  | ExportStmt
                  | AssertStmt
                  | DekhaStmt
                  | ExprStmt ;

Block           ::= "{" Statement* "}" ;

VarDecl         ::= "rakha" IDENTIFIER ("=" Expression)? ;
ConstDecl       ::= "sthayi" IDENTIFIER "=" Expression ;
Assignment      ::= "badla" Target "=" Expression ;
Target          ::= IDENTIFIER ( "[" Expression "]" | "." IDENTIFIER )* ;

IfStmt          ::= "yadi" Expression Block
                    ( "athawa" Expression Block )*
                    ( "natra" Block )? ;

WhileStmt       ::= "jaba" Expression Block ;
ForStmt         ::= "ko_lagi" IDENTIFIER "ma" Expression Block ;

FunctionDecl    ::= "kaam" IDENTIFIER "(" ParameterList? ")" Block ;
ParameterList   ::= IDENTIFIER ( "," IDENTIFIER )* ;

ReturnStmt      ::= "farka" Expression? ;
TryStmt         ::= "koshish" Block "samata" IDENTIFIER? Block ;
ThrowStmt       ::= "fal" Expression ;
AssertStmt      ::= "jaach" Expression ( "," Expression )? ;
DekhaStmt       ::= "dekha" Expression ;

Expression      ::= LogicalOr ;
LogicalOr       ::= LogicalAnd ( ( "wa" | "or" | "||" ) LogicalAnd )* ;
LogicalAnd      ::= Equality ( ( "ra" | "and" | "&&" ) Equality )* ;
Equality        ::= Relational ( ( "==" | "!=" ) Relational )* ;
Relational      ::= Additive ( ( "<" | "<=" | ">" | ">=" ) Additive )* ;
Additive        ::= Multiplicative ( ( "+" | "-" ) Multiplicative )* ;
Multiplicative  ::= Unary ( ( "*" | "/" | "%" ) Unary )* ;
Unary           ::= ( "-" | "hoina" | "not" | "!" ) Unary | Postfix ;
Postfix         ::= Primary ( "(" ArgumentList? ")" | "[" Expression "]" | "." IDENTIFIER )* ;
ArgumentList    ::= Expression ( "," Expression )* ;

Primary         ::= NUMBER
                  | DECIMAL
                  | STRING
                  | "sacho" | "jutho"
                  | "khali"
                  | IDENTIFIER
                  | ListLiteral
                  | MapLiteral
                  | FunctionExpr
                  | "(" Expression ")" ;

ListLiteral     ::= "[" ( Expression ( "," Expression )* )? "]" ;
MapLiteral      ::= "{" ( KeyValue ( "," KeyValue )* )? "}" ;
KeyValue        ::= ( STRING | IDENTIFIER ) ":" Expression ;
FunctionExpr    ::= "kaam" IDENTIFIER? "(" ParameterList? ")" Block ;
```

---

## 4. Type System & Value Semantics

Sikhar values belong to one of the following canonical types:

1. **`number`**: Signed 64-bit integer values.
2. **`decimal`**: Double-precision IEEE 754 floating-point values.
3. **`text`**: Immutable sequence of UTF-8 characters.
4. **`boolean`**: `sacho` (true) or `jutho` (false). Truthiness: `jutho` and `khali` are falsy; all other values (including `0`, `""`, `[]`, `{}`) are truthy.
5. **`null`**: The singleton `khali` representing nil/none.
6. **`list`**: Dynamically-sized, ordered array of arbitrary values.
7. **`map`**: Hash-mapped key-value dictionary. Keys are typically text strings.
8. **`function`**: First-class callable closure capturing its lexical environment.
9. **`module`**: Namespace container exporting functions, constants, and objects.

---

## 5. Bytecode Virtual Machine Architecture

Conforming implementations provide both an AST Tree-Walking interpreter and a high-performance stack-based Virtual Machine:

### 5.1 Bytecode Container (`Chunk`)
- Sequential 8-bit instruction stream (`code`).
- Dedicated constant pool (`constants`) storing numbers, strings, and `BytecodeFunction` objects.
- Source line-column debug map (`lines`).

### 5.2 Instruction Set (Selected OpCodes)

| OpCode | Hex / Val | Description |
| :--- | :--- | :--- |
| `OP_CONSTANT` | 1 | Push constant from constant pool onto stack |
| `OP_NIL` | 2 | Push `khali` onto stack |
| `OP_TRUE` | 3 | Push `sacho` onto stack |
| `OP_FALSE` | 4 | Push `jutho` onto stack |
| `OP_POP` | 5 | Pop top value from stack |
| `OP_ADD` | 15 | Binary addition or string concatenation |
| `OP_SUBTRACT` | 16 | Binary subtraction |
| `OP_MULTIPLY` | 17 | Binary multiplication or string repetition |
| `OP_DIVIDE` | 18 | Division (integer division if exact, float otherwise) |
| `OP_MODULO` | 19 | Modulo arithmetic |
| `OP_EQUAL` | 25 | Equality comparison |
| `OP_GET_LOCAL` | 39 | Load local from call frame base slot |
| `OP_SET_LOCAL` | 40 | Store value to local slot |
| `OP_GET_GLOBAL`| 37 | Load variable from module/global environment |
| `OP_SET_GLOBAL`| 38 | Mutate global variable |
| `OP_JUMP` | 45 | Unconditional 16-bit forward jump |
| `OP_JUMP_IF_FALSE` | 46 | Jump forward if top of stack is falsy |
| `OP_LOOP` | 47 | Unconditional 16-bit backward jump |
| `OP_FOR_ITER` | 49 | Advance iterator or jump past loop body |
| `OP_MAKE_FUNCTION` | 65 | Instantiate `BytecodeFunction` with captured scope |
| `OP_CALL` | 66 | Invoke callable with N arguments |
| `OP_RETURN` | 67 | Return from active CallFrame |
| `OP_PUSH_TRY` | 86 | Push exception handler frame |
| `OP_POP_TRY` | 87 | Pop exception handler frame |
| `OP_THROW` | 88 | Raise exception unwinding call stack |

---

## 6. Standard Library Specifications

The Sikhar standard library (`std.*`) guarantees zero third-party dependencies and consistent behavior across all operating systems:

- **`std.math`**: `sqrt`, `pow`, `abs`, `ceil`, `floor`, `sin`, `cos`, `tan`, `pi`, `e`.
- **`std.text`**: `length`, `upper` (`thulo`), `lower` (`sano`), `trim`, `split`, `join`, `replace`, `contains`, `starts_with`, `ends_with`.
- **`std.list`**: `push` (`thap`), `pop` (`nikala`), `insert`, `remove`, `sort`, `reverse`, `slice`, `contains`, `sum`, `min`, `max`.
- **`std.map`**: `keys`, `values`, `items`, `has`, `get`, `remove` (`hatau`), `merge`.
- **`std.time`**: `now`, `sleep` (`suta`), `timestamp`.
- **`std.file`**: `read` (`padh`), `write` (`lekh`), `append` (`thap`), `exists` (`chha`), `remove` (`hatau`).
- **`std.json`**: `parse` (`padh`, `chin`), `stringify` (`rupantar`, `lekh`), `valid` (`sacho`).
- **`std.http`**: `get` (`lyaau`), `post` (`pathaau`), `put`, `delete` (`hatau`), `patch`, `request`, `server`.
- **`std.web`**: `app()`, route registration (`get`, `post`, `put`, `delete`, `all`), dynamic path params (`:id`), middleware (`use`), static asset serving (`static`), in-memory dispatch (`handle`), live server (`listen`, `start`, `stop`).
- **`std.db`**: `connect` (`joda`), query execution (`execute`, `chalaau`, `query`, `khoja`, `query_one`), transactions (`commit`, `rollback`, `close`, `banda`).
- **`std.crypto`**: `sha256` (`hashing`), `sha512`, `md5`, `hmac_sha256` (`gupta`), `base64_encode`, `base64_decode`, `random_bytes`, `random_token` (`chinno`).
- **`std.csv`**: `parse`, `stringify`, `read` (`padh`), `write` (`lekh`).
- **`std.regex`**: `match` (`milcha`), `find_all` (`khoja`), `replace` (`badla`), `split`.
- **`std.process`**: `exec` (`chalaau`), `env`, `set_env`, `args`, `cwd`.
- **`std.task`**: `spawn` (`suru`), `wait` (`parkha`), `sleep` (`suta`).

---

## 7. Official Tooling Standards

Conforming distributions provide the unified `sk` command-line interface:

- `sk run [--vm] <file>`: Run source (`.sk`) or binary bytecode (`.skc`).
- `sk build <file> [options]`: Compile and package into standalone binary archive (`.pyz` and companion `.bat`).
- `sk serve [file|dir] [options]`: Serve web applications or static directories over HTTP.
- `sk bench <file.sk> [--runs N]`: Benchmark program performance comparing AST vs VM.
- `sk compile <file.sk> [-o <file.skc>]`: Compile source to portable `.skc` bytecode.
- `sk dis <file>`: Disassemble source or bytecode into human-readable instructions.
- `sk format [file.sk]`: Canonical AST code formatter.
- `sk check <file.sk>`: Validate syntax and parser errors without execution.
- `sk init <project>`: Scaffold a new project structure.
- `sk add <package> [version]`: Add package dependency to `sikhar.toml`.
- `sk install`: Install project dependencies declared in `sikhar.toml`.
- `sk publish`: Package project into distributable archive.
- `sk lsp`: Launch JSON-RPC 2.0 Language Server on stdio.
- `sk test`: Run full automated test suite (Python + Native `.sk`).
- `sk repl`: Interactive Read-Eval-Print Loop.

- `sk version`: Print active version.
