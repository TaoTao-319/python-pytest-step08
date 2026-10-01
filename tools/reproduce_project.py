"""从本地 Git 克隆，创建全新环境并离线安装依赖后验证。"""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheels", required=True, help="包含 pytest 及其依赖 wheel 的目录")
    args = parser.parse_args()
    destination = ROOT / ".verification" / "fresh-clone"
    if destination.exists():
        raise SystemExit("验证目录已存在，请指定新的工作副本或先检查现有目录。")
    wheels = Path(args.wheels).resolve()
    if not wheels.is_dir():
        raise SystemExit("依赖包目录不存在。")
    records = []

    def run(command, cwd):
        result = subprocess.run(
            [str(part) for part in command], cwd=cwd, capture_output=True,
            encoding="utf-8", errors="replace",
            env=os.environ | {"PYTHONIOENCODING": "utf-8"},
        )
        records.append(
            "> " + " ".join(str(part) for part in command)
            + "\n" + result.stdout + result.stderr
            + f"\nExit code: {result.returncode}\n"
        )
        (ROOT / "artifacts" / "reproduction.txt").write_text(
            "\n".join(records), encoding="utf-8"
        )
        if result.returncode:
            raise SystemExit(f"独立副本验证失败，详情见 artifacts/reproduction.txt：{result.returncode}")
        return result

    commit = run(["git", "rev-parse", "HEAD"], ROOT).stdout.strip()
    run(["git", "clone", "--no-hardlinks", ROOT, destination], ROOT)
    run([sys.executable, "-m", "venv", ".venv"], destination)
    fresh_python = destination / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    run(
        [fresh_python, "-m", "pip", "install", "--no-index", "--find-links", wheels, "-r", "requirements.txt"],
        destination,
    )
    run(
        [fresh_python, "-m", "pytest", "-q", "--junitxml=artifacts/fresh-tests.xml"],
        destination,
    )
    demo = run([fresh_python, "demo.py"], destination).stdout.strip()
    cases = ET.parse(destination / "artifacts" / "fresh-tests.xml").findall(".//testcase")
    all_passed = all(
        not any(case.find(tag) is not None for tag in ("failure", "error", "skipped"))
        for case in cases
    )
    summary = {
        "source_commit": commit,
        "method": "local_git_clone_and_fresh_venv",
        "dependencies_installed_offline": True,
        "tests": len(cases),
        "all_tests_passed": bool(cases) and all_passed,
        "demo_output": demo,
        "github_clone_verified": False,
    }
    (ROOT / "artifacts" / "reproduction.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if cases and all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
