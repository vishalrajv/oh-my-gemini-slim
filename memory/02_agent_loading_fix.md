# Agent Loading Fix (Porting from opencode-slim)

## Root Cause
We faced agent loading errors upon starting the Gemini CLI session because the agent markdown files in `oh_my_gemini_cli/agents/` were directly ported from `oh-my-opencode-slim`. They contained OpenCode-specific tool names (e.g., `list_dir`, `view_file`, `multi_replace_file_content`, `search_web`, `generate_image`, `read_browser_page`) in their YAML frontmatter. 

Gemini CLI validates tool names against its own built-in tools (like `list_directory`, `read_file`, `replace`, `google_web_search`, `web_fetch`, `run_shell_command`, etc.). Since it did not recognize the OpenCode tool names, the agent loading failed with validation errors.

## Fix
Updated the `tools:` lists in the following agent templates to use valid Gemini CLI equivalents:
- **explorer.md**: `list_dir` -> `list_directory`, `view_file` -> `read_file`, added `glob`.
- **fixer.md**: `multi_replace_file_content` & `replace_file_content` -> `replace`, `write_to_file` -> `write_file`, `view_file` -> `read_file`, added `glob`.
- **librarian.md**: `search_web` -> `google_web_search`, `read_url_content` -> `web_fetch`.
- **designer.md**: `generate_image` & `read_browser_page` -> `run_shell_command`, `web_fetch`.

Also updated the body text of `explorer.md` and `librarian.md` to reference the correct tool names so the LLM doesn't hallucinate invalid tools.

After making the changes to `oh_my_gemini_cli/agents/`, the installation was reapplied to the local project (`.gemini/agents/`) using `.venv/Scripts/python.exe` so the environment picks up the fixed agents.