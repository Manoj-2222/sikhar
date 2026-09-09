# Introduction to Sikhar

**Sikhar** is a modern, simple, expressive, and beginner-friendly programming language featuring Nepali-inspired keywords and clean grammar.

Designed from the ground up to empower both beginners and experienced developers, Sikhar avoids artificial complexity while maintaining rigorous language engineering standards.

## Core Identity

* **Name**: Sikhar
* **Version**: v0.1.0
* **Source Extension**: `.sk`
* **CLI Command**: `sk`
* **Current Model**: Pure AST Tree-Walking Interpreter in Python
* **Future Execution Model**: Bytecode Compiler & Virtual Machine

## Language Philosophy

1. **Simple and Intuitive**: Clean syntax without unnecessary boilerplate or punctuation noise.
2. **Nepali-Inspired Identity**: Meaningful keywords such as `rakha` (variable), `sthayi` (constant), `badla` (change/mutate), `dekha` (output), `yadi` (if), and `kaam` (function).
3. **Strict and Safe by Default**: Variables must be explicitly declared (`rakha`), mutations are intentional (`badla`), and constants (`sthayi`) cannot be overwritten.
4. **Developer-Friendly Diagnostics**: Clear, pinpoint error messages showing the exact file, line, and column with ASCII pointers (`^`). Sikhar never exposes raw Python stack traces.
5. **Practical Ecosystem**: Designed for long-term scalability across CLI tools, APIs, web applications, and embedded platforms.

## First Program

Create a file named `hello.sk`:

```sk
rakha sandesh = "Namaste, Sansar!"
dekha sandesh

rakha x = 10
dekha x

yadi x > 5 {
    dekha "Thulo"
}
```

Run it using the Sikhar CLI:

```bash
sk run hello.sk
```

Output:

```text
Namaste, Sansar!
10
Thulo
```
