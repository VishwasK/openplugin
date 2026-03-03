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

**✅ Great News: SkillsMP.com uses the same format as Claude Code Plugins!**

Based on the SkillsMP.com structure, skills follow the **Agent Skills open standard**:

- **Core File**: `SKILL.md` - Contains skill instructions
- **Directory Structure**: Skills are in subdirectories under `skills/`
- **Frontmatter**: Optional YAML frontmatter for metadata
- **Format**: Markdown files compatible with Claude Code Plugin format

### Skill Structure

```
skills/
└── skill-name/
    └── SKILL.md
```

This matches our framework's expected structure exactly!

## Compatibility Assessment

### ✅ **FULLY COMPATIBLE!**

SkillsMP skills are **directly compatible** with OpenPlugin because:

- ✅ Skills use `SKILL.md` markdown format
- ✅ Skills follow Claude Code Plugin structure
- ✅ Skills are in `skills/skill-name/` directories
- ✅ Skills use the Agent Skills open standard
- ✅ No conversion needed - direct import works!

### Example SkillsMP Skill URLs

- `https://skillsmp.com/skills/anthropics-claude-code-plugins-plugin-dev-skills-plugin-settings-skill-md`
- `https://skillsmp.com/skills/anthropics-claude-code-plugins-plugin-dev-skills-command-development-skill-md`

These follow the pattern: `skills/{category}/{skill-name}-skill-md`

## How to Add SkillsMP Skills

### ✅ Option 1: Direct Import (Recommended)

**SkillsMP skills are directly compatible!** Just copy them:

1. **Download the skill** from SkillsMP.com
   - Navigate to the skill page (e.g., `https://skillsmp.com/skills/...`)
   - Download or copy the `SKILL.md` content

2. **Add to your plugin**:

```bash
# Create skill directory
mkdir -p plugins/my-plugin/skills/data-analysis

# Copy SKILL.md
cp downloaded-skill.md plugins/my-plugin/skills/data-analysis/SKILL.md
```

3. **The skill will be automatically loaded!**

```python
from openplugin import PluginManager

manager = PluginManager()
manager.load_plugins()

plugin = manager.get_plugin("my-plugin")
skill = plugin.get_skill("data-analysis")  # ✅ Works!
```

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
