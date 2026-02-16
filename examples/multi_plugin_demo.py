"""Demo showing multiple plugins working together."""

import asyncio
import os
from pathlib import Path
from openplugin import PluginManager, OpenAIProvider


async def demo_code_plugin():
    """Demonstrate code plugin."""
    print("=" * 70)
    print("📝 CODE PLUGIN DEMO")
    print("=" * 70)
    
    manager = PluginManager(plugins_dir=Path(__file__).parent.parent / "plugins")
    manager.load_plugins()
    provider = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
    
    code = """
def calculate_total(items):
    total = 0
    for item in items:
        total = total + item.price
    return total
"""
    
    # Analyze code
    print("\n1️⃣ Analyzing code...")
    analysis = await manager.execute_command(
        "code-plugin",
        "analyze",
        provider=provider,
        user_input=f"Analyze this Python code:\n\n{code}"
    )
    print(analysis[:500] + "...")
    
    # Explain code
    print("\n2️⃣ Explaining code...")
    explanation = await manager.execute_command(
        "code-plugin",
        "explain",
        provider=provider,
        user_input=f"Explain this code:\n\n{code}"
    )
    print(explanation[:500] + "...")
    
    await manager.shutdown()


async def demo_translation_plugin():
    """Demonstrate translation plugin."""
    print("\n" + "=" * 70)
    print("🌍 TRANSLATION PLUGIN DEMO")
    print("=" * 70)
    
    manager = PluginManager(plugins_dir=Path(__file__).parent.parent / "plugins")
    manager.load_plugins()
    provider = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
    
    text = "Hello, how are you? I'm learning about AI and machine learning."
    
    # Translate
    print("\n1️⃣ Translating to Spanish...")
    translation = await manager.execute_command(
        "translation-plugin",
        "translate",
        provider=provider,
        user_input=f"Translate this to Spanish: {text}"
    )
    print(f"Original: {text}")
    print(f"Translation: {translation}")
    
    # Detect language
    print("\n2️⃣ Detecting language...")
    detection = await manager.execute_command(
        "translation-plugin",
        "detect",
        provider=provider,
        user_input=f"What language is this: Bonjour, comment allez-vous?"
    )
    print(detection)
    
    await manager.shutdown()


async def demo_text_processing_plugin():
    """Demonstrate text processing plugin."""
    print("\n" + "=" * 70)
    print("📄 TEXT PROCESSING PLUGIN DEMO")
    print("=" * 70)
    
    manager = PluginManager(plugins_dir=Path(__file__).parent.parent / "plugins")
    manager.load_plugins()
    provider = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
    
    long_text = """
    Artificial Intelligence (AI) has revolutionized many industries in recent years.
    Machine learning algorithms can now process vast amounts of data and make predictions
    with remarkable accuracy. Deep learning, a subset of machine learning, uses neural
    networks to solve complex problems. Natural language processing allows computers to
    understand and generate human language. Computer vision enables machines to interpret
    visual information. These technologies are being applied in healthcare, finance,
    transportation, and many other fields.
    """
    
    # Summarize
    print("\n1️⃣ Summarizing text...")
    summary = await manager.execute_command(
        "text-processing-plugin",
        "summarize",
        provider=provider,
        user_input=f"Summarize this text in 2 sentences:\n\n{long_text}"
    )
    print(summary)
    
    # Extract information
    print("\n2️⃣ Extracting key information...")
    extracted = await manager.execute_command(
        "text-processing-plugin",
        "extract",
        provider=provider,
        user_input=f"Extract key topics and applications from this text:\n\n{long_text}"
    )
    print(extracted[:500] + "...")
    
    await manager.shutdown()


async def demo_combined_workflow():
    """Demonstrate plugins working together."""
    print("\n" + "=" * 70)
    print("🔄 COMBINED WORKFLOW DEMO")
    print("=" * 70)
    
    manager = PluginManager(plugins_dir=Path(__file__).parent.parent / "plugins")
    manager.load_plugins()
    provider = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Step 1: Get code explanation
    code = "def fibonacci(n): return n if n < 2 else fibonacci(n-1) + fibonacci(n-2)"
    print("\n1️⃣ Explaining code...")
    explanation = await manager.execute_command(
        "code-plugin",
        "explain",
        provider=provider,
        user_input=f"Explain this code:\n\n{code}"
    )
    
    # Step 2: Translate explanation
    print("\n2️⃣ Translating explanation to Spanish...")
    translated = await manager.execute_command(
        "translation-plugin",
        "translate",
        provider=provider,
        user_input=f"Translate this to Spanish: {explanation[:200]}"
    )
    print(f"English: {explanation[:200]}...")
    print(f"Spanish: {translated[:200]}...")
    
    # Step 3: Summarize
    print("\n3️⃣ Summarizing explanation...")
    summary = await manager.execute_command(
        "text-processing-plugin",
        "summarize",
        provider=provider,
        user_input=f"Summarize in one sentence: {explanation}"
    )
    print(summary)
    
    await manager.shutdown()


async def main():
    """Run all demos."""
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set")
        return
    
    await demo_code_plugin()
    await demo_translation_plugin()
    await demo_text_processing_plugin()
    await demo_combined_workflow()
    
    print("\n" + "=" * 70)
    print("✅ All demos completed!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
