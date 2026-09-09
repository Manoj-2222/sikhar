# Modules in Sikhar (v0.2.0)

Sikhar v0.2.0 introduces a modular architecture enabling code reuse across files and access to the structured standard library (`std.*`).

## Keywords

* `aayaat`: Import a module or file
* `pathaau`: Export a variable, constant, or function from a module

---

## 1. Exporting Symbols (`pathaau`)

In Sikhar, variables, constants, and functions marked with `pathaau` are publicly exported by that file:

```sk
# math_utils.sk
pathaau sthayi PI = 3.14159

pathaau kaam barga(n) {
    farka n * n
}

pathaau kaam ghan(n) {
    farka n * n * n
}
```

Symbols not marked with `pathaau` remain private to the module.

---

## 2. Importing Modules (`aayaat`)

### Importing Local Files

You can import local `.sk` files using relative file paths:

```sk
# main.sk
aayaat "math_utils.sk"

dekha math_utils.PI
dekha math_utils.barga(5)
```

You can also bind the imported module to a custom identifier:

```sk
rakha mu = aayaat "math_utils.sk"
dekha mu.ghan(3)
```

### Importing Standard Library Modules

Sikhar provides structured namespaces under `std`:

```sk
aayaat std.math
aayaat std.text

dekha math.sqrt(144)
dekha text.thulo("sikhar")
```

Or with explicit assignment:

```sk
rakha m = aayaat std.math
dekha m.pow(2, 8)
```

---

## 3. Module Caching and Isolation

* **Isolated Execution**: Each module runs in its own isolated top-level environment. Global variables from the importer do not leak into the imported module.
* **Module Caching**: Modules are parsed and evaluated once per session. Subsequent `aayaat` calls for the same file return the cached module instance, preventing redundant execution and circular dependency loops.
