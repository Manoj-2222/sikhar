# Concurrency & System Processes

Sikhar provides multi-threaded task concurrency via `std.task` and operating system subprocess management via `std.process`. Both execution engines (AST Tree-Walker and Bytecode Virtual Machine) offer full thread isolation and process safety.

---

## Asynchronous Task Spawning (`std.task`)

The `std.task` module allows spawning concurrent background worker threads to execute Sikhar functions in parallel without blocking the main execution thread.

### Spawning and Waiting

```sk
aayaat std.task

kaam compute_factorials(n) {
    # Simulate heavy computation
    task.sleep(0.05)
    rakha prod = 1
    ko_lagi i ma [1, 2, 3, 4, 5] {
        badla prod = prod * i
    }
    farka prod
}

dekha "Starting background computation..."
rakha handle = task.spawn(compute_factorials, [5])
dekha "Spawned task ID: " + handle["id"]

# Main thread continues doing other work
dekha "Main thread is non-blocked and working..."

# Wait for background task result
rakha result = task.wait(handle)
dekha "Result from task: " + result
# Result from task: 120
```

Nepali aliases:
- `task.spawn` -> `task.suru(kaam, [args])`
- `task.wait` -> `task.parkha(handle)`
- `task.sleep` -> `task.suta(seconds)`

### Non-Blocking Status Checking

A task handle provides an `is_done()` method:

```sk
rakha handle = task.spawn(my_worker, [100])

yadi handle.is_done() {
    dekha "Completed immediately!"
} natra {
    dekha "Still running in background..."
}
```

---

## System Subprocesses (`std.process`)

The `std.process` module allows executing system shell commands, reading environment variables, and configuring process context.

### Executing Commands

```sk
aayaat std.process
aayaat std.text

# Execute command (Nepali alias: process.chalaau)
rakha result = process.exec("echo Hello From OS Shell")

dekha "Exit Code: " + result["code"]
dekha "Success:   " + result["ok"]
dekha "Output:    " + text.trim(result["stdout"])
```

The returned dictionary has:
- `code`: Process return code (`int`)
- `ok`: Boolean indicating zero exit code (`bool`)
- `stdout`: Standard output capture (`str`)
- `stderr`: Standard error capture (`str`)

### Environment Variables

Inspect and set environment variables dynamically:

```sk
# Set an environment variable
process.set_env("APP_ENV", "production")

# Read an environment variable (returns default if not found)
rakha env = process.env("APP_ENV", "development")
dekha "Current environment: " + env
```

### Process Metadata

```sk
# Working directory
dekha "Current directory: " + process.cwd()

# Command line arguments passed to Sikhar
rakha args = process.args()
dekha "Arguments: " + args
```

---

## Function Summary

### `std.task`
| Function | Nepali Alias | Description |
|---|---|---|
| `task.spawn(fn, [args])` | `task.suru` | Spawns a background worker thread |
| `task.wait(handle, [timeout])` | `task.parkha` | Blocks until task completes and returns result |
| `task.sleep(seconds)` | `task.suta` | Pauses current thread for specified seconds |

### `std.process`
| Function | Nepali Alias | Description |
|---|---|---|
| `process.exec(cmd, [timeout=60], [shell=true])` | `process.chalaau` | Executes a shell command synchronously |
| `process.env(name, [default=khali])` | — | Retrieves an environment variable |
| `process.set_env(name, value)` | — | Sets an environment variable |
| `process.args()` | — | Returns CLI arguments list |
| `process.cwd()` | — | Returns current working directory |
