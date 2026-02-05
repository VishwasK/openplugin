# Story Plugin

A simple, fun plugin for creative writing using LLM. Perfect for testing OpenPlugin without any external dependencies!

## Features

- **Write Stories**: Generate creative stories from prompts
- **Continue Stories**: Seamlessly continue existing stories
- **Improve Stories**: Enhance and refine story writing

## Commands

### `/write`
Write a new story based on your prompt.

Example:
```
Write a fantasy story about a young wizard discovering their powers. 
Make it adventurous and include a magical quest.
```

### `/continue`
Continue an existing story.

Example:
```
Continue this story: [your story text]
Add a plot twist and introduce a new character.
```

### `/improve`
Improve and refine a story.

Example:
```
Improve this story with better descriptions and dialogue:
[your story text]
```

## Usage

See `examples/story_app.py` for a complete example.

## Why This Plugin?

- ✅ **No External Dependencies**: Just needs OpenAI API key
- ✅ **Easy to Test**: Simple, fun, and interactive
- ✅ **No Setup Required**: No SMTP, MFA, or complex configuration
- ✅ **Great for Learning**: Perfect example of how plugins work

## Quick Test

```python
from openplugin import PluginManager, OpenAIProvider
import os

manager = PluginManager(plugins_dir="./plugins")
manager.load_plugins()

provider = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))

result = await manager.execute_command(
    "story-plugin",
    "write",
    provider=provider,
    user_input="Write a short sci-fi story about AI"
)

print(result)
```
