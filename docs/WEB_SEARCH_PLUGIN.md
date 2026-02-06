# Web Search Plugin Guide

## Overview

The Web Search Plugin allows you to search the web and retrieve information without needing a browser or API keys. It uses DuckDuckGo search which is free and doesn't require authentication.

## Key Features

- ✅ **No Browser Required**: Uses HTTP requests, not browser automation
- ✅ **No API Keys**: Free DuckDuckGo search (no authentication needed)
- ✅ **Simple Integration**: Easy to use in your applications
- ✅ **LLM Summarization**: Optional LLM-powered summaries of search results

## How It Works

The plugin uses the `duckduckgo-search` Python library which:
- Makes HTTP requests to DuckDuckGo's search API
- Returns structured search results (title, URL, snippet)
- Doesn't require browser automation
- Works without API keys

## Installation

```bash
pip install duckduckgo-search
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

## Basic Usage

### Simple Search (No LLM)

```python
from openplugin.utils import WebSearcher

searcher = WebSearcher()

# Search and get results
results = searcher.search("Python async programming", max_results=5)

for result in results:
    print(f"{result['title']}")
    print(f"URL: {result['url']}")
    print(f"Snippet: {result['snippet']}\n")
```

### Search with Plugin (LLM Formatting)

```python
from openplugin import PluginManager, OpenAIProvider
from openplugin.utils import WebSearcher

manager = PluginManager()
manager.load_plugins()

provider = OpenAIProvider(api_key="your-key")
searcher = WebSearcher()

# Get search results
results = searcher.search("latest AI developments", max_results=5)

# Format for LLM
context = searcher.get_summary_context("latest AI developments", max_results=5)

# Use plugin to process
result = await manager.execute_command(
    "web-search-plugin",
    "search",
    provider=provider,
    user_input=f"Search results:\n{context}\n\nFormat these results."
)
```

### Search and Summarize

```python
from examples.web_search_app import WebSearchApp

app = WebSearchApp(openai_api_key="your-key")

result = await app.search_and_summarize(
    query="What are the latest features in Python 3.12?",
    num_results=5,
    focus="new features"
)

print(result["summary"])
```

## Commands

### `/search`

Searches the web and returns formatted results.

**Input:**
- Query to search for
- Number of results (optional)

**Output:**
- Formatted search results with titles, URLs, and snippets

### `/summarize`

Searches the web and provides a summarized answer using LLM.

**Input:**
- Question or topic
- Number of sources to use
- Focus area (optional)

**Output:**
- Comprehensive summary based on search results

## Example: Building a Research Assistant

```python
from openplugin import PluginManager, OpenAIProvider
from openplugin.utils import WebSearcher

class ResearchAssistant:
    def __init__(self, api_key):
        self.manager = PluginManager()
        self.manager.load_plugins()
        self.provider = OpenAIProvider(api_key=api_key)
        self.searcher = WebSearcher()
    
    async def research(self, topic):
        # Search for information
        results = self.searcher.search(topic, max_results=5)
        
        # Get context
        context = self.searcher.get_summary_context(topic, max_results=5)
        
        # Generate summary
        summary = await self.manager.execute_command(
            "web-search-plugin",
            "summarize",
            provider=self.provider,
            user_input=f"Research topic: {topic}\n\nSources:\n{context}"
        )
        
        return {
            "topic": topic,
            "sources": results,
            "summary": summary
        }
```

## Why DuckDuckGo?

- **Free**: No API keys or authentication required
- **Privacy**: Doesn't track searches
- **Simple**: Easy HTTP API
- **Reliable**: Works consistently
- **No Browser**: Direct API calls, no Selenium/Playwright needed

## Alternatives

If you want to use other search engines:

### Google Custom Search API
```python
# Requires API key
from googleapiclient.discovery import build

service = build("customsearch", "v1", developerKey="your-key")
results = service.cse().list(q="query", cx="your-cx").execute()
```

### Bing Search API
```python
# Requires API key
import requests

headers = {"Ocp-Apim-Subscription-Key": "your-key"}
response = requests.get(
    "https://api.bing.microsoft.com/v7.0/search",
    headers=headers,
    params={"q": "query"}
)
```

### SerpAPI
```python
# Requires API key
from serpapi import GoogleSearch

search = GoogleSearch({"q": "query", "api_key": "your-key"})
results = search.get_dict()
```

## Limitations

- DuckDuckGo may have rate limits (not officially documented)
- Results may vary compared to Google/Bing
- Some specialized searches may not be available
- No image/video search in this implementation

## Best Practices

1. **Cache Results**: Cache search results to avoid repeated searches
2. **Rate Limiting**: Add delays between searches if doing many
3. **Error Handling**: Always handle search failures gracefully
4. **Result Validation**: Validate URLs and content before using
5. **Privacy**: Be mindful of what you're searching for

## Troubleshooting

### "duckduckgo-search is not installed"
```bash
pip install duckduckgo-search
```

### Search returns empty results
- Try a different query
- Check your internet connection
- DuckDuckGo may be temporarily unavailable

### Rate limiting
- Add delays between searches
- Consider caching results
- Use multiple search providers

## Next Steps

- Try the example: `python examples/web_search_app.py`
- Build your own search-powered app
- Combine with other plugins for powerful workflows
- Add result caching for better performance
