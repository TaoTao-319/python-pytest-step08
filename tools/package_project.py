"""按项目白名单生成压缩包，并记录每个成果文件的 SHA-256。"""

import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = ("src", "tests", "examples", "tools", "artifacts", "docs")
FILES = ("README.md", "requirements.txt", "pytest.ini", ".gitignore")
MANIFEST = ROOT / "artifacts" / "package-manifest.json"


def main():
    files = [ROOT / name for name in FILES]
    for folder in FOLDERS:
        files.extend(
            path for path in (ROOT / folder).rglob("*")
            if path.is_file()
            and "__pycache__" not in path.parts
            and path.suffix not in {".pyc", ".pyo"}
            and path != MANIFEST
        )
    files.append(ROOT / "demo.py")
    files = sorted(files)
    manifest = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        }
        for path in files
    ]
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    files.append(MANIFEST)
    output = ROOT / "dist" / "python-pytest-portfolio.zip"
    output.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, "python-pytest-portfolio/" + path.relative_to(ROOT).as_posix())
    print(f"Packaged files: {len(files)}")
    print(output)


if __name__ == "__main__":
    main()
