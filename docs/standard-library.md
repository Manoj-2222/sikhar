# Sikhar Standard Library (v1.0.0)

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

### 8. `std.json`
JSON parsing, serialization, and validation:
* `json.parse(str)` / `json.padh(str)` / `json.chin(str)`: Parse JSON text into Sikhar data structures
* `json.stringify(value, [indent])` / `json.rupantar(value, [indent])` / `json.lekh(...)`: Serialize value to JSON string with optional pretty formatting
* `json.valid(str)` / `json.sacho(str)`: Validate JSON text syntax returning boolean without throwing

### 9. `std.http`
HTTP client and standalone server:
* `http.get(url, [headers], [timeout])` / `http.lyaau(url, ...)`: Perform HTTP GET request
* `http.post(url, body, [headers], [timeout])` / `http.pathaau(...)`: Perform HTTP POST request
* `http.put(url, body, [headers], [timeout])`: Perform HTTP PUT request
* `http.delete(url, [headers], [timeout])` / `http.hatau(...)`: Perform HTTP DELETE request
* `http.patch(url, body, [headers], [timeout])`: Perform HTTP PATCH request
* `http.request(method, url, [body], [headers], [timeout])`: General HTTP request dispatcher
* `http.server(port, handler_fn, [host])`: Create standalone HTTP server instance with `.start()`, `.serve_forever()`, and `.stop()`

### 10. `std.web`
Official Sikhar Web Framework:
* `web.app()` / `web.new_app()`: Creates a web application instance
  * `app.get(path, handler)`: Register GET route with support for `:param` dynamic parameters
  * `app.post(path, handler)`: Register POST route
  * `app.put(path, handler)`: Register PUT route
  * `app.delete(path, handler)`: Register DELETE route
  * `app.patch(path, handler)`: Register PATCH route
  * `app.all(path, handler)`: Register handler for all HTTP verbs
  * `app.use(middleware_fn)`: Register middleware executed before matching route handlers
  * `app.static(url_prefix, directory_path)`: Mount directory for static asset file serving
  * `app.handle(request_map)`: Programmatic in-memory request evaluation for fast testing
  * `app.listen(port, [host])`: Bind and serve HTTP traffic synchronously
  * `app.start([port], [host])`: Bind and serve in background thread, returning bound port
  * `app.stop()`: Shutdown running web server

### 11. `std.db`
Embedded SQLite database driver:
* `db.connect(database_path)`: Connect to SQLite database (`":memory:"` or file path)
  * `conn.execute(sql, [params])`: Execute DDL/DML query; returns `{"rows_affected": int, "last_id": int}`
  * `conn.query(sql, [params])`: Execute `SELECT` query; returns list of column-mapped dictionaries
  * `conn.query_one(sql, [params])`: Execute `SELECT` query; returns first column-mapped dictionary or `khali`
  * `conn.commit()`: Commit current transaction
  * `conn.rollback()`: Rollback current transaction
  * `conn.close()`: Close database connection

### 12. `std.crypto`
Cryptography and secure primitives:
* `crypto.sha256(data)` / `crypto.hashing(data)`: Computes SHA-256 hex digest
* `crypto.sha512(data)`: Computes SHA-512 hex digest
* `crypto.md5(data)`: Computes legacy MD5 hex checksum
* `crypto.hmac_sha256(key, data)` / `crypto.gupta(...)`: Keyed HMAC authentication code
* `crypto.base64_encode(data)`: Base64 encodes string
* `crypto.base64_decode(str)`: Decodes Base64 into original string
* `crypto.random_bytes([count=16])`: Generates cryptographically secure random hex string
* `crypto.random_token([length=32])` / `crypto.chinno(...)`: Generates URL-safe random token

### 13. `std.csv`
Tabular data and CSV processing:
* `csv.parse(text, [has_headers=true], [delimiter=','])`: Parse CSV string into list of maps or lists
* `csv.stringify(rows, [headers], [delimiter=','])`: Convert tabular data into CSV string
* `csv.read(path, [has_headers=true], [delimiter=','])` / `csv.padh(...)`: Read and parse CSV file
* `csv.write(path, rows, [headers], [delimiter=','])` / `csv.lekh(...)`: Write tabular data to file

### 14. `std.regex`
Regular expression pattern matching and search:
* `regex.match(pattern, text)` / `regex.milcha(...)`: Check if text matches regex pattern
* `regex.find_all(pattern, text)` / `regex.khoja(...)`: Extract all occurrences matching pattern
* `regex.replace(pattern, replacement, text)` / `regex.badla(...)`: Substitute matching patterns
* `regex.split(pattern, text)`: Split string by regex pattern

### 15. `std.process`
System process execution and OS environment:
* `process.exec(command, [timeout=60], [shell=true])` / `process.chalaau(...)`: Execute system command
* `process.env(name, [default=khali])`: Retrieve environment variable value
* `process.set_env(name, value)`: Set environment variable
* `process.args()`: Command line arguments passed to script
* `process.cwd()`: Current working directory

### 16. `std.task`
Asynchronous concurrency and background thread workers:
* `task.spawn(kaam_fn, [arguments_list])` / `task.suru(...)`: Spawn background concurrent worker task
* `task.wait(task_handle, [timeout])` / `task.parkha(...)`: Wait for task completion and retrieve result
* `task.sleep(seconds)` / `task.suta(...)`: Non-blocking sleep for current thread
