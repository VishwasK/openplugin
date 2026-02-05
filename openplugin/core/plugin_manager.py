"""Plugin manager for loading and managing plugins."""

import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any
from .plugin import Plugin
from ..providers.base import LLMProvider
from ..mcp.client import MCPClient


class PluginManager:
    """Manages plugin discovery, loading, and execution."""

    def __init__(self, plugins_dir: Optional[Path] = None):
        """Initialize plugin manager.
        
        Args:
            plugins_dir: Directory to search for plugins. Defaults to ./plugins
        """
        self.plugins_dir = Path(plugins_dir) if plugins_dir else Path("./plugins")
        self.plugins: Dict[str, Plugin] = {}
        self.mcp_clients: Dict[str, MCPClient] = {}

    def load_plugins(self, plugins_path: Optional[Path] = None) -> List[str]:
        """Load all plugins from the specified directory.
        
        Args:
            plugins_path: Path to plugins directory. Defaults to self.plugins_dir
            
        Returns:
            List of loaded plugin names
        """
        if plugins_path:
            search_path = Path(plugins_path)
        else:
            search_path = self.plugins_dir
        
        if not search_path.exists():
            search_path.mkdir(parents=True, exist_ok=True)
            return []
        
        loaded = []
        for plugin_dir in search_path.iterdir():
            if plugin_dir.is_dir() and not plugin_dir.name.startswith("."):
                try:
                    plugin = Plugin(plugin_dir)
                    self.plugins[plugin.name] = plugin
                    loaded.append(plugin.name)
                    
                    # Initialize MCP client if MCP config exists
                    if plugin.mcp_config:
                        self._initialize_mcp_client(plugin)
                except Exception as e:
                    print(f"Failed to load plugin {plugin_dir.name}: {e}")
        
        return loaded

    def load_plugin(self, plugin_path: Path) -> Plugin:
        """Load a single plugin from path.
        
        Args:
            plugin_path: Path to plugin directory
            
        Returns:
            Loaded Plugin instance
        """
        plugin = Plugin(plugin_path)
        self.plugins[plugin.name] = plugin
        
        if plugin.mcp_config:
            self._initialize_mcp_client(plugin)
        
        return plugin

    def _initialize_mcp_client(self, plugin: Plugin) -> None:
        """Initialize MCP client for plugin if MCP config exists."""
        if not plugin.mcp_config:
            return
        
        # Create MCP client for each configured server
        for server_name, server_config in plugin.mcp_config.get("mcpServers", {}).items():
            client = MCPClient(server_name, server_config)
            self.mcp_clients[f"{plugin.name}:{server_name}"] = client

    def get_plugin(self, plugin_name: str) -> Optional[Plugin]:
        """Get plugin by name."""
        return self.plugins.get(plugin_name)

    def list_plugins(self) -> List[str]:
        """List all loaded plugin names."""
        return list(self.plugins.keys())

    async def execute_command(
        self,
        plugin_name: str,
        command_name: str,
        provider: LLMProvider,
        user_input: str,
        **kwargs: Any
    ) -> str:
        """Execute a plugin command.
        
        Args:
            plugin_name: Name of the plugin
            command_name: Name of the command to execute
            provider: LLM provider instance
            user_input: User input for the command
            **kwargs: Additional arguments to pass to the provider
            
        Returns:
            Command execution result
        """
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            raise ValueError(f"Plugin '{plugin_name}' not found")
        
        command_content = plugin.get_command(command_name)
        if not command_content:
            raise ValueError(f"Command '{command_name}' not found in plugin '{plugin_name}'")
        
        # Get MCP tools if available
        mcp_tools = []
        for client_key, client in self.mcp_clients.items():
            if client_key.startswith(f"{plugin_name}:"):
                tools = await client.list_tools()
                mcp_tools.extend(tools)
        
        # Execute command using provider
        result = await provider.execute_command(
            command_content=command_content,
            user_input=user_input,
            mcp_tools=mcp_tools,
            **kwargs
        )
        
        return result

    async def execute_agent(
        self,
        plugin_name: str,
        agent_name: str,
        provider: LLMProvider,
        user_input: str,
        **kwargs: Any
    ) -> str:
        """Execute a plugin agent.
        
        Args:
            plugin_name: Name of the plugin
            agent_name: Name of the agent to execute
            provider: LLM provider instance
            user_input: User input for the agent
            **kwargs: Additional arguments to pass to the provider
            
        Returns:
            Agent execution result
        """
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            raise ValueError(f"Plugin '{plugin_name}' not found")
        
        agent_content = plugin.get_agent(agent_name)
        if not agent_content:
            raise ValueError(f"Agent '{agent_name}' not found in plugin '{plugin_name}'")
        
        # Get MCP tools if available
        mcp_tools = []
        for client_key, client in self.mcp_clients.items():
            if client_key.startswith(f"{plugin_name}:"):
                tools = await client.list_tools()
                mcp_tools.extend(tools)
        
        # Execute agent using provider
        result = await provider.execute_agent(
            agent_content=agent_content,
            user_input=user_input,
            mcp_tools=mcp_tools,
            **kwargs
        )
        
        return result

    async def shutdown(self) -> None:
        """Shutdown all MCP clients."""
        for client in self.mcp_clients.values():
            await client.close()
