# Examples

This directory contains example applications demonstrating how to use OpenPlugin.

## Email App (`email_app.py`)

A complete email drafting and sending application.

### Setup

1. Install dependencies:
```bash
pip install -r ../requirements.txt
```

2. Set environment variables:
```bash
export OPENAI_API_KEY="your-openai-api-key"
export SMTP_HOST="smtp.gmail.com"  # Optional, defaults to Gmail
export SMTP_PORT="587"              # Optional, defaults to 587
export SMTP_USERNAME="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"  # Gmail App Password
```

### Gmail Setup

For Gmail, you need to:
1. Enable 2-Factor Authentication
2. Generate an App Password:
   - Go to Google Account → Security
   - Enable 2-Step Verification
   - Go to App Passwords
   - Generate password for "Mail"
   - Use this password (not your regular password)

### Run

```bash
python email_app.py
```

### Usage in Your Code

```python
from email_app import EmailApp

app = EmailApp(openai_api_key="your-key")

# Draft an email
draft = await app.draft_email(
    recipient="John Doe",
    purpose="Project update",
    tone="professional"
)

# Send it
result = await app.send_email(
    to="john@example.com",
    subject="Project Update",
    body=draft
)
```

## Basic Usage (`basic_usage.py`)

Simple example showing plugin loading and command execution.

```bash
python basic_usage.py
```
