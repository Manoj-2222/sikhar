# Functions in Sikhar

Functions are declared with `kaam` and return values using `farka`.

## Declaration & Calling

```sk
kaam jod(a, b) {
    farka a + b
}

rakha result = jod(10, 20)
dekha result # 30
```

If a function completes without executing a `farka` statement, it returns `khali` (null).

## Parameters & Local Scope

Functions create their own lexical scope. Variables defined within a function do not leak into outer scopes:

```sk
rakha title = "Global"

kaam demo() {
    rakha title = "Local"
    farka title
}

dekha demo() # Local
dekha title  # Global
```

## Recursion

Sikhar fully supports recursive function definitions:

### Factorial

```sk
kaam factorial(n) {
    yadi n <= 1 {
        farka 1
    }
    farka n * factorial(n - 1)
}

dekha factorial(5) # 120
```

### Fibonacci

```sk
kaam fib(n) {
    yadi n <= 0 {
        farka 0
    }
    yadi n == 1 {
        farka 1
    }
    farka fib(n - 1) + fib(n - 2)
}

dekha fib(7) # 13
```

## Functions as First-Class Values

Functions are values and can be assigned to variables, stored in collections, or passed as arguments:

```sk
kaam guna(a, b) {
    farka a * b
}

rakha op = guna
dekha op(4, 5) # 20
```
