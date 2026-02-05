# Example Plugin

This is an example plugin demonstrating the OpenPlugin framework structure.

## Structure

```
example-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── commands/                 # Slash commands
│   └── hello.md
└── README.md                 # This file
```

## Commands

- `/hello` - A simple greeting command

## Usage

```python
from openplugin import PluginManager, OpenAIProvider

manager = PluginManager()
manager.load_plugins("./plugins")

provider = OpenAIProvider(api_key="your-key")

result = await manager.execute_command(
    "example-plugin",
    "hello",
    provider=provider,
    user_input="Hello, world!"
)
```
