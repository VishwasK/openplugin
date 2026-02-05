"""Simple story writing app using OpenPlugin - No external dependencies needed!"""

import asyncio
import os
from pathlib import Path
from openplugin import PluginManager, OpenAIProvider


class StoryApp:
    """Simple story writing application using OpenPlugin."""

    def __init__(self, openai_api_key: str):
        """Initialize story app.
        
        Args:
            openai_api_key: OpenAI API key
        """
        # Initialize plugin manager
        self.manager = PluginManager(plugins_dir=Path(__file__).parent.parent / "plugins")
        self.manager.load_plugins()
        
        # Initialize LLM provider
        self.provider = OpenAIProvider(api_key=openai_api_key, model="gpt-4")

    async def write_story(
        self,
        prompt: str,
        genre: str = None,
        length: str = "medium",
        tone: str = None
    ) -> str:
        """Write a new story.
        
        Args:
            prompt: What kind of story to write
            genre: Story genre (fantasy, sci-fi, mystery, etc.)
            length: Story length (short, medium, long)
            tone: Story tone (funny, serious, dark, etc.)
            
        Returns:
            Generated story text
        """
        # Build user input
        user_input = prompt
        if genre:
            user_input += f"\nGenre: {genre}"
        if length:
            user_input += f"\nLength: {length}"
        if tone:
            user_input += f"\nTone: {tone}"
        
        # Execute the write command
        result = await self.manager.execute_command(
            "story-plugin",
            "write",
            provider=self.provider,
            user_input=user_input,
            temperature=0.8  # Higher temperature for creativity
        )
        
        return result

    async def continue_story(
        self,
        story: str,
        direction: str = None,
        length: str = "medium"
    ) -> str:
        """Continue an existing story.
        
        Args:
            story: The existing story text
            direction: Optional direction (e.g., "add a twist", "introduce new character")
            length: How much to add (short, medium, long)
            
        Returns:
            Story continuation
        """
        user_input = f"Continue this story:\n\n{story}"
        if direction:
            user_input += f"\n\nDirection: {direction}"
        if length:
            user_input += f"\nLength: {length}"
        
        result = await self.manager.execute_command(
            "story-plugin",
            "continue",
            provider=self.provider,
            user_input=user_input,
            temperature=0.8
        )
        
        return result

    async def improve_story(
        self,
        story: str,
        focus: str = None,
        style: str = None
    ) -> str:
        """Improve an existing story.
        
        Args:
            story: The story to improve
            focus: What to focus on (dialogue, descriptions, pacing, etc.)
            style: Desired style (literary, casual, poetic, etc.)
            
        Returns:
            Improved story
        """
        user_input = f"Improve this story:\n\n{story}"
        if focus:
            user_input += f"\n\nFocus on: {focus}"
        if style:
            user_input += f"\nStyle: {style}"
        
        result = await self.manager.execute_command(
            "story-plugin",
            "improve",
            provider=self.provider,
            user_input=user_input,
            temperature=0.7
        )
        
        return result

    async def interactive_story(self):
        """Interactive story writing session."""
        print("=" * 60)
        print("📖 Interactive Story Writer")
        print("=" * 60)
        print("\nLet's write a story together!")
        
        # Get story prompt
        print("\nWhat kind of story would you like to write?")
        prompt = input("> ")
        
        print("\nOptional settings (press Enter to skip):")
        genre = input("Genre (fantasy, sci-fi, mystery, etc.): ").strip() or None
        length = input("Length (short, medium, long) [medium]: ").strip() or "medium"
        tone = input("Tone (funny, serious, dark, etc.): ").strip() or None
        
        print("\n✨ Writing your story...")
        story = await self.write_story(
            prompt=prompt,
            genre=genre,
            length=length,
            tone=tone
        )
        
        print("\n" + "=" * 60)
        print("📝 YOUR STORY")
        print("=" * 60)
        print("\n" + story)
        print("\n" + "=" * 60)
        
        # Ask if user wants to continue
        while True:
            action = input("\nWhat would you like to do?\n"
                         "[c]ontinue, [i]mprove, [n]ew story, [q]uit: ").strip().lower()
            
            if action == 'c':
                direction = input("How should I continue? (optional): ").strip() or None
                print("\n✨ Continuing your story...")
                continuation = await self.continue_story(story, direction=direction)
                print("\n" + continuation)
                story += "\n\n" + continuation
                
            elif action == 'i':
                focus = input("What to improve? (dialogue, descriptions, etc.) (optional): ").strip() or None
                print("\n✨ Improving your story...")
                improved = await self.improve_story(story, focus=focus)
                print("\n" + improved)
                story = improved
                
            elif action == 'n':
                return await self.interactive_story()
                
            elif action == 'q':
                print("\n👋 Thanks for writing with us!")
                break
            else:
                print("Invalid option. Please try again.")

    async def shutdown(self):
        """Cleanup resources."""
        await self.manager.shutdown()


async def main():
    """Example usage of the story app."""
    
    # Get API key from environment
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("\nSet it with: export OPENAI_API_KEY='your-key'")
        return
    
    # Initialize app
    app = StoryApp(openai_api_key=openai_key)
    
    try:
        # Example 1: Simple story writing
        print("=" * 60)
        print("Example 1: Write a Simple Story")
        print("=" * 60)
        
        story = await app.write_story(
            prompt="Write a fantasy story about a young wizard discovering their powers",
            genre="fantasy",
            length="short",
            tone="adventurous"
        )
        
        print("\n📖 Generated Story:")
        print("-" * 60)
        print(story)
        print("-" * 60)
        
        # Example 2: Continue the story
        print("\n" + "=" * 60)
        print("Example 2: Continue the Story")
        print("=" * 60)
        
        continuation = await app.continue_story(
            story=story,
            direction="Add a plot twist where the wizard discovers a dark secret",
            length="short"
        )
        
        print("\n📖 Story Continuation:")
        print("-" * 60)
        print(continuation)
        print("-" * 60)
        
        # Example 3: Improve the story
        print("\n" + "=" * 60)
        print("Example 3: Improve the Story")
        print("=" * 60)
        
        full_story = story + "\n\n" + continuation
        improved = await app.improve_story(
            story=full_story,
            focus="descriptions and dialogue",
            style="literary"
        )
        
        print("\n📖 Improved Story:")
        print("-" * 60)
        print(improved)
        print("-" * 60)
        
        # Interactive mode
        print("\n" + "=" * 60)
        print("Interactive Mode")
        print("=" * 60)
        print("\nWould you like to try interactive story writing? (y/n)")
        if input().strip().lower() == 'y':
            await app.interactive_story()
        
    finally:
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
