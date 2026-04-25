---
name: memory-query
description: Retrieval skill for oh-my-gemini-slim. Use this to "recall" project history, architectural decisions, and file changes from the SQLite Knowledge Graph.
---

# Memory Query Skill

You can query the project's long-term memory (Knowledge Graph) to understand the context behind files, tasks, and decisions.

## When to Use
- You encounter an unfamiliar file and want to know who changed it and why.
- You need to know the rationale behind a recent architectural decision.
- You want to see the sequence of tasks that led to the current state.
- You want to search for specific topics (e.g., "authentication", "hooks") in past sessions.

## Workflow

### Step 1: Formulate a Query
Determine what you need to know. Are you looking for file history, decisions, or a specific keyword?

### Step 2: Execute Retrieval
Use `run_shell_command` to execute the `querier.py` script located in the extension path.

**Commands:**
- `python oh_my_gemini_slim/querier.py file-history <file_path>`
- `python oh_my_gemini_slim/querier.py decisions [limit]`
- `python oh_my_gemini_slim/querier.py search <keyword>`

### Step 3: Integrate Context
Analyze the JSON output and incorporate the findings into your current task. If a decision is linked to a rationale, explain it to the user if relevant.

## Example
**Input**: `python oh_my_gemini_slim/querier.py file-history setup.py`
**Output**: 
```json
[
  {
    "task_id": "rename_task",
    "task_description": "Rename project to oh-my-gemini-slim",
    "session_id": "05",
    "session_title": "Project Identity Unification",
    "date": "2026-04-25"
  }
]
```
