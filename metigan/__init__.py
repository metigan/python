"""
Metigan Python SDK
Official Metigan SDK for Python - Email, Forms, Contacts, and Audiences management
"""

from .client import MetiganClient
from .errors import MetiganError, ApiError, ValidationError

__version__ = "1.0.0"
__all__ = ["MetiganClient", "MetiganError", "ApiError", "ValidationError"]

