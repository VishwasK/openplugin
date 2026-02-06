"""Web search app using OpenPlugin - Search the web without a browser!"""

import asyncio
import os
from pathlib import Path
from openplugin import PluginManager, OpenAIProvider
from openplugin.utils import WebSearcher


class WebSearchApp:
    """Web search application using OpenPlugin."""

    def __init__(self, openai_api_key: str):
        """Initialize web search app.
        
        Args:
            openai_api_key: OpenAI API key (for summarize command)
        """
        # Initialize plugin manager
        self.manager = PluginManager(plugins_dir=Path(__file__).parent.parent / "plugins")
        self.manager.load_plugins()
        
        # Initialize LLM provider (for summarize command)
        self.provider = OpenAIProvider(api_key=openai_api_key, model="gpt-4")
        
        # Initialize web searcher
        self.searcher = WebSearcher()

    async def search(
        self,
        query: str,
        num_results: int = 5
    ) -> dict:
        """Search the web.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            Dictionary with search results
        """
        # Perform actual web search
        raw_results = self.searcher.search(query, max_results=num_results)
        
        # Format results for LLM
        formatted_results = self.searcher.search_and_format(query, max_results=num_results)
        
        # Use the search command from plugin to format/process results
        user_input = f"Search query: {query}\n\nSearch Results:\n{formatted_results}\n\nFormat these results in a clear, readable way."
        
        # Execute search command (LLM can format/process the results)
        try:
            llm_formatted = await self.manager.execute_command(
                "web-search-plugin",
                "search",
                provider=self.provider,
                user_input=user_input
            )
        except Exception:
            # If LLM fails, just use formatted results
            llm_formatted = formatted_results
        
        return {
            "query": query,
            "results": raw_results,
            "formatted": formatted_results,
            "llm_formatted": llm_formatted
        }

    async def search_and_summarize(
        self,
        query: str,
        num_results: int = 5,
        focus: str = None
    ) -> dict:
        """Search the web and get a summarized answer.
        
        Args:
            query: Search query or question
            num_results: Number of search results to use
            focus: What to focus on (optional)
            
        Returns:
            Dictionary with search results and summary
        """
        # Get search results
        print(f"🔍 Searching for: {query}...")
        search_results = self.searcher.search(query, max_results=num_results)
        
        if not search_results or "error" in search_results[0]:
            return {
                "error": "Search failed",
                "query": query
            }
        
        # Format results for LLM
        context = self.searcher.get_summary_context(query, max_results=num_results)
        
        # Use summarize command
        user_input = f"Question: {query}\n\nSearch Results:\n{context}"
        if focus:
            user_input += f"\n\nFocus on: {focus}"
        
        print("📝 Generating summary...")
        summary = await self.manager.execute_command(
            "web-search-plugin",
            "summarize",
            provider=self.provider,
            user_input=user_input,
            temperature=0.7
        )
        
        return {
            "query": query,
            "search_results": search_results,
            "summary": summary
        }

    def simple_search(self, query: str, num_results: int = 5) -> str:
        """Simple search without LLM (just returns formatted results).
        
        ⚠️ IMPORTANT: This method uses ZERO tokens - no LLM involved!
        Perfect for when you just need search results without processing.
        
        Args:
            query: Search query
            num_results: Number of results
            
        Returns:
            Formatted search results string
        """
        return self.searcher.search_and_format(query, max_results=num_results)
    
    def get_raw_results(self, query: str, num_results: int = 5) -> list:
        """Get raw search results without any formatting.
        
        ⚠️ IMPORTANT: This method uses ZERO tokens - no LLM involved!
        Returns raw list of dictionaries with title, url, snippet.
        
        Args:
            query: Search query
            num_results: Number of results
            
        Returns:
            List of result dictionaries
        """
        return self.searcher.search(query, max_results=num_results)

    async def interactive_search(self):
        """Interactive search session."""
        print("=" * 60)
        print("🔍 Interactive Web Search")
        print("=" * 60)
        print("\nSearch the web for information!")
        print("Commands: [s]earch, [sum]marize, [q]uit\n")
        
        while True:
            command = input("Command: ").strip().lower()
            
            if command == 'q':
                print("👋 Goodbye!")
                break
            
            if command in ['s', 'search']:
                query = input("Search query: ").strip()
                if not query:
                    continue
                
                num_results = input("Number of results [5]: ").strip() or "5"
                try:
                    num_results = int(num_results)
                except ValueError:
                    num_results = 5
                
                print("\n🔍 Searching...")
                results = await self.search(query, num_results=num_results)
                
                print("\n" + "=" * 60)
                print("📋 SEARCH RESULTS")
                print("=" * 60)
                print(self.searcher.search_and_format(query, max_results=num_results))
                print("=" * 60)
            
            elif command in ['sum', 'summarize']:
                query = input("Question to research: ").strip()
                if not query:
                    continue
                
                num_results = input("Number of sources [5]: ").strip() or "5"
                try:
                    num_results = int(num_results)
                except ValueError:
                    num_results = 5
                
                focus = input("Focus area (optional): ").strip() or None
                
                result = await self.search_and_summarize(
                    query=query,
                    num_results=num_results,
                    focus=focus
                )
                
                if "error" in result:
                    print(f"\n❌ Error: {result['error']}")
                else:
                    print("\n" + "=" * 60)
                    print("📊 SUMMARY")
                    print("=" * 60)
                    print(f"\nQuestion: {query}\n")
                    print(result["summary"])
                    print("\n" + "=" * 60)
                    print(f"\n📚 Sources used: {len(result['search_results'])}")
                    for i, r in enumerate(result['search_results'][:3], 1):
                        print(f"  {i}. {r['title']}")
                    print("=" * 60)
            
            else:
                print("Unknown command. Use [s]earch, [sum]marize, or [q]uit")

    async def shutdown(self):
        """Cleanup resources."""
        await self.manager.shutdown()


