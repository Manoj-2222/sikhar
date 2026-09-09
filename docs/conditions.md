# Conditions in Sikhar

Conditional branching in Sikhar is expressed with `yadi` (if), `athawa` (else-if), and `natra` (else).

## Basic `yadi` Statement

```sk
rakha age = 20

yadi age >= 18 {
    dekha "Adult"
}
```

The condition expression does not require enclosing parentheses, and the block body must be enclosed in `{ ... }`.

## `yadi` with `natra`

```sk
rakha score = 45

yadi score >= 50 {
    dekha "Passed"
} natra {
    dekha "Failed"
}
```

## Multi-Branch: `yadi` - `athawa` - `natra`

Use `athawa` for intermediate alternative branches:

```sk
rakha marks = 82

yadi marks >= 90 {
    dekha "Grade A"
} athawa marks >= 80 {
    dekha "Grade B"
} athawa marks >= 70 {
    dekha "Grade C"
} natra {
    dekha "Grade F"
}
```

## Nested Conditions

Conditions can be nested inside blocks:

```sk
rakha registered = sacho
rakha verified = jutho

yadi registered {
    yadi verified {
        dekha "Account active"
    } natra {
        dekha "Please verify your email"
    }
} natra {
    dekha "Please register first"
}
```
