#!/usr/bin/env python3
"""Check a model response against checkpoints from evals/checkpoints.json.

Usage:
    python check_response_against_checkpoints.py <test_name> <response_file>
    python check_response_against_checkpoints.py <test_name> '<inline response>'
    python check_response_against_checkpoints.py <test_name> <response_file> --soft
"""

import os
import sys
import json
from typing import List, Dict, Any, Tuple

CHECKPOINTS_JSON = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "evals", "checkpoints.json"
)


def load_checkpoints() -> Dict[str, Dict[str, Any]]:
    if not os.path.exists(CHECKPOINTS_JSON):
        print(f"ERROR: {CHECKPOINTS_JSON} not found")
        sys.exit(1)
    with open(CHECKPOINTS_JSON, encoding="utf-8") as f:
        return json.load(f)


def check_response(test_name: str, response_text: str, soft: bool = False) -> Tuple[bool, int, List[str], List[str]]:
    """Check response and return (passed, score, missing, forbidden_hits)."""
    checkpoints = load_checkpoints()

    if test_name not in checkpoints:
        print(f"ERROR: Unknown test '{test_name}'. Available tests:")
        for t in checkpoints:
            desc = checkpoints[t].get("test_name", "")
            print(f"  - {t}: {desc}")
        sys.exit(1)

    rules = checkpoints[test_name]
    required_groups = rules.get("required_any", [])
    forbidden_list = rules.get("forbidden", [])
    min_score = rules.get("min_score", 3)

    passed_groups = 0
    missing = []

    for group in required_groups:
        found = False
        for keyword in group:
            if keyword in response_text:
                found = True
                break
        if found:
            passed_groups += 1
        else:
            missing.append(group[0])

    total = len(required_groups)
    score = int((passed_groups / total) * 100) if total > 0 else 0

    forbidden_hits = []
    # Only check forbidden if score passes minimum threshold
    if passed_groups >= min_score:
        for keyword in forbidden_list:
            if keyword in response_text:
                forbidden_hits.append(keyword)

    passed = passed_groups >= min_score and not forbidden_hits

    if not soft:
        print(f"=== {test_name}: {rules.get('test_name', '')} ===\n")
        print(f"Score: {score}% ({passed_groups}/{total} keyword groups)")
        print(f"Minimum required: {min_score}/{total}")
        if missing:
            print(f"\nMissing keyword groups:")
            for m in missing:
                print(f"  - '{m}'")
        if forbidden_hits:
            print(f"\nForbidden patterns found:")
            for f in forbidden_hits:
                print(f"  - '{f}'")

    return passed, score, missing, forbidden_hits


def main():
    soft = "--soft" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--soft"]

    if len(args) < 2:
        print("Usage: python check_response_against_checkpoints.py <test_name> <response_file> [--soft]")
        print("       python check_response_against_checkpoints.py <test_name> '<inline response>' [--soft]")
        print("\nAvailable tests:")
        checkpoints = load_checkpoints()
        for t in checkpoints:
            desc = checkpoints[t].get("test_name", "")
            print(f"  - {t}: {desc}")
        sys.exit(1)

    test_name = args[0]
    input_arg = args[1]

    if os.path.exists(input_arg):
        with open(input_arg, encoding="utf-8") as f:
            response_text = f.read()
    else:
        response_text = input_arg

    passed, score, missing, forbidden_hits = check_response(test_name, response_text, soft=soft)

    if soft:
        result = "PASS" if passed else "FAIL"
        print(f"{test_name}: {result} (score={score}%, missing={len(missing)}, forbidden={len(forbidden_hits)})")
    elif passed:
        print(f"\nRESULT: PASS")
        sys.exit(0)
    else:
        reasons = []
        if score < 70:
            reasons.append(f"score={score}%")
        if forbidden_hits:
            reasons.append("forbidden patterns found")
        print(f"\nRESULT: FAIL ({', '.join(reasons)})")
        sys.exit(1)


if __name__ == "__main__":
    main()
