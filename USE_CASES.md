# Use Cases for OpenPlugin

## Email Application

Create an email drafting and sending app that uses LLM to compose professional emails.

**See**: `examples/email_app.py` and `docs/EMAIL_APP_TUTORIAL.md`

### Features:
- Draft emails using LLM
- Send emails via SMTP
- Customize tone and style
- Include key points automatically

## Content Generation App

Build an app that generates various types of content (blog posts, social media, reports).

### Example Plugin Structure:
```
content-plugin/
├── .claude-plugin/plugin.json
├── commands/
│   ├── blog-post.md
│   ├── social-media.md
│   └── report.md
```

### Usage:
```python
manager = PluginManager()
manager.load_plugins()

result = await manager.execute_command(
    "content-plugin",
    "blog-post",
    provider=provider,
    user_input="Write about AI trends in 2024"
)
```

## Customer Support Bot

Create a support bot that uses plugins for different support scenarios.

### Example:
```python
# Load support plugins
manager.load_plugins("./support-plugins")

# Handle refund request
response = await manager.execute_command(
    "support-plugin",
    "refund-request",
    provider=provider,
    user_input=user_message
)
```

## Code Review Assistant

Build a tool that reviews code and provides suggestions.

### Plugin Commands:
- `review-code`: Analyze code quality
- `suggest-improvements`: Provide optimization suggestions
- `check-security`: Security vulnerability checks

## Data Analysis Assistant

Create an app that analyzes data and generates insights.

### Example:
```python
result = await manager.execute_command(
    "analysis-plugin",
    "generate-insights",
    provider=provider,
    user_input=f"Analyze this data: {data_summary}"
)
```

## Meeting Notes Generator

Build an app that takes meeting transcripts and generates structured notes.

### Workflow:
1. User provides meeting transcript
2. Plugin generates formatted notes
3. Extract action items
4. Create follow-up emails

## Research Assistant

Create a tool that helps with research and summarization.

### Features:
- Summarize articles
- Extract key points
- Generate research reports
- Create citations

## Translation Service

Build a multi-language translation app with context awareness.

### Example:
```python
result = await manager.execute_command(
    "translation-plugin",
    "translate",
    provider=provider,
    user_input=f"Translate to Spanish: {text}"
)
```

## Custom Business Applications

### Sales Email Generator
- Generate personalized sales emails
- Adapt to different customer segments
- Include product recommendations

### HR Assistant
- Draft job descriptions
- Create interview questions
- Generate offer letters

### Legal Document Assistant
- Draft contracts
- Review legal documents
- Generate compliance reports

## Getting Started with Your Use Case

1. **Define Your Commands**: What actions do you want the LLM to perform?
2. **Create Plugin Structure**: Use the standard plugin format
3. **Write Command Definitions**: Describe what each command does
4. **Build Your App**: Use PluginManager to load and execute commands
5. **Integrate with Your Workflow**: Connect plugins to your existing systems

### Quick Template:

```python
from openplugin import PluginManager, OpenAIProvider

# Initialize
manager = PluginManager(plugins_dir="./your-plugins")
manager.load_plugins()
provider = OpenAIProvider(api_key="your-key")

# Use in your app
class YourApp:
    async def do_something(self, user_input):
        result = await manager.execute_command(
            "your-plugin",
            "your-command",
            provider=provider,
            user_input=user_input
        )
        return result
```

## Tips for Building Plugins

1. **Clear Command Descriptions**: Write detailed command definitions
2. **Use Context**: Provide relevant context in user_input
3. **Iterate**: Test and refine your command prompts
4. **Combine Commands**: Chain multiple commands for complex workflows
5. **Add MCP Tools**: Integrate external tools via MCP servers

## Need Help?

- See `docs/GETTING_STARTED.md` for basics
- Check `examples/` for working examples
- Review `docs/EMAIL_APP_TUTORIAL.md` for a complete app walkthrough
