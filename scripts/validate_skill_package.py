#!/usr/bin/env python3
"""Validate the thinking-essence-extraction skill package integrity."""

import os
import sys
import re
from typing import List

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_FILES = {
    "SKILL.md": "main skill file",
    "README.md": "project readme",
    "CHANGELOG.md": "version history",
    "CONTRIBUTING.md": "contribution guidelines",
    "LICENSE": "license file",
    "examples/remote_sensing_segmentation_examples.md": "remote sensing examples",
    "examples/engineering_design_examples.md": "engineering design examples",
    "evals/test_prompts.md": "test prompts",
    "evals/expected_checkpoints.md": "expected checkpoints",
    "evals/checkpoints.json": "JSON checkpoints for test scoring",
    "docs/anti_patterns.md": "anti-patterns documentation",
    "docs/variable_cards.md": "variable cards",
    "scripts/validate_skill_package.py": "package validator",
    "scripts/check_response_against_checkpoints.py": "test scoring script",
    "scripts/sync_claude_skill.py": "sync script for .claude SKILL.md copy",
    "docs/baseline_defect_taxonomy.md": "baseline defect taxonomy (10 types)",
    "docs/module_cards.md": "module cards (15 modules)",
    "docs/baseline_evolution_workflow.md": "baseline evolution workflow",
    "examples/baseline_evolution_examples.md": "baseline evolution examples",
    "AGENTS.md": "Codex agent manifest",
    "CLAUDE.md": "Claude project entry",
    "install/install.sh": "Unix install script",
    "install/install.ps1": "Windows install script",
    "install/install_codex.sh": "Codex Unix install",
    "install/install_codex.ps1": "Codex Windows install",
    "install/install_claude.sh": "Claude Unix install",
    "install/install_claude.ps1": "Claude Windows install",
    "install/README.md": "install guide",
    "install/verify_installation.py": "install verification script",
    ".github/workflows/release.yml": "GitHub release workflow",
    ".codex/skills/thinking-essence-extraction/SKILL.md": "Codex skill copy",
}

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
    skill_path = os.path.join(ROOT, "SKILL.md")
    if not os.path.exists(skill_path):
        return ["MISSING: SKILL.md (cannot check frontmatter)"]

    with open(skill_path, encoding="utf-8") as f:
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
    ]
    for section in required_sections:
        if f"## {section}" not in content:
            errors.append(f"SKILL.md: missing section '{section}'")

    # Check forbidden phrases are present
    forbidden = ["增强语义信息", "提升表达能力", "加强特征融合"]
    for phrase in forbidden:
        if phrase not in content:
            errors.append(f"SKILL.md: missing forbidden phrase '{phrase}'")

    # Check version field
    if "version:" not in frontmatter if match else "":
        errors.append("SKILL.md: frontmatter missing 'version:' field")

    return errors


def check_file_nonempty(rel_path: str, min_chars: int = 100) -> List[str]:
    errors = []
    full_path = os.path.join(ROOT, rel_path)
    if os.path.exists(full_path) and os.path.getsize(full_path) < min_chars:
        errors.append(f"TOO_SHORT: {rel_path} (< {min_chars} chars)")
    return errors


def check_claude_skill_copy() -> List[str]:
    """Check that SKILL.md is available at .claude/skills/ for auto-discovery."""
    errors = []
    claude_skill = os.path.join(
        ROOT, ".claude", "skills", "thinking-essence-extraction", "SKILL.md"
    )
    if not os.path.exists(claude_skill):
        errors.append(
            "MISSING: .claude/skills/thinking-essence-extraction/SKILL.md "
            "(required for Claude Code auto-discovery)"
        )
    return errors


def check_claude_skill_sync() -> List[str]:
    """Check root SKILL.md is in sync with .claude copy."""
    errors = []
    root_skill = os.path.join(ROOT, "SKILL.md")
    claude_skill = os.path.join(
        ROOT, ".claude", "skills", "thinking-essence-extraction", "SKILL.md"
    )
    if not os.path.exists(root_skill) or not os.path.exists(claude_skill):
        return errors
    with open(root_skill, encoding="utf-8") as f:
        root_content = f.read()
    with open(claude_skill, encoding="utf-8") as f:
        claude_content = f.read()
    if root_content != claude_content:
        errors.append(
            "SYNC_ERROR: root SKILL.md and .claude/skills/thinking-essence-extraction/SKILL.md differ. "
            "Run `python scripts/sync_claude_skill.py` to sync."
        )
    return errors


def check_no_ide_files() -> List[str]:
    """Check that IDE files are not committed (should be in .gitignore)."""
    errors = []
    idea_dir = os.path.join(ROOT, ".idea")
    if os.path.exists(idea_dir):
        # Check if there are tracked files under .idea
        # This is advisory; actual enforcement is via .gitignore
        for f in os.listdir(idea_dir):
            fp = os.path.join(idea_dir, f)
            if os.path.isfile(fp):
                rel = os.path.join(".idea", f)
                errors.append(
                    f"WARNING: {rel} exists locally. Ensure .gitignore excludes it."
                )
                break  # one warning is enough
    return errors


def main():
    errors = []

    # 1. Check required files exist
    for rel_path, description in REQUIRED_FILES.items():
        errors.extend(check_file_exists(rel_path, description))
        errors.extend(check_file_nonempty(rel_path))

    # 2. Validate SKILL.md content
    errors.extend(check_skill_frontmatter())

    # 3. Check Claude Code skill copy exists and is in sync
    errors.extend(check_claude_skill_copy())
    errors.extend(check_claude_skill_sync())

    # 4. Check for IDE files (advisory only, not blocking)
    warnings = check_no_ide_files()

    # 5. Summary
    if errors:
        print("=== VALIDATION FAILED ===\n")
        for err in errors:
            print(f"  - {err}")
        print(f"\n{len(errors)} issue(s) found.")
        sys.exit(1)
    else:
        print("=== VALIDATION PASSED ===\n")
        print("All files present, SKILL.md structure valid, Claude Code copy exists.")
        if warnings:
            print("\nWarnings (non-blocking):")
            for w in warnings:
                print(f"  - {w}")
        sys.exit(0)


if __name__ == "__main__":
    main()
