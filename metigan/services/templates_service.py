"""Templates service for managing email templates"""

from typing import Dict, Any, List
from urllib.parse import urlencode
from ..errors import ValidationError
from ..http_client import HttpClient


class TemplatesService:
    """Service for managing email templates"""

    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    def get(self, template_id: str) -> Dict[str, Any]:
        """Get template by ID"""
        if not template_id:
            raise ValidationError("template_id is required", "template_id")
        return self.http_client.get(f"/templates/{template_id}")

    def list(self, page: int = 1, limit: int = 10) -> List[Dict[str, Any]]:
        """List all templates"""
        params = {}
        if page:
            params["page"] = page
        if limit:
            params["limit"] = limit

        if params:
            query_string = urlencode(params)
            endpoint = f"/templates?{query_string}"
            result = self.http_client.get(endpoint, None)
        else:
            result = self.http_client.get("/templates", None)
        return result.get("templates", [])

