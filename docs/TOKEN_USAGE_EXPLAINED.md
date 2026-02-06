# Token Usage in Web Search Plugin - Explained

## Quick Answer

**It depends on which method you use:**

1. **`simple_search()`** - ✅ **NO LLM, NO TOKENS** - Just HTTP requests
2. **`search()`** - ⚠️ **YES LLM, TOKENS USED** - Search results sent to LLM
3. **`search_and_summarize()`** - ⚠️ **YES LLM, TOKENS USED** - Results + summary

## Detailed Breakdown

### 1. Simple Search (NO Tokens)

```python
from openplugin.utils import WebSearcher

searcher = WebSearcher()
results = searcher.search("Python async", max_results=5)
formatted = searcher.search_and_format("Python async", max_results=5)
```

**Token Usage: 0** ✅
- Pure HTTP requests to DuckDuckGo
- No LLM involved
- Returns raw search results

### 2. Search with Plugin (Tokens Used)

```python
app = WebSearchApp(api_key="your-key")
result = await app.search("Python async", num_results=5)
```

**Token Usage Breakdown:**

**INPUT TOKENS:**
- System prompt (command definition): ~100-200 tokens
- Your query: ~5-10 tokens
- **Search results (all 5 results): ~500-1000 tokens** ⚠️
- Instruction: ~20 tokens
- **Total Input: ~625-1230 tokens**

**OUTPUT TOKENS:**
- LLM formatted response: ~100-300 tokens
- **Total Output: ~100-300 tokens**

**Total: ~725-1530 tokens per search**

### 3. Search and Summarize (More Tokens)

```python
result = await app.search_and_summarize(
    query="What is Python async?",
    num_results=5
)
```

**Token Usage Breakdown:**

**INPUT TOKENS:**
- System prompt: ~200-300 tokens
- Your question: ~10-20 tokens
- **Search results (all 5): ~500-1000 tokens** ⚠️
- Focus instructions: ~20 tokens
- **Total Input: ~730-1340 tokens**

**OUTPUT TOKENS:**
- Summary response: ~200-500 tokens
- **Total Output: ~200-500 tokens**

**Total: ~930-1840 tokens per search+summarize**

## Key Point: Search Results Count as Input Tokens

⚠️ **Yes, search results ARE included in the prompt and count as INPUT tokens.**

When you call:
```python
user_input = f"Question: {query}\n\nSearch Results:\n{context}"
```

The `context` contains all search results (titles, URLs, snippets), and this entire string is sent to the LLM as part of the input prompt.

## Token Usage Examples

### Example 1: Simple Search (5 results)
```
Query: "Python async programming"
Results: 5 results, ~150 words each snippet = ~750 words
Tokens: ~1000 input tokens (results) + ~200 (prompt) = ~1200 input
Output: ~200 tokens
Total: ~1400 tokens
```

### Example 2: Search + Summarize (10 results)
```
Query: "Latest AI developments"
Results: 10 results, ~150 words each = ~1500 words
Tokens: ~2000 input tokens (results) + ~300 (prompt) = ~2300 input
Output: ~400 tokens (summary)
Total: ~2700 tokens
```

## How to Minimize Token Usage

### Option 1: Use Simple Search (No LLM)
```python
# Zero tokens!
searcher = WebSearcher()
results = searcher.search("query", max_results=3)
```

### Option 2: Reduce Number of Results
```python
# Fewer results = fewer tokens
result = await app.search("query", num_results=2)  # Instead of 5
```

### Option 3: Extract Only Key Info
```python
# Only send titles and URLs, not full snippets
results = searcher.search("query", max_results=5)
context = "\n".join([f"{r['title']}: {r['url']}" for r in results])
# Much shorter = fewer tokens
```

### Option 4: Use Cheaper Model
```python
provider = OpenAIProvider(
    api_key="key",
    model="gpt-3.5-turbo"  # Cheaper than gpt-4
)
```

## Cost Estimation (OpenAI Pricing)

### GPT-4 Pricing (as of 2024)
- Input: $30 per 1M tokens
- Output: $60 per 1M tokens

**Example: Search + Summarize (5 results)**
- Input: ~1200 tokens = $0.036
- Output: ~300 tokens = $0.018
- **Total: ~$0.054 per search**

### GPT-3.5 Turbo Pricing
- Input: $0.50 per 1M tokens
- Output: $1.50 per 1M tokens

**Example: Search + Summarize (5 results)**
- Input: ~1200 tokens = $0.0006
- Output: ~300 tokens = $0.00045
- **Total: ~$0.001 per search**

## Comparison Table

| Method | LLM Used? | Input Tokens | Output Tokens | Total Tokens | Cost (GPT-4) |
|--------|-----------|--------------|---------------|--------------|--------------|
| `simple_search()` | ❌ No | 0 | 0 | 0 | $0 |
| `search()` (3 results) | ✅ Yes | ~600 | ~200 | ~800 | ~$0.03 |
| `search()` (5 results) | ✅ Yes | ~1200 | ~200 | ~1400 | ~$0.05 |
| `search_and_summarize()` (5 results) | ✅ Yes | ~1200 | ~400 | ~1600 | ~$0.06 |
| `search_and_summarize()` (10 results) | ✅ Yes | ~2300 | ~500 | ~2800 | ~$0.10 |

## Best Practices

1. **Use `simple_search()` when you just need raw results** - Zero cost!
2. **Limit results** - Use `num_results=2-3` instead of 5-10
3. **Cache results** - Don't re-search the same query
4. **Use GPT-3.5** - Much cheaper for simple formatting
5. **Extract key info** - Only send essential parts of results to LLM

## Code Example: Token-Efficient Search

```python
class EfficientWebSearch:
    def __init__(self, api_key):
        self.searcher = WebSearcher()
        self.provider = OpenAIProvider(api_key=api_key, model="gpt-3.5-turbo")
        self.cache = {}
    
    async def search_efficient(self, query, use_llm=False):
        # Check cache first
        if query in self.cache:
            return self.cache[query]
        
        # Get minimal results
        results = self.searcher.search(query, max_results=2)
        
        if not use_llm:
            # No LLM = no tokens
            return results
        
        # Only send titles, not full snippets
        context = "\n".join([
            f"{r['title']}: {r['url']}" 
            for r in results
        ])
        
        # Minimal prompt
        summary = await self.provider.chat(
            messages=[{
                "role": "user",
                "content": f"Summarize these search results:\n{context}"
            }],
            max_tokens=150  # Limit output
        )
        
        self.cache[query] = summary
        return summary
```

## Summary

- ✅ **Search itself**: No tokens (just HTTP requests)
- ⚠️ **Search results sent to LLM**: Count as INPUT tokens
- ⚠️ **LLM response**: Count as OUTPUT tokens
- 💡 **Use `simple_search()` for zero-cost searches**
- 💡 **Limit results and use GPT-3.5 to reduce costs**
