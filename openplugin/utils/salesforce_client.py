"""Salesforce client for Salesforce plugin."""

import os
import json
from typing import Dict, List, Optional, Any
try:
    from simple_salesforce import Salesforce
except ImportError:
    Salesforce = None


class SalesforceClient:
    """Client for interacting with Salesforce API."""

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        security_token: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        instance_url: Optional[str] = None,
        domain: Optional[str] = None,
        access_token: Optional[str] = None
    ):
        """Initialize Salesforce client.
        
        Args:
            username: Salesforce username
            password: Salesforce password
            security_token: Security token (for username-password auth)
            client_id: Connected App Client ID (for OAuth)
            client_secret: Connected App Client Secret (for OAuth)
            instance_url: Salesforce instance URL
            domain: Salesforce domain (login, test, custom)
            access_token: OAuth access token (if using token-based auth)
        """
        if Salesforce is None:
            raise ImportError(
                "simple-salesforce is not installed. "
                "Install it with: pip install simple-salesforce"
            )
        
        # Get credentials from environment if not provided
        self.username = username or os.getenv("SALESFORCE_USERNAME")
        self.password = password or os.getenv("SALESFORCE_PASSWORD")
        self.security_token = security_token or os.getenv("SALESFORCE_SECURITY_TOKEN")
        self.client_id = client_id or os.getenv("SALESFORCE_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("SALESFORCE_CLIENT_SECRET")
        self.instance_url = instance_url or os.getenv("SALESFORCE_INSTANCE_URL")
        self.domain = domain or os.getenv("SALESFORCE_DOMAIN", "login")
        self.access_token = access_token or os.getenv("SALESFORCE_ACCESS_TOKEN")
        
        self.sf = None
        self._connect()

    def _connect(self) -> None:
        """Connect to Salesforce."""
        # Check if using OAuth access token first
        if self.access_token and self.instance_url:
            try:
                self.sf = Salesforce(instance_url=self.instance_url, session_id=self.access_token)
                return
            except Exception as e:
                raise ConnectionError(f"Failed to connect to Salesforce with access token: {str(e)}")
        
        # Fall back to username/password authentication
        if not self.username or not self.password:
            raise ValueError(
                "Salesforce credentials not configured. "
                "Set SALESFORCE_USERNAME and SALESFORCE_PASSWORD environment variables, "
                "or provide access_token and instance_url for OAuth token-based authentication."
            )
        
        try:
            if self.client_id and self.client_secret:
                # OAuth authentication
                self.sf = Salesforce(
                    username=self.username,
                    password=self.password,
                    security_token=self.security_token,
                    consumer_key=self.client_id,
                    consumer_secret=self.client_secret,
                    domain=self.domain
                )
            else:
                # Username-password authentication
                self.sf = Salesforce(
                    username=self.username,
                    password=self.password,
                    security_token=self.security_token,
                    domain=self.domain
                )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Salesforce: {str(e)}")
    
    @classmethod
    def from_token(cls, access_token: str, instance_url: str) -> "SalesforceClient":
        """Create client from existing OAuth access token.
        
        Args:
            access_token: OAuth access token
            instance_url: Salesforce instance URL
            
        Returns:
            SalesforceClient instance
        """
        if Salesforce is None:
            raise ImportError(
                "simple-salesforce is not installed. "
                "Install it with: pip install simple-salesforce"
            )
        
        client = cls.__new__(cls)
        client.access_token = access_token
        client.instance_url = instance_url
        client.username = None
        client.password = None
        client.security_token = None
        client.client_id = None
        client.client_secret = None
        client.domain = None
        
        try:
            client.sf = Salesforce(instance_url=instance_url, session_id=access_token)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Salesforce with access token: {str(e)}")
        
        return client

    def query(self, soql: str) -> Dict[str, Any]:
        """Execute SOQL query.
        
        Args:
            soql: SOQL query string
            
        Returns:
            Query results dictionary
        """
        try:
            results = self.sf.query(soql)
            return {
                "success": True,
                "records": results.get("records", []),
                "total_size": results.get("totalSize", 0),
                "done": results.get("done", True)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "records": []
            }

    def create_record(self, object_type: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Create a Salesforce record.
        
        Args:
            object_type: Salesforce object type (Account, Contact, etc.)
            fields: Field values dictionary
            
        Returns:
            Creation result dictionary
        """
        try:
            obj = getattr(self.sf, object_type)
            result = obj.create(fields)
            return {
                "success": True,
                "id": result.get("id"),
                "message": f"Record created successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def update_record(self, object_type: str, record_id: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Update a Salesforce record.
        
        Args:
            object_type: Salesforce object type
            record_id: Record ID to update
            fields: Field values to update
            
        Returns:
            Update result dictionary
        """
        try:
            obj = getattr(self.sf, object_type)
            result = obj.update(record_id, fields)
            return {
                "success": True,
                "id": record_id,
                "message": f"Record updated successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def execute_agentforce_action(
        self,
        action_name: str,
        action_params: Dict[str, Any],
        record_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute a Salesforce Agentforce action.
        
        Args:
            action_name: Name of the Agentforce action
            action_params: Parameters for the action
            record_id: Optional record ID if action is record-specific
            
        Returns:
            Action execution result
        
        Note: This is a placeholder implementation. Actual Agentforce action
        execution depends on Salesforce's Agentforce API which may use:
        - REST API endpoints
        - Tooling API
        - Custom Apex endpoints
        - Flow API
        
        You'll need to implement based on your Agentforce configuration.
        """
        try:
            # Placeholder: Actual implementation depends on Agentforce API
            # This might use REST API, Tooling API, or custom endpoints
            
            # Example: If Agentforce actions are exposed via REST API
            # endpoint = f"{self.sf.base_url}/services/data/v58.0/actions/custom/{action_name}"
            # response = self.sf.restful(endpoint, method='POST', data=action_params)
            
            # For now, return a structured response
            return {
                "success": True,
                "action_name": action_name,
                "message": f"Action '{action_name}' executed successfully",
                "params": action_params,
                "note": "Implement actual Agentforce API call based on your configuration"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "action_name": action_name
            }

    def get_record(self, object_type: str, record_id: str, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get a single record by ID.
        
        Args:
            object_type: Salesforce object type
            record_id: Record ID
            fields: Optional list of fields to retrieve
            
        Returns:
            Record data dictionary
        """
        try:
            obj = getattr(self.sf, object_type)
            if fields:
                soql = f"SELECT {', '.join(fields)} FROM {object_type} WHERE Id = '{record_id}'"
                result = self.query(soql)
                if result["success"] and result["records"]:
                    return {
                        "success": True,
                        "record": result["records"][0]
                    }
            else:
                record = obj.get(record_id)
                return {
                    "success": True,
                    "record": record
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
