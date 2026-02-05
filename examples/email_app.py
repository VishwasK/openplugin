"""Complete example: Email drafting and sending application using OpenPlugin."""

import asyncio
import os
from pathlib import Path
from openplugin import PluginManager, OpenAIProvider
from openplugin.utils import EmailSender


class EmailApp:
    """Email application using OpenPlugin framework."""

    def __init__(self, openai_api_key: str, smtp_config: dict = None):
        """Initialize email app.
        
        Args:
            openai_api_key: OpenAI API key
            smtp_config: SMTP configuration dict with host, port, username, password
        """
        # Initialize plugin manager
        self.manager = PluginManager(plugins_dir=Path(__file__).parent.parent / "plugins")
        self.manager.load_plugins()
        
        # Initialize LLM provider
        self.provider = OpenAIProvider(api_key=openai_api_key, model="gpt-4")
        
        # Initialize email sender
        if smtp_config:
            self.email_sender = EmailSender(**smtp_config)
        else:
            # Use environment variables
            self.email_sender = EmailSender()

    async def draft_email(
        self,
        recipient: str,
        purpose: str,
        tone: str = "professional",
        key_points: list = None
    ) -> dict:
        """Draft an email using LLM.
        
        Args:
            recipient: Email recipient name/address
            purpose: What the email is about
            tone: Desired tone (professional, casual, formal, friendly)
            key_points: List of key points to include
            
        Returns:
            Dictionary with drafted email content
        """
        # Build user input for the draft command
        key_points_str = "\n".join([f"- {point}" for point in (key_points or [])])
        
        user_input = f"""Draft an email with the following requirements:
        
Recipient: {recipient}
Purpose: {purpose}
Tone: {tone}
Key Points to Include:
{key_points_str if key_points_str else "None specified"}

Please generate a complete email with subject line, greeting, body, and closing."""
        
        # Execute the draft command
        result = await self.manager.execute_command(
            "email-plugin",
            "draft",
            provider=self.provider,
            user_input=user_input,
            temperature=0.7
        )
        
        return {
            "draft": result,
            "recipient": recipient,
            "purpose": purpose
        }

    async def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        from_email: str = None
    ) -> dict:
        """Send an email.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body content
            from_email: Sender email (optional)
            
        Returns:
            Dictionary with send result
        """
        # Use the send command to prepare (could add validation logic here)
        user_input = f"""Send an email with:
To: {to}
Subject: {subject}
Body: {body}"""
        
        # Execute send command (for validation/preparation)
        await self.manager.execute_command(
            "email-plugin",
            "send",
            provider=self.provider,
            user_input=user_input
        )
        
        # Actually send the email
        result = self.email_sender.send_email(
            to=to,
            subject=subject,
            body=body,
            from_email=from_email
        )
        
        return result

    async def draft_and_send(
        self,
        to: str,
        recipient_name: str,
        purpose: str,
        tone: str = "professional",
        key_points: list = None,
        from_email: str = None
    ) -> dict:
        """Draft and send an email in one go.
        
        Args:
            to: Recipient email address
            recipient_name: Recipient name for the draft
            purpose: What the email is about
            tone: Desired tone
            key_points: List of key points to include
            from_email: Sender email (optional)
            
        Returns:
            Dictionary with draft and send results
        """
        # Step 1: Draft the email
        print(f"📝 Drafting email to {recipient_name}...")
        draft_result = await self.draft_email(
            recipient=recipient_name,
            purpose=purpose,
            tone=tone,
            key_points=key_points
        )
        
        # Extract subject and body from draft (simple parsing)
        # In a real app, you'd parse the LLM response more carefully
        draft_content = draft_result["draft"]
        
        # Simple extraction (you might want more sophisticated parsing)
        lines = draft_content.split("\n")
        subject = ""
        body_start = 0
        
        for i, line in enumerate(lines):
            if "subject:" in line.lower() and not subject:
                subject = line.split(":", 1)[1].strip()
            elif line.strip() and not subject:
                # First non-empty line might be subject
                subject = line.strip()
                body_start = i + 1
                break
        
        body = "\n".join(lines[body_start:]).strip()
        
        # If we couldn't parse, use the whole draft as body
        if not body:
            body = draft_content
        if not subject:
            subject = f"Re: {purpose}"
        
        print(f"✅ Draft complete!")
        print(f"\nSubject: {subject}")
        print(f"\nBody:\n{body}\n")
        
        # Step 2: Send the email
        print(f"📧 Sending email to {to}...")
        send_result = await self.send_email(
            to=to,
            subject=subject,
            body=body,
            from_email=from_email
        )
        
        return {
            "draft": draft_result,
            "send": send_result,
            "subject": subject,
            "body": body
        }

    async def shutdown(self):
        """Cleanup resources."""
        await self.manager.shutdown()


async def main():
    """Example usage of the email app."""
    
    # Get API keys from environment
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        return
    
    # SMTP configuration (optional - can use environment variables)
    smtp_config = {
        "smtp_host": os.getenv("SMTP_HOST", "smtp.gmail.com"),
        "smtp_port": int(os.getenv("SMTP_PORT", "587")),
        "smtp_username": os.getenv("SMTP_USERNAME"),
        "smtp_password": os.getenv("SMTP_PASSWORD"),
    }
    
    # Initialize app
    app = EmailApp(openai_api_key=openai_key, smtp_config=smtp_config)
    
    try:
        # Example 1: Just draft an email
        print("=" * 60)
        print("Example 1: Drafting an email")
        print("=" * 60)
        
        draft_result = await app.draft_email(
            recipient="Sarah Johnson",
            purpose="Follow up on our meeting about the Q4 project timeline",
            tone="professional",
            key_points=[
                "Thank her for the productive meeting",
                "Confirm the key deliverables we discussed",
                "Request her feedback on the proposed timeline",
                "Suggest a follow-up call next week"
            ]
        )
        
        print("\n📄 Drafted Email:")
        print("-" * 60)
        print(draft_result["draft"])
        print("-" * 60)
        
        # Example 2: Draft and send (uncomment to actually send)
        print("\n" + "=" * 60)
        print("Example 2: Drafting and sending an email")
        print("=" * 60)
        print("\n⚠️  Note: Uncomment the code below to actually send emails")
        print("    Make sure SMTP credentials are configured\n")
        
        # Uncomment below to actually send emails:
        # result = await app.draft_and_send(
        #     to="recipient@example.com",
        #     recipient_name="Sarah Johnson",
        #     purpose="Follow up on our meeting",
        #     tone="professional",
        #     key_points=[
        #         "Thank her for the meeting",
        #         "Confirm next steps"
        #     ],
        #     from_email="your-email@example.com"
        # )
        # 
        # if result["send"]["success"]:
        #     print("✅ Email sent successfully!")
        # else:
        #     print(f"❌ Failed to send: {result['send']['message']}")
        
    finally:
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
