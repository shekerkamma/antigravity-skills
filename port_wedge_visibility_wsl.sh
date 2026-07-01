#!/bin/bash
echo "Porting Agentic Wedge Visibility Skill to WSL Environments (Claude Code / Codex)..."

# Define the source directory (Windows path mapped in WSL)
SOURCE_DIR="/mnt/d/New folder/Antigravity-test/antigravity-skills/.agents/skills/agentic-wedge-visibility"

if [ ! -d "$SOURCE_DIR" ]; then
    echo "Warning: Source path '$SOURCE_DIR' not found. Ensure you are running this from within WSL."
    exit 1
fi

# Create target directories
mkdir -p ~/.claude/skills/agentic-wedge-visibility
mkdir -p ~/.codex/skills/agentic-wedge-visibility

# Copy the skill directory contents
cp -r "$SOURCE_DIR/"* ~/.claude/skills/agentic-wedge-visibility/
cp -r "$SOURCE_DIR/"* ~/.codex/skills/agentic-wedge-visibility/

echo "Porting complete. The agentic-wedge-visibility skill is now available in your WSL hosts."
