#!/usr/bin/env python3
"""Sync root SKILL.md to .claude/skills/thinking-essence-extraction/SKILL.md."""

import os
import sys
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "SKILL.md")
DST = os.path.join(ROOT, ".claude", "skills", "thinking-essence-extraction", "SKILL.md")


def main():
    if not os.path.exists(SRC):
        print("ERROR: root SKILL.md not found")
        sys.exit(1)

    os.makedirs(os.path.dirname(DST), exist_ok=True)
    shutil.copy2(SRC, DST)
    print(f"Synced: {SRC} -> {DST}")


if __name__ == "__main__":
    main()
