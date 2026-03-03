# SkillsMP.com Compatibility Guide

## Overview

This document explains how to use skills from [skillsmp.com](https://skillsmp.com/categories/data-ai) with the OpenPlugin framework.

## Current Framework Structure

OpenPlugin expects skills in this structure:

```
plugin-name/
└── skills/
    └── skill-name/
        └── SKILL.md
```

Skills are:
- Markdown files (`.md`)
- Stored in subdirectories under `skills/`
- Loaded automatically by the `Plugin` class
- Accessed via `plugin.get_skill(skill_name)`

## SkillsMP.com Format

SkillsMP.com appears to be a marketplace for Claude Code skills. To determine compatibility, we need to understand:

1. **Skill Format**: What format do SkillsMP skills use?
   - Are they markdown files?
   - Do they have a specific structure?
   - Are they compatible with Claude Code Plugin format?

2. **Skill Structure**: How are skills organized?
   - Single file or directory structure?
   - What metadata is included?
   - Are there dependencies or requirements?

## Compatibility Assessment

### ✅ Likely Compatible If:

- SkillsMP skills use markdown format
- Skills follow Claude Code Plugin structure
- Skills are self-contained (no external dependencies)
- Skills use standard skill definitions

### ⚠️ May Need Adaptation If:

- SkillsMP uses a different format (JSON, YAML, etc.)
- Skills have different metadata structure
- Skills require specific tooling or APIs
- Skills have dependencies on other skills

## How to Add SkillsMP Skills

### Option 1: Direct Import (If Compatible)

If SkillsMP skills match our format:

1. Download the skill from SkillsMP
2. Extract to your plugin's `skills/` directory:

```bash
plugins/my-plugin/
└── skills/
    └── skillsmp-data-analysis/
        └── SKILL.md
```

3. The skill will be automatically loaded!

### Option 2: Create Adapter Plugin

If SkillsMP uses a different format, create an adapter:

```python
# utils/skillsmp_adapter.py
def convert_skillsmp_to_openplugin(skillsmp_skill_path):
    """Convert SkillsMP skill format to OpenPlugin format."""
    # Read SkillsMP skill
    # Convert to our format
    # Save to plugins/ directory
    pass
```

### Option 3: Manual Conversion

1. Download skill from SkillsMP
2. Review the skill structure
3. Convert to OpenPlugin format:
   - Create `skills/skill-name/` directory
   - Create `SKILL.md` with skill content
   - Update plugin manifest if needed

## Example: Adding a Data/AI Skill

Let's say you want to add a "Data Analysis" skill from SkillsMP:

### Step 1: Create Skill Directory

```bash
mkdir -p plugins/data-plugin/skills/data-analysis
```

### Step 2: Add Skill File

Create `plugins/data-plugin/skills/data-analysis/SKILL.md`:

```markdown
# Data Analysis Skill

This skill enables AI agents to analyze datasets and generate insights.

## Capabilities

- Load and parse CSV/JSON data
- Generate statistical summaries
- Create data visualizations (descriptions)
- Identify patterns and trends

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
```

### Step 3: Use the Skill

```python
from openplugin import PluginManager, OpenAIProvider

manager = PluginManager()
manager.load_plugins()

plugin = manager.get_plugin("data-plugin")
skill_content = plugin.get_skill("data-analysis")

# Use skill content with LLM
provider = OpenAIProvider(api_key="your-key")
result = await provider.chat(
    messages=[{
        "role": "system",
        "content": f"You have access to this skill:\n\n{skill_content}"
    }]
)
```

## Checking Compatibility

To check if a SkillsMP skill is compatible:

1. **Download the skill** from SkillsMP
2. **Inspect the format**:
   ```bash
   # Check file structure
   ls -la downloaded-skill/
   
   # Check if it's markdown
   file downloaded-skill/*.md
   ```

3. **Compare with our structure**:
   - Does it have a `SKILL.md` file?
   - Is it in a directory structure?
   - Does it match our expected format?

4. **Test loading**:
   ```python
   # Try loading as a skill
   plugin = Plugin(Path("path/to/skill"))
   skill = plugin.get_skill("skill-name")
   ```

## Creating a SkillsMP Integration

If SkillsMP has an API, we could create an integration:

```python
# utils/skillsmp_importer.py
class SkillsMPImporter:
    """Import skills from SkillsMP.com."""
    
    def import_skill(self, skill_id: str, plugin_name: str):
        """Import a skill from SkillsMP to a plugin."""
        # Fetch skill from SkillsMP API
        # Convert to OpenPlugin format
        # Save to plugins directory
        pass
    
    def list_available_skills(self, category: str = None):
        """List available skills from SkillsMP."""
        # Query SkillsMP API
        # Return list of skills
        pass
```

## Recommendations

1. **Investigate SkillsMP Format**: 
   - Check if they publish their format specification
   - Download a sample skill to inspect
   - Compare with Claude Code Plugin format

2. **Create Compatibility Layer**:
   - If formats differ, create a converter
   - Support both formats if needed
   - Document conversion process

3. **Test Integration**:
   - Try importing a few skills
   - Verify they work with our framework
   - Document any issues

## Next Steps

1. ✅ Document our skill format (this doc)
2. 🔄 Investigate SkillsMP format
3. 🔄 Create adapter/converter if needed
4. 🔄 Test with real SkillsMP skills
5. 🔄 Add import utility if useful

## Questions to Answer

- What format does SkillsMP use?
- Are SkillsMP skills compatible with Claude Code Plugin format?
- Do we need a converter/adapter?
- Can we directly use SkillsMP skills?

## Contributing

If you've successfully imported SkillsMP skills, please:
1. Document the process
2. Share conversion scripts
3. Update this guide
4. Add examples
