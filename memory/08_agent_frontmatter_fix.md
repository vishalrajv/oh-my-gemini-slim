# Agent Frontmatter Fix (YAML Schema Alignment)

## Issue
Agent templates contained a `skills:` key in their YAML frontmatter. This key is not recognized by Gemini CLI's agent definition schema, leading to validation errors during agent loading.

## Fix
1.  **Removed `skills:` key**: Stripped the invalid `skills` field from the YAML frontmatter of all agent templates in `agents/`:
    - `designer.md`
    - `explorer.md`
    - `fixer.md`
    - `librarian.md`
    - `observer.md`
    - `oracle.md`
2.  **Verified System Prompt**: Confirmed that the **HARD RULE** instructing agents to use the `memory-logging` skill remains at the end of each agent's system prompt. This ensures the skill is still triggered even without the frontmatter key.
3.  **Local Deployment Sync**: Manually synchronized the fixed templates to the local project deployment directory `.gemini/agents/` to resolve immediate loading errors in the current workspace.

## Verification
- Grep search confirmed no `skills:` keys remain in `agents/*.md`.
- Manual inspection of both source templates and local `.gemini/agents/` files confirmed valid YAML and presence of the `memory-logging` instruction.
