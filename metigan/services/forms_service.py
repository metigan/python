"""Forms service for managing forms"""

from typing import Dict, Any, Optional
from urllib.parse import urlencode
from ..errors import ValidationError
from ..http_client import HttpClient


class FormsService:
    """Service for managing forms"""

    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    def submit(self, form_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a form"""
        if not form_id:
            raise ValidationError("form_id is required", "form_id")
        if not data:
            raise ValidationError("form data is required", "data")

        return self.http_client.post(
            "/api/submissions", {"formId": form_id, "data": data}
        )

    def get(self, form_id_or_slug: str) -> Dict[str, Any]:
        """Get form by ID or slug"""
        if not form_id_or_slug:
            raise ValidationError("form_id_or_slug is required", "form_id_or_slug")
        return self.http_client.get(f"/api/forms/{form_id_or_slug}")

    def list(self, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """List all forms"""
        params = {}
        if page:
            params["page"] = page
        if limit:
            params["limit"] = limit

        if params:
            query_string = urlencode(params)
            endpoint = f"/api/forms?{query_string}"
            return self.http_client.get(endpoint, None)
        return self.http_client.get("/api/forms", None)

