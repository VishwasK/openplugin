"""Salesforce integration app using OpenPlugin with Agentforce actions."""

import asyncio
import os
import json
from pathlib import Path
from openplugin import PluginManager, OpenAIProvider
from openplugin.utils import SalesforceClient


class SalesforceApp:
    """Salesforce integration application using OpenPlugin."""

    def __init__(self, openai_api_key: str):
        """Initialize Salesforce app.
        
        Args:
            openai_api_key: OpenAI API key
        """
        # Initialize plugin manager
        self.manager = PluginManager(plugins_dir=Path(__file__).parent.parent / "plugins")
        self.manager.load_plugins()
        
        # Initialize LLM provider
        self.provider = OpenAIProvider(api_key=openai_api_key, model="gpt-4")
        
        # Initialize Salesforce client
        try:
            self.sf_client = SalesforceClient()
        except Exception as e:
            print(f"Warning: Salesforce client not initialized: {e}")
            print("Set SALESFORCE_USERNAME, SALESFORCE_PASSWORD, etc.")
            print("Or use OAuth token: SalesforceClient.from_token(access_token, instance_url)")
            self.sf_client = None

    async def query_salesforce(
        self,
        query_description: str,
        soql: Optional[str] = None
    ) -> dict:
        """Query Salesforce data.
        
        Args:
            query_description: Natural language description of what to query
            soql: Optional SOQL query (if not provided, will be generated)
            
        Returns:
            Query results
        """
        if not self.sf_client:
            return {"error": "Salesforce client not initialized"}
        
        # If SOQL not provided, use LLM to generate it
        if not soql:
            soql_prompt = f"""Generate a SOQL query for Salesforce based on this request:
{query_description}

Return only the SOQL query, nothing else."""
            
            soql = await self.provider.chat(
                messages=[{"role": "user", "content": soql_prompt}],
                max_tokens=200,
                temperature=0.1
            )
            soql = soql.strip().strip('"').strip("'")
        
        # Execute query
        results = self.sf_client.query(soql)
        
        # Format results using plugin
        if results["success"]:
            formatted = await self.manager.execute_command(
                "salesforce-plugin",
                "query",
                provider=self.provider,
                user_input=f"Query: {query_description}\nSOQL: {soql}\nResults: {json.dumps(results['records'][:5], indent=2)}"
            )
            results["formatted"] = formatted
        
        return results

    async def create_record(
        self,
        object_type: str,
        description: str
    ) -> dict:
        """Create a Salesforce record.
        
        Args:
            object_type: Salesforce object type
            description: Natural language description of record to create
            
        Returns:
            Creation result
        """
        if not self.sf_client:
            return {"error": "Salesforce client not initialized"}
        
        # Use LLM to extract fields from description
        extract_prompt = f"""Extract field values for creating a {object_type} record in Salesforce.

Description: {description}

Return a JSON object with field names and values. Only include the JSON, nothing else."""
        
        fields_json = await self.provider.chat(
            messages=[{"role": "user", "content": extract_prompt}],
            max_tokens=300,
            temperature=0.1
        )
        
        try:
            fields = json.loads(fields_json.strip().strip('`').strip('json'))
        except:
            # Fallback: use plugin command
            result = await self.manager.execute_command(
                "salesforce-plugin",
                "create-record",
                provider=self.provider,
                user_input=f"Create {object_type}: {description}"
            )
            return {"result": result, "note": "Used LLM to generate creation"}
        
        # Create record
        result = self.sf_client.create_record(object_type, fields)
        
        return result

    async def execute_agentforce_action(
        self,
        action_name: str,
        action_description: str,
        record_id: Optional[str] = None
    ) -> dict:
        """Execute a Salesforce Agentforce action.
        
        Args:
            action_name: Name of the Agentforce action
            action_description: Description of what the action should do
            record_id: Optional record ID
            
        Returns:
            Action execution result
        """
        if not self.sf_client:
            return {"error": "Salesforce client not initialized"}
        
        # Extract parameters from description
        params_prompt = f"""Extract parameters for Salesforce Agentforce action '{action_name}'.

Action description: {action_description}
Record ID: {record_id or 'N/A'}

Return a JSON object with parameter names and values."""
        
        params_json = await self.provider.chat(
            messages=[{"role": "user", "content": params_prompt}],
            max_tokens=300,
            temperature=0.1
        )
        
        try:
            params = json.loads(params_json.strip().strip('`').strip('json'))
        except:
            params = {}
        
        # Execute action
        result = self.sf_client.execute_agentforce_action(
            action_name=action_name,
            action_params=params,
            record_id=record_id
        )
        
        # Format using plugin
        formatted = await self.manager.execute_command(
            "salesforce-plugin",
            "execute-action",
            provider=self.provider,
            user_input=f"Action: {action_name}\nDescription: {action_description}\nResult: {json.dumps(result, indent=2)}"
        )
        
        result["formatted"] = formatted
        return result

    async def shutdown(self):
        """Cleanup resources."""
        await self.manager.shutdown()


