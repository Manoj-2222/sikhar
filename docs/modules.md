# Modules (Roadmap & Design)

*Status: Reserved in v0.1.0; Scheduled for v0.2.0.*

## Keywords

* `aayaat`: Import module or symbol
* `pathaau`: Export module or symbol

## Planned Syntax

### Importing Standard Modules

```sk
aayaat std.math
aayaat std.io

rakha root = std.math.sqrt(16)
```

### Importing Selective Symbols

```sk
aayaat { sqrt, pow } bata std.math
```

### Exporting from Local Files

In `math_utils.sk`:

```sk
pathaau kaam jod(a, b) {
    farka a + b
}

pathaau sthayi PI = 3.14159
```

In `main.sk`:

```sk
aayaat "./math_utils.sk"
dekha math_utils.jod(10, 20)
```

## Security Design

The module loader will isolate file system execution and prevent unauthorized external script evaluation without explicit relative path or dependency declaration.
