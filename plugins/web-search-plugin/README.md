# Web Search Plugin

A plugin for searching the web and retrieving information. Perfect for getting current information and answering questions with up-to-date data.

## Features

- **Web Search**: Search the web for information
- **Summarize Results**: Get LLM-powered summaries of search results
- **No Browser Required**: Uses search APIs, no browser automation needed
- **No API Keys**: Uses free DuckDuckGo search (no API key required)

## Commands

### `/search`
Search the web and get results.

Example:
```
Search for "latest AI developments in 2024"
```

### `/summarize`
Search and get a summarized answer.

Example:
```
Summarize recent news about quantum computing
```

## Setup

No special setup required! The plugin uses DuckDuckGo search which doesn't require API keys.

## Usage

See `examples/web_search_app.py` for a complete example.

## How It Works

The plugin uses the `duckduckgo-search` library which:
- Doesn't require API keys
- Doesn't need a browser
- Provides clean search results
- Works out of the box

## Why This Approach?

- ✅ **No Browser**: Uses HTTP requests, not browser automation
- ✅ **No API Keys**: Free DuckDuckGo search
- ✅ **Simple**: Easy to use and understand
- ✅ **Fast**: Direct API calls, no browser overhead
- ✅ **Reliable**: Works consistently without browser dependencies
