# Building an Email App with OpenPlugin

This tutorial shows you how to build a complete email drafting and sending application using the OpenPlugin framework.

## Overview

We'll create an application that:
1. Uses LLM to draft professional emails
2. Sends emails via SMTP
3. Combines drafting and sending in one workflow

## Step 1: Create the Email Plugin

First, create a plugin for email functionality:

```
plugins/email-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── draft.md
│   └── send.md
└── README.md
```

The plugin defines two commands:
- **draft**: Uses LLM to generate email drafts
- **send**: Handles email sending logic

## Step 2: Create the Application

Create `email_app.py`:

```python
from openplugin import PluginManager, OpenAIProvider
from openplugin.utils import EmailSender

class EmailApp:
    def __init__(self, openai_api_key: str):
        # Load plugins
        self.manager = PluginManager(plugins_dir="./plugins")
        self.manager.load_plugins()
        
        # Initialize LLM provider
        self.provider = OpenAIProvider(api_key=openai_api_key)
        
        # Initialize email sender
        self.email_sender = EmailSender()
    
    async def draft_email(self, recipient, purpose, tone="professional"):
        # Use the draft command
        result = await self.manager.execute_command(
            "email-plugin",
            "draft",
            provider=self.provider,
            user_input=f"Draft email to {recipient} about {purpose}. Tone: {tone}"
        )
        return result
    
    async def send_email(self, to, subject, body):
        # Send via SMTP
        return self.email_sender.send_email(to, subject, body)
```

## Step 3: Configure SMTP

Set environment variables:

```bash
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USERNAME=your-email@gmail.com
export SMTP_PASSWORD=your-app-password
export OPENAI_API_KEY=your-openai-key
```

For Gmail, you'll need to:
1. Enable 2-factor authentication
2. Generate an App Password (not your regular password)

## Step 4: Use the Application

```python
import asyncio
from email_app import EmailApp

async def main():
    app = EmailApp(openai_api_key="your-key")
    
    # Draft an email
    draft = await app.draft_email(
        recipient="John Doe",
        purpose="Project update",
        tone="professional"
    )
    
    print(draft)
    
    # Send the email
    result = await app.send_email(
        to="john@example.com",
        subject="Project Update",
        body=draft
    )
    
    print(result)

asyncio.run(main())
```

## Complete Example

See `examples/email_app.py` for a complete working example with:
- Email drafting with LLM
- Email sending via SMTP
- Error handling
- Combined draft-and-send workflow

## Running the Example

```bash
# Set environment variables
export OPENAI_API_KEY="your-key"
export SMTP_USERNAME="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"

# Run the example
python examples/email_app.py
```

## Customization

### Different LLM Providers

You can use any provider that implements `LLMProvider`:

```python
from openplugin.providers.base import LLMProvider

class MyProvider(LLMProvider):
    # Implement the interface
    pass

app = EmailApp(provider=MyProvider())
```

### Custom Email Templates

Modify the draft command in `commands/draft.md` to include specific templates or formatting requirements.

### Additional Features

- Email scheduling
- Email templates
- Multi-recipient support
- Attachments
- HTML emails
- Email tracking

## Architecture

```
User Request
    ↓
EmailApp.draft_email()
    ↓
PluginManager.execute_command("draft")
    ↓
OpenAIProvider → LLM API
    ↓
Email Draft Generated
    ↓
EmailApp.send_email()
    ↓
EmailSender → SMTP Server
    ↓
Email Sent
```

## Best Practices

1. **Error Handling**: Always handle LLM and SMTP errors gracefully
2. **Validation**: Validate email addresses before sending
3. **Rate Limiting**: Respect LLM API rate limits
4. **Security**: Never hardcode credentials, use environment variables
5. **Testing**: Test with a test email account first

## Next Steps

- Add email templates
- Implement email scheduling
- Add support for attachments
- Create a web interface
- Add email tracking and analytics
