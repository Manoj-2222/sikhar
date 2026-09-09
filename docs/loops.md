# Loops and Iteration in Sikhar

Sikhar supports `jaba` (while loop) for condition-driven iteration and `ko_lagi ... ma ...` (for loop) for collection iteration, controlled by `rok` (break) and `jaari` (continue).

## While Loop: `jaba`

The `jaba` loop runs as long as the condition evaluates to truthy:

```sk
rakha i = 1

jaba i <= 5 {
    dekha i
    badla i = i + 1
}
```

Output:
```text
1
2
3
4
5
```

## For Loop: `ko_lagi ... ma ...`

Iterate over collections (lists, maps, strings) using `ko_lagi <var> ma <collection>`:

### Over a List

```sk
rakha cities = ["Kathmandu", "Pokhara", "Lalitpur"]

ko_lagi city ma cities {
    dekha city
}
```

### Over a Map

Iterating over a map visits each key:

```sk
rakha config = {"port": 8080, "host": "localhost"}

ko_lagi key ma config {
    dekha key + " = " + config[key]
}
```

### Over a String

Iterating over a string yields each character:

```sk
ko_lagi char ma "Sikhar" {
    dekha char
}
```

## Loop Control: `rok` (break) and `jaari` (continue)

* `rok` immediately terminates the nearest enclosing loop.
* `jaari` skips the rest of the current iteration and begins the next.

```sk
rakha numbers = [10, 20, 30, 40, 50]

ko_lagi x ma numbers {
    yadi x == 20 {
        jaari # Skip 20
    }
    yadi x == 40 {
        rok   # Stop at 40
    }
    dekha x
}
```

Output:
```text
10
30
```
