# Email Plugin

A plugin for drafting and sending emails using LLM assistance.

## Features

- **Draft Emails**: Generate professional email drafts using LLM
- **Send Emails**: Send emails via SMTP
- **Smart Composition**: Context-aware email generation

## Commands

### `/draft`
Drafts a professional email based on your requirements.

Example:
```
Draft an email to john@example.com about the project update. 
Make it professional and include the key milestones we've achieved.
```

### `/send`
Sends a drafted email.

Example:
```
Send an email to john@example.com with subject "Project Update" 
and the drafted body content.
```

## Setup

1. Configure SMTP settings in your application
2. Load the plugin using PluginManager
3. Use the commands to draft and send emails

## Usage

See `examples/email_app.py` for a complete example application.
