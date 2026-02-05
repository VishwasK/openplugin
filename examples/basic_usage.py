"""Basic usage example of OpenPlugin framework."""

import asyncio
import os
from pathlib import Path
from openplugin import PluginManager, OpenAIProvider


async def main():
    """Run basic plugin example."""
    # Initialize plugin manager
    manager = PluginManager(plugins_dir=Path(__file__).parent.parent / "plugins")
    
    # Load plugins
    print("Loading plugins...")
    loaded = manager.load_plugins()
    print(f"Loaded plugins: {loaded}")
    
    # Initialize OpenAI provider
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Warning: OPENAI_API_KEY not set. Please set it to use OpenAI provider.")
        return
    
    provider = OpenAIProvider(api_key=api_key, model="gpt-4")
    
    # Execute a command
    if "example-plugin" in loaded:
        print("\nExecuting 'hello' command from example-plugin...")
        try:
            result = await manager.execute_command(
                "example-plugin",
                "hello",
                provider=provider,
                user_input="Hello! I'm testing the plugin system."
            )
            print(f"\nResult:\n{result}")
        except Exception as e:
            print(f"Error executing command: {e}")
    
    # Cleanup
    await manager.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
