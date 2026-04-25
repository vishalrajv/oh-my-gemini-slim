# Developer: Vishal Raj V, Senior Engineer
import os
import shutil
import json
import click
import threading
import sys
from pathlib import Path

def ask_mode(action="Installation"):
    prompt_text = (
        f"\n{action} Modes:\n"
        "1. Global (Applies to ~/.gemini for all projects)\n"
        "2. Local  (Applies to current project directory ./.gemini)\n"
        "Please select an option (1 or 2): "
    )
    for _ in range(3):
        choice = input(prompt_text).strip()
        if choice == '1':
            return 'global'
        elif choice == '2':
            return 'local'
        else:
            print("Error: Invalid option. Please type 1 or 2.")
    
    print(f"Aborting {action.lower()} after 3 invalid attempts.")
    sys.exit(1)

@click.group()
def main():
    """oh-my-gemini-cli: A toolkit for Gemini CLI subagents."""
    pass

@main.command()
def init():
    """Initialize the oh-my-gemini-cli ecosystem."""
    mode = ask_mode("Installation")
    is_global = mode == 'global'
    
    gemini_base = Path.home() / ".gemini" if is_global else Path.cwd() / ".gemini"
    agents_base = Path.home() / ".agents" if is_global else Path.cwd() / ".agents"
    
    # 1. Install Agents
    gemini_agents_dir = gemini_base / "agents"
    gemini_agents_dir.mkdir(parents=True, exist_ok=True)
    source_agents_dir = Path(__file__).parent.parent / "agents"
    
    click.echo(f"\nInstalling subagents into {gemini_agents_dir}...")
    for md_file in source_agents_dir.glob("*.md"):
        shutil.copy(md_file, gemini_agents_dir / md_file.name)
        click.echo(f"  -> Installed {md_file.name}")
        
    # 2. Install Skills
    gemini_skills_dir = agents_base / "skills"
    gemini_skills_dir.mkdir(parents=True, exist_ok=True)
    source_skills_dir = Path(__file__).parent.parent / "skills"
    
    click.echo(f"\nInstalling skills into {gemini_skills_dir}...")
    if source_skills_dir.exists():
        for item in source_skills_dir.iterdir():
            dest = gemini_skills_dir / item.name
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy(item, dest)
            click.echo(f"  -> Installed skill: {item.name}")

    # 3. Install Hooks
    gemini_hooks_dir = gemini_base / "hooks"
    gemini_hooks_dir.mkdir(parents=True, exist_ok=True)
    source_hooks_dir = Path(__file__).parent.parent / "hooks"
    
    click.echo(f"\nInstalling hooks into {gemini_hooks_dir}...")
    if source_hooks_dir.exists():
        for py_file in source_hooks_dir.glob("*.py"):
            shutil.copy(py_file, gemini_hooks_dir / py_file.name)
            click.echo(f"  -> Installed hook: {py_file.name}")
            
    # 4. Configure MCP
    click.echo("\nConfiguring MCP Servers...")
    antigravity_dir = gemini_base / "antigravity"
    antigravity_dir.mkdir(parents=True, exist_ok=True)
    mcp_config_file = antigravity_dir / "mcp_config.json"
    
    mcp_config = {"mcpServers": {}}
    if mcp_config_file.exists():
        try:
            mcp_config = json.loads(mcp_config_file.read_text())
        except json.JSONDecodeError:
            pass
            
    if "mcpServers" not in mcp_config:
        mcp_config["mcpServers"] = {}
        
    mcp_config["mcpServers"]["context7"] = {
        "command": "npx",
        "args": ["-y", "context7"]
    }
    
    mcp_config_file.write_text(json.dumps(mcp_config, indent=2))
    click.echo("  -> Successfully registered context7 in mcp_config.json")
        
    click.echo("\nInitialization complete! Ecosystem is ready.")


@main.command()
def uninstall():
    """Remove the oh-my-gemini-cli ecosystem from your setup."""
    mode = ask_mode("Uninstallation")
    is_global = mode == 'global'
    gemini_base = Path.home() / ".gemini" if is_global else Path.cwd() / ".gemini"
    agents_base = Path.home() / ".agents" if is_global else Path.cwd() / ".agents"
    
    # Files to remove
    agents_to_remove = ['designer.md', 'explorer.md', 'fixer.md', 'librarian.md', 'observer.md', 'oracle.md']
    skills_to_remove = ['codemap', 'codemap.md', 'simplify']
    hooks_to_remove = ['post-run-todo.py', 'pre-prompt-phase.py']
    
    click.echo(f"\nUninstalling from {mode} environment...")
    
    for agent in agents_to_remove:
        agent_path = gemini_base / "agents" / agent
        if agent_path.exists():
            agent_path.unlink()
            click.echo(f"  -> Removed {agent}")
            
    for skill in skills_to_remove:
        skill_path = agents_base / "skills" / skill
        if skill_path.exists():
            if skill_path.is_dir():
                shutil.rmtree(skill_path)
            else:
                skill_path.unlink()
            click.echo(f"  -> Removed {skill}")
            
    for hook in hooks_to_remove:
        hook_path = gemini_base / "hooks" / hook
        if hook_path.exists():
            hook_path.unlink()
            click.echo(f"  -> Removed {hook}")
            
    mcp_config_file = gemini_base / "antigravity" / "mcp_config.json"
    if mcp_config_file.exists():
        try:
            mcp_config = json.loads(mcp_config_file.read_text())
            if "context7" in mcp_config.get("mcpServers", {}):
                del mcp_config["mcpServers"]["context7"]
                mcp_config_file.write_text(json.dumps(mcp_config, indent=2))
                click.echo("  -> Unregistered context7 from mcp_config.json")
        except json.JSONDecodeError:
            pass
            
    click.echo("Uninstall complete.")


@main.command()
def ping():
    """Ping the agents to check status."""
    click.echo("Ping command running... verifying installed agents.\n")
    
    global_dir = Path.home() / ".gemini" / "agents"
    local_dir = Path.cwd() / ".gemini" / "agents"
    
    def check_agents(directory, label):
        click.echo(f"[{label} Environment]: {directory}")
        if not directory.exists():
            click.echo("  -> Not installed or directory missing.")
            return
        agents = list(directory.glob("*.md"))
        if not agents:
            click.echo("  -> Directory exists but no agent files found.")
        else:
            for agent in agents:
                click.echo(f"  [OK] {agent.stem} is ready.")
                
    check_agents(global_dir, "GLOBAL")
    click.echo("")
    check_agents(local_dir, "LOCAL")

if __name__ == "__main__":
    main()
