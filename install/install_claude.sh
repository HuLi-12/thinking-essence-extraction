#!/usr/bin/env bash
# install_claude.sh — Install thinking-essence-extraction for Claude Code (Unix)
set -euo pipefail

REPO_URL="https://github.com/HuLi-12/thinking-essence-extraction"
BRANCH="master"
TARGET="${1:-.}"
TARGET="$(cd "$TARGET" 2>/dev/null && pwd || echo "$TARGET")"

echo "Installing thinking-essence-extraction for Claude Code → $TARGET"

mkdir -p "$TARGET/.claude/skills/thinking-essence-extraction/docs"
mkdir -p "$TARGET/.claude/skills/thinking-essence-extraction/examples"

curl -fsSL "$REPO_URL/raw/$BRANCH/.claude/skills/thinking-essence-extraction/SKILL.md" \
  -o "$TARGET/.claude/skills/thinking-essence-extraction/SKILL.md"
curl -fsSL "$REPO_URL/raw/$BRANCH/CLAUDE.md" -o "$TARGET/CLAUDE.md"

for file in variable_cards.md anti_patterns.md baseline_defect_taxonomy.md module_cards.md baseline_evolution_workflow.md; do
  curl -fsSL "$REPO_URL/raw/$BRANCH/docs/$file" -o "$TARGET/.claude/skills/thinking-essence-extraction/docs/$file"
done
for file in remote_sensing_segmentation_examples.md engineering_design_examples.md baseline_evolution_examples.md; do
  curl -fsSL "$REPO_URL/raw/$BRANCH/examples/$file" -o "$TARGET/.claude/skills/thinking-essence-extraction/examples/$file"
done

echo "Done. Test with: claude \"用本质变量抽取分析：1×1 卷积的本质是什么？\""
