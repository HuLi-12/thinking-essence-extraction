#!/usr/bin/env python3
"""Check a model response against expected checkpoints from evals/expected_checkpoints.md."""

import os
import sys
import re
import json
from typing import List, Dict

CHECKPOINT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "evals", "expected_checkpoints.md"
)

TEST_PATHS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "evals", "test_prompts.md"
)


def load_checkpoints() -> Dict[str, Dict[str, List[str]]]:
    """Parse expected_checkpoints.md into {test_name: {required: [...], forbidden: [...]}}."""
    if not os.path.exists(CHECKPOINT_PATH):
        print(f"ERROR: {CHECKPOINT_PATH} not found")
        sys.exit(1)

    with open(CHECKPOINT_PATH, encoding="utf-8") as f:
        content = f.read()

    tests = {}
    current_test = None

    # Split by Test headers
    sections = re.split(r"## Test (\d+)", content)
    # sections[0] = preamble, sections[1] = test number, sections[2] = body, sections[3] = next test number...
    i = 1
    while i < len(sections):
        test_num = sections[i].strip()
        body = sections[i + 1] if i + 1 < len(sections) else ""
        test_name = f"Test {test_num}"
        tests[test_name] = {"required": [], "forbidden": []}

        # Extract required checkpoints: lines starting with "- [ ]"
        required_matches = re.findall(r"- \[ \] [R\d]+: (.+)", body)
        tests[test_name]["required"] = required_matches

        # Extract forbidden patterns: lines after "禁止出现的错误"
        forbidden_section = re.search(r"### 禁止出现的错误\n\n(.*?)(?:\n\n|$)", body, re.DOTALL)
        if forbidden_section:
            forbidden_lines = re.findall(r"- \[ \] (.+)", forbidden_section.group(1))
            tests[test_name]["forbidden"] = forbidden_lines

        i += 2

    return tests


def check_response(test_name: str, response_text: str) -> None:
    """Check a response against checkpoints for the given test."""
    checkpoints = load_checkpoints()

    if test_name not in checkpoints:
        print(f"ERROR: Unknown test '{test_name}'. Available tests:")
        for t in checkpoints:
            print(f"  - {t}")
        sys.exit(1)

    rules = checkpoints[test_name]
    missing = []
    bad = []

    for req in rules["required"]:
        # Extract key terms from requirement
        terms = [t for t in re.split(r"[：:，,。\.]", req) if len(t) > 4]
        if not terms:
            continue
        # Check if any key term from requirement appears in response
        found = False
        for term in terms:
            if term in response_text:
                found = True
                break
        if not found:
            # Use the first 30 chars as the requirement label
            missing.append(req[:60])

    for forbidden in rules["forbidden"]:
        terms = [t for t in re.split(r"[：:，,。\.]", forbidden) if len(t) > 2]
        for term in terms:
            if term in response_text:
                bad.append(term)

    score = 0
    total = len(rules["required"])
    if total > 0:
        score = int((total - len(missing)) / total * 100)

    print(f"=== {test_name} Check Result ===\n")
    print(f"Score: {score}/{100}")
    print(f"Required checkpoints: {len(rules['required'])}")
    print(f"  - Passed: {len(rules['required']) - len(missing)}")
    print(f"  - Failed: {len(missing)}")

    if missing:
        print(f"\nMissing requirements:")
        for m in missing:
            print(f"  - {m}...")

    if bad:
        print(f"\nForbidden patterns found:")
        for b in bad:
            print(f"  - Found: '{b}'")

    if score >= 70 and not bad:
        print(f"\nRESULT: PASS (score={score}, no forbidden patterns)")
        sys.exit(0)
    else:
        reasons = []
        if score < 70:
            reasons.append(f"score={score} < 70")
        if bad:
            reasons.append(f"forbidden patterns found")
        print(f"\nRESULT: FAIL ({', '.join(reasons)})")
        sys.exit(1)


def main():
    if len(sys.argv) < 3:
        print("Usage: python check_response_against_checkpoints.py <test_name> <response_file>")
        print("       python check_response_against_checkpoints.py <test_name> '<inline response text>'")
        print("\nAvailable tests:")
        checkpoints = load_checkpoints()
        for t in checkpoints:
            print(f"  - {t}")
        sys.exit(1)

    test_name = sys.argv[1]
    input_arg = sys.argv[2]

    if os.path.exists(input_arg):
        with open(input_arg, encoding="utf-8") as f:
            response_text = f.read()
    else:
        response_text = input_arg

    check_response(test_name, response_text)


if __name__ == "__main__":
    main()
