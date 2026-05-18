#!/usr/bin/env bash
# install_codex.sh — Install thinking-essence-extraction for Codex CLI (Unix)
set -euo pipefail

REPO_URL="https://github.com/<your-org>/thinking-essence-extraction"
BRANCH="main"
TARGET="${1:-.}"
TARGET="$(cd "$TARGET" 2>/dev/null && pwd || echo "$TARGET")"

echo "Installing thinking-essence-extraction for Codex CLI → $TARGET"

mkdir -p "$TARGET/.codex/skills/thinking-essence-extraction/docs"
mkdir -p "$TARGET/.codex/skills/thinking-essence-extraction/examples"
mkdir -p "$TARGET/.codex/skills/thinking-essence-extraction/evals"

curl -sL "$REPO_URL/raw/$BRANCH/SKILL.md" -o "$TARGET/.codex/skills/thinking-essence-extraction/SKILL.md"
for file in variable_cards.md anti_patterns.md baseline_defect_taxonomy.md module_cards.md baseline_evolution_workflow.md; do
  curl -sL "$REPO_URL/raw/$BRANCH/docs/$file" -o "$TARGET/.codex/skills/thinking-essence-extraction/docs/$file"
done
for file in remote_sensing_segmentation_examples.md engineering_design_examples.md baseline_evolution_examples.md; do
  curl -sL "$REPO_URL/raw/$BRANCH/examples/$file" -o "$TARGET/.codex/skills/thinking-essence-extraction/examples/$file"
done
curl -sL "$REPO_URL/raw/$BRANCH/evals/checkpoints.json" -o "$TARGET/.codex/skills/thinking-essence-extraction/evals/checkpoints.json"
curl -sL "$REPO_URL/raw/$BRANCH/AGENTS.md" -o "$TARGET/AGENTS.md"

echo "Done. Test with: codex \"用本质变量抽取分析：1×1 卷积的本质是什么？\""
