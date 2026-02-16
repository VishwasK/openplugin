# Execute Agentforce Action Command

Executes Salesforce Agentforce actions to perform operations in Salesforce.

## Usage

This command invokes Agentforce actions that can perform various Salesforce operations like creating records, updating data, executing flows, or calling Apex methods.

## Input Parameters

- **action_name**: Name of the Agentforce action to execute
- **action_params**: Parameters for the action (JSON or key-value pairs)
- **object_type**: Salesforce object type if applicable
- **record_id**: Record ID if updating/deleting

## Output

Returns action execution result including:
- Success/failure status
- Result data
- Any errors or warnings
- Affected record IDs

## Behavior

- Executes Agentforce actions via API
- Validates action parameters
- Handles errors appropriately
- Returns detailed results
- Supports all Agentforce action types

## Examples

- "Execute action 'CreateAccount' with name 'Acme Corp'"
- "Run action 'UpdateOpportunity' for record 006xx000004TmiQ"
- "Call action 'SendEmail' to contact 003xx000004TmiQ"

## Agentforce Actions

Common action types:
- Create/Update/Delete records
- Execute Flows
- Call Apex methods
- Send emails
- Create tasks
- Update related records
