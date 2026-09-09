# Collections in Sikhar

Sikhar provides two fundamental collection types: **Lists** (ordered sequences) and **Maps** (key-value associations).

## Lists

Lists are declared with square brackets `[ ... ]`:

```sk
rakha numbers = [10, 20, 30]
rakha mixed = [1, "two", sacho, khali]
```

### Indexing

Lists use zero-based integer indexing:

```sk
dekha numbers[0] # 10
dekha numbers[2] # 30
```

Accessing an out-of-range index raises `IndexError`.

### Modifying Elements

Update elements in place using `badla`:

```sk
badla numbers[1] = 99
dekha numbers # [10, 99, 30]
```

### Built-in List Operations

* `lamba(lst)`: Length of the list.
* `jod_suchi(lst, item)`: Appends an item to the list.
* `hatau_suchi(lst, index)`: Removes and returns the item at index.
* `khoj_suchi(lst, item)`: Returns the first index of item, or `-1` if not found.

Example:

```sk
rakha scores = [80, 90]
jod_suchi(scores, 100)
dekha scores # [80, 90, 100]

rakha first = hatau_suchi(scores, 0)
dekha first  # 80
dekha scores # [90, 100]
```

## Maps

Maps are associative dictionaries mapping string/number keys to arbitrary values:

```sk
rakha user = {
    "name": "Manoj",
    "age": 20,
    "role": "Engineer"
}
```

### Accessing & Modifying Keys

```sk
dekha user["name"] # Manoj

badla user["age"] = 21
badla user["country"] = "Nepal"
```

Accessing a non-existent key raises `KeyError`.

### Map Iteration

Iterating over a map visits all its keys:

```sk
ko_lagi k ma user {
    dekha k + " => " + user[k]
}
```
