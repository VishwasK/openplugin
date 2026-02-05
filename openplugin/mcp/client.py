"""MCP client implementation."""

import json
import subprocess
import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path


class MCPClient:
    """MCP client for communicating with MCP servers."""

    def __init__(self, server_name: str, config: Dict[str, Any]):
        """Initialize MCP client.
        
        Args:
            server_name: Name of the MCP server
            config: MCP server configuration from .mcp.json
        """
        self.server_name = server_name
        self.config = config
        self.process: Optional[subprocess.Popen] = None
        self._request_id = 0

    async def initialize(self) -> None:
        """Initialize connection to MCP server."""
        # Extract command and args from config
        command = self.config.get("command")
        args = self.config.get("args", [])
        env = self.config.get("env", {})
        
        if not command:
            raise ValueError(f"MCP server '{self.server_name}' missing command")
        
        # Start subprocess
        full_command = [command] + args
        import os
        process_env = {**os.environ, **env}
        self.process = await asyncio.create_subprocess_exec(
            *full_command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=process_env
        )
        
        # Send initialize request
        await self._send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "openplugin-framework",
                "version": "0.1.0"
            }
        })
        
        # Send initialized notification
        await self._send_notification("initialized", {})

    async def _send_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send a JSON-RPC request to the MCP server."""
        if not self.process or not self.process.stdin:
            raise RuntimeError("MCP server not initialized")
        
        self._request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self._request_id,
            "method": method,
            "params": params
        }
        
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json.encode())
        await self.process.stdin.drain()
        
        # Read response
        response_line = await self.process.stdout.readline()
        response = json.loads(response_line.decode())
        
        return response.get("result", {})

    async def _send_notification(self, method: str, params: Dict[str, Any]) -> None:
        """Send a JSON-RPC notification to the MCP server."""
        if not self.process or not self.process.stdin:
            raise RuntimeError("MCP server not initialized")
        
        notification = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        
        notification_json = json.dumps(notification) + "\n"
        self.process.stdin.write(notification_json.encode())
        await self.process.stdin.drain()

    async def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools from the MCP server."""
        try:
            result = await self._send_request("tools/list", {})
            return result.get("tools", [])
        except Exception as e:
            print(f"Error listing tools from MCP server '{self.server_name}': {e}")
            return []

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call a tool on the MCP server.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments
            
        Returns:
            Tool execution result
        """
        result = await self._send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })
        return result

    async def close(self) -> None:
        """Close the MCP client connection."""
        if self.process:
            try:
                self.process.terminate()
                await asyncio.wait_for(self.process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                self.process.kill()
                await self.process.wait()
            finally:
                self.process = None
