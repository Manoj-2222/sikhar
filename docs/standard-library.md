# Sikhar Standard Library (v0.2.0)

Sikhar provides both high-performance built-in functions in the global scope and a modular standard library accessible via `aayaat std.<module>`.

---

## Global Built-in Functions

### Input / Output
* `dekha(*args)`: Prints arguments separated by space.
* `sodha(prompt="")`: Reads a line of input from standard input.

### File I/O Builtins
* `khola(path, mode="padh")`: Opens a file handle. Supported modes: `"padh"` (read), `"lekh"` (write), `"thap"` (append), `"r"`, `"w"`, `"a"`.
* `banda(handle)`: Closes an open file handle.
* `padh(handle_or_path)`: Reads all content from a file handle or file path.
* `lekh(handle, content)`: Writes content to an open file handle.

### Collection Operations
* `lamba(collection)`: Returns length of string, list, or map.
* `jod_suchi(list, item)`: Appends `item` to `list`.
* `hatau_suchi(list, index)`: Removes and returns element at index.
* `khoj_suchi(list, item)`: Finds index of item, or returns `-1`.

### Math Helpers
* `thulo(a, b, ...)`: Returns maximum.
* `sano(a, b, ...)`: Returns minimum.
* `ghat(n)`: Returns absolute value.

### Type Inspection
* `prakaar(value)`: Returns type name (`"number"`, `"decimal"`, `"text"`, `"boolean"`, `"list"`, `"map"`, `"khali"`, `"kaam"`).

---

## Structured Standard Library (`std.*`)

Import any module using `aayaat std.<module>`:

### 1. `std.math`
Mathematical operations and constants:
* `math.pi`: Mathematical constant $\pi$ (3.14159...)
* `math.e`: Euler's constant $e$ (2.71828...)
* `math.sqrt(x)` / `math.vargamul(x)`: Square root of $x$
* `math.pow(x, y)` / `math.ghaat(x, y)`: $x^y$
* `math.abs(x)`: Absolute value
* `math.sin(x)`, `math.cos(x)`, `math.tan(x)`: Trigonometric functions
* `math.floor(x)`, `math.ceil(x)`, `math.round(x, [decimals])`: Rounding helpers
* `math.log(x, [base])`: Natural logarithm or specified base

### 2. `std.text`
String manipulation utilities:
* `text.upper(s)` / `text.thulo(s)`: Convert string to uppercase
* `text.lower(s)` / `text.sano(s)`: Convert string to lowercase
* `text.trim(s)`: Strip leading and trailing whitespace
* `text.split(s, [delimiter])` / `text.tukra(s, [delimiter])`: Split string into list
* `text.join(list, delimiter)`: Join list of elements into string
* `text.replace(s, old, new)`: Replace occurrences of substring
* `text.contains(s, sub)`: Check if string contains substring
* `text.starts_with(s, prefix)`: Check if string begins with prefix
* `text.ends_with(s, suffix)`: Check if string ends with suffix

### 3. `std.list`
Functional and sequence operations:
* `list.sort(lst)` / `list.kram(lst)`: Returns sorted list
* `list.reverse(lst)` / `list.ulta(lst)`: Returns reversed list
* `list.slice(lst, start, [end])` / `list.tukra(lst, start, [end])`: Slices list
* `list.filter(lst, predicate_fn)`: Filters elements matching predicate
* `list.map(lst, transform_fn)`: Transforms elements using function
* `list.sum(lst)` / `list.jamma(lst)`: Sum of numeric elements
* `list.min(lst)`: Minimum element
* `list.max(lst)`: Maximum element
* `list.contains(lst, item)`: Check if item is in list

### 4. `std.map`
Dictionary and key-value operations:
* `map.keys(m)` / `map.kunji(m)`: Returns list of keys
* `map.values(m)` / `map.man(m)`: Returns list of values
* `map.entries(m)`: Returns list of `[key, value]` pairs
* `map.has(m, key)` / `map.cha(m, key)`: Checks if map contains key
* `map.merge(m1, m2)` / `map.misa(m1, m2)`: Merges two maps into a new map

### 5. `std.file`
Safe file operations:
* `file.read(path)` / `file.padh(path)`: Reads entire text file
* `file.write(path, content)` / `file.lekh(path, content)`: Writes string to file
* `file.append(path, content)` / `file.thap(path, content)`: Appends string to file
* `file.exists(path)` / `file.cha(path)`: Checks if file exists
* `file.remove(path)` / `file.hatau(path)`: Deletes file from filesystem

### 6. `std.time`
Timestamps and sleep:
* `time.now()` / `time.samaya()`: Current Unix timestamp in seconds
* `time.sleep(seconds)` / `time.suta(seconds)`: Pauses execution for duration
* `time.format([ts], [format])` / `time.dhacha([ts], [format])`: Formats timestamp

### 7. `std.system`
Operating system and environment inspection:
* `system.args()`: Command-line arguments passed to script
* `system.env(key, [default])`: Read environment variable
* `system.os_name()`: Current operating system (`"windows"`, `"linux"`, `"darwin"`)
* `system.exit([code])` / `system.samapta([code])`: Terminate process with exit code
