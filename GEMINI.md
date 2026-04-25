# Developer Context: oh-my-gemini-slim

**Project Purpose:**
`oh-my-gemini-slim` is a Python-based utility (`omg` command) designed to bootstrap a powerful, multi-agent ecosystem directly into a developer's Gemini CLI environment. This project is a direct fork and Python port of the original `oh-my-opencode-slim` architecture.

## Architectural Setup
This is NOT a runtime orchestrator. Gemini CLI naturally handles multi-agent orchestration via its native `.md` template routing. This project acts purely as a **deployment engine**.

**Core Directories to Know:**
- `agents/`: Contains the Markdown templates (`oracle.md`, `explorer.md`, etc.) defining the personalities and strict behaviors of specialized subagents.
- `skills/`: Contains the Markdown and Javascript files for complex agent abilities (like `codemap` and `simplify`).
- `hooks/`: Contains executable Python scripts (`pre-prompt`, `post-run`) that enforce system rules during a Gemini CLI session.
- `oh_my_gemini_slim/cli.py`: The heart of the installer. It securely copies the above assets into the user's `~/.gemini/` (Global) or `./.gemini/` (Local) directories based on user input.

## Developer Rules
- **Python**: Uses `click` for CLI argument parsing.
- **Paths**: When adding new assets, ensure they are strictly mapped in the `cli.py` deployment/uninstallation loops.
- **Dependencies**: Native standard library + `click`. Keep it lean.
- **Agent Prompts**: If editing an agent's prompt, modify the source `.md` file inside `agents/` and then run `omg init` to deploy it.

## Mandatory Workflow Rules (CRITICAL)

- **Memory Logging**: **HARD RULE.** At the end of every significant session or task, you MUST activate the `memory-logging` skill and generate or append a Markdown log inside the `memory/` folder.
- **Structured Metadata**: Every log MUST include a valid JSON block for the Knowledge Graph. See [KNOWLEDGE_GRAPH.md](./KNOWLEDGE_GRAPH.md) for schema details.
- **Contextual Recall**: You can "remember" project history by using the `memory-query` skill. Use it to find who changed a file, why a decision was made, or search for past session topics.
- **PowerShell Safety**: You are working in a Windows PowerShell environment. **NEVER use `&&`** to concatenate commands. **ALWAYS use `;`** as the statement separator.

## Knowledge Graph Maintenance

The project history is persisted in a structured SQLite database. Developers must ensure the integrity of this graph:
- **Indexing**: After adding new session logs, run `python -m oh_my_gemini_slim.indexer` to update the graph.
- **Querying**: Use `python -m oh_my_gemini_slim.querier <command>` for manual history inspection.
- **Schema**: Refer to [KNOWLEDGE_GRAPH.md](./KNOWLEDGE_GRAPH.md) for a deep-dive into the nodes, edges, and retrieval logic.

## Recent Fixes
- **Agent Loading Errors**: Fixed outdated OpenCode tool names in agent templates to match valid Gemini CLI tools. See memory/02_agent_loading_fix.md for details.
