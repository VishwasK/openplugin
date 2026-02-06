# Automatic Tool Selection in OpenPlugin

## Overview

By default, OpenPlugin requires you to manually specify which plugin and command to use. However, you can build intelligent agents that automatically select and use the right tools based on user queries.

## Current State: Manual Selection

```python
# You need to specify plugin and command
result = await manager.execute_command(
    plugin_name="web-search-plugin",  # Manual selection
    command_name="search",             # Manual selection
    provider=provider,
    user_input="query"
)
```

## Solution: Smart Agent

The `SmartAgent` class automatically:
1. **Decides when to use web search** based on the question
2. **Selects appropriate plugins** based on the request
3. **Routes to the right commands** automatically

## How It Works

### 1. Automatic Web Search Detection

The agent uses the LLM to determine if a question needs current information:

```python
from openplugin.core.smart_agent import SmartAgent

agent = SmartAgent(plugin_manager=manager, provider=provider)

# Automatically decides if web search is needed
result = await agent.answer("What are the latest AI developments?")
# ✅ Automatically uses web search

result = await agent.answer("What is Python?")
# ✅ Answers from training data (no search needed)
```

### 2. Automatic Plugin Routing

The agent can automatically select which plugin to use:

```python
# Automatically routes to the right plugin
result = await agent.execute_with_auto_routing(
    "Write a fantasy story about dragons"
)
# ✅ Automatically uses story-plugin:write

result = await agent.execute_with_auto_routing(
    "Search for latest Python news"
)
# ✅ Automatically uses web-search-plugin:search
```

## Complete Example: Smart Q&A App

```python
from openplugin import PluginManager, OpenAIProvider
from openplugin.core.smart_agent import SmartAgent

# Setup
manager = PluginManager()
manager.load_plugins()
provider = OpenAIProvider(api_key="your-key")

# Create smart agent
agent = SmartAgent(
    plugin_manager=manager,
    provider=provider,
    enable_web_search=True
)

# Ask questions - agent decides what to do
result = await agent.answer(
    "What are the latest features in Python 3.12?"
)
# Automatically:
# 1. Detects need for current info
# 2. Searches the web
# 3. Generates answer using search results

print(result['answer'])
print(f"Used web search: {result['used_web_search']}")
print(f"Sources: {result['sources']}")
```

## Architecture

```
User Question
    ↓
SmartAgent.answer()
    ↓
_needs_web_search() → LLM decides if search needed
    ↓
If YES: WebSearcher.search() → Get current info
    ↓
Build prompt with context (search results or not)
    ↓
LLM generates answer
    ↓
Return answer + metadata
```

## When Does It Use Web Search?

The agent automatically uses web search for:
- ✅ Questions about recent events/news
- ✅ "What is the latest..." questions
- ✅ Current data or statistics
- ✅ Recent developments in technology
- ✅ Questions that benefit from up-to-date info

The agent skips web search for:
- ✅ General knowledge questions
- ✅ Conceptual explanations
- ✅ Questions answerable from training data
- ✅ Mathematical or logical problems

## Customization

### Force Web Search

```python
# Always use web search
result = await agent.answer(
    question="Explain quantum computing",
    use_web_search=True  # Force search
)
```

### Skip Web Search

```python
# Never use web search
result = await agent.answer(
    question="What is Python?",
    use_web_search=False  # Skip search
)
```

### Custom Routing Logic

```python
class CustomSmartAgent(SmartAgent):
    async def _needs_web_search(self, question: str) -> bool:
        # Your custom logic
        keywords = ["latest", "current", "recent", "2024"]
        return any(kw in question.lower() for kw in keywords)
```

## Comparison: Manual vs Automatic

### Manual Approach

```python
# You decide everything
if "latest" in question.lower():
    # Search web
    results = searcher.search(question)
    answer = await llm.answer(question, context=results)
else:
    # Direct answer
    answer = await llm.answer(question)
```

**Pros:**
- Full control
- Predictable behavior
- Lower token usage (no routing LLM calls)

**Cons:**
- More code to write
- Need to maintain routing logic
- Less flexible

### Automatic Approach

```python
# Agent decides
result = await agent.answer(question)
```

**Pros:**
- Less code
- Handles edge cases automatically
- Easy to add new plugins

**Cons:**
- Extra LLM call for routing (small cost)
- Less control over exact behavior
- May not always choose optimally

## Best Practices

1. **Use SmartAgent for general Q&A** - Let it decide
2. **Use manual selection for specific workflows** - When you know exactly what you need
3. **Combine both approaches** - Use SmartAgent for routing, manual for execution
4. **Cache routing decisions** - Avoid repeated LLM calls for similar queries
5. **Monitor token usage** - Routing adds ~50-100 tokens per query

## Token Usage

### Manual Selection
- Direct answer: ~500-1000 tokens
- With search: ~1500-2000 tokens

### Automatic Selection
- Routing decision: ~50-100 tokens (one-time)
- Direct answer: ~500-1000 tokens
- With search: ~1500-2000 tokens
- **Total: ~50-100 extra tokens for routing**

## Example: Building Your Own Smart App

```python
class MySmartApp:
    def __init__(self, api_key):
        self.manager = PluginManager()
        self.manager.load_plugins()
        self.provider = OpenAIProvider(api_key=api_key)
        self.agent = SmartAgent(
            plugin_manager=self.manager,
            provider=self.provider
        )
    
    async def handle_query(self, user_query):
        # Agent automatically decides what to do
        result = await self.agent.answer(user_query)
        
        # You can add your own logic
        if result['used_web_search']:
            # Log search usage
            self.log_search(user_query)
        
        return result['answer']
```

## Advanced: Multi-Step Reasoning

For complex queries, you can chain multiple tool calls:

```python
async def complex_query(self, question):
    # Step 1: Answer with search if needed
    result = await self.agent.answer(question)
    
    # Step 2: If answer is incomplete, use another plugin
    if "incomplete" in result['answer'].lower():
        # Use story plugin to create example
        story = await self.manager.execute_command(
            "story-plugin",
            "write",
            provider=self.provider,
            user_input=f"Create an example story about: {question}"
        )
        result['answer'] += f"\n\nExample: {story}"
    
    return result
```

## Summary

- **Default**: Manual plugin/command selection
- **SmartAgent**: Automatic tool selection and routing
- **Best for Q&A**: Use SmartAgent for automatic web search
- **Best for workflows**: Use manual selection for specific tasks
- **You can combine both**: Use SmartAgent for routing, manual for execution

See `examples/smart_qa_app.py` for a complete working example!
