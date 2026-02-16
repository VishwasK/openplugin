# Query Salesforce Command

Queries Salesforce data using SOQL (Salesforce Object Query Language).

## Usage

This command executes SOQL queries against Salesforce to retrieve records.

## Input Parameters

- **soql**: SOQL query string (e.g., "SELECT Id, Name FROM Account LIMIT 10")
- **object_type**: Salesforce object type (Account, Contact, Opportunity, etc.)
- **fields**: Fields to retrieve (optional, can be inferred from SOQL)
- **filters**: Additional filters (optional)

## Output

Returns query results including:
- Retrieved records with all requested fields
- Record count
- Formatted data for easy reading

## Behavior

- Executes SOQL queries safely
- Validates query syntax
- Returns formatted results
- Handles errors gracefully
- Can query any Salesforce object

## Examples

- "Query all Accounts: SELECT Id, Name FROM Account LIMIT 10"
- "Get Contacts for Account 001xx000003DGbQ"
- "Find Opportunities with Amount > 10000"

## Security

- Respects Salesforce security model
- Only returns data user has access to
- Validates permissions before querying
