# Package Manager & Project Configuration

Sikhar includes a built-in package management system that manages project dependencies, configures project metadata via `sikhar.toml`, and creates distributable standalone packages (`.pyz`).

---

## Project Manifest (`sikhar.toml`)

Every standard Sikhar project can declare its dependencies and metadata in a `sikhar.toml` file at the root of the workspace.

```toml
name = "my_app"
version = "1.0.0"
main = "src/main.sk"

[dependencies]
nepal_utils = "^1.2.0"
himalaya_auth = "0.5.0"
```

---

## CLI Commands

### 1. Initializing a Project (`sk init`)
Create a new project scaffold:
```bash
sk init my_project
```
This generates:
- `sikhar.toml`
- `src/main.sk`
- `tests/test_main.sk`

### 2. Adding a Dependency (`sk add`)
Add a new package dependency to `sikhar.toml`:
```bash
sk add math_extra ^2.0.0
```
This updates `sikhar.toml`:
```toml
[dependencies]
math_extra = "^2.0.0"
```

### 3. Installing Dependencies (`sk install`)
Install all packages declared in `sikhar.toml` into `.sikhar/packages/`:
```bash
sk install
```
Output:
```
Resolving 2 dependencies:
  [+] himalaya_auth@0.5.0 installed in .sikhar/packages/himalaya_auth/
  [+] nepal_utils@^1.2.0 installed in .sikhar/packages/nepal_utils/

All dependencies successfully installed!
```

### 4. Publishing / Packaging a Project (`sk publish`)
Packages the project into a standalone distributable bundle:
```bash
sk publish
```
Output:
```
[*] Packaging my_app v1.0.0 for publication...
  [+] Created package distribution: dist/my_app-1.0.0.pyz
Package publication check passed!
```

The resulting `.pyz` package in `dist/` is directly executable on any system with Python 3.10+ without needing Sikhar installed:
```bash
python dist/my_app-1.0.0.pyz
```
