#!/usr/bin/env bash
# install.sh — Full install (Codex + Claude) for Unix (macOS/Linux)
set -euo pipefail

REPO_URL="https://github.com/HuLi-12/thinking-essence-extraction"
BRANCH="master"
TARGET="${1:-.}"

echo "Installing thinking-essence-extraction skill to: $TARGET"
echo ""

# Resolve target to absolute path
TARGET="$(cd "$TARGET" 2>/dev/null && pwd || echo "$TARGET")"

# --- Codex ---
echo "[1/4] Installing Codex files..."
mkdir -p "$TARGET/.codex/skills/thinking-essence-extraction/docs"
mkdir -p "$TARGET/.codex/skills/thinking-essence-extraction/examples"
mkdir -p "$TARGET/.codex/skills/thinking-essence-extraction/evals"

# Download from GitHub
for file in SKILL.md; do
  curl -fsSL "$REPO_URL/raw/$BRANCH/$file" -o "$TARGET/.codex/skills/thinking-essence-extraction/$file"
done
for file in variable_cards.md anti_patterns.md baseline_defect_taxonomy.md module_cards.md baseline_evolution_workflow.md; do
  curl -fsSL "$REPO_URL/raw/$BRANCH/docs/$file" -o "$TARGET/.codex/skills/thinking-essence-extraction/docs/$file"
done
for file in remote_sensing_segmentation_examples.md engineering_design_examples.md baseline_evolution_examples.md; do
  curl -fsSL "$REPO_URL/raw/$BRANCH/examples/$file" -o "$TARGET/.codex/skills/thinking-essence-extraction/examples/$file"
done
for file in checkpoints.json; do
  curl -fsSL "$REPO_URL/raw/$BRANCH/evals/$file" -o "$TARGET/.codex/skills/thinking-essence-extraction/evals/$file"
done
echo "  Codex files installed."

# Copy or download AGENTS.md
if [ -f "AGENTS.md" ]; then
  cp AGENTS.md "$TARGET/AGENTS.md" 2>/dev/null || true
fi
curl -fsSL "$REPO_URL/raw/$BRANCH/AGENTS.md" -o "$TARGET/AGENTS.md"
echo "  AGENTS.md installed."

# --- Claude ---
echo "[2/4] Installing Claude files..."
mkdir -p "$TARGET/.claude/skills/thinking-essence-extraction"
curl -fsSL "$REPO_URL/raw/$BRANCH/.claude/skills/thinking-essence-extraction/SKILL.md" \
  -o "$TARGET/.claude/skills/thinking-essence-extraction/SKILL.md"

if [ -f "CLAUDE.md" ]; then
  cp CLAUDE.md "$TARGET/CLAUDE.md" 2>/dev/null || true
fi
curl -fsSL "$REPO_URL/raw/$BRANCH/CLAUDE.md" -o "$TARGET/CLAUDE.md"
echo "  Claude files installed."

# --- Verify ---
echo "[3/4] Verifying installation..."
MISSING=0
for f in "$TARGET/.codex/skills/thinking-essence-extraction/SKILL.md" \
         "$TARGET/.claude/skills/thinking-essence-extraction/SKILL.md" \
         "$TARGET/AGENTS.md" "$TARGET/CLAUDE.md"; do
  if [ ! -f "$f" ]; then
    echo "  MISSING: $f"
    MISSING=$((MISSING + 1))
  fi
done
if [ "$MISSING" -eq 0 ]; then
  echo "  All core files present."
fi

# --- Summary ---
echo "[4/4] Installation complete."
echo ""
echo "  Codex:   codex \"用本质变量抽取分析：1×1 卷积的本质是什么？\""
echo "  Claude:  claude \"用本质变量抽取分析：1×1 卷积的本质是什么？\""
echo ""
if [ "$MISSING" -gt 0 ]; then
  echo "  WARNING: $MISSING file(s) missing. Check network connection."
  exit 1
fi
