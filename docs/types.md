# Data Types in Sikhar

Sikhar v0.1.0 supports the following core data types:

| Type Name | Sikhar Value / Literal | Description |
| :--- | :--- | :--- |
| `number` | `10`, `-42`, `0` | 64-bit integer values |
| `decimal` | `3.14159`, `99.50` | Floating-point decimal values |
| `text` | `"Hello, world!"` | UTF-8 encoded string sequence |
| `boolean` | `sacho`, `jutho` | True / False boolean flags |
| `null` | `khali` | Represents absence of a value |
| `list` | `[1, 2, 3]` | Ordered sequence of values |
| `map` | `{"key": "value"}` | Key-value associative dictionary |
| `kaam` | `<kaam name>` | First-class callable function |

## Examples

```sk
rakha age = 20                 # number
rakha price = 99.50            # decimal
rakha greeting = "Namaste"     # text
rakha is_active = sacho        # boolean
rakha is_admin = jutho         # boolean
rakha empty_val = khali        # null
rakha items = ["apple", 42]    # list
rakha profile = {"id": 1}      # map
```

## Type Inspection: `prakaar()`

You can inspect the runtime type of any value using the built-in `prakaar` function:

```sk
dekha prakaar(10)          # number
dekha prakaar(3.14)        # decimal
dekha prakaar("Sikhar")    # text
dekha prakaar(sacho)       # boolean
dekha prakaar([1, 2])      # list
dekha prakaar({"a": 1})    # map
dekha prakaar(khali)       # khali
```

## Truthiness Rules

The following values evaluate to falsy (`jutho`):
* `khali` (null)
* `jutho` (false)
* `0` and `0.0` (zero)
* `""` (empty string)
* `[]` (empty list)
* `{}` (empty map)

All other values evaluate to truthy (`sacho`).
