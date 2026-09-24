import unittest
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from sikhar.pkg.manager import (
    load_manifest,
    save_manifest,
    add_dependency,
    install_dependencies,
    publish_package,
)


class TestPackageManager(unittest.TestCase):
    def test_add_and_install_dependencies(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            manifest = root / "sikhar.toml"
            manifest.write_text(
                'name = "testpkg"\nversion = "1.0.0"\nmain = "src/main.sk"\n\n[dependencies]\n',
                encoding="utf-8",
            )

            # Add dependencies
            rc1 = add_dependency("nepal_utils", "^1.2.0", root_dir=root)
            self.assertEqual(rc1, 0)
            rc2 = add_dependency("himalaya_auth", "0.5.0", root_dir=root)
            self.assertEqual(rc2, 0)

            # Verify manifest
            data = load_manifest(manifest)
            self.assertEqual(data["name"], "testpkg")
            self.assertIn("nepal_utils", data["dependencies"])
            self.assertEqual(data["dependencies"]["nepal_utils"], "^1.2.0")
            self.assertEqual(data["dependencies"]["himalaya_auth"], "0.5.0")

            # Run install
            rc_install = install_dependencies(root_dir=root)
            self.assertEqual(rc_install, 0)

            # Verify installed package stubs
            pkg_file = root / ".sikhar" / "packages" / "nepal_utils" / "nepal_utils.sk"
            self.assertTrue(pkg_file.exists())
            self.assertIn("^1.2.0", pkg_file.read_text(encoding="utf-8"))

    def test_publish_package_validation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            manifest = root / "sikhar.toml"
            manifest.write_text(
                'name = "verified_module"\nversion = "1.0.0"\nmain = "main.sk"\n',
                encoding="utf-8",
            )
            # Create main entrypoint
            main_sk = root / "main.sk"
            main_sk.write_text('dekha "Sikhar Package"', encoding="utf-8")

            rc = publish_package(root_dir=root)
            self.assertEqual(rc, 0)
            dist_zip = root / "dist" / "verified_module-1.0.0.pyz"
            self.assertTrue(dist_zip.exists())


if __name__ == "__main__":
    unittest.main()
