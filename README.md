# OpenPlugin Framework

A vendor-agnostic plugin framework inspired by Claude Code Plugins, designed to work with any LLM provider (OpenAI, Anthropic, Google, etc.).

## Features

- 🔌 **Plugin System**: Load and manage plugins with standardized structure
- 🌐 **Vendor Agnostic**: Works with OpenAI, Anthropic, Google, and other LLM providers
- 🔧 **MCP Support**: Full Model Context Protocol (MCP) server integration
- 📦 **Plugin Discovery**: Automatic plugin discovery and registry
- 🎯 **Commands & Skills**: Support for slash commands, agents, and skills
- 🚀 **Easy Integration**: Simple API for adding plugins to your LLM applications

## Installation

```bash
pip install openplugin-framework
```

## Quick Start

```python
from openplugin import PluginManager, OpenAIProvider

# Initialize plugin manager
manager = PluginManager()

# Load plugins from directory
manager.load_plugins("./plugins")

# Initialize OpenAI provider
provider = OpenAIProvider(api_key="your-api-key")

# Run a plugin command
result = await manager.execute_command(
    "plugin-name",
    "command-name",
    provider=provider,
    user_input="Hello, world!"
)
```

## Plugin Structure

Plugins follow a standardized structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest (required)
├── .mcp.json                # MCP server configuration (optional)
├── commands/                # Slash commands (.md files)
├── agents/                  # Agent definitions (.md files)
├── skills/                  # Skill definitions (subdirectories)
│   └── skill-name/
│       └── SKILL.md
└── README.md                # Plugin documentation
```

## Supported Providers

- ✅ OpenAI (GPT-4, GPT-3.5, etc.)
- 🔄 Anthropic (Claude) - Coming soon
- 🔄 Google (Gemini) - Coming soon
- 🔄 Custom providers via adapter interface

## Documentation

See [docs/](docs/) for detailed documentation.

## License

MIT License
