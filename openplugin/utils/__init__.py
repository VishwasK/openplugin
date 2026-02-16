"""Utility modules for OpenPlugin."""

from .email_sender import EmailSender
from .web_search import WebSearcher

try:
    from .salesforce_client import SalesforceClient
    __all__ = ["EmailSender", "WebSearcher", "SalesforceClient"]
except ImportError:
    __all__ = ["EmailSender", "WebSearcher"]
