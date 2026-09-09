"""
Sikhar module execution entrypoint (python -m sikhar ...)
"""
import sys
from sikhar.cli.main import main

if __name__ == "__main__":
    sys.exit(main())
