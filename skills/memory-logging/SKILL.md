---
name: memory-logging
description: Mandatory skill for oh-my-gemini-slim. Use this to document session changes, architectural decisions, and bug fixes into the `memory/` directory. Trigger this at the end of every significant task or session.
---

# Memory Logging Skill

You are responsible for maintaining the long-term project memory by documenting every significant change, decision, and fix.

## When to Use
- **HARD RULE**: You MUST use this skill at the end of every task or session.
- Use it after completing a feature, fixing a bug, or refactoring code.
- Use it when a new architectural pattern is established.

## Workflow

### Step 1: Analyze Changes
Review the current session's history and `git diff` to identify:
- What files were modified/added/deleted.
- The rationale behind the changes.
- Any new assumptions or technical debt introduced.

### Step 2: Determine Log Destination
1. Check the `memory/` directory for existing logs.
2. If the task is a continuation of an existing log (e.g., "Phase 2" of a migration), **append** to that log.
3. If it is a new task or a distinct fix, **create a new file** using the naming convention: `NN_descriptive_name.md` (e.g., `06_memory_logging_skill.md`).

### Step 3: Write the Log
The log MUST follow this structure:

```markdown
# Session Log NN: [Descriptive Title]

## Overview
Brief 1-2 sentence summary of what was accomplished in this session.

## Changes
- **Component A**: Detailed list of changes.
- **Component B**: Detailed list of changes.

## Rationale
Explain WHY these changes were made and any technical trade-offs considered.

## Verification
List the commands or tests run to prove the changes work.

## Metadata (Mandatory for Knowledge Graph)
Add this JSON block at the very end of the file. It is used by the system to build a structured graph of project history.

```json
{
  "session_id": "NN",
  "title": "[Descriptive Title]",
  "date": "YYYY-MM-DD",
  "agent": "[Agent Name]",
  "nodes": [
    {"id": "task_id", "type": "Task", "label": "Short description"},
    {"id": "file_path", "type": "File", "label": "filename"},
    {"id": "decision_id", "type": "Decision", "label": "The decision"}
  ],
  "edges": [
    {"from": "session_id", "to": "task_id", "type": "EXECUTED"},
    {"from": "task_id", "to": "file_path", "type": "MODIFIED"},
    {"from": "decision_id", "to": "task_id", "type": "RATIONALE_FOR"}
  ]
}
```
```

## PowerShell Constraint
When executing shell commands to write or move files, **ALWAYS use `;`** as a statement separator. **NEVER use `&&`**, as it is not supported in the user's PowerShell environment.

Example: `mkdir temp ; cp file.txt temp/`
