import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from io import StringIO
from sikhar.cli.main import main


class TestCLI(unittest.TestCase):
    def test_version_command(self):
        old_stdout = sys.stdout
        sys.stdout = captured = StringIO()
        try:
            exit_code = main(["version"])
            self.assertEqual(exit_code, 0)
            self.assertIn("Sikhar v0.1.0", captured.getvalue())
        finally:
            sys.stdout = old_stdout

    def test_help_command(self):
        old_stdout = sys.stdout
        sys.stdout = captured = StringIO()
        try:
            exit_code = main(["help"])
            self.assertEqual(exit_code, 0)
            self.assertIn("Commands:", captured.getvalue())
        finally:
            sys.stdout = old_stdout

    def test_check_valid_file(self):
        old_stdout = sys.stdout
        sys.stdout = captured = StringIO()
        try:
            exit_code = main(["check", "hello.sk"])
            self.assertEqual(exit_code, 0)
            self.assertIn("Syntax OK", captured.getvalue())
        finally:
            sys.stdout = old_stdout

    def test_run_valid_file(self):
        old_stdout = sys.stdout
        sys.stdout = captured = StringIO()
        try:
            exit_code = main(["run", "hello.sk"])
            self.assertEqual(exit_code, 0)
            output = captured.getvalue().strip().splitlines()
            self.assertIn("10", output)
            self.assertIn("Thulo", output)
        finally:
            sys.stdout = old_stdout

    def test_run_missing_file_returns_error_code(self):
        old_stderr = sys.stderr
        sys.stderr = captured = StringIO()
        try:
            exit_code = main(["run", "non_existent_file_xyz.sk"])
            self.assertEqual(exit_code, 1)
        finally:
            sys.stderr = old_stderr


if __name__ == "__main__":
    unittest.main()
