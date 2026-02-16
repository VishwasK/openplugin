"""Plugin class representing a loaded plugin."""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class AuthConfig(BaseModel):
    """Plugin authentication configuration."""

    type: str = Field(..., description="Auth type: none, api_key, oauth2, smtp")
    flow: Optional[str] = Field(None, description="OAuth flow: authorization_code, client_credentials")
    authorization_url: Optional[str] = Field(None, description="OAuth authorization endpoint")
    token_url: Optional[str] = Field(None, description="OAuth token endpoint")
    scopes: Optional[List[str]] = Field(None, description="Required OAuth scopes")
    pkce_required: Optional[bool] = Field(False, description="Whether PKCE is required")
    credential_fields: Optional[Dict[str, str]] = Field(None, description="Required credential fields and descriptions")


class PluginManifest(BaseModel):
    """Plugin manifest schema."""

    name: str = Field(..., description="Plugin name")
    version: str = Field(..., description="Plugin version")
    description: Optional[str] = Field(None, description="Plugin description")
    author: Optional[str] = Field(None, description="Plugin author")
    homepage: Optional[str] = Field(None, description="Plugin homepage URL")
    repository: Optional[str] = Field(None, description="Plugin repository URL")
    license: Optional[str] = Field(None, description="Plugin license")
    keywords: Optional[List[str]] = Field(None, description="Plugin keywords")
    dependencies: Optional[Dict[str, str]] = Field(None, description="Plugin dependencies")
    mcp_servers: Optional[Dict[str, Any]] = Field(None, description="MCP server configurations")
    auth: Optional[AuthConfig] = Field(None, description="Plugin authentication configuration")


class Plugin:
    """Represents a loaded plugin."""

    def __init__(self, path: Path):
        """Initialize plugin from directory path."""
        self.path = Path(path)
        self.manifest_path = self.path / ".claude-plugin" / "plugin.json"
        self.mcp_config_path = self.path / ".mcp.json"
        
        if not self.manifest_path.exists():
            raise ValueError(f"Plugin manifest not found: {self.manifest_path}")
        
        self._load_manifest()
        self._load_commands()
        self._load_agents()
        self._load_skills()
        self._load_mcp_config()

    def _load_manifest(self) -> None:
        """Load plugin manifest."""
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)
        
        self.manifest = PluginManifest(**manifest_data)
        self.name = self.manifest.name
        self.version = self.manifest.version

    def _load_commands(self) -> None:
        """Load slash commands from commands/ directory."""
        self.commands: Dict[str, str] = {}
        commands_dir = self.path / "commands"
        
        if commands_dir.exists():
            for cmd_file in commands_dir.glob("*.md"):
                cmd_name = cmd_file.stem
                with open(cmd_file, "r", encoding="utf-8") as f:
                    self.commands[cmd_name] = f.read()

    def _load_agents(self) -> None:
        """Load agent definitions from agents/ directory."""
        self.agents: Dict[str, str] = {}
        agents_dir = self.path / "agents"
        
        if agents_dir.exists():
            for agent_file in agents_dir.glob("*.md"):
                agent_name = agent_file.stem
                with open(agent_file, "r", encoding="utf-8") as f:
                    self.agents[agent_name] = f.read()

    def _load_skills(self) -> None:
        """Load skill definitions from skills/ directory."""
        self.skills: Dict[str, str] = {}
        skills_dir = self.path / "skills"
        
        if skills_dir.exists():
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir():
                    skill_file = skill_dir / "SKILL.md"
                    if skill_file.exists():
                        skill_name = skill_dir.name
                        with open(skill_file, "r", encoding="utf-8") as f:
                            self.skills[skill_name] = f.read()

    def _load_mcp_config(self) -> None:
        """Load MCP server configuration."""
        self.mcp_config: Optional[Dict[str, Any]] = None
        
        if self.mcp_config_path.exists():
            with open(self.mcp_config_path, "r", encoding="utf-8") as f:
                self.mcp_config = json.load(f)

    def get_command(self, command_name: str) -> Optional[str]:
        """Get command content by name."""
        return self.commands.get(command_name)

    def get_agent(self, agent_name: str) -> Optional[str]:
        """Get agent definition by name."""
        return self.agents.get(agent_name)

    def get_skill(self, skill_name: str) -> Optional[str]:
        """Get skill definition by name."""
        return self.skills.get(skill_name)

    def get_auth_config(self) -> Optional[AuthConfig]:
        """Get plugin's auth configuration, or None if no auth required."""
        return self.manifest.auth

    def __repr__(self) -> str:
        """String representation."""
        return f"Plugin(name={self.name}, version={self.version}, path={self.path})"
