import os
import shutil
from pathlib import Path

source_dir = Path(os.path.expanduser("~/.claude/skills"))
target_dir = Path("/mnt/c/Users/sheke/.gemini/config/skills")

print(f"WSL Source directory: {source_dir}")
print(f"Windows Target directory: {target_dir}")

if not source_dir.exists():
    print(f"Error: Source directory {source_dir} does not exist.")
    exit(1)

target_dir.mkdir(parents=True, exist_ok=True)

copied_count = 0
skipped_count = 0

for item in source_dir.iterdir():
    # Resolve the path to follow symlinks to their actual targets
    try:
        resolved_item = item.resolve()
    except Exception as e:
        print(f"Error resolving symlink {item.name}: {e}")
        skipped_count += 1
        continue
    
    if not resolved_item.is_dir():
        continue
        
    if item.name.startswith("google-agents-cli-"):
        print(f"Skipping {item.name} (google-agents-cli package)")
        skipped_count += 1
        continue
        
    # Check if SKILL.md exists in the resolved directory
    skill_file = resolved_item / "SKILL.md"
    if not skill_file.exists():
        print(f"Skipping {item.name} (no SKILL.md found in {resolved_item})")
        skipped_count += 1
        continue

    dest_item = target_dir / item.name
    print(f"Copying {item.name} (from {resolved_item}) to {dest_item}...")
    
    try:
        if dest_item.exists():
            if dest_item.is_symlink() or dest_item.is_file():
                dest_item.unlink()
            else:
                shutil.rmtree(dest_item)
        
        # Copy content, resolving symlinks inside the folder as well
        shutil.copytree(resolved_item, dest_item, symlinks=False)
        print(f"Successfully copied {item.name}")
        copied_count += 1
    except Exception as e:
        print(f"Error copying {item.name}: {e}")

print(f"\nDone! Copied: {copied_count}, Skipped: {skipped_count}")
