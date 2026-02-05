"""MCP server implementation (for creating MCP servers)."""

from typing import Dict, Any, List, Callable, Optional
from abc import ABC, abstractmethod


class MCPServer(ABC):
    """Base class for MCP servers."""

    @abstractmethod
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools."""
        pass

    @abstractmethod
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call a tool."""
        pass
