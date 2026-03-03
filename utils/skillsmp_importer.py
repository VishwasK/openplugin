"""Utility for importing skills from SkillsMP.com into OpenPlugin format."""

import json
import requests
from pathlib import Path
from typing import Dict, List, Optional, Any
import os


class SkillsMPImporter:
    """Import skills from SkillsMP.com to OpenPlugin format."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize SkillsMP importer.
        
        Args:
            api_key: Optional API key for SkillsMP (if required)
        """
        self.api_key = api_key or os.getenv("SKILLSMP_API_KEY")
        self.base_url = "https://skillsmp.com/api"  # Placeholder - verify actual API

    def import_skill(
        self,
        skill_id: str,
        plugin_path: Path,
        skill_name: Optional[str] = None
    ) -> bool:
        """Import a skill from SkillsMP to a plugin.
        
        Args:
            skill_id: SkillsMP skill ID
            plugin_path: Path to plugin directory
            skill_name: Optional name for the skill (defaults to skill_id)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Fetch skill from SkillsMP
            skill_data = self._fetch_skill(skill_id)
            if not skill_data:
                return False
            
            # Convert to OpenPlugin format
            skill_content = self._convert_to_openplugin_format(skill_data)
            
            # Save to plugin
            skill_name = skill_name or skill_id
            skill_dir = plugin_path / "skills" / skill_name
            skill_dir.mkdir(parents=True, exist_ok=True)
            
            skill_file = skill_dir / "SKILL.md"
            with open(skill_file, "w", encoding="utf-8") as f:
                f.write(skill_content)
            
            return True
        except Exception as e:
            print(f"Error importing skill {skill_id}: {e}")
            return False

    def _fetch_skill(self, skill_id: str) -> Optional[Dict[str, Any]]:
        """Fetch skill data from SkillsMP.
        
        Args:
            skill_id: Skill ID
            
        Returns:
            Skill data dictionary or None
        """
        # Placeholder - implement actual API call
        # This would need to be updated based on SkillsMP's actual API
        
        try:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            # Example API call (needs to be verified)
            response = requests.get(
                f"{self.base_url}/skills/{skill_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to fetch skill: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching skill: {e}")
            return None

    def _convert_to_openplugin_format(self, skill_data: Dict[str, Any]) -> str:
        """Convert SkillsMP skill format to OpenPlugin SKILL.md format.
        
        Args:
            skill_data: SkillsMP skill data
            
        Returns:
            Markdown content for SKILL.md
        """
        # Extract skill information
        name = skill_data.get("name", "Unknown Skill")
        description = skill_data.get("description", "")
        content = skill_data.get("content", "")
        capabilities = skill_data.get("capabilities", [])
        
        # Build markdown
        md_content = f"# {name}\n\n"
        
        if description:
            md_content += f"{description}\n\n"
        
        if capabilities:
            md_content += "## Capabilities\n\n"
            for cap in capabilities:
                md_content += f"- {cap}\n"
            md_content += "\n"
        
        if content:
            md_content += f"## Skill Definition\n\n{content}\n\n"
        
        # Add metadata if available
        if skill_data.get("examples"):
            md_content += "## Examples\n\n"
            for example in skill_data.get("examples", []):
                md_content += f"- {example}\n"
            md_content += "\n"
        
        return md_content

    def list_available_skills(
        self,
        category: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """List available skills from SkillsMP.
        
        Args:
            category: Optional category filter (e.g., "data-ai")
            limit: Maximum number of skills to return
            
        Returns:
            List of skill dictionaries
        """
        try:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            params = {"limit": limit}
            if category:
                params["category"] = category
            
            # Example API call (needs to be verified)
            response = requests.get(
                f"{self.base_url}/skills",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get("skills", [])
            else:
                print(f"Failed to list skills: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error listing skills: {e}")
            return []

    def search_skills(self, query: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for skills on SkillsMP.
        
        Args:
            query: Search query
            category: Optional category filter
            
        Returns:
            List of matching skills
        """
        try:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            params = {"q": query}
            if category:
                params["category"] = category
            
            response = requests.get(
                f"{self.base_url}/skills/search",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get("results", [])
            else:
                return []
        except Exception as e:
            print(f"Error searching skills: {e}")
            return []


def import_skill_from_skillsmp(
    skill_id: str,
    plugin_path: Path,
    skill_name: Optional[str] = None
) -> bool:
    """Convenience function to import a skill from SkillsMP.
    
    Args:
        skill_id: SkillsMP skill ID
        plugin_path: Path to plugin directory
        skill_name: Optional skill name
        
    Returns:
        True if successful
    """
    importer = SkillsMPImporter()
    return importer.import_skill(skill_id, plugin_path, skill_name)
