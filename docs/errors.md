# Error Handling in Sikhar

Sikhar features a native error handling architecture that prevents raw implementation stack traces from leaking to end users while pinpointing errors clearly.

## Try / Catch: `koshish` and `samata`

Surround risky code in a `koshish` block and capture any error using `samata`:

```sk
koshish {
    rakha result = 10 / 0
    dekha result
} samata err {
    dekha "Caught an error: " + err
}
```

Output:
```text
Caught an error: Division by zero
```

The error identifier after `samata` is optional:

```sk
koshish {
    # risky code
} samata {
    dekha "Error occurred"
}
```

## Throwing Errors: `fal`

Raise custom errors using `fal`:

```sk
kaam check_age(age) {
    yadi age < 0 {
        fal "Age cannot be negative"
    }
    farka "Valid"
}

koshish {
    check_age(-5)
} samata message {
    dekha "Validation failed: " + message
}
```

## Sikhar Error Diagnostics

When an unhandled error terminates execution, Sikhar displays formatted diagnostic information with source pointers:

```text
Sikhar Error

Type: UndefinedVariable
Message: Variable 'xyz' is not defined

File: script.sk
Line: 4
Column: 8

   4 |     badla xyz = 10
     |           ^
```

### Standard Error Types

* `SyntaxError`: Lexer and parser syntax violations.
* `UndefinedVariable`: Accessing an undeclared identifier.
* `ConstantMutation`: Attempting to modify a `sthayi` constant.
* `TypeError`: Incompatible operand or argument types.
* `IndexError`: List or string index out of range.
* `KeyError`: Map key not found.
* `DivisionByZeroError`: Division or modulo by zero.
