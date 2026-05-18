#!/usr/bin/env python3
"""Verify thinking-essence-extraction installation in a target project.

Usage:
    python install/verify_installation.py /path/to/target-project
"""

import os
import sys


REQUIRED_FILES = {
    # Codex
    ".codex/skills/thinking-essence-extraction/SKILL.md": "Codex skill file",
    "AGENTS.md": "Codex agent manifest",
    # Claude
    ".claude/skills/thinking-essence-extraction/SKILL.md": "Claude skill file",
    "CLAUDE.md": "Claude project entry",
}

OPTIONAL_FILES = {
    ".codex/skills/thinking-essence-extraction/docs/variable_cards.md": "Variable cards",
    ".codex/skills/thinking-essence-extraction/docs/baseline_defect_taxonomy.md": "Defect taxonomy",
    ".codex/skills/thinking-essence-extraction/docs/module_cards.md": "Module cards",
    ".codex/skills/thinking-essence-extraction/docs/baseline_evolution_workflow.md": "Evolution workflow",
    ".codex/skills/thinking-essence-extraction/docs/anti_patterns.md": "Anti-patterns",
    ".codex/skills/thinking-essence-extraction/examples/remote_sensing_segmentation_examples.md": "Remote sensing examples",
    ".codex/skills/thinking-essence-extraction/examples/engineering_design_examples.md": "Engineering examples",
    ".codex/skills/thinking-essence-extraction/examples/baseline_evolution_examples.md": "Evolution examples",
    ".codex/skills/thinking-essence-extraction/evals/checkpoints.json": "Test checkpoints",
}


def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_installation.py /path/to/target-project")
        sys.exit(1)

    target = os.path.abspath(sys.argv[1])
    if not os.path.isdir(target):
        print(f"ERROR: {target} is not a directory")
        sys.exit(1)

    print(f"Verifying installation in: {target}\n")

    errors = []
    warnings = []

    for rel_path, description in REQUIRED_FILES.items():
        full_path = os.path.join(target, rel_path)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            if size == 0:
                errors.append(f"  EMPTY: {rel_path} ({description})")
            else:
                print(f"  [OK] {rel_path} ({size} bytes)")
        else:
            errors.append(f"  MISSING: {rel_path} ({description})")

    print()
    for rel_path, description in OPTIONAL_FILES.items():
        full_path = os.path.join(target, rel_path)
        if os.path.exists(full_path):
            print(f"  [OK] {rel_path}")
        else:
            warnings.append(f"  MISSING (optional): {rel_path} ({description})")

    if warnings:
        print("\nOptional files missing (non-blocking):")
        for w in warnings:
            print(w)

    print()
    if errors:
        print(f"FAILED: {len(errors)} core file(s) missing.")
        for e in errors:
            print(e)
        sys.exit(1)
    else:
        print("PASSED: All core files present.")
        sys.exit(0)


if __name__ == "__main__":
    main()
