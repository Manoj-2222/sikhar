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
            self.assertIn("Sikhar v0.3.0", captured.getvalue())
        finally:
            sys.stdout = old_stdout

    def test_help_command(self):
        old_stdout = sys.stdout
        sys.stdout = captured = StringIO()
        try:
            exit_code = main(["help"])
            self.assertEqual(exit_code, 0)
            self.assertIn("Commands:", captured.getvalue())
            self.assertIn("compile", captured.getvalue())
            self.assertIn("dis", captured.getvalue())
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

    def test_run_vm_flag(self):
        old_stdout = sys.stdout
        sys.stdout = captured = StringIO()
        try:
            exit_code = main(["run", "--vm", "hello.sk"])
            self.assertEqual(exit_code, 0)
            output = captured.getvalue().strip().splitlines()
            self.assertIn("10", output)
            self.assertIn("Thulo", output)
        finally:
            sys.stdout = old_stdout

    def test_dis_command(self):
        old_stdout = sys.stdout
        sys.stdout = captured = StringIO()
        try:
            exit_code = main(["dis", "hello.sk"])
            self.assertEqual(exit_code, 0)
            self.assertIn("Bytecode Disassembly", captured.getvalue())
        finally:
            sys.stdout = old_stdout

    def test_compile_command(self):
        old_stdout = sys.stdout
        sys.stdout = captured = StringIO()
        out_skc = Path("test_cli_out.skc")
        try:
            exit_code = main(["compile", "hello.sk", "-o", str(out_skc)])
            self.assertEqual(exit_code, 0)
            self.assertTrue(out_skc.exists())
            self.assertIn("Compiled:", captured.getvalue())
        finally:
            sys.stdout = old_stdout
            if out_skc.exists():
                out_skc.unlink()

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

