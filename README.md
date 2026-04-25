# oh-my-gemini-slim

`oh-my-gemini-slim` is a Python-based utility that bootstraps a powerful, multi-agent ecosystem directly into your Gemini CLI environment. It deploys pre-configured expert subagents, complex codebase skills, lifecycle hooks, and MCP servers seamlessly.

## Acknowledgements & Credits

**This project is a direct Python fork and port of the original [oh-my-opencode-slim](https://github.com/alvinunreal/oh-my-opencode-slim) by alvinunreal.** 

The original TS architecture, system prompts, skills (like `codemap` and `simplify`), and overarching agent logic (The Pantheon) were conceived by the OpenCode authors. `oh-my-gemini-slim` simply bridges that brilliance natively into the Python/Gemini CLI ecosystem.

## Features

- **The Pantheon (Agents)**: Deploys 6 pre-configured expert subagents (`@explorer`, `@oracle`, `@librarian`, `@fixer`, `@designer`, `@observer`).
- **Skills**: Integrates complex markdown-based rulebooks (e.g., `codemap`, `simplify`) so agents know exactly how to map out and refactor codebases.
- **Hooks**: Injects lifecycle event scripts (like TODO continuations and phase reminders) into Gemini CLI.
- **Advanced Knowledge Graph Memory**: Automates session persistence using a queryable SQLite database, allowing agents to 'recall' past decisions and file history.
- **MCP Auto-Configuration**: Safely registers `context7` directly into your `mcp_config.json`.

### Memory Skills

- **`memory-logging`**: Automatically captures structured JSON metadata (tasks, decisions, modified files) at the end of every session and saves it to the `memory/` directory.
- **`memory-query`**: Empowers agents to use the `querier.py` tool to retrieve historical context, such as why a specific file was changed or what architectural decisions were made.

### Memory Architecture

The system employs a **Markdown-to-SQLite indexing pipeline** to ensure long-term project awareness:

1.  **Capture**: Agents use the `memory-logging` skill to write session logs in Markdown with embedded JSON metadata.
2.  **Index**: After every session, a Gemini CLI hook (`knowledge-graph-indexer`) automatically triggers `indexer.py`.
3.  **Store**: `indexer.py` parses the new logs and updates a centralized Knowledge Graph in `memory/memory.db`.
4.  **Recall**: Agents use the `memory-query` skill to search this graph via `querier.py` for instant project context.

## Installation

### Method 1: Native Gemini CLI Extension (Recommended)

This project is now a native Gemini CLI extension. You can install it directly from the marketplace or link it locally for development.

**Local Linking (Beta/Testing):**
```bash
# 1. Clone the repository
git clone https://github.com/vishalrajv/oh-my-gemini-slim.git
cd oh-my-gemini-slim

# 2. Link the extension
gemini extensions link . --consent
```

**Direct Installation from GitHub:**
```bash
gemini extensions install vishalrajv/oh-my-gemini-slim --consent
```

**Marketplace Installation:**
Once published, you can install it using:
```bash
gemini extensions install oh-my-gemini-slim
```

### Method 2: Python CLI Installer (Backup/Fallback)

If you prefer the classic installation method, you can still use the `omg` tool.

```bash
# 1. Install the CLI package locally in editable mode
pip install -e .

# 2. Deploy the ecosystem
omg init
```

During initialization, you can choose to deploy **Globally** (`~/.gemini/`) or **Local** to the current directory (`./.gemini/`).

## Usage

Check your active deployment:
```bash
omg ping
```

If you ever wish to remove the ecosystem:
```bash
omg uninstall
```
