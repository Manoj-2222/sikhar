# Variables and Constants in Sikhar

Sikhar makes state management intentional by separating declaration, mutation, and constants.

## Variable Declaration: `rakha`

Variables are declared using the `rakha` keyword:

```sk
rakha naam = "Manoj"
rakha age = 20
rakha active = sacho
```

Variables declared with `rakha` are mutable.

### Uninitialized Variables

Variables can be declared without an immediate initial value (defaults to `khali`):

```sk
rakha buffer
```

### Type Annotations

Sikhar supports optional type annotations in the grammar for future static checking:

```sk
rakha age: number = 20
rakha rate: decimal = 14.5
rakha title: text = "Compiler"
```

## Mutation: `badla`

To modify the value of an existing variable, use `badla`:

```sk
rakha score = 50
badla score = 75
```

Direct assignment `score = 75` is also accepted, but `badla` clearly communicates intent.

Attempting to assign to an undeclared variable produces an `UndefinedVariable` error:

```sk
badla unknown = 10
# Sikhar Error: Type: UndefinedVariable, Message: Variable 'unknown' is not defined
```

## Constants: `sthayi`

Constants represent immutable bindings declared with `sthayi`:

```sk
sthayi pi = 3.14159
sthayi base_url = "https://api.sikhar.org"
```

Attempting to mutate a constant produces a `ConstantMutation` error:

```sk
sthayi max_connections = 100
badla max_connections = 200
```

Output:

```text
Sikhar Error

Type: ConstantMutation
Message: Cannot modify constant 'max_connections' declared with 'sthayi'

File: main.sk
Line: 2
Column: 1

   2 | badla max_connections = 200
       ^
```
