# Create Record Command

Creates a new record in Salesforce.

## Usage

This command creates a new record in any Salesforce object.

## Input Parameters

- **object_type**: Salesforce object type (Account, Contact, Opportunity, etc.)
- **fields**: Field values as key-value pairs or JSON
- **required_fields**: List of required fields

## Output

Returns creation result including:
- Created record ID
- Success status
- Any validation errors
- Created record details

## Behavior

- Creates records in Salesforce
- Validates required fields
- Handles validation errors
- Returns record ID on success
- Supports all standard and custom objects

## Examples

- "Create Account with name 'Acme Corp' and industry 'Technology'"
- "Create Contact: John Doe, email john@example.com, Account 001xx000003DGbQ"
- "Create Opportunity: 'New Deal', Amount 50000, Close Date 2024-12-31"
