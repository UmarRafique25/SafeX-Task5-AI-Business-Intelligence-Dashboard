"""
run_all_tests.py

Master test runner for the
AI Business Intelligence Dashboard.
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")


# ============================================================
# TEST DIRECTORY
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent
TEST_DIR = PROJECT_ROOT / "tests"
TEST_FILES = sorted(TEST_DIR.glob("test_*.py"))


# ============================================================
# TEST RESULTS
# ============================================================

results = []


# ============================================================
# HEADER
# ============================================================

print()
print("=" * 70)
print("🧪 AI BUSINESS INTELLIGENCE DASHBOARD")
print("   AUTOMATED TEST SUITE")
print("=" * 70)
print()


# ============================================================
# RUN TESTS
# ============================================================

for test_path in TEST_FILES:

    test_file = test_path.name

    print()
    print("-" * 70)
    print(f"▶ Running: {test_file}")
    print("-" * 70)

    if not test_path.exists():

        print(
            f"⚠️ Test file not found: {test_file}"
        )

        results.append(
            {
                "test": test_file,
                "status": "NOT FOUND"
            }
        )

        continue

    process = subprocess.run(
        [
            sys.executable,
            str(test_path)
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=PROJECT_ROOT,
        env={
            **os.environ,
            "PYTHONPATH": str(PROJECT_ROOT),
            "PYTHONIOENCODING": "utf-8"
        }
    )

    print(
        process.stdout
    )

    if process.stderr:

        print(
            process.stderr
        )

    if process.returncode == 0:

        results.append(
            {
                "test": test_file,
                "status": "PASSED"
            }
        )

    else:

        results.append(
            {
                "test": test_file,
                "status": "FAILED"
            }
        )


# ============================================================
# FINAL REPORT
# ============================================================

print()
print()
print("=" * 70)
print("📋 FINAL TEST REPORT")
print("=" * 70)
print()


passed = 0
failed = 0
not_found = 0


for result in results:

    test_name = result["test"]
    status = result["status"]

    if status == "PASSED":

        print(
            f"✅ {test_name:<40} PASSED"
        )

        passed += 1

    elif status == "FAILED":

        print(
            f"❌ {test_name:<40} FAILED"
        )

        failed += 1

    else:

        print(
            f"⚠️ {test_name:<40} NOT FOUND"
        )

        not_found += 1


# ============================================================
# SUMMARY
# ============================================================

total = len(results)

print()
print("-" * 70)

print(
    f"Total Tests : {total}"
)

print(
    f"Passed      : {passed}"
)

print(
    f"Failed      : {failed}"
)

print(
    f"Not Found   : {not_found}"
)

print("-" * 70)

# ============================================================
# SAVE TEST REPORT
# ============================================================

report_path = (
    PROJECT_ROOT
    / "test_results.txt"
)

with open(
    report_path,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "AI Business Intelligence Dashboard\n"
    )

    file.write(
        "Automated Test Report\n"
    )

    file.write(
        f"Generated: "
        f"{datetime.now()}\n\n"
    )

    for result in results:

        file.write(
            f"{result['test']}: "
            f"{result['status']}\n"
        )

    file.write("\n")

    file.write(
        f"Total: {total}\n"
    )

    file.write(
        f"Passed: {passed}\n"
    )

    file.write(
        f"Failed: {failed}\n"
    )

    file.write(
        f"Not Found: {not_found}\n"
    )

# ============================================================
# FINAL STATUS
# ============================================================

if failed == 0 and not_found == 0:

    print()
    print(
        "🎉 ALL TESTS PASSED"
    )

    print(
        "The dashboard is ready for the next stage."
    )

    print()

    sys.exit(0)

else:

    print()
    print(
        "❌ TEST SUITE FAILED"
    )

    print(
        "Fix the failed tests before continuing."
    )

    print()

    sys.exit(1)