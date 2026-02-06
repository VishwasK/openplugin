"""Demonstrate token usage differences in web search plugin."""

import asyncio
import os
from openplugin.utils import WebSearcher
from examples.web_search_app import WebSearchApp


def demonstrate_token_usage():
    """Show which methods use tokens and which don't."""
    
    print("=" * 70)
    print("TOKEN USAGE IN WEB SEARCH PLUGIN")
    print("=" * 70)
    
    searcher = WebSearcher()
    query = "Python async programming"
    
    print("\n1️⃣  SIMPLE SEARCH (NO LLM, NO TOKENS)")
    print("-" * 70)
    print("Method: searcher.search() or searcher.search_and_format()")
    print("Token Usage: 0 ✅")
    print("\nExample:")
    results = searcher.search(query, max_results=3)
    print(f"   Found {len(results)} results")
    print(f"   First result: {results[0]['title'][:50]}...")
    print("   ✅ Zero tokens used!")
    
    print("\n" + "=" * 70)
    print("2️⃣  SEARCH WITH PLUGIN (USES LLM, TOKENS COUNT)")
    print("-" * 70)
    print("Method: app.search()")
    print("Token Usage: ~1200-1400 tokens ⚠️")
    print("\nWhat counts as tokens:")
    print("   ✅ Your query: ~10 tokens")
    print("   ✅ Search results (all snippets): ~1000 tokens")
    print("   ✅ System prompt: ~200 tokens")
    print("   ✅ LLM response: ~200 tokens")
    print("\n⚠️  Search results ARE included in prompt = INPUT tokens!")
    
    print("\n" + "=" * 70)
    print("3️⃣  SEARCH AND SUMMARIZE (MORE TOKENS)")
    print("-" * 70)
    print("Method: app.search_and_summarize()")
    print("Token Usage: ~1600-2800 tokens ⚠️")
    print("\nWhat counts as tokens:")
    print("   ✅ Your question: ~20 tokens")
    print("   ✅ Search results: ~1000-2000 tokens")
    print("   ✅ System prompt: ~300 tokens")
    print("   ✅ Summary response: ~400-500 tokens")
    
    print("\n" + "=" * 70)
    print("COST ESTIMATION (OpenAI GPT-4)")
    print("-" * 70)
    print("Simple Search:        $0.00 (no LLM)")
    print("Search (3 results):   ~$0.03 per search")
    print("Search (5 results):   ~$0.05 per search")
    print("Summarize (5 results): ~$0.06 per search")
    print("\n💡 Tip: Use GPT-3.5-turbo for 20x cheaper (~$0.001 per search)")
    
    print("\n" + "=" * 70)
    print("HOW TO MINIMIZE TOKENS")
    print("-" * 70)
    print("1. Use simple_search() when you just need results")
    print("2. Reduce num_results (2-3 instead of 5-10)")
    print("3. Use GPT-3.5-turbo instead of GPT-4")
    print("4. Cache results to avoid re-searching")
    print("5. Extract only titles/URLs, not full snippets")


async def compare_methods():
    """Compare different search methods side by side."""
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  OPENAI_API_KEY not set. Skipping LLM examples.")
        print("   Set it to see token usage with LLM methods.")
        return
    
    app = WebSearchApp(openai_api_key=os.getenv("OPENAI_API_KEY"))
    query = "Python async programming best practices"
    
    print("\n" + "=" * 70)
    print("COMPARISON: Different Search Methods")
    print("=" * 70)
    
    # Method 1: No LLM
    print("\n📊 Method 1: Simple Search (NO TOKENS)")
    print("-" * 70)
    start = asyncio.get_event_loop().time()
    simple_results = app.simple_search(query, num_results=3)
    elapsed = asyncio.get_event_loop().time() - start
    print(f"✅ Completed in {elapsed:.2f}s")
    print(f"✅ Token usage: 0")
    print(f"✅ Results: {len(app.get_raw_results(query, 3))} found")
    
    # Method 2: With LLM formatting
    print("\n📊 Method 2: Search with LLM Formatting (TOKENS USED)")
    print("-" * 70)
    start = asyncio.get_event_loop().time()
    llm_results = await app.search(query, num_results=3)
    elapsed = asyncio.get_event_loop().time() - start
    print(f"✅ Completed in {elapsed:.2f}s")
    print(f"⚠️  Token usage: ~800-1200 tokens")
    print(f"✅ Results formatted by LLM")
    
    # Method 3: Summarize
    print("\n📊 Method 3: Search and Summarize (MORE TOKENS)")
    print("-" * 70)
    start = asyncio.get_event_loop().time()
    summary_results = await app.search_and_summarize(query, num_results=3)
    elapsed = asyncio.get_event_loop().time() - start
    print(f"✅ Completed in {elapsed:.2f}s")
    print(f"⚠️  Token usage: ~1200-1600 tokens")
    print(f"✅ Summary generated")
    
    await app.shutdown()


if __name__ == "__main__":
    demonstrate_token_usage()
    
    print("\n" + "=" * 70)
    print("Would you like to see a live comparison? (y/n)")
    if input().strip().lower() == 'y':
        asyncio.run(compare_methods())
