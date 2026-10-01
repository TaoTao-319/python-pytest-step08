"""执行测试并保存真实日志、JUnit 报告和逐场景结果。"""

import csv
import json
import platform
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"


def run(args, filename):
    command = [sys.executable, *args]
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=__import__("os").environ | {"PYTHONIOENCODING": "utf-8"},
    )
    display = "python " + " ".join(args)
    output = f"> {display}\n\n{result.stdout}{result.stderr}\nExit code: {result.returncode}\n"
    (ARTIFACTS / filename).write_text(output, encoding="utf-8")
    return result


def main():
    ARTIFACTS.mkdir(exist_ok=True)
    normal = run(
        ["-m", "pytest", "-v", "--color=no", "--junitxml=artifacts/tests.xml"],
        "pytest-pass.txt",
    )
    if normal.returncode != 0:
        print(normal.stdout)
        print(normal.stderr)
        return normal.returncode

    tree = ET.parse(ARTIFACTS / "tests.xml")
    cases = []
    for case in tree.findall(".//testcase"):
        status = "passed"
        for kind in ("failure", "error", "skipped"):
            if case.find(kind) is not None:
                status = kind
                break
        cases.append({
            "module": case.attrib["classname"],
            "scenario": case.attrib["name"],
            "status": status,
            "duration_seconds": case.attrib.get("time", ""),
        })
    with (ARTIFACTS / "test_cases.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=["module", "scenario", "status", "duration_seconds"])
        writer.writeheader()
        writer.writerows(cases)

    failure = run(
        ["-m", "pytest", "examples/failure_example.py", "-v", "--color=no", "--tb=short"],
        "pytest-failure.txt",
    )
    # 错误示例必须因为断言不一致而失败，不能将导入错误当成有效演示。
    expected_failure = (
        failure.returncode == 1
        and "AssertionError" in failure.stdout
        and "1 failed" in failure.stdout
    )
    demo = run(["demo.py"], "demo-output.txt")
    summary = {
        "python_version": platform.python_version(),
        "platform": platform.system(),
        "pytest_version": __import__("pytest").__version__,
        "tests": len(cases),
        "passed": sum(case["status"] == "passed" for case in cases),
        "normal_suite_exit_code": normal.returncode,
        "failure_example_exit_code": failure.returncode,
        "failure_example_behaved_as_expected": expected_failure,
        "demo_exit_code": demo.returncode,
    }
    (ARTIFACTS / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if expected_failure and demo.returncode == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