async def main():
    """Example usage of Salesforce app."""
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("Error: OPENAI_API_KEY not set")
        return
    
    app = SalesforceApp(openai_api_key=openai_key)
    
    if not app.sf_client:
        print("\n⚠️  Salesforce not configured. Examples will show structure only.")
        print("\nTo use Salesforce, set:")
        print("  export SALESFORCE_USERNAME='your-username'")
        print("  export SALESFORCE_PASSWORD='your-password'")
        print("  export SALESFORCE_SECURITY_TOKEN='your-token'")
        print("\nOr use OAuth token:")
        print("  # Alternative: Connect with existing OAuth token")
        print("  # sf_client = SalesforceClient.from_token(")
        print("  #     access_token='your_access_token',")
        print("  #     instance_url='https://yourorg.my.salesforce.com'")
        print("  # )")
        return
    
    try:
        # Example 1: Query Salesforce
        print("=" * 70)
        print("Example 1: Query Salesforce")
        print("=" * 70)
        
        result = await app.query_salesforce(
            query_description="Get all Accounts with Industry 'Technology'"
        )
        
        if result.get("success"):
            print(f"\n✅ Found {result['total_size']} records")
            print(f"\nFormatted results:\n{result.get('formatted', 'N/A')}")
        else:
            print(f"\n❌ Error: {result.get('error')}")
        
        # Example 2: Create Record
        print("\n" + "=" * 70)
        print("Example 2: Create Salesforce Record")
        print("=" * 70)
        
        create_result = await app.create_record(
            object_type="Account",
            description="Create Account: Acme Corp, Industry Technology, Phone 555-1234"
        )
        
        if create_result.get("success"):
            print(f"\n✅ Record created: {create_result.get('id')}")
        else:
            print(f"\n❌ Error: {create_result.get('error')}")
        
        # Example 3: Execute Agentforce Action
        print("\n" + "=" * 70)
        print("Example 3: Execute Agentforce Action")
        print("=" * 70)
        
        action_result = await app.execute_agentforce_action(
            action_name="CreateAccount",
            action_description="Create account with name 'New Corp' and industry 'Finance'",
            record_id=None
        )
        
        print(f"\nAction result:\n{json.dumps(action_result, indent=2)}")
        
        # Example 4: Using OAuth token (commented out)
        print("\n" + "=" * 70)
        print("Example 4: OAuth Token-Based Connection")
        print("=" * 70)
        print("\n# Alternative: Connect with existing OAuth token")
        print("# sf_client = SalesforceClient.from_token(")
        print("#     access_token='your_access_token',")
        print("#     instance_url='https://yourorg.my.salesforce.com'")
        print("# )")
        
    finally:
        await app.shutdown()


if __name__ == "__main__":
    import sys
    from typing import Optional
    asyncio.run(main())
