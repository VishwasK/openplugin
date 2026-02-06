"""Web search utility for web search plugin."""

from typing import List, Dict, Any, Optional
try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None


class WebSearcher:
    """Handles web search using DuckDuckGo (no API key required)."""

    def __init__(self):
        """Initialize web searcher."""
        if DDGS is None:
            raise ImportError(
                "duckduckgo-search is not installed. "
                "Install it with: pip install duckduckgo-search"
            )
        self.ddgs = DDGS()

    def search(
        self,
        query: str,
        max_results: int = 5,
        region: str = "us-en"
    ) -> List[Dict[str, Any]]:
        """Search the web.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            region: Region/language for search (default: us-en)
            
        Returns:
            List of search results with title, url, and snippet
        """
        try:
            results = self.ddgs.text(
                query,
                max_results=max_results,
                region=region
            )
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "snippet": result.get("body", ""),
                    "rank": len(formatted_results) + 1
                })
            
            return formatted_results
        except Exception as e:
            return [{
                "error": f"Search failed: {str(e)}",
                "title": "",
                "url": "",
                "snippet": ""
            }]

    def search_and_format(
        self,
        query: str,
        max_results: int = 5
    ) -> str:
        """Search and format results as a readable string.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            Formatted search results as string
        """
        results = self.search(query, max_results=max_results)
        
        if not results or "error" in results[0]:
            return f"Search failed for query: {query}"
        
        formatted = f"Search results for: {query}\n\n"
        formatted += "=" * 60 + "\n\n"
        
        for i, result in enumerate(results, 1):
            formatted += f"{i}. {result['title']}\n"
            formatted += f"   URL: {result['url']}\n"
            formatted += f"   {result['snippet']}\n\n"
        
        return formatted

    def get_summary_context(
        self,
        query: str,
        max_results: int = 5
    ) -> str:
        """Get search results formatted for LLM summarization.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            Formatted context string for LLM
        """
        results = self.search(query, max_results=max_results)
        
        if not results or "error" in results[0]:
            return f"Could not find information about: {query}"
        
        context = f"Web search results for: {query}\n\n"
        
        for i, result in enumerate(results, 1):
            context += f"Source {i}: {result['title']}\n"
            context += f"URL: {result['url']}\n"
            context += f"Content: {result['snippet']}\n\n"
        
        return context
