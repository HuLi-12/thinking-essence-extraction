#!/usr/bin/env python3
"""Validate the thinking-essence-extraction skill package integrity."""

import os
import sys
import re
from typing import List

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_FILES = {
    # Root level
    "README.md": "registry readme",
    "install.md": "installation guide",
    "CHANGELOG.md": "version history",
    "CONTRIBUTING.md": "contribution guidelines",
    "LICENSE": "license file",
    # Skill unit
    "skills/thinking-essence-extraction/README.md": "skill readme",
    "skills/thinking-essence-extraction/SKILL.md": "main skill file",
    "skills/thinking-essence-extraction/docs/variable_cards.md": "variable cards",
    "skills/thinking-essence-extraction/docs/anti_patterns.md": "anti-patterns",
    "skills/thinking-essence-extraction/docs/baseline_defect_taxonomy.md": "baseline defect taxonomy",
    "skills/thinking-essence-extraction/docs/module_cards.md": "module cards",
    "skills/thinking-essence-extraction/docs/baseline_evolution_workflow.md": "baseline evolution workflow",
    "skills/thinking-essence-extraction/examples/remote_sensing_segmentation_examples.md": "remote sensing examples",
    "skills/thinking-essence-extraction/examples/engineering_design_examples.md": "engineering design examples",
    "skills/thinking-essence-extraction/examples/baseline_evolution_examples.md": "baseline evolution examples",
    "skills/thinking-essence-extraction/evals/test_prompts.md": "test prompts",
    "skills/thinking-essence-extraction/evals/expected_checkpoints.md": "expected checkpoints",
    "skills/thinking-essence-extraction/evals/checkpoints.json": "JSON checkpoints",
    # Wrappers
    "wrappers/codex/AGENTS.md": "Codex agent manifest",
    "wrappers/claude/subagent.md": "Claude subagent wrapper",
    "wrappers/claude/command.md": "Claude slash command wrapper",
    # Scripts
    "scripts/validate_skill_package.py": "package validator",
    "scripts/check_response_against_checkpoints.py": "test scoring script",
    # CI
    ".github/workflows/validate.yml": "CI validation workflow",
    ".github/workflows/release.yml": "GitHub release workflow",
}

OPTIONAL_FILES = {
    "install/install.sh": "Unix install script (optional)",
    "install/install.ps1": "Windows install script (optional)",
    "install/install_codex.sh": "Codex Unix install (optional)",
    "install/install_codex.ps1": "Codex Windows install (optional)",
    "install/install_claude.sh": "Claude Unix install (optional)",
    "install/install_claude.ps1": "Claude Windows install (optional)",
    "install/README.md": "install scripts guide (optional)",
    "install/verify_installation.py": "install verification script (optional)",
}

SKILL_MD_PATH = os.path.join(ROOT, "skills", "thinking-essence-extraction", "SKILL.md")

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def check_file_exists(rel_path: str, description: str) -> List[str]:
    errors = []
    full_path = os.path.join(ROOT, rel_path)
    if not os.path.exists(full_path):
        errors.append(f"MISSING: {rel_path} ({description})")
    elif os.path.getsize(full_path) == 0:
        errors.append(f"EMPTY: {rel_path} ({description})")
    return errors


def check_skill_frontmatter() -> List[str]:
    errors = []
    if not os.path.exists(SKILL_MD_PATH):
        return ["MISSING: skills/thinking-essence-extraction/SKILL.md (cannot check frontmatter)"]

    with open(SKILL_MD_PATH, encoding="utf-8") as f:
        content = f.read()

    match = FRONTMATTER_RE.match(content)
    if not match:
        errors.append("SKILL.md: missing YAML frontmatter (---)")
    else:
        frontmatter = match.group(1)
        if "name:" not in frontmatter:
            errors.append("SKILL.md: frontmatter missing 'name:' field")
        if "description:" not in frontmatter:
            errors.append("SKILL.md: frontmatter missing 'description:' field")
        if "version:" not in frontmatter:
            errors.append("SKILL.md: frontmatter missing 'version:' field")

    # Check essential sections
    required_sections = [
        "Core Rule",
        "Problem Type Router",
        "Core Output Requirements",
        "Output Mode Rule",
        "Forbidden Phrases",
        "Variable Table Rule",
        "Evidence Level Rule",
        "Mechanism Chain Rule",
        "Cost Trade-off Rule",
        "Verifiable Hypothesis Rule",
        "Standard Output Template",
        "Anti-pattern Self-check",
        "Literature/Module Search Rule",
        "Baseline Evolution Rule",
        "Domain Reference",
    ]
    for section in required_sections:
        if f"## {section}" not in content:
            errors.append(f"SKILL.md: missing section '{section}'")

    # Check forbidden phrases are present
    forbidden = ["增强语义信息", "提升表达能力", "加强特征融合"]
    for phrase in forbidden:
        if phrase not in content:
            errors.append(f"SKILL.md: missing forbidden phrase '{phrase}'")

    return errors


def check_file_nonempty(rel_path: str, min_chars: int = 100) -> List[str]:
    errors = []
    full_path = os.path.join(ROOT, rel_path)
    if os.path.exists(full_path) and os.path.getsize(full_path) < min_chars:
        errors.append(f"TOO_SHORT: {rel_path} (< {min_chars} chars)")
    return errors


def check_no_ide_files() -> List[str]:
    """Check that IDE files are not committed (should be in .gitignore)."""
    errors = []
    idea_dir = os.path.join(ROOT, ".idea")
    if os.path.exists(idea_dir):
        for f in os.listdir(idea_dir):
            fp = os.path.join(idea_dir, f)
            if os.path.isfile(fp):
                rel = os.path.join(".idea", f)
                errors.append(
                    f"WARNING: {rel} exists locally. Ensure .gitignore excludes it."
                )
                break
    return errors


def main():
    errors = []

    # 1. Check required files exist
    for rel_path, description in REQUIRED_FILES.items():
        errors.extend(check_file_exists(rel_path, description))
        errors.extend(check_file_nonempty(rel_path))

    # 2. Check optional files (warn, not fail)
    warnings = []
    for rel_path, description in OPTIONAL_FILES.items():
        errs = check_file_exists(rel_path, description)
        if errs:
            warnings.extend(errs)

    # 3. Validate SKILL.md content
    errors.extend(check_skill_frontmatter())

    # 4. Check for IDE files
    warnings.extend(check_no_ide_files())

    # 5. Summary
    if errors:
        print("=== VALIDATION FAILED ===\n")
        for err in errors:
            print(f"  - {err}")
        print(f"\n{len(errors)} issue(s) found.")
        sys.exit(1)
    else:
        print("=== VALIDATION PASSED ===\n")
        print("All required files present, SKILL.md structure valid.")
        if warnings:
            print("\nWarnings (non-blocking):")
            for w in warnings:
                print(f"  - {w}")
        sys.exit(0)


if __name__ == "__main__":
    main()
