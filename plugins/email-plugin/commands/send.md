# Send Email Command

Sends an email using the drafted content.

## Usage

This command takes a drafted email and sends it via SMTP.

## Input Parameters

- **to**: Recipient email address
- **subject**: Email subject line
- **body**: Email body content
- **from**: Sender email address (optional, uses default if not provided)

## Behavior

- Validates email addresses
- Sends email via configured SMTP server
- Returns confirmation of successful send
- Handles errors gracefully

## Requirements

- SMTP server configuration (host, port, username, password)
- Valid email credentials
