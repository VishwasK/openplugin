# Building an Email App with OpenPlugin - Complete Guide

## Overview

This guide shows you how to use OpenPlugin to build a complete email drafting and sending application that uses LLM (like GPT-4) to compose emails and SMTP to send them.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Your Application                     │
│  (email_app.py, web app, API, script, etc.)            │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌──────────────┐         ┌──────────────┐
│ OpenPlugin   │         │ EmailSender  │
│ Framework    │         │   (SMTP)     │
└──────┬───────┘         └──────────────┘
       │
       ├─── PluginManager (loads plugins)
       ├─── Email Plugin (draft/send commands)
       └─── OpenAIProvider (LLM calls)
```

## Components

### 1. Email Plugin (`plugins/email-plugin/`)

Defines two commands:
- **`draft.md`**: Instructions for LLM to draft emails
- **`send.md`**: Instructions for email sending logic

### 2. Email App (`examples/email_app.py`)

Main application class that:
- Loads the email plugin
- Uses LLM to draft emails
- Sends emails via SMTP

### 3. Email Sender (`openplugin/utils/email_sender.py`)

Utility class for SMTP email sending.

## Quick Start

### 1. Installation

```bash
git clone https://github.com/VishwasK/openplugin
cd openplugin
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Required
export OPENAI_API_KEY="sk-your-openai-key"

# For email sending (Gmail example)
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USERNAME="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
```

**Gmail Setup:**
1. Enable 2-Factor Authentication
2. Generate App Password: Google Account → Security → App Passwords
3. Use the generated password (not your regular password)

### 3. Run Example

```bash
python examples/email_app.py
```

## Usage Examples

### Example 1: Draft Only

```python
import asyncio
from examples.email_app import EmailApp
import os

