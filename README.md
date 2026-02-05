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

### ⭐ Simplest Example: Story Plugin (No Setup Required!)

The easiest way to test OpenPlugin - just needs an OpenAI API key:

```bash
# Set your API key
export OPENAI_API_KEY="sk-your-key"

# Run the story example
python examples/story_app.py
```

This will let you write, continue, and improve stories interactively!

### Basic Usage

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
    "story-plugin",  # Try the story plugin!
    "write",
    provider=provider,
    user_input="Write a short sci-fi story about AI"
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

## Examples

- **Story Plugin** (`examples/story_app.py`) - ⭐ **Start here!** Simplest example, no external dependencies
- **Email App** (`examples/email_app.py`) - Complete email drafting and sending
- **Basic Usage** (`examples/basic_usage.py`) - Simple plugin loading example

## Documentation

- [Getting Started](docs/GETTING_STARTED.md) - Detailed setup guide
- [Story Plugin Tutorial](docs/STORY_PLUGIN_TUTORIAL.md) - ⭐ **Easiest way to learn!**
- [Email App Tutorial](docs/EMAIL_APP_TUTORIAL.md) - Building email apps
- [Architecture](docs/ARCHITECTURE.md) - Framework internals
- [Use Cases](USE_CASES.md) - More application ideas

## License

MIT License
