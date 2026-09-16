#!/bin/bash
echo "Porting book-to-skill, deepgrid-mature-silicon, and deepgrid-sku-compendium to WSL / Linux Hosts..."

SOURCE_DIR="/mnt/d/New folder/Antigravity-test/antigravity-skills/.agents/skills"

if [ ! -d "$SOURCE_DIR" ]; then
    echo "Warning: Source path '$SOURCE_DIR' not found."
    exit 1
fi

SKILLS=(
    "book-to-skill"
    "deepgrid-architecture"
    "deepgrid-datasheet-qfn64"
    "deepgrid-dg32-2dom"
    "deepgrid-dg32-lite-ai"
    "deepgrid-dshot-bidir"
    "deepgrid-mature-silicon"
    "deepgrid-sku-compendium"
)

TARGET_ROOTS=(
    "$HOME/.claude/skills"
    "$HOME/.codex/skills"
    "$HOME/.agents/skills"
    "$HOME/.copilot/skills"
    "$HOME/.hermes/skills"
    "$HOME/.config/agents/skills"
)

for TARGET in "${TARGET_ROOTS[@]}"; do
    mkdir -p "$TARGET"
    for SKILL in "${SKILLS[@]}"; do
        if [ -d "$SOURCE_DIR/$SKILL" ]; then
            mkdir -p "$TARGET/$SKILL"
            cp -r "$SOURCE_DIR/$SKILL/"* "$TARGET/$SKILL/"
            echo "Ported $SKILL -> $TARGET/$SKILL"
        fi
    done
done

echo "WSL Porting completed successfully."
