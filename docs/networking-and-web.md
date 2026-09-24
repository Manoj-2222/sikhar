# Networking, Web Framework & Databases in Sikhar (v0.4.0)

Sikhar v0.4.0 introduces native networking, modern Web microframework capabilities, JSON processing, and embedded SQLite database drivers.

In keeping with Sikhar's core philosophy, **all networking and database capabilities are built strictly using the standard runtime with zero third-party dependencies**. Both the AST Interpreter and the Bytecode Virtual Machine are supported with dual-engine parity.

---

## 1. JSON Processing (`std.json`)

Import the JSON module using:

```sk
aayaat std.json
```

### Functions

| Function | Nepali Alias | Description |
| :--- | :--- | :--- |
| `json.parse(str)` | `json.padh`, `json.chin` | Parses a JSON string into Sikhar data structures (maps, lists, primitives). |
| `json.stringify(val, [indent])` | `json.rupantar`, `json.lekh` | Serializes Sikhar values to a JSON string. Optional `indent` enables pretty printing. |
| `json.valid(str)` | `json.sacho` | Validates whether a string is syntactically valid JSON without throwing errors. |

### Example

```sk
aayaat std.json

rakha raw_text = '{"name": "Sikhar", "version": "0.4.0", "stable": true}'

# Parse JSON
rakha config = json.parse(raw_text)
dekha config["name"]     # Output: Sikhar
dekha config["version"]  # Output: 0.4.0

# Modify and Serialize
config["port"] = 8080
rakha pretty_json = json.stringify(config, 2)
dekha pretty_json

# Validate JSON
yadi json.valid(pretty_json) {
    dekha "JSON configuration is valid."
}
```

---

## 2. HTTP Client & Server (`std.http`)

Import the HTTP module using:

```sk
aayaat std.http
```

### HTTP Client Methods

* `http.get(url, [headers], [timeout])` (alias: `http.lyaau`)
* `http.post(url, body, [headers], [timeout])` (alias: `http.pathaau`)
* `http.put(url, body, [headers], [timeout])`
* `http.delete(url, [headers], [timeout])` (alias: `http.hatau`)
* `http.patch(url, body, [headers], [timeout])`
* `http.request(method, url, [body], [headers], [timeout])`

#### Client Response Object Structure

Every HTTP client request returns a response map:

```sk
{
    "status": 200,             # HTTP status integer
    "ok": true,                # Boolean: sacho if status between 200 and 299
    "body": "...",             # String response payload
    "headers": { ... }         # Map of lowercased header names to values
}
```

#### Client Example

```sk
aayaat std.http
aayaat std.json

rakha res = http.get("https://httpbin.org/get")
yadi res.ok {
    rakha data = json.parse(res.body)
    dekha "Your IP: " + data["origin"]
}
```

### Low-Level HTTP Server

For simple request dispatching, `http.server(port, handler, [host])` starts a server:

```sk
aayaat std.http

kaam handle_request(req) {
    # req.method, req.path, req.query, req.headers, req.body
    yadi req.path == "/health" {
        farka {"status": 200, "body": "OK"}
    }
    farka {"status": 404, "body": "Not Found"}
}

rakha srv = http.server(8080, handle_request)
# srv.start() runs in background; srv.serve_forever() runs blocking
srv.serve_forever()
```

---

## 3. Official Web Framework (`std.web`)

`std.web` is Sikhar's official microframework for building REST APIs, single-page backends, and full web applications.

```sk
aayaat std.web

rakha app = web.app()
```

### Routing

Register handlers for HTTP verbs:

```sk
app.get(path, handler)
app.post(path, handler)
app.put(path, handler)
app.delete(path, handler)
app.patch(path, handler)
app.all(path, handler)
```

#### Parameterized Paths

Route segments beginning with `:` or `{}` are captured into `req.params`:

```sk
app.get("/users/:id", kaam(req) {
    rakha user_id = req.params["id"]
    farka {"id": user_id, "name": "User " + user_id}
})

app.get("/files/*", kaam(req) {
    rakha wildcard_path = req.params["wildcard"]
    farka "Accessing: " + wildcard_path
})
```

#### Request Context (`req`)

Every route handler receives a request context map:

