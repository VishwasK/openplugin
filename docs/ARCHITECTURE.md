# OpenPlugin Architecture

## Overview

OpenPlugin is a vendor-agnostic plugin framework that allows you to:
- Load and manage plugins with standardized structure
- Execute plugin commands and agents using any LLM provider
- Integrate with MCP (Model Context Protocol) servers
- Build extensible AI applications

## Core Components

### Plugin Manager

The `PluginManager` is the central component that:
- Discovers and loads plugins from directories
- Manages plugin lifecycle
- Coordinates command/agent execution
- Handles MCP client connections

### Plugin

The `Plugin` class represents a loaded plugin:
- Parses plugin manifest (`plugin.json`)
- Loads commands, agents, and skills
- Manages MCP configuration
- Provides access to plugin resources

### Providers

Providers implement the `LLMProvider` interface:
- `OpenAIProvider`: OpenAI GPT models
- Future: `AnthropicProvider`, `GoogleProvider`, etc.
- Custom providers can be implemented

### MCP Support

MCP (Model Context Protocol) integration:
- `MCPClient`: Communicates with MCP servers
- Supports stdio transport
- Tool discovery and execution
- Automatic tool conversion for providers

## Data Flow

```
User Input
    ↓
PluginManager.execute_command()
    ↓
Plugin.get_command() → Command Content
    ↓
MCPClient.list_tools() → Available Tools
    ↓
Provider.execute_command() → LLM API Call
    ↓
Response with Tool Calls (if any)
    ↓
MCPClient.call_tool() → Tool Execution
    ↓
Final Response
```

## Plugin Discovery

Plugins are discovered by:
1. Scanning the plugins directory
2. Looking for `.claude-plugin/plugin.json` files
3. Validating plugin structure
4. Loading plugin resources

## MCP Integration

MCP servers are configured in `.mcp.json`:
- Each server has a command and arguments
- Servers run as subprocesses
- Communication via JSON-RPC 2.0 over stdio
- Tools are automatically discovered and made available

## Provider Abstraction

The `LLMProvider` interface abstracts LLM differences:
- Standardized command/agent execution
- Tool/function calling support
- Message format conversion
- Provider-specific optimizations

## Extension Points

### Adding a New Provider

1. Implement `LLMProvider` interface
2. Convert MCP tools to provider format
3. Handle provider-specific features
4. Register in `providers/__init__.py`

### Adding Plugin Features

1. Extend `Plugin` class
2. Add resource loading methods
3. Update `PluginManager` to use new features
4. Document in plugin structure guide

## Future Enhancements

- [ ] HTTP/SSE transport for MCP servers
- [ ] Plugin registry and discovery
- [ ] Plugin versioning and updates
- [ ] Plugin dependencies resolution
- [ ] Caching and optimization
- [ ] Multi-provider fallback
- [ ] Plugin marketplace integration
