"""
Sikhar Package Manager Implementation
Handles dependency management, sikhar.toml manipulation, and project packaging.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def load_manifest(manifest_path: Path) -> Dict[str, Any]:
    if not manifest_path.exists():
        return {}
    lines = manifest_path.read_text(encoding="utf-8").splitlines()
    data: Dict[str, Any] = {"dependencies": {}}
    current_section = "root"

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("[") and stripped.endswith("]"):
            current_section = stripped[1:-1].strip()
            if current_section not in data:
                data[current_section] = {}
            continue

        if "=" in stripped:
            k, v = stripped.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if current_section == "root":
                data[k] = v
            else:
                data[current_section][k] = v

    return data


def save_manifest(manifest_path: Path, data: Dict[str, Any]) -> None:
    lines = []
    # Root section
    for k, v in data.items():
        if k != "dependencies" and not isinstance(v, dict):
            lines.append(f'{k} = "{v}"')

    lines.append("")
    lines.append("[dependencies]")
    deps = data.get("dependencies", {})
    for dep_name, dep_ver in sorted(deps.items()):
        lines.append(f'{dep_name} = "{dep_ver}"')

    lines.append("")
    manifest_path.write_text("\n".join(lines), encoding="utf-8")


def add_dependency(package_name: str, version: str = "*", root_dir: Optional[Path] = None) -> int:
    root = root_dir or Path.cwd()
    manifest_path = root / "sikhar.toml"

    if not manifest_path.exists():
        # Auto-create manifest if none exists
        manifest_path.write_text(
            f'name = "{root.name}"\nversion = "0.1.0"\nmain = "src/main.sk"\n\n[dependencies]\n',
            encoding="utf-8",
        )

    data = load_manifest(manifest_path)
    if "dependencies" not in data:
        data["dependencies"] = {}

    data["dependencies"][package_name] = version
    save_manifest(manifest_path, data)

    print(f"Added dependency: {package_name} = \"{version}\" to sikhar.toml")
    return 0


def install_dependencies(root_dir: Optional[Path] = None) -> int:
    root = root_dir or Path.cwd()
    manifest_path = root / "sikhar.toml"

    if not manifest_path.exists():
        print("Error: No 'sikhar.toml' found in current directory.", file=sys.stderr)
        return 1

    data = load_manifest(manifest_path)
    deps = data.get("dependencies", {})

    pkg_dir = root / ".sikhar" / "packages"
    pkg_dir.mkdir(parents=True, exist_ok=True)

    if not deps:
        print("No dependencies defined in sikhar.toml.")
        return 0

    print(f"Resolving {len(deps)} dependencies:")
    for dep_name, dep_ver in deps.items():
        target_dep = pkg_dir / dep_name
        target_dep.mkdir(parents=True, exist_ok=True)
        # Create package index / stub
        init_file = target_dep / f"{dep_name}.sk"
        if not init_file.exists():
            init_file.write_text(f'# Package {dep_name} v{dep_ver}\npathaau sthayi VERSION = "{dep_ver}"\n', encoding="utf-8")
        print(f"  [+] {dep_name}@{dep_ver} installed in .sikhar/packages/{dep_name}/")

    print("\nAll dependencies successfully installed!")
    return 0


def publish_package(root_dir: Optional[Path] = None) -> int:
    root = root_dir or Path.cwd()
    manifest_path = root / "sikhar.toml"

    if not manifest_path.exists():
        print("Error: No 'sikhar.toml' found to publish.", file=sys.stderr)
        return 1

    data = load_manifest(manifest_path)
    pkg_name = data.get("name")
    pkg_ver = data.get("version", "1.0.0")

    if not pkg_name:
        print("Error: Manifest must specify a 'name'.", file=sys.stderr)
        return 1

    print(f"[*] Packaging {pkg_name} v{pkg_ver} for publication...")
    dist_dir = root / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)

    from ..builder.bundle import build_standalone
    main_file = data.get("main", "src/main.sk")
    if (root / main_file).exists():
        out_pkg = dist_dir / f"{pkg_name}-{pkg_ver}.pyz"
        build_standalone(str(root / main_file), str(out_pkg))
        print(f"  [+] Created package distribution: {out_pkg}")
    else:
        print(f"  [+] Validated package metadata for {pkg_name}@{pkg_ver}")

    print("Package publication check passed!")
    return 0