async def main():
    """Example usage of the web search app."""
    
    # Get API key (only needed for summarize command)
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("Warning: OPENAI_API_KEY not set.")
        print("You can still use simple_search() without LLM.")
        print("Set OPENAI_API_KEY for summarize functionality.\n")
    
    # Initialize app
    app = WebSearchApp(openai_api_key=openai_key or "dummy")
    
    try:
        # Example 1: Simple search (no LLM needed)
        print("=" * 60)
        print("Example 1: Simple Web Search (No LLM)")
        print("=" * 60)
        
        results = app.simple_search("Python async programming", num_results=3)
        print(results)
        
        # Example 2: Search with plugin (uses LLM for formatting)
        if openai_key:
            print("\n" + "=" * 60)
            print("Example 2: Search with Plugin")
            print("=" * 60)
            
            search_result = await app.search(
                query="latest developments in AI 2024",
                num_results=3
            )
            
            print("\nSearch Results:")
            for result in search_result["results"]:
                print(f"\n{result['title']}")
                print(f"URL: {result['url']}")
                print(f"Snippet: {result['snippet'][:100]}...")
        
        # Example 3: Search and summarize
        if openai_key:
            print("\n" + "=" * 60)
            print("Example 3: Search and Summarize")
            print("=" * 60)
            
            summary_result = await app.search_and_summarize(
                query="What are the latest features in Python 3.12?",
                num_results=5,
                focus="new features and improvements"
            )
            
            if "error" not in summary_result:
                print("\n📊 Summary:")
                print("-" * 60)
                print(summary_result["summary"])
                print("-" * 60)
        
        # Interactive mode
        print("\n" + "=" * 60)
        print("Interactive Mode")
        print("=" * 60)
        print("\nWould you like to try interactive search? (y/n)")
        if input().strip().lower() == 'y':
            await app.interactive_search()
        
    finally:
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
