import unittest
import sys
import subprocess
from pathlib import Path
from io import StringIO

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sikhar.builder import build_standalone
from sikhar.cli.main import main


class TestBuild(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path("build_test_tmp")
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        if self.temp_dir.exists():
            for f in self.temp_dir.glob("*"):
                try:
                    f.unlink()
                except Exception:
                    pass
            try:
                self.temp_dir.rmdir()
            except Exception:
                pass

    def test_build_standalone_vm(self):
        out_pyz = self.temp_dir / "test_hello_vm.pyz"
        pyz_path, bat_path = build_standalone(
            entry_file="examples/01_hello.sk",
            output_path=str(out_pyz),
            use_vm=True,
            create_wrapper=True,
        )
        self.assertTrue(pyz_path.exists())
        self.assertTrue(bat_path.exists())

        # Execute the generated .pyz with Python
        proc = subprocess.run(
            [sys.executable, str(pyz_path)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertIn("Namaste, Sansar!", proc.stdout)
        self.assertIn("10", proc.stdout)
        self.assertIn("Thulo", proc.stdout)

    def test_build_standalone_ast(self):
        out_pyz = self.temp_dir / "test_hello_ast.pyz"
        pyz_path, _ = build_standalone(
            entry_file="examples/01_hello.sk",
            output_path=str(out_pyz),
            use_vm=False,
            create_wrapper=False,
        )
        self.assertTrue(pyz_path.exists())

        proc = subprocess.run(
            [sys.executable, str(pyz_path)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertIn("Namaste, Sansar!", proc.stdout)

    def test_build_cli_command(self):
        old_stdout = sys.stdout
        sys.stdout = captured = StringIO()
        out_pyz = self.temp_dir / "cli_bundle.pyz"
        try:
            exit_code = main(["build", "examples/01_hello.sk", "-o", str(out_pyz)])
            self.assertEqual(exit_code, 0)
            self.assertTrue(out_pyz.exists())
            self.assertIn("Successfully built standalone executable", captured.getvalue())
        finally:
            sys.stdout = old_stdout

    def test_build_missing_file_returns_error(self):
        old_stderr = sys.stderr
        sys.stderr = captured = StringIO()
        try:
            exit_code = main(["build", "completely_missing_file_xyz.sk"])
            self.assertEqual(exit_code, 1)
            self.assertIn("does not exist", captured.getvalue())
        finally:
            sys.stderr = old_stderr


if __name__ == "__main__":
    unittest.main()
