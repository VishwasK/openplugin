# Salesforce Plugin with Agentforce Actions

## Overview

The Salesforce Plugin enables AI agents to interact with Salesforce data and execute Agentforce actions. This allows you to build AI-powered applications that can query, create, update, and perform actions in Salesforce.

## Features

- ✅ **Query Salesforce Data**: Execute SOQL queries
- ✅ **Create Records**: Create new Salesforce records
- ✅ **Update Records**: Update existing records
- ✅ **Agentforce Actions**: Execute Salesforce Agentforce actions
- ✅ **Natural Language**: Use natural language to describe operations

## What are Agentforce Actions?

Salesforce Agentforce allows you to create AI agents that can perform actions in Salesforce. Agentforce actions are predefined operations that can:

- Create/Update/Delete records
- Execute Salesforce Flows
- Call Apex methods
- Send emails
- Create tasks
- Perform complex business logic

## Setup

### 1. Install Dependencies

```bash
pip install simple-salesforce
```

### 2. Configure Salesforce Authentication

Set environment variables:

```bash
export SALESFORCE_USERNAME="your-username"
export SALESFORCE_PASSWORD="your-password"
export SALESFORCE_SECURITY_TOKEN="your-security-token"
export SALESFORCE_INSTANCE_URL="https://yourinstance.salesforce.com"
```

**For OAuth (Connected App):**
```bash
export SALESFORCE_CLIENT_ID="your-client-id"
export SALESFORCE_CLIENT_SECRET="your-client-secret"
```

### 3. Get Security Token

1. Log into Salesforce
2. Go to Setup → My Personal Information → Reset My Security Token
3. Check your email for the security token

## Commands

### `/query`
Query Salesforce data using SOQL.

```python
result = await manager.execute_command(
    "salesforce-plugin",
    "query",
    provider=provider,
    user_input="Query all Accounts: SELECT Id, Name FROM Account LIMIT 10"
)
```

### `/execute-action`
Execute Salesforce Agentforce actions.

```python
result = await manager.execute_command(
    "salesforce-plugin",
    "execute-action",
    provider=provider,
    user_input="Execute action 'CreateAccount' with name 'Acme Corp'"
)
```

### `/create-record`
Create a new Salesforce record.

```python
result = await manager.execute_command(
    "salesforce-plugin",
    "create-record",
    provider=provider,
    user_input="Create Account: name 'Acme Corp', industry 'Technology'"
)
```

### `/update-record`
Update an existing Salesforce record.

```python
result = await manager.execute_command(
    "salesforce-plugin",
    "update-record",
    provider=provider,
    user_input="Update Account 001xx000003DGbQ: set Industry to 'Technology'"
)
```

## Agentforce Actions Integration

### How Agentforce Actions Work

Agentforce actions are typically exposed via:

1. **REST API Endpoints**: Custom REST endpoints
2. **Tooling API**: Salesforce Tooling API
3. **Flow API**: Invocable flows
4. **Apex Methods**: @InvocableMethod annotations

### Implementing Agentforce Action Execution

The `SalesforceClient.execute_agentforce_action()` method is a placeholder. You need to implement it based on how your Agentforce actions are configured:

#### Option 1: REST API Endpoint

```python
def execute_agentforce_action(self, action_name, action_params, record_id=None):
    endpoint = f"{self.sf.base_url}/services/data/v58.0/actions/custom/{action_name}"
    response = self.sf.restful(endpoint, method='POST', data={
        "inputs": [{
            **action_params,
            "recordId": record_id
        }]
    })
    return response
```

#### Option 2: Invocable Flow

```python
def execute_agentforce_action(self, action_name, action_params, record_id=None):
    # Invoke a Flow
    endpoint = f"{self.sf.base_url}/services/data/v58.0/actions/custom/flow/{action_name}"
    response = self.sf.restful(endpoint, method='POST', data={
        "inputs": [action_params]
    })
    return response
```

#### Option 3: Apex Method

```python
def execute_agentforce_action(self, action_name, action_params, record_id=None):
    # Call Apex method via Tooling API
    endpoint = f"{self.sf.base_url}/services/data/v58.0/tooling/executeAnonymous/"
    apex_code = f"""
        MyAgentforceActions.{action_name}({json.dumps(action_params)});
    """
    response = self.sf.restful(endpoint, method='POST', data={
        "anonymousBody": apex_code
    })
    return response
```

## Example: Building an AI Agent for Salesforce

```python
from openplugin import PluginManager, OpenAIProvider, SmartAgent
from openplugin.utils import SalesforceClient

# Setup
manager = PluginManager()
manager.load_plugins()
provider = OpenAIProvider(api_key="your-key")
sf_client = SalesforceClient()

# Create smart agent that can use Salesforce
agent = SmartAgent(
    plugin_manager=manager,
    provider=provider,
    enable_web_search=True
)

# Ask questions that require Salesforce data
result = await agent.answer(
    "What are the top 5 Accounts by revenue this quarter?"
)
# Agent can:
# 1. Decide to query Salesforce
# 2. Execute SOQL query
# 3. Format and present results
```

## Use Cases

### 1. AI-Powered CRM Assistant

```python
# Natural language queries
"Show me all Opportunities closing this month"
"Create a Contact for John Doe at Acme Corp"
"Update Account 001xx000003DGbQ: change industry to Technology"
```

### 2. Automated Record Management

```python
# Bulk operations via AI
"Create 10 test Accounts in the Technology industry"
"Update all Contacts in Account 001xx000003DGbQ"
```

### 3. Agentforce Action Execution

```python
# Execute complex business logic
"Run the 'SendWelcomeEmail' action for new Contact 003xx000004TmiQ"
"Execute 'CalculateCommission' action for Opportunity 006xx000004TmiQ"
```

### 4. Data Analysis

```python
# Query and analyze Salesforce data
"What's the average deal size this quarter?"
"Which Accounts haven't been contacted in 30 days?"
```

## Security Considerations

1. **Authentication**: Always use secure authentication (OAuth preferred)
2. **Permissions**: Respect Salesforce field-level security
3. **Validation**: Validate all inputs before creating/updating
4. **Error Handling**: Handle Salesforce errors gracefully
5. **Logging**: Log all Salesforce operations for audit

## Best Practices

1. **Use SOQL Safely**: Always validate SOQL queries
2. **Handle Errors**: Salesforce can return various errors
3. **Respect Limits**: Be aware of Salesforce API limits
4. **Cache Results**: Cache frequently accessed data
5. **Batch Operations**: Use bulk API for large operations

## Troubleshooting

### "Authentication failed"
- Check username/password
- Verify security token
- Ensure IP is whitelisted (if required)

### "Insufficient access"
- Check object permissions
- Verify field-level security
- Ensure user has required access

### "Agentforce action not found"
- Verify action name is correct
- Check action is enabled
- Ensure action is accessible via API

## Next Steps

1. Configure your Salesforce org
2. Set up Agentforce actions
3. Implement action execution based on your setup
4. Test with the example app
5. Build your AI-powered Salesforce application!

See `examples/salesforce_app.py` for a complete working example.
