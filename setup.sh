#!/usr/bin/env bash
# boss-mode skill setup — installs and configures SKILL.md

case "$(uname -s)" in
    Darwin*) SED_ARGS=("-i" "") ;;    # macOS BSD sed
    *)       SED_ARGS=("-i") ;;       # Linux / Git Bash
esac

SKILL_DIR="$HOME/.claude/skills/boss-mode"
TARGET="$SKILL_DIR/SKILL.md"

mkdir -p "$SKILL_DIR"
cp SKILL.md "$TARGET" 2>/dev/null || {
    echo "Error: SKILL.md not found in current directory."
    exit 1
}

echo "=== boss-mode skill setup ==="
echo ""

read -r -p "DeepSeek worker command (e.g. python ~/workers/deepseek.py) [press Enter to skip]: " DS
read -r -p "Groq worker command   (e.g. python ~/workers/groq.py)   [press Enter to skip]: " GQ
read -r -p "Ollama command        (default: ollama run llama3.2)       [press Enter to keep default]: " OL

[[ -n "$DS" ]] && sed "${SED_ARGS[@]}" "s|python /path/to/your/deepseek_worker.py|$DS|g" "$TARGET"
[[ -n "$GQ" ]] && sed "${SED_ARGS[@]}" "s|python /path/to/your/groq_worker.py|$GQ|g" "$TARGET"
[[ -n "$OL" ]] && sed "${SED_ARGS[@]}" "s|ollama run llama3.2|$OL|g" "$TARGET"

echo ""
echo "✓ boss-mode skill installed to $TARGET"
echo "  Restart Claude Code to load the skill."
