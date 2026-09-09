# Installation & Setup

Sikhar v0.1.0 is implemented in pure Python 3.10+ with **zero external dependencies**.

## Requirements

* **Python**: 3.10 or newer (tested on Python 3.12)
* **Operating System**: Windows, macOS, or Linux

## Setup Options

### 1. Direct Execution via Python

If you are already inside the project directory, you are ready to go immediately!

If cloning fresh from source:

```bash
git clone https://github.com/sikhar-lang/sikhar.git
cd sikhar
```

Execute scripts using the module launcher:

```bash
python -m sikhar run path/to/file.sk
```

### 2. Using the Command Line Launcher (`sk`)

#### Windows
Use the included `sk.bat` launcher in the project root or add the `bin/` directory to your system `PATH`:

```cmd
.\sk.bat run hello.sk
```

To use `sk` from any folder in PowerShell or Command Prompt, add your repository's `bin/` directory to your User `PATH` environment variable:

```powershell
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";<path-to-workspace>\bin", [EnvironmentVariableTarget]::User)
```

#### Linux / macOS
Make `bin/sk` executable and symlink it to your local binary path:

```bash
chmod +x bin/sk
sudo ln -s $(pwd)/bin/sk /usr/local/bin/sk
```

Verify your installation:

```bash
sk version
```

Expected output:
```text
Sikhar v0.1.0
```
