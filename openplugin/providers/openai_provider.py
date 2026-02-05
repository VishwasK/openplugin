"""OpenAI provider implementation."""

import json
from typing import List, Dict, Any, Optional
from openai import OpenAI, AsyncOpenAI
from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI provider implementation."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4",
        base_url: Optional[str] = None,
        **kwargs: Any
    ):
        """Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key. If None, uses OPENAI_API_KEY env var
            model: Model name to use (default: gpt-4)
            base_url: Custom base URL for API (useful for proxies)
            **kwargs: Additional arguments passed to OpenAI client
        """
        self.model = model
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url, **kwargs)

    def _convert_mcp_tools_to_openai(self, mcp_tools: Optional[List[Dict[str, Any]]]) -> Optional[List[Dict[str, Any]]]:
        """Convert MCP tools to OpenAI function calling format."""
        if not mcp_tools:
            return None
        
        functions = []
        for tool in mcp_tools:
            # MCP tools have name, description, and inputSchema
            tool_name = tool.get("name", "")
            tool_description = tool.get("description", "")
            input_schema = tool.get("inputSchema", {})
            
            functions.append({
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": tool_description,
                    "parameters": input_schema.get("properties", {}),
                    "required": input_schema.get("required", [])
                }
            })
        
        return functions

    async def execute_command(
        self,
        command_content: str,
        user_input: str,
        mcp_tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs: Any
    ) -> str:
        """Execute a command using OpenAI.
        
        Args:
            command_content: Command definition/content
            user_input: User input for the command
            mcp_tools: Optional list of MCP tools available
            **kwargs: Additional arguments (temperature, max_tokens, etc.)
            
        Returns:
            Command execution result
        """
        # Build messages with command context
        messages = [
            {
                "role": "system",
                "content": f"You are executing a plugin command. Here is the command definition:\n\n{command_content}"
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
        
        # Convert MCP tools to OpenAI format
        tools = self._convert_mcp_tools_to_openai(mcp_tools)
        
        # Call OpenAI API
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            **kwargs
        )
        
        # Extract response content
        message = response.choices[0].message
        
        # Handle tool calls if any
        if message.tool_calls:
            # For now, return the tool calls as JSON
            # In a full implementation, you'd execute the tools and continue the conversation
            tool_calls = [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in message.tool_calls
            ]
            return json.dumps({"tool_calls": tool_calls, "content": message.content}, indent=2)
        
        return message.content or ""

    async def execute_agent(
        self,
        agent_content: str,
        user_input: str,
        mcp_tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs: Any
    ) -> str:
        """Execute an agent using OpenAI.
        
        Args:
            agent_content: Agent definition/content
            user_input: User input for the agent
            mcp_tools: Optional list of MCP tools available
            **kwargs: Additional arguments
            
        Returns:
            Agent execution result
        """
        # Build messages with agent context
        messages = [
            {
                "role": "system",
                "content": f"You are an AI agent. Here is your agent definition:\n\n{agent_content}"
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
        
        # Convert MCP tools to OpenAI format
        tools = self._convert_mcp_tools_to_openai(mcp_tools)
        
        # Call OpenAI API
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            **kwargs
        )
        
        message = response.choices[0].message
        
        # Handle tool calls if any
        if message.tool_calls:
            tool_calls = [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in message.tool_calls
            ]
            return json.dumps({"tool_calls": tool_calls, "content": message.content}, indent=2)
        
        return message.content or ""

    async def chat(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs: Any
    ) -> str:
        """Send a chat message to OpenAI.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            tools: Optional list of tools/functions available
            **kwargs: Additional arguments
            
        Returns:
            LLM response
        """
        # Convert tools if provided
        openai_tools = None
        if tools:
            openai_tools = self._convert_mcp_tools_to_openai(tools)
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=openai_tools,
            **kwargs
        )
        
        return response.choices[0].message.content or ""
