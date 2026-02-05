# Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/openplugin
cd openplugin

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

## Set Up OpenAI API Key

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Run the Example

```bash
python examples/basic_usage.py
```

## Create Your First Plugin

1. Create a plugin directory:
```bash
mkdir -p plugins/my-plugin/.claude-plugin
mkdir -p plugins/my-plugin/commands
```

2. Create the plugin manifest:
```bash
cat > plugins/my-plugin/.claude-plugin/plugin.json << EOF
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "My first plugin",
  "author": "Your Name"
}
EOF
```

3. Create a command:
```bash
cat > plugins/my-plugin/commands/greet.md << EOF
# Greet Command

A simple greeting command that responds warmly to user input.
EOF
```

4. Use it in Python:
```python
import asyncio
from openplugin import PluginManager, OpenAIProvider
import os

async def main():
    manager = PluginManager(plugins_dir="./plugins")
    manager.load_plugins()
    
    provider = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
    
    result = await manager.execute_command(
        "my-plugin",
        "greet",
        provider=provider,
        user_input="Hello!"
    )
    
    print(result)
    await manager.shutdown()

asyncio.run(main())
```

## Next Steps

- Read [GETTING_STARTED.md](docs/GETTING_STARTED.md) for detailed documentation
- Check [COMPARISON.md](COMPARISON.md) to understand differences from Claude Plugins
- Explore [examples/](examples/) for more usage patterns
- See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for framework internals
