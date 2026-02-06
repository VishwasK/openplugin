"""Smart Q&A app that automatically uses web search when needed."""

import asyncio
import os
from pathlib import Path
from openplugin import PluginManager, OpenAIProvider
from openplugin.core.smart_agent import SmartAgent


class SmartQAApp:
    """Smart Q&A application that automatically decides when to search the web."""

    def __init__(self, openai_api_key: str):
        """Initialize smart Q&A app.
        
        Args:
            openai_api_key: OpenAI API key
        """
        # Initialize plugin manager
        self.manager = PluginManager(plugins_dir=Path(__file__).parent.parent / "plugins")
        self.manager.load_plugins()
        
        # Initialize LLM provider
        self.provider = OpenAIProvider(api_key=openai_api_key, model="gpt-4")
        
        # Initialize smart agent
        self.agent = SmartAgent(
            plugin_manager=self.manager,
            provider=self.provider,
            enable_web_search=True
        )

    async def ask(self, question: str, force_search: bool = None) -> dict:
        """Ask a question - automatically uses web search if needed.
        
        Args:
            question: User's question
            force_search: Force web search (True) or skip (False). 
                         None = auto-decide
            
        Returns:
            Dictionary with answer and metadata
        """
        print(f"❓ Question: {question}\n")
        
        if force_search is not None:
            print(f"🔧 Search mode: {'Forced' if force_search else 'Skipped'}\n")
        else:
            print("🤔 Analyzing if web search is needed...\n")
        
        result = await self.agent.answer(
            question=question,
            use_web_search=force_search
        )
        
        return result

    async def interactive_mode(self):
        """Interactive Q&A session."""
        print("=" * 70)
        print("🤖 Smart Q&A Assistant")
        print("=" * 70)
        print("\nAsk me anything! I'll automatically search the web when needed.")
        print("Commands: [q]uit, [s]earch mode, [n]o search mode\n")
        
        search_mode = None  # None = auto
        
        while True:
            question = input("\n💬 Your question: ").strip()
            
            if not question:
                continue
            
            if question.lower() == 'q':
                print("\n👋 Goodbye!")
                break
            
            if question.lower() == 's':
                search_mode = True
                print("✅ Web search enabled for next question")
                continue
            
            if question.lower() == 'n':
                search_mode = False
                print("✅ Web search disabled for next question")
                continue
            
            # Ask the question
            result = await self.ask(question, force_search=search_mode)
            
            # Reset search mode after use
            search_mode = None
            
            # Display answer
            print("\n" + "=" * 70)
            print("📝 ANSWER")
            print("=" * 70)
            print(f"\n{result['answer']}\n")
            
            if result['used_web_search']:
                print("-" * 70)
                print("🌐 Sources:")
                for i, url in enumerate(result['sources'][:3], 1):
                    print(f"  {i}. {url}")
            
            print("=" * 70)

    async def shutdown(self):
        """Cleanup resources."""
        await self.manager.shutdown()


async def main():
    """Example usage of the smart Q&A app."""
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        return
    
    app = SmartQAApp(openai_api_key=openai_key)
    
    try:
        # Example 1: Question that needs web search
        print("=" * 70)
        print("Example 1: Question Needing Current Information")
        print("=" * 70)
        
        result1 = await app.ask(
            "What are the latest features in Python 3.12?"
        )
        
        print("\n📝 Answer:")
        print(result1['answer'])
        print(f"\n🌐 Used web search: {result1['used_web_search']}")
        if result1['sources']:
            print(f"📚 Sources: {len(result1['sources'])}")
        
        # Example 2: Question that might not need search
        print("\n" + "=" * 70)
        print("Example 2: General Knowledge Question")
        print("=" * 70)
        
        result2 = await app.ask(
            "What is the difference between async and sync programming?"
        )
        
        print("\n📝 Answer:")
        print(result2['answer'])
        print(f"\n🌐 Used web search: {result2['used_web_search']}")
        
        # Example 3: Force search
        print("\n" + "=" * 70)
        print("Example 3: Force Web Search")
        print("=" * 70)
        
        result3 = await app.ask(
            "Explain quantum computing",
            force_search=True
        )
        
        print("\n📝 Answer:")
        print(result3['answer'])
        print(f"\n🌐 Used web search: {result3['used_web_search']}")
        
        # Interactive mode
        print("\n" + "=" * 70)
        print("Interactive Mode")
        print("=" * 70)
        print("\nWould you like to try interactive mode? (y/n)")
        if input().strip().lower() == 'y':
            await app.interactive_mode()
        
    finally:
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
