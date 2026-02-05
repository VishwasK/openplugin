"""Base provider interface for LLM providers."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class LLMProvider(ABC):
    """Base class for LLM providers."""

    @abstractmethod
    async def execute_command(
        self,
        command_content: str,
        user_input: str,
        mcp_tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs: Any
    ) -> str:
        """Execute a command using the LLM provider.
        
        Args:
            command_content: Command definition/content
            user_input: User input for the command
            mcp_tools: Optional list of MCP tools available
            **kwargs: Additional provider-specific arguments
            
        Returns:
            Command execution result
        """
        pass

    @abstractmethod
    async def execute_agent(
        self,
        agent_content: str,
        user_input: str,
        mcp_tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs: Any
    ) -> str:
        """Execute an agent using the LLM provider.
        
        Args:
            agent_content: Agent definition/content
            user_input: User input for the agent
            mcp_tools: Optional list of MCP tools available
            **kwargs: Additional provider-specific arguments
            
        Returns:
            Agent execution result
        """
        pass

    @abstractmethod
    async def chat(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs: Any
    ) -> str:
        """Send a chat message to the LLM.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            tools: Optional list of tools/functions available
            **kwargs: Additional provider-specific arguments
            
        Returns:
            LLM response
        """
        pass
