"""Example: Importing a skill from SkillsMP.com into OpenPlugin."""

import asyncio
from pathlib import Path
from openplugin import PluginManager, OpenAIProvider
from openplugin.utils.skillsmp_importer import SkillsMPImporter, import_skill_from_skillsmp


async def example_manual_import():
    """Example: Manually importing a SkillsMP skill."""
    print("=" * 70)
    print("Example 1: Manual Import from SkillsMP")
    print("=" * 70)
    
    # Step 1: Download skill from SkillsMP (you'd do this manually)
    # For example: https://skillsmp.com/skills/.../data-analysis-skill-md
    
    # Step 2: Create plugin directory structure
    plugin_path = Path("./plugins/data-plugin")
    skill_dir = plugin_path / "skills" / "data-analysis"
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 3: Copy SKILL.md content
    # In real usage, you'd download this from SkillsMP
    skill_content = """# Data Analysis Skill

This skill enables AI agents to analyze datasets and generate insights.

## Capabilities

- Load and parse CSV/JSON data
- Generate statistical summaries
- Create data visualizations (descriptions)
- Identify patterns and trends
- Generate reports

## Usage

The agent can analyze data by:
1. Loading the dataset
2. Examining structure and types
3. Computing statistics
4. Identifying insights
5. Generating reports

## Examples

- "Analyze this sales data and find trends"
- "What are the key insights from this dataset?"
- "Generate a summary of this data"
"""
    
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(skill_content)
    
    print(f"✅ Skill saved to: {skill_file}")
    print("\nThe skill will be automatically loaded when you load the plugin!")


async def example_using_importer():
    """Example: Using the SkillsMPImporter utility."""
    print("\n" + "=" * 70)
    print("Example 2: Using SkillsMPImporter")
    print("=" * 70)
    
    # Initialize importer
    importer = SkillsMPImporter()
    
    # List available skills
    print("\n📋 Available Data/AI skills:")
    skills = importer.list_available_skills(category="data-ai", limit=10)
    for skill in skills[:5]:
        print(f"  - {skill.get('name', 'Unknown')} (ID: {skill.get('id', 'N/A')})")
    
    # Import a specific skill
    print("\n📥 Importing skill...")
    plugin_path = Path("./plugins/data-plugin")
    success = import_skill_from_skillsmp(
        skill_id="example-skill-id",
        plugin_path=plugin_path,
        skill_name="data-analysis"
    )
    
    if success:
        print("✅ Skill imported successfully!")
    else:
        print("⚠️  Import failed (this is expected if SkillsMP API is not configured)")


async def example_using_imported_skill():
    """Example: Using an imported skill."""
    print("\n" + "=" * 70)
    print("Example 3: Using Imported Skill")
    print("=" * 70)
    
    import os
    
    # Load plugins
    manager = PluginManager(plugins_dir=Path("./plugins"))
    manager.load_plugins()
    
    # Get plugin
    plugin = manager.get_plugin("data-plugin")
    if not plugin:
        print("⚠️  Plugin not found. Make sure you've imported a skill first.")
        return
    
    # Get skill
    skill = plugin.get_skill("data-analysis")
    if not skill:
        print("⚠️  Skill not found. Make sure you've imported it.")
        return
    
    print("\n📖 Skill Content:")
    print("-" * 70)
    print(skill[:500] + "..." if len(skill) > 500 else skill)
    print("-" * 70)
    
    # Use skill with LLM
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        provider = OpenAIProvider(api_key=api_key)
        
        print("\n🤖 Using skill with LLM...")
        result = await provider.chat(
            messages=[
                {
                    "role": "system",
                    "content": f"You have access to this skill:\n\n{skill}\n\nUse it to help analyze data."
                },
                {
                    "role": "user",
                    "content": "Analyze this dataset: [1, 2, 3, 4, 5, 10, 15, 20]"
                }
            ]
        )
        
        print("\n📊 Analysis Result:")
        print(result)
    
    await manager.shutdown()


async def main():
    """Run all examples."""
    await example_manual_import()
    await example_using_importer()
    await example_using_imported_skill()
    
    print("\n" + "=" * 70)
    print("✅ Examples completed!")
    print("=" * 70)
    print("\nTo import real SkillsMP skills:")
    print("1. Visit https://skillsmp.com/categories/data-ai")
    print("2. Choose a skill")
    print("3. Copy the SKILL.md content")
    print("4. Save to plugins/your-plugin/skills/skill-name/SKILL.md")


if __name__ == "__main__":
    asyncio.run(main())
