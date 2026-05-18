#!/usr/bin/env bash
# install_claude.sh — Install thinking-essence-extraction for Claude Code (Unix)
set -euo pipefail

REPO_URL="https://github.com/<your-org>/thinking-essence-extraction"
BRANCH="main"
TARGET="${1:-.}"
TARGET="$(cd "$TARGET" 2>/dev/null && pwd || echo "$TARGET")"

echo "Installing thinking-essence-extraction for Claude Code → $TARGET"

mkdir -p "$TARGET/.claude/skills/thinking-essence-extraction"
curl -sL "$REPO_URL/raw/$BRANCH/.claude/skills/thinking-essence-extraction/SKILL.md" \
  -o "$TARGET/.claude/skills/thinking-essence-extraction/SKILL.md"
curl -sL "$REPO_URL/raw/$BRANCH/CLAUDE.md" -o "$TARGET/CLAUDE.md"

echo "Done. Test with: claude \"用本质变量抽取分析：1×1 卷积的本质是什么？\""
