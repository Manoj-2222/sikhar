# Sikhar Syntax Guide

Sikhar syntax balances minimalism, readability, and modern expression.

## Comments

Single-line comments begin with `#`. The parser ignores everything following `#` up to the end of the line:

```sk
# This is a comment in Sikhar
rakha version = 1 # Inline comment
```

## Statements & Whitespace

Statements in Sikhar are separated by newlines. Semicolons (`;`) are optional.

```sk
rakha a = 1
rakha b = 2
```

## Blocks & Scoping

Code blocks are delineated by curly braces `{ ... }`:

```sk
yadi a < b {
    dekha "a is smaller"
}
```

Blocks introduce local scopes. Variables defined within a block are isolated to that block and its nested children.

## Identifiers

Identifiers begin with an alphabetic letter, an underscore `_`, or supported unicode characters, followed by alphanumeric characters or underscores:

```sk
rakha age = 20
rakha user_name = "Manoj"
rakha _private_key = "1234"
```

## Keywords Overview

| Keyword | Meaning / Role |
| :--- | :--- |
| `rakha` | Variable declaration |
| `badla` | Variable mutation |
| `sthayi` | Constant declaration |
| `khali` | Null value |
| `sacho` | Boolean true |
| `jutho` | Boolean false |
| `dekha` | Standard output / print |
| `sodha` | Standard input |
| `yadi` | If branch |
| `athawa` | Else-if branch |
| `natra` | Else branch |
| `jaba` | While loop |
| `ko_lagi` | For collection loop |
| `ma` | In (collection membership) |
| `rok` | Break loop |
| `jaari` | Continue loop |
| `kaam` | Function declaration |
| `farka` | Return statement |
| `koshish` | Try block |
| `samata` | Catch block |
| `fal` | Throw error |
| `aayaat` | Import module or file |
| `pathaau` | Export symbol from module |
| `jaach` | In-language test assertion |

## String Interpolation

Strings enclosed in quotes support dynamic interpolation using `{expression}` syntax:

```sk
rakha naam = "Manoj"
dekha "Namaste, {naam}!"
dekha "Calculation: {10 * 20}"
```

To display curly braces literally without evaluating them, escape them using `\{` and `\}`:

```sk
dekha "Literal braces: \{not_evaluated\}"
```

