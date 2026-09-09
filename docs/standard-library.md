# Standard Library Foundation

Sikhar provides an initial set of built-in functions in v0.1.0, establishing the foundation for a structured namespace system (`std.*`) in v0.2.0.

## Current Built-in Functions

### Input / Output

* `dekha(*args)`: Prints arguments to standard output separated by space.
* `sodha(prompt="")`: Prompts the user and reads a line from standard input.

```sk
rakha naam = sodha("Tapainko naam k ho? ")
dekha "Namaste, " + naam
```

### Collection & Sequence Operations

* `lamba(collection)`: Returns length of string, list, or map.
* `jod_suchi(list, item)`: Appends `item` to `list` and returns it.
* `hatau_suchi(list, index)`: Removes and returns element at `index`.
* `khoj_suchi(list, item)`: Returns zero-based index or `-1` if not found.

### Type & Inspection

* `prakaar(value)`: Returns type name (`"number"`, `"decimal"`, `"text"`, `"boolean"`, `"list"`, `"map"`, `"khali"`, `"kaam"`).

### Math Helpers

* `thulo(a, b, ...)`: Returns the maximum of provided numbers.
* `sano(a, b, ...)`: Returns the minimum of provided numbers.
* `ghat(n)`: Returns absolute value of a number.

---

## Future Modular Standard Library (`std.*`)

Planned for v0.2.0:

* `std.io`: Advanced stream reader/writer, formatting.
* `std.math`: Trigonometry, logarithms, statistics.
* `std.text`: Regular expressions, string transforms, encoding.
* `std.list`: Sorting, map/filter/reduce, slicing.
* `std.map`: Keys, values, merging, filtering.
* `std.time`: Timestamps, timers, formatting dates.
* `std.file`: Reading and writing files with `khola`, `padh`, `lekh`, `banda`.
* `std.system`: Environment variables, OS arguments, process execution.