async def main():
    app = EmailApp(openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    draft = await app.draft_email(
        recipient="Sarah Johnson",
        purpose="Follow up on Q4 project timeline",
        tone="professional",
        key_points=[
            "Thank her for the meeting",
            "Confirm deliverables",
            "Request feedback on timeline"
        ]
    )
    
    print(draft)
    await app.shutdown()

asyncio.run(main())
```

### Example 2: Draft and Send

```python
async def main():
    app = EmailApp(openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    result = await app.draft_and_send(
        to="sarah@example.com",
        recipient_name="Sarah Johnson",
        purpose="Project update",
        tone="professional",
        key_points=["Milestone 1 complete", "Next steps"],
        from_email="you@example.com"
    )
    
    if result["send"]["success"]:
        print("✅ Email sent!")
    else:
        print(f"❌ Error: {result['send']['message']}")
    
    await app.shutdown()
```

### Example 3: Custom Integration

```python
from openplugin import PluginManager, OpenAIProvider
from openplugin.utils import EmailSender

class MyEmailService:
    def __init__(self):
        self.manager = PluginManager(plugins_dir="./plugins")
        self.manager.load_plugins()
        self.provider = OpenAIProvider(api_key="your-key")
        self.email_sender = EmailSender()
    
    async def send_followup(self, customer_email, meeting_notes):
        # Draft email using LLM
        draft = await self.manager.execute_command(
            "email-plugin",
            "draft",
            provider=self.provider,
            user_input=f"""
            Draft a follow-up email to {customer_email} based on these meeting notes:
            {meeting_notes}
            
            Tone: Professional
            Include: Key action items and next steps
            """
        )
        
        # Extract subject and body (you'd parse this properly)
        subject = "Follow-up: Meeting Notes"
        body = draft
        
        # Send
        return self.email_sender.send_email(
            to=customer_email,
            subject=subject,
            body=body
        )
```

## How It Works

### Step 1: Plugin Loading

```python
manager = PluginManager(plugins_dir="./plugins")
manager.load_plugins()  # Discovers and loads email-plugin
```

The manager:
- Scans `plugins/` directory
- Finds `email-plugin/.claude-plugin/plugin.json`
- Loads command definitions from `commands/`

### Step 2: Drafting Email

```python
draft = await manager.execute_command(
    "email-plugin",
    "draft",
    provider=provider,
    user_input="Draft email to John about project..."
)
```

Behind the scenes:
1. Finds "draft" command in email-plugin
2. Reads `commands/draft.md` (command instructions)
3. Sends your input + command instructions to OpenAI
4. Returns LLM-generated email draft

### Step 3: Sending Email

```python
email_sender.send_email(to="...", subject="...", body="...")
```

The EmailSender:
1. Connects to SMTP server
2. Authenticates with credentials
3. Sends email
4. Returns success/error status

## Customization

### Change LLM Model

```python
provider = OpenAIProvider(
    api_key="your-key",
    model="gpt-3.5-turbo"  # or "gpt-4", etc.
)
```

### Customize Drafting

Edit `plugins/email-plugin/commands/draft.md` to change:
- Email format
- Tone options
- Required fields
- Output structure

### Add New Commands

Create `plugins/email-plugin/commands/schedule.md`:

```markdown
# Schedule Email Command

Schedules an email to be sent later.

## Usage
...
```

Then use it:
```python
await manager.execute_command(
    "email-plugin",
    "schedule",
    provider=provider,
    user_input="..."
)
```

### Use Different SMTP Provider

```python
email_sender = EmailSender(
    smtp_host="smtp.sendgrid.net",
    smtp_port=587,
    smtp_username="apikey",
    smtp_password="your-sendgrid-key"
)
```

## Integration Ideas

### Web Application

```python
from flask import Flask, request, jsonify

app = Flask(__name__)
email_app = EmailApp(openai_api_key=OPENAI_KEY)

@app.route('/draft-email', methods=['POST'])
async def draft_email():
    data = request.json
    draft = await email_app.draft_email(
        recipient=data['recipient'],
        purpose=data['purpose'],
        tone=data.get('tone', 'professional')
    )
    return jsonify({"draft": draft})
```

### CLI Tool

```python
import click

@click.command()
@click.option('--to', required=True)
@click.option('--purpose', required=True)
def send_email(to, purpose):
    app = EmailApp(openai_api_key=os.getenv("OPENAI_API_KEY"))
    result = asyncio.run(app.draft_and_send(...))
    click.echo(result)
```

### Scheduled Jobs

```python
import schedule

def send_daily_report():
    app = EmailApp(...)
    asyncio.run(app.draft_and_send(
        to="team@company.com",
        purpose="Daily report",
        ...
    ))

schedule.every().day.at("09:00").do(send_daily_report)
```

## Error Handling

```python
try:
    draft = await app.draft_email(...)
except Exception as e:
    print(f"Drafting failed: {e}")
    # Fallback to template

try:
    result = app.email_sender.send_email(...)
    if not result["success"]:
        print(f"Send failed: {result['message']}")
except Exception as e:
    print(f"SMTP error: {e}")
```

## Best Practices

1. **Validate Input**: Check email addresses before sending
2. **Handle Errors**: Always wrap LLM and SMTP calls in try/except
3. **Rate Limiting**: Respect OpenAI API rate limits
4. **Security**: Never hardcode credentials
5. **Testing**: Test with a test email account first
6. **Logging**: Log all email operations for debugging

## Troubleshooting

### "SMTP credentials not configured"
- Set `SMTP_USERNAME` and `SMTP_PASSWORD` environment variables
- Or pass them to `EmailSender()` constructor

### "Plugin not found"
- Ensure plugin is in `plugins/email-plugin/`
- Check `plugin.json` exists and is valid

### "OpenAI API error"
- Verify `OPENAI_API_KEY` is set correctly
- Check API key has sufficient credits
- Verify model name is correct

### "Email not sending"
- Check SMTP credentials
- Verify firewall allows SMTP connections
- For Gmail: Use App Password, not regular password

## Next Steps

- Read `docs/EMAIL_APP_TUTORIAL.md` for detailed walkthrough
- Check `USE_CASES.md` for more application ideas
- Explore `examples/` for more examples
- Create your own plugins and commands!

## Support

- GitHub Issues: https://github.com/VishwasK/openplugin/issues
- Documentation: See `docs/` directory
- Examples: See `examples/` directory
