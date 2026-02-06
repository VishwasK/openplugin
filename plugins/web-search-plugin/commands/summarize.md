# Summarize Search Results Command

Searches the web and provides a summarized answer based on the results.

## Usage

This command combines web search with LLM summarization to provide comprehensive answers.

## Input Parameters

- **query**: The question or topic to search for
- **num_results**: Number of search results to use (default: 5)
- **focus**: What aspect to focus on (facts, opinions, recent updates, etc.)

## Output

Returns a comprehensive summary that:
- Combines information from multiple sources
- Provides a coherent answer
- Cites sources when relevant
- Addresses the query directly

## Behavior

- Performs web search for the query
- Retrieves relevant results
- Uses LLM to synthesize information from results
- Provides a well-structured summary
- Can answer complex questions using web information

## Examples

- "Summarize recent developments in quantum computing"
- "What are the pros and cons of remote work based on current research?"
- "Give me an overview of the latest Python 3.12 features"
