"""
OpenPlugin Framework - A vendor-agnostic plugin system for LLM applications.
"""

from .core.plugin_manager import PluginManager
from .core.plugin import Plugin
from .providers.base import LLMProvider
from .providers.openai_provider import OpenAIProvider
from .mcp.server import MCPServer
from .mcp.client import MCPClient

__version__ = "0.1.0"

__all__ = [
    "PluginManager",
    "Plugin",
    "LLMProvider",
    "OpenAIProvider",
    "MCPServer",
    "MCPClient",
]
