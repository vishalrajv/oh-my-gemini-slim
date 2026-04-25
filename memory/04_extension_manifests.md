# Task 3.1: Native Extension Manifests

## Changes
- Created `gemini-extension.json` in the project root to define the extension metadata and MCP server configuration.
- Created `hooks/hooks.json` to register the `post-run` and `pre-prompt` Python hooks.

## Rationale
These manifests are required for Gemini CLI to recognize the project as a native extension and execute the included hooks and MCP servers.

## Files Created
- `gemini-extension.json`
- `hooks/hooks.json`
