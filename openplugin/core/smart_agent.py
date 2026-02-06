"""Smart agent that automatically selects and uses appropriate tools/plugins."""

import asyncio
from typing import Dict, List, Optional, Any
from .plugin_manager import PluginManager
from ..providers.base import LLMProvider
from ..utils.web_search import WebSearcher


class SmartAgent:
    """Intelligent agent that automatically selects and uses plugins/tools based on user queries."""

    def __init__(
        self,
        plugin_manager: PluginManager,
        provider: LLMProvider,
        enable_web_search: bool = True
    ):
        """Initialize smart agent.
        
        Args:
            plugin_manager: PluginManager instance with loaded plugins
            provider: LLM provider instance
            enable_web_search: Whether to enable automatic web search
        """
        self.manager = plugin_manager
        self.provider = provider
        self.enable_web_search = enable_web_search
        self.searcher = WebSearcher() if enable_web_search else None

    async def answer(
        self,
        question: str,
        use_web_search: Optional[bool] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Answer a question, automatically deciding whether to use web search.
        
        Args:
            question: User's question
            use_web_search: Force web search (True) or skip it (False). 
                           If None, agent decides automatically.
            **kwargs: Additional arguments for LLM
            
        Returns:
            Dictionary with answer, sources, and metadata
        """
        # Step 1: Decide if web search is needed
        if use_web_search is None:
            needs_search = await self._needs_web_search(question)
        else:
            needs_search = use_web_search
        
        # Step 2: Get web search results if needed
        search_results = None
        if needs_search and self.enable_web_search:
            search_results = self.searcher.search(question, max_results=5)
            if search_results and "error" not in search_results[0]:
                context = self.searcher.get_summary_context(question, max_results=5)
            else:
                context = None
        else:
            context = None
        
        # Step 3: Generate answer
        messages = [
            {
                "role": "system",
                "content": """You are a helpful AI assistant. Answer questions accurately and helpfully.
If web search results are provided, use them to give current, accurate information.
If no search results are provided, answer based on your training data but mention if information might be outdated."""
            },
            {
                "role": "user",
                "content": self._build_prompt(question, context)
            }
        ]
        
        answer = await self.provider.chat(messages=messages, **kwargs)
        
        return {
            "answer": answer,
            "used_web_search": needs_search and self.enable_web_search,
            "search_results": search_results if needs_search else None,
            "sources": [r["url"] for r in search_results] if search_results else []
        }

    async def _needs_web_search(self, question: str) -> bool:
        """Determine if a question needs web search.
        
        Args:
            question: User's question
            
        Returns:
            True if web search is recommended
        """
        # Use LLM to decide if search is needed
        decision_prompt = f"""Analyze this question and determine if it needs current/recent information from the web.

Question: {question}

Consider:
- Does it ask about recent events, news, or current data?
- Does it ask about specific facts that might change?
- Does it ask "what is the latest..." or "current..."?
- Would the answer benefit from up-to-date information?

Respond with only "YES" or "NO"."""
        
        try:
            response = await self.provider.chat(
                messages=[{"role": "user", "content": decision_prompt}],
                max_tokens=10,
                temperature=0.1
            )
            return "YES" in response.upper()
        except Exception:
            # Default to searching if we can't determine
            return True

    def _build_prompt(self, question: str, context: Optional[str] = None) -> str:
        """Build the prompt for answering.
        
        Args:
            question: User's question
            context: Optional web search context
            
        Returns:
            Formatted prompt
        """
        if context:
            return f"""Question: {question}

Web Search Results:
{context}

Please answer the question using the search results above. If the search results don't fully answer the question, use your knowledge to provide additional context."""
        else:
            return f"""Question: {question}

Please answer this question. Note: You're answering based on your training data, which may not include the most recent information."""

    async def execute_with_auto_routing(
        self,
        user_input: str,
        available_plugins: Optional[List[str]] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Execute user input with automatic plugin/tool routing.
        
        Args:
            user_input: User's input/request
            available_plugins: List of plugin names to consider (None = all)
            **kwargs: Additional arguments
            
        Returns:
            Dictionary with result and metadata
        """
        # Get available plugins
        if available_plugins is None:
            available_plugins = self.manager.list_plugins()
        
        # Describe available plugins to LLM
        plugin_descriptions = []
        for plugin_name in available_plugins:
            plugin = self.manager.get_plugin(plugin_name)
            if plugin:
                commands = list(plugin.commands.keys())
                plugin_descriptions.append(
                    f"- {plugin_name}: {plugin.manifest.description or 'No description'}. "
                    f"Commands: {', '.join(commands)}"
                )
        
        # Ask LLM which plugin/command to use
        routing_prompt = f"""User request: {user_input}

Available plugins:
{chr(10).join(plugin_descriptions)}

Determine which plugin and command would best handle this request.
Respond in format: PLUGIN_NAME:COMMAND_NAME
If no plugin is suitable, respond: NONE"""
        
        try:
            routing_response = await self.provider.chat(
                messages=[{"role": "user", "content": routing_prompt}],
                max_tokens=50,
                temperature=0.1
            )
            
            routing_response = routing_response.strip()
            
            if ":" in routing_response and routing_response != "NONE":
                plugin_name, command_name = routing_response.split(":", 1)
                plugin_name = plugin_name.strip()
                command_name = command_name.strip()
                
                # Execute the selected plugin command
                result = await self.manager.execute_command(
                    plugin_name=plugin_name,
                    command_name=command_name,
                    provider=self.provider,
                    user_input=user_input,
                    **kwargs
                )
                
                return {
                    "result": result,
                    "plugin_used": plugin_name,
                    "command_used": command_name,
                    "routing": "automatic"
                }
        except Exception as e:
            pass
        
        # Fallback: try to answer directly
        answer_result = await self.answer(user_input, **kwargs)
        return {
            "result": answer_result["answer"],
            "plugin_used": None,
            "command_used": None,
            "routing": "direct_answer"
        }
