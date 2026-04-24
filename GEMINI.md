# Developer Context: oh-my-gemini-cli

**Project Purpose:**
`oh-my-gemini-cli` is a Python-based utility (`omg` command) designed to bootstrap a powerful, multi-agent ecosystem directly into a developer's Gemini CLI environment. This project is a direct fork and Python port of the original `oh-my-opencode-slim` architecture.

## Architectural Setup
This is NOT a runtime orchestrator. Gemini CLI naturally handles multi-agent orchestration via its native `.md` template routing. This project acts purely as a **deployment engine**.

**Core Directories to Know:**
- `oh_my_gemini_cli/agents/`: Contains the Markdown templates (`oracle.md`, `explorer.md`, etc.) defining the personalities and strict behaviors of specialized subagents.
- `oh_my_gemini_cli/skills/`: Contains the Markdown and Javascript files for complex agent abilities (like `codemap` and `simplify`).
- `oh_my_gemini_cli/hooks/`: Contains executable Python scripts (`pre-prompt`, `post-run`) that enforce system rules during a Gemini CLI session.
- `oh_my_gemini_cli/cli.py`: The heart of the installer. It securely copies the above assets into the user's `~/.gemini/` (Global) or `./.gemini/` (Local) directories based on user input.

## Developer Rules
- **Python**: Uses `click` for CLI argument parsing.
- **Paths**: When adding new assets, ensure they are strictly mapped in the `cli.py` deployment/uninstallation loops.
- **Dependencies**: Native standard library + `click`. Keep it lean.
- **Agent Prompts**: If editing an agent's prompt, modify the source `.md` file inside `oh_my_gemini_cli/agents/` and then run `omg init` to deploy it.
- **Memory Logging**: HARD RULE. At the end of every significant session or task, you MUST generate or append a Markdown log inside the `memory/` folder detailing what was changed and why. Future sessions rely on this folder for context.
