# Operators in Sikhar

Sikhar provides arithmetic, comparison, logical, and assignment operators with standard mathematical precedence.

## Arithmetic Operators

| Operator | Operation | Example | Result |
| :--- | :--- | :--- | :--- |
| `+` | Addition / Concatenation | `10 + 20` | `30` |
| `+` | String concatenation | `"Hi " + "there"` | `"Hi there"` |
| `+` | List concatenation | `[1] + [2]` | `[1, 2]` |
| `-` | Subtraction | `50 - 15` | `35` |
| `*` | Multiplication | `6 * 7` | `42` |
| `*` | String repetition | `"ha" * 3` | `"hahaha"` |
| `/` | Division | `40 / 4` | `10` |
| `%` | Modulo | `17 % 5` | `2` |

Dividing or taking modulo by zero raises `DivisionByZeroError`.

## Comparison Operators

| Operator | Description | Example |
| :--- | :--- | :--- |
| `==` | Equal | `x == 10` |
| `!=` | Not equal | `x != 5` |
| `<` | Less than | `x < 20` |
| `<=` | Less than or equal | `x <= 10` |
| `>` | Greater than | `x > 0` |
| `>=` | Greater than or equal | `x >= 10` |

Comparisons evaluate to `sacho` or `jutho`.

## Logical Operators

| Operator | Description | Short-circuiting |
| :--- | :--- | :--- |
| `and` | Logical AND | Returns right operand if left is truthy |
| `or` | Logical OR | Returns left operand if truthy, else right |
| `not` | Logical NOT | Inverts truthiness (`not sacho` -> `jutho`) |

### Example

```sk
rakha authenticated = sacho
rakha has_role = sacho

yadi authenticated and has_role {
    dekha "Access granted"
}
```

## Operator Precedence (Highest to Lowest)

1. Primary (`()`, `[]`, `{}`)
2. Postfix (Calls `()`, Indexing `[]`)
3. Unary (`not`, `-`)
4. Factor (`*`, `/`, `%`)
5. Term (`+`, `-`)
6. Comparison (`<`, `<=`, `>`, `>=`)
7. Equality (`==`, `!=`)
8. Logical AND (`and`)
9. Logical OR (`or`)
10. Assignment (`=`, `badla`)
