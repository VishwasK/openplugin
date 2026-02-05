# Story Plugin Tutorial - The Simplest Way to Test OpenPlugin

## Why Story Plugin?

The Story Plugin is perfect for testing OpenPlugin because:
- ✅ **No External Dependencies**: Only needs OpenAI API key
- ✅ **No Complex Setup**: No SMTP, MFA, or configuration files
- ✅ **Fun & Interactive**: Creative and engaging to use
- ✅ **Easy to Understand**: Simple commands, clear results
- ✅ **Great for Learning**: Perfect example of plugin structure

## Quick Start

### 1. Install OpenPlugin

```bash
git clone https://github.com/VishwasK/openplugin
cd openplugin
pip install -r requirements.txt
```

### 2. Set Your API Key

```bash
export OPENAI_API_KEY="sk-your-openai-key"
```

That's it! No other setup needed.

### 3. Run the Example

```bash
python examples/story_app.py
```

## Basic Usage

### Write a Story

```python
from openplugin import PluginManager, OpenAIProvider
import asyncio
import os

async def main():
    # Initialize
    manager = PluginManager(plugins_dir="./plugins")
    manager.load_plugins()
    
    provider = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Write a story
    story = await manager.execute_command(
        "story-plugin",
        "write",
        provider=provider,
        user_input="Write a short sci-fi story about AI discovering emotions"
    )
    
    print(story)

asyncio.run(main())
```

### Continue a Story

```python
# Continue the story
continuation = await manager.execute_command(
    "story-plugin",
    "continue",
    provider=provider,
    user_input=f"Continue this story:\n\n{story}\n\nAdd a plot twist"
)
```

### Improve a Story

```python
# Improve the story
improved = await manager.execute_command(
    "story-plugin",
    "improve",
    provider=provider,
    user_input=f"Improve this story with better descriptions:\n\n{story}"
)
```

## Using the StoryApp Class

For easier usage, use the `StoryApp` class:

```python
from examples.story_app import StoryApp

app = StoryApp(openai_api_key="your-key")

# Write
story = await app.write_story(
    prompt="A fantasy adventure",
    genre="fantasy",
    length="medium",
    tone="adventurous"
)

# Continue
continued = await app.continue_story(
    story=story,
    direction="Add a new character",
    length="short"
)

# Improve
improved = await app.improve_story(
    story=continued,
    focus="dialogue",
    style="literary"
)
```

## Interactive Mode

Run the interactive story writer:

```python
app = StoryApp(openai_api_key="your-key")
await app.interactive_story()
```

This gives you a command-line interface to:
- Write new stories
- Continue existing stories
- Improve stories
- Start over with a new story

## Example Output

```
============================================================
📖 Interactive Story Writer
============================================================

Let's write a story together!

What kind of story would you like to write?
> A detective story set in Victorian London

Optional settings (press Enter to skip):
Genre (fantasy, sci-fi, mystery, etc.): mystery
Length (short, medium, long) [medium]: short
Tone (funny, serious, dark, etc.): serious

✨ Writing your story...

============================================================
📝 YOUR STORY
============================================================

[Generated story appears here...]

============================================================

What would you like to do?
[c]ontinue, [i]mprove, [n]ew story, [q]uit: c
```

## Plugin Structure

The story plugin follows the standard structure:

```
story-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── commands/
│   ├── write.md             # Write story command
│   ├── continue.md          # Continue story command
│   └── improve.md           # Improve story command
└── README.md                # Plugin documentation
```

## Command Definitions

### write.md
Defines how to write stories:
- What parameters to accept
- What output to generate
- How to structure the story

### continue.md
Defines how to continue stories:
- How to maintain consistency
- How to follow the original style
- How to add new elements

### improve.md
Defines how to improve stories:
- What aspects to enhance
- How to maintain the original plot
- How to improve writing quality

## Customization

### Change Model

```python
provider = OpenAIProvider(
    api_key="your-key",
    model="gpt-3.5-turbo"  # Use cheaper model
)
```

### Adjust Creativity

```python
# More creative (higher temperature)
story = await manager.execute_command(
    "story-plugin",
    "write",
    provider=provider,
    user_input="...",
    temperature=0.9  # More creative
)

# More focused (lower temperature)
story = await manager.execute_command(
    "story-plugin",
    "write",
    provider=provider,
    user_input="...",
    temperature=0.7  # More focused
)
```

### Modify Commands

Edit the `.md` files in `plugins/story-plugin/commands/` to change:
- What the command does
- What parameters it accepts
- How it formats output
- What style it uses

## Integration Ideas

### Web App

```python
from flask import Flask, request, jsonify

app = Flask(__name__)
story_app = StoryApp(openai_api_key=OPENAI_KEY)

@app.route('/write-story', methods=['POST'])
async def write_story():
    data = request.json
    story = await story_app.write_story(
        prompt=data['prompt'],
        genre=data.get('genre'),
        length=data.get('length', 'medium')
    )
    return jsonify({"story": story})
```

### CLI Tool

```python
import click

@click.command()
@click.option('--prompt', required=True)
@click.option('--genre')
def write_story(prompt, genre):
    app = StoryApp(openai_api_key=os.getenv("OPENAI_API_KEY"))
    story = asyncio.run(app.write_story(prompt=prompt, genre=genre))
    click.echo(story)
```

### Story Generator API

```python
class StoryAPI:
    def __init__(self):
        self.app = StoryApp(openai_api_key=OPENAI_KEY)
    
    async def generate_story(self, user_preferences):
        return await self.app.write_story(**user_preferences)
    
    async def continue_story(self, story_id, direction):
        story = self.get_story(story_id)
        return await self.app.continue_story(story, direction)
```

## Tips

1. **Start Simple**: Begin with basic prompts, then add details
2. **Iterate**: Use continue/improve to refine stories
3. **Experiment**: Try different genres, tones, and lengths
4. **Save Stories**: Store generated stories for later continuation
5. **Combine Commands**: Write → Continue → Improve → Continue

## Troubleshooting

### "Plugin not found"
- Ensure `plugins/story-plugin/` exists
- Check `plugin.json` is valid
- Verify plugin was loaded: `manager.list_plugins()`

### "OpenAI API error"
- Verify API key is correct
- Check you have API credits
- Ensure model name is valid

### "Story too short/long"
- Adjust `length` parameter (short, medium, long)
- Modify the command definition in `write.md`
- Use `continue` to add more content

## Next Steps

- Try the interactive mode: `python examples/story_app.py`
- Create your own commands in the plugin
- Build a web interface for story writing
- Add more creative commands (poetry, scripts, etc.)
- Explore other plugins in the `plugins/` directory

## Why This is Perfect for Testing

1. **Immediate Results**: See output right away
2. **No Configuration**: Just API key needed
3. **Visual Feedback**: Stories are easy to read and verify
4. **Fun**: Engaging to use and test
5. **Educational**: Shows all plugin concepts clearly

Enjoy writing stories with OpenPlugin! 🎨📖
