# Getting Started with OpenPlugin

## Installation

```bash
pip install openplugin-framework
```

Or install from source:

```bash
git clone https://github.com/yourusername/openplugin
cd openplugin
pip install -e .
```

## Quick Start

### 1. Create a Plugin

Create a plugin directory structure:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── my-command.md
└── README.md
```

### 2. Define Plugin Manifest

Create `.claude-plugin/plugin.json`:

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "My awesome plugin",
  "author": "Your Name"
}
```

### 3. Create a Command

Create `commands/my-command.md`:

```markdown
# My Command

This command does something awesome.

## Usage

Describe how to use this command.
```

### 4. Use the Plugin

```python
import asyncio
from openplugin import PluginManager, OpenAIProvider

async def main():
    # Initialize manager
    manager = PluginManager(plugins_dir="./plugins")
    manager.load_plugins()
    
    # Initialize provider
    provider = OpenAIProvider(api_key="your-api-key")
    
    # Execute command
    result = await manager.execute_command(
        "my-plugin",
        "my-command",
        provider=provider,
        user_input="Hello!"
    )
    
    print(result)
    
    await manager.shutdown()

asyncio.run(main())
```

## Plugin Structure

Plugins follow this structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: Plugin manifest
├── .mcp.json                # Optional: MCP server configuration
├── commands/                # Optional: Slash commands (.md files)
├── agents/                  # Optional: Agent definitions (.md files)
├── skills/                  # Optional: Skill definitions
│   └── skill-name/
│       └── SKILL.md
└── README.md                # Optional: Plugin documentation
```

## Plugin Manifest Schema

The `plugin.json` file supports these fields:

- `name` (required): Plugin name (kebab-case)
- `version` (required): Plugin version (semver)
- `description` (optional): Plugin description
- `author` (optional): Plugin author
- `homepage` (optional): Plugin homepage URL
- `repository` (optional): Plugin repository URL
- `license` (optional): Plugin license
- `keywords` (optional): List of keywords
- `dependencies` (optional): Plugin dependencies
- `mcp_servers` (optional): MCP server configurations

## MCP Integration

To add MCP server support, create `.mcp.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["-m", "my_mcp_server"],
      "env": {
        "API_KEY": "${MY_API_KEY}"
      }
    }
  }
}
```

## Providers

### OpenAI Provider

```python
from openplugin import OpenAIProvider

provider = OpenAIProvider(
    api_key="your-api-key",
    model="gpt-4",  # or "gpt-3.5-turbo"
    temperature=0.7
)
```

### Custom Provider

Implement the `LLMProvider` interface:

```python
from openplugin.providers.base import LLMProvider

class MyProvider(LLMProvider):
    async def execute_command(self, command_content, user_input, mcp_tools=None, **kwargs):
        # Your implementation
        pass
    
    async def execute_agent(self, agent_content, user_input, mcp_tools=None, **kwargs):
        # Your implementation
        pass
    
    async def chat(self, messages, tools=None, **kwargs):
        # Your implementation
        pass
```

## Next Steps

- See [examples/](examples/) for more usage examples
- Check out [plugins/](plugins/) for example plugins
- Read the [API documentation](API.md) for detailed API reference