* `req.method`: Upper-case HTTP method (`"GET"`, `"POST"`, etc.)
* `req.path`: URL path without query string (e.g. `"/api/items"`)
* `req.url`: Full raw request URL
* `req.params`: Dictionary of captured path parameters
* `req.query`: Dictionary of query string parameters
* `req.headers`: Dictionary of lowercase request headers
* `req.body`: Raw request body string
* `req.data`: Automatically parsed JSON body (if `Content-Type` was JSON)

#### Response Handling & Auto-Formatting

Handlers can return:

1. **Dictionary or List**: Automatically serialized to JSON with `Content-Type: application/json`.
2. **Explicit Response Map**: `{"status": 201, "body": ..., "headers": {...}}`.
3. **HTML String**: If string starts with `<` and ends with `>`, served as `text/html`.
4. **Plain Text String**: Served as `text/plain`.

### Middleware

Register middleware functions with `app.use(fn)`. Middlewares run sequentially before route handlers:

```sk
app.use(kaam(req) {
    dekha "[" + req.method + "] " + req.path
    # Return a response to short-circuit the request, or return khali to continue
    yadi req.path == "/protected" and req.headers["authorization"] == khali {
        farka {"status": 401, "body": "Unauthorized"}
    }
    farka khali
})
```

### Static File Serving

Serve HTML, CSS, JavaScript, and asset directories:

```sk
app.static("/public", "./static")
app.static("/", "./build")
```

### In-Memory Programmatic Testing (`app.handle`)

You can test web applications instantly without opening TCP sockets:

```sk
rakha res = app.handle({"method": "GET", "path": "/users/42"})
jaach res.status == 200
jaach json.parse(res.body)["id"] == "42"
```

### Starting the Server

* `app.listen(port, [host])`: Starts the server synchronously on the current thread.
* `app.start([port], [host])`: Starts the server in a background thread and returns the bound port (pass `0` for dynamic port assignment).
* `app.stop()`: Stops the running server.

---

## 4. SQLite Database Driver (`std.db`)

Sikhar includes an embedded SQLite database engine with zero external dependencies.

```sk
aayaat std.db
```

### Opening Connections

```sk
# In-memory database
rakha conn = db.connect(":memory:")

# Persistent file database
rakha conn = db.connect("data/app.db")
```

### Connection Methods

* `conn.execute(sql, [params])`: Runs DDL/DML statements (`CREATE`, `INSERT`, `UPDATE`, `DELETE`). Returns `{"rows_affected": int, "last_id": int}`.
* `conn.query(sql, [params])`: Runs `SELECT` queries and returns a list of column-mapped dictionaries.
* `conn.query_one(sql, [params])`: Runs `SELECT` queries and returns a single row dictionary or `khali`.
* `conn.commit()`: Commits current transaction.
* `conn.rollback()`: Rolls back current transaction.
* `conn.close()`: Closes the database connection.

### Example: CRUD with SQLite

```sk
aayaat std.db

rakha conn = db.connect(":memory:")

# 1. Create table
conn.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL)")

# 2. Parameterized Insert
conn.execute("INSERT INTO products (name, price) VALUES (?, ?)", ["Laptop", 1299.99])
conn.execute("INSERT INTO products (name, price) VALUES (?, ?)", ["Mouse", 29.50])

# 3. Query rows
rakha items = conn.query("SELECT * FROM products WHERE price > ?", [50.0])
ko_lagi item ma items {
    dekha item["name"] + " -> $" + item["price"]
}

# 4. Query single row
rakha cheap_item = conn.query_one("SELECT * FROM products ORDER BY price ASC LIMIT 1")
dekha "Cheapest item: " + cheap_item["name"]

conn.close()
```

---

## 5. CLI Web Server Command (`sk serve`)

Sikhar provides the `sk serve` command to instantly run web applications or serve static file directories:

```bash
# Serve a Sikhar web script on port 8000
sk serve app.sk

# Specify custom port and host
sk serve app.sk --port 3000 --host 0.0.0.0

# Run with Bytecode VM
sk serve app.sk --vm --port 8080

# Serve a directory of static assets (HTML/CSS/JS)
sk serve ./dist --port 5000
```
