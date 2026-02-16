# Update Record Command

Updates an existing Salesforce record.

## Usage

This command updates fields on an existing Salesforce record.

## Input Parameters

- **record_id**: Salesforce record ID to update
- **object_type**: Object type (optional, can be inferred from ID)
- **fields**: Field values to update (key-value pairs or JSON)

## Output

Returns update result including:
- Success status
- Updated record ID
- Any validation errors
- Updated field values

## Behavior

- Updates records in Salesforce
- Validates field values
- Handles validation errors
- Returns success confirmation
- Supports all standard and custom objects

## Examples

- "Update Account 001xx000003DGbQ: set Industry to 'Technology'"
- "Update Contact 003xx000004TmiQ: change email to newemail@example.com"
- "Update Opportunity 006xx000004TmiQ: set Stage to 'Closed Won', Amount to 75000"
