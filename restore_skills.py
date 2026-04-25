# Developer: Vishal Raj V, Senior Engineer
import os
from pathlib import Path

def restore_skills():
    source_base = Path("oh-my-opencode-slim/src/skills")
    target_base = Path("oh_my_gemini_slim/skills")

    files_to_restore = [
        "codemap/SKILL.md",
        "codemap/README.md",
        "codemap/codemap.md",
        "codemap/scripts/codemap.mjs",
        "codemap/scripts/codemap.test.ts",
        "simplify/SKILL.md",
        "simplify/README.md",
        "simplify/codemap.md"
    ]

    for rel_path in files_to_restore:
        src = source_base / rel_path
        dest = target_base / rel_path
        
        if not src.exists():
            print(f"Source missing: {src}")
            continue
            
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        content = src.read_text(encoding="utf-8")
        # Apply replacements
        content = content.replace(".slim", ".gemini")
        content = content.replace("OpenCode", "Gemini CLI")
        
        dest.write_text(content, encoding="utf-8")
        print(f"Restored: {dest} ({len(content)} bytes)")

if __name__ == "__main__":
    restore_skills()
