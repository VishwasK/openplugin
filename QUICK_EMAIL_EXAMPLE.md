# Quick Start: Email App Example

## The Problem

You want to build an app that drafts and sends emails using an LLM, without being locked into Claude Pro.

## The Solution

Use OpenPlugin with OpenAI (or any LLM provider) to:
1. Draft emails using LLM
2. Send emails via SMTP
3. Combine both in one workflow

## Step-by-Step

### 1. Install OpenPlugin

```bash
git clone https://github.com/VishwasK/openplugin
cd openplugin
pip install -r requirements.txt
```

### 2. Set Up Credentials

```bash
export OPENAI_API_KEY="sk-..."
export SMTP_USERNAME="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
```

### 3. Run the Example

```bash
python examples/email_app.py
```

## How It Works

```
┌─────────────────┐
│   Your App      │
│  (email_app.py) │
└────────┬────────┘
         │
         ├─────────────────┐
         │                  │
         ▼                  ▼
┌─────────────────┐  ┌──────────────┐
│  PluginManager │  │ EmailSender  │
│  (loads plugins)│  │  (SMTP)      │
└────────┬────────┘  └──────────────┘
         │
         ▼
┌─────────────────┐
│  Email Plugin   │
│  (draft/send)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ OpenAI Provider │
│   (GPT-4)       │
└─────────────────┘
```

## Code Flow

```python
# 1. Initialize
app = EmailApp(openai_api_key="your-key")

# 2. Draft email (uses LLM)
draft = await app.draft_email(
    recipient="John Doe",
    purpose="Project update",
    tone="professional"
)

# 3. Send email (uses SMTP)
result = await app.send_email(
    to="john@example.com",
    subject="Project Update",
    body=draft
)
```

## What Happens Behind the Scenes

1. **Plugin Loading**: `PluginManager` loads the `email-plugin` from `plugins/`
2. **Command Execution**: When you call `draft_email()`, it:
   - Finds the "draft" command in the plugin
   - Sends your requirements to OpenAI via `OpenAIProvider`
   - Returns the drafted email
3. **Email Sending**: `EmailSender` connects to SMTP and sends the email

## Customization

### Use Different LLM

```python
# Instead of OpenAI, use Anthropic (when implemented)
from openplugin.providers.anthropic_provider import AnthropicProvider

provider = AnthropicProvider(api_key="your-key")
app = EmailApp(provider=provider)
```

### Add More Commands

Create new `.md` files in `plugins/email-plugin/commands/`:
- `schedule.md` - Schedule emails
- `template.md` - Use email templates
- `reply.md` - Generate replies

### Customize Email Logic

Modify `commands/draft.md` to change how emails are drafted, or `commands/send.md` for sending logic.

## Real-World Example

```python
# In your web app, API, or script
async def handle_email_request(request):
    app = EmailApp(openai_api_key=OPENAI_KEY)
    
    # User wants to send a follow-up email
    draft = await app.draft_email(
        recipient=request.recipient_name,
        purpose=request.purpose,
        tone="friendly",
        key_points=request.key_points
    )
    
    # Review draft (optional)
    if request.auto_send:
        result = await app.send_email(
            to=request.recipient_email,
            subject=extract_subject(draft),
            body=extract_body(draft)
        )
        return {"status": "sent", "result": result}
    else:
        return {"status": "drafted", "draft": draft}
```

## Key Benefits

✅ **Vendor Agnostic**: Use OpenAI, Anthropic, or any provider  
✅ **Plugin System**: Easy to add new commands  
✅ **No Lock-in**: Works without Claude Pro  
✅ **Extensible**: Add your own providers and plugins  
✅ **Open Source**: Full control over your code  

## Next Steps

- Read `docs/EMAIL_APP_TUTORIAL.md` for detailed walkthrough
- Check `USE_CASES.md` for more application ideas
- Explore `examples/` for more examples
- Create your own plugins!
