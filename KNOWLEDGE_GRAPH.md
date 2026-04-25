# Knowledge Graph: Technical Reference

The `oh-my-gemini-cli` ecosystem utilizes a structured Memory System to maintain long-term project context across independent agent sessions. This memory is persisted as Markdown logs in the `memory/` directory and indexed into a SQLite Knowledge Graph for efficient querying.

## Memory Architecture

The system follows a **Write-Then-Index** flow:
1.  **Generation**: At the end of a session, the agent uses the `memory-logging` skill to generate a session log (e.g., `memory/06_memory_logging_fix.md`).
2.  **Structuring**: Each log MUST contain a JSON block in its metadata section.
3.  **Indexing**: The `indexer.py` script parses these JSON blocks and updates the `memory/memory.db` SQLite database.
4.  **Retrieval**: The `querier.py` script (or internal agent logic) queries the database to reconstruct project history, file modifications, and rationale.

## SQLite Schema

The Knowledge Graph is stored in `memory/memory.db` with the following schema:

### Tables

#### `nodes`
Stores the fundamental entities of the project history.
- `id` (TEXT, PK): Unique identifier (e.g., "06", "task_id", "path/to/file").
- `type` (TEXT): The category of the node (Task, File, Decision).
- `label` (TEXT): A human-readable description.

#### `edges`
Defines the relationships between nodes.
- `id` (INTEGER, PK): Auto-incrementing ID.
- `from_id` (TEXT): Source node ID.
- `to_id` (TEXT): Target node ID.
- `type` (TEXT): The nature of the relationship (MODIFIED, EXECUTED, RATIONALE_FOR).
- `UNIQUE(from_id, to_id, type)`: Prevents redundant relationship entries.

#### `sessions`
Tracks individual agent interaction sessions.
- `id` (TEXT, PK): The session number or UUID.
- `title` (TEXT): Summary of the session.
- `date` (TEXT): ISO 8601 date.
- `agent` (TEXT): The agent name (e.g., "Gemini CLI", "fixer").

## Core Entities

### Node Types
- **Task**: A specific action performed during a session (e.g., "Implement SQLite schema").
- **File**: A source code file or configuration modified during the session.
- **Decision**: An architectural or technical choice made (e.g., "Use SQLite instead of JSON for graph storage").

### Edge Types
- **EXECUTED**: Links a `Session` to a `Task`.
- **MODIFIED**: Links a `Task` to a `File`.
- **CREATED**: Links a `Task` to a new `File`.
- **RATIONALE_FOR**: Links a `Decision` to a `Task` or another `Decision`, explaining *why* an action was taken.

## Implementation Logic

### `indexer.py`
The indexer performs a regex-based extraction of the `json` block at the end of each `.md` file in the `memory/` directory. It uses `INSERT OR REPLACE` logic for nodes and sessions to ensure the graph stays synchronized with the source Markdown files.

### `querier.py`
The querier provides specialized methods for graph traversal:
- `get_file_history(path)`: Joins `edges`, `nodes`, and `sessions` to find all tasks that touched a specific file.
- `get_recent_decisions()`: Filters for nodes of type `Decision` linked by `RATIONALE_FOR` edges.
- `search_nodes(keyword)`: Performs a broad keyword search across all node IDs and labels.

## Manual Query Examples

You can interact with the Knowledge Graph directly using the Python interpreter or by running the script:

### 1. View File Modification History
```bash
python -m oh_my_gemini_slim.querier file-history GEMINI.md
```

### 2. Retrieve Recent Architectural Decisions
```bash
python -m oh_my_gemini_slim.querier decisions 5
```

### 3. Search for Specific Tasks or Files
```bash
python -m oh_my_gemini_slim.querier search "memory"
```

---
*Note: Ensure you run `python -m oh_my_gemini_slim.indexer` after adding new session logs to keep the graph up to date.*
