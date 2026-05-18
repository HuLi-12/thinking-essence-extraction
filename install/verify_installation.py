#!/usr/bin/env python3
"""Verify thinking-essence-extraction installation in a target project.

Usage:
    python install/verify_installation.py /path/to/target-project
    python install/verify_installation.py /path/to/target-project --agent codex
    python install/verify_installation.py /path/to/target-project --agent claude
    python install/verify_installation.py /path/to/target-project --agent both
"""

import os
import sys


CODEX_REQUIRED = {
    ".codex/skills/thinking-essence-extraction/SKILL.md": "Codex skill file",
    "AGENTS.md": "Codex agent manifest",
}

CLAUDE_REQUIRED = {
    ".claude/skills/thinking-essence-extraction/SKILL.md": "Claude skill file",
    "CLAUDE.md": "Claude project entry",
}

CODEX_OPTIONAL = {
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

CLAUDE_OPTIONAL = {
    ".claude/skills/thinking-essence-extraction/docs/variable_cards.md": "Variable cards",
    ".claude/skills/thinking-essence-extraction/docs/baseline_defect_taxonomy.md": "Defect taxonomy",
    ".claude/skills/thinking-essence-extraction/docs/module_cards.md": "Module cards",
    ".claude/skills/thinking-essence-extraction/docs/baseline_evolution_workflow.md": "Evolution workflow",
    ".claude/skills/thinking-essence-extraction/docs/anti_patterns.md": "Anti-patterns",
    ".claude/skills/thinking-essence-extraction/examples/remote_sensing_segmentation_examples.md": "Remote sensing examples",
    ".claude/skills/thinking-essence-extraction/examples/engineering_design_examples.md": "Engineering examples",
    ".claude/skills/thinking-essence-extraction/examples/baseline_evolution_examples.md": "Evolution examples",
}


def check_files(target, required, optional):
    errors = []
    warnings = []
    for rel_path, description in required.items():
        full_path = os.path.join(target, rel_path)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            if size == 0:
                errors.append(f"  EMPTY: {rel_path} ({description})")
            else:
                print(f"  [OK] {rel_path} ({size} bytes)")
        else:
            errors.append(f"  MISSING: {rel_path} ({description})")

    for rel_path, description in optional.items():
        full_path = os.path.join(target, rel_path)
        if os.path.exists(full_path):
            print(f"  [OK] {rel_path}")
        else:
            warnings.append(f"  MISSING (optional): {rel_path} ({description})")
    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    target = os.path.abspath(sys.argv[1])
    if not os.path.isdir(target):
        print(f"ERROR: {target} is not a directory")
        sys.exit(1)

    agent = "both"
    if "--agent" in sys.argv:
        idx = sys.argv.index("--agent")
        if idx + 1 < len(sys.argv):
            agent = sys.argv[idx + 1]
    if agent not in ("codex", "claude", "both"):
        print(f"ERROR: --agent must be 'codex', 'claude', or 'both', got '{agent}'")
        sys.exit(1)

    print(f"Verifying {agent} installation in: {target}\n")

    all_errors = []
    all_warnings = []

    if agent in ("codex", "both"):
        print("--- Codex ---")
        e, w = check_files(target, CODEX_REQUIRED, CODEX_OPTIONAL)
        all_errors.extend(e)
        all_warnings.extend(w)
        print()

    if agent in ("claude", "both"):
        print("--- Claude ---")
        e, w = check_files(target, CLAUDE_REQUIRED, CLAUDE_OPTIONAL)
        all_errors.extend(e)
        all_warnings.extend(w)
        print()

    if all_warnings:
        print("Optional files missing (non-blocking):")
        for w in set(all_warnings):
            print(w)
        print()

    if all_errors:
        print(f"FAILED: {len(all_errors)} core file(s) missing.")
        for e in all_errors:
            print(e)
        sys.exit(1)
    else:
        print("PASSED: All core files present.")
        sys.exit(0)


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
