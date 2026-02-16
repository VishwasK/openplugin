# Salesforce Plugin

A plugin for interacting with Salesforce data and executing Agentforce actions.

## Features

- **Query Data**: Execute SOQL queries to retrieve Salesforce records
- **Agentforce Actions**: Execute Salesforce Agentforce actions
- **Create Records**: Create new records in Salesforce
- **Update Records**: Update existing Salesforce records

## Commands

### `/query`
Query Salesforce data using SOQL.

Example:
```
Query all Accounts: SELECT Id, Name, Industry FROM Account LIMIT 10
```

### `/execute-action`
Execute Salesforce Agentforce actions.

Example:
```
Execute action 'CreateAccount' with name 'Acme Corp' and industry 'Technology'
```

### `/create-record`
Create a new Salesforce record.

Example:
```
Create Account with name 'Acme Corp' and industry 'Technology'
```

### `/update-record`
Update an existing Salesforce record.

Example:
```
Update Account 001xx000003DGbQ: set Industry to 'Technology'
```

## Setup

### Authentication

The plugin uses Salesforce authentication. You need:

1. **OAuth 2.0** (Username-Password or JWT Bearer flow)
2. **Connected App** credentials
3. **Security Token** (for username-password)

Set environment variables:
```bash
export SALESFORCE_USERNAME="your-username"
export SALESFORCE_PASSWORD="your-password"
export SALESFORCE_SECURITY_TOKEN="your-token"
export SALESFORCE_CLIENT_ID="your-client-id"
export SALESFORCE_CLIENT_SECRET="your-client-secret"
export SALESFORCE_INSTANCE_URL="https://yourinstance.salesforce.com"
```

### Agentforce Actions

To use Agentforce actions, you need:
- Agentforce enabled in your org
- Actions configured in Agentforce
- Appropriate permissions

## Usage

See `examples/salesforce_app.py` for a complete example.

## Use Cases

- AI agents that interact with Salesforce data
- Automated Salesforce operations
- Data analysis and reporting
- Record management via AI
- Integration with AI workflows

## Security

- Respects Salesforce security model
- Uses OAuth 2.0 authentication
- Validates permissions
- Only accesses authorized data
