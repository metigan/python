"""Audiences service for managing audiences"""

from typing import Optional, Dict, Any
from urllib.parse import urlencode
from ..errors import ValidationError
from ..http_client import HttpClient


class AudiencesService:
    """Service for managing audiences"""

    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    def create(
        self, name: str, description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new audience"""
        if not name:
            raise ValidationError("name is required", "name")

        body = {"name": name}
        if description:
            body["description"] = description

        return self.http_client.post("/api/audiences", body)

    def get(self, audience_id: str) -> Dict[str, Any]:
        """Get audience by ID"""
        if not audience_id:
            raise ValidationError("audience_id is required", "audience_id")
        return self.http_client.get(f"/api/audiences/{audience_id}")

    def list(self, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """List audiences with optional pagination"""
        params = {}
        if page:
            params["page"] = page
        if limit:
            params["limit"] = limit

        if params:
            query_string = urlencode(params)
            endpoint = f"/api/audiences?{query_string}"
            return self.http_client.get(endpoint, None)
        return self.http_client.get("/api/audiences", None)

    def get_stats(self, audience_id: str) -> Dict[str, Any]:
        """Get statistics for an audience"""
        if not audience_id:
            raise ValidationError("audience_id is required", "audience_id")
        return self.http_client.get(f"/api/audiences/{audience_id}/stats")

    def delete(self, audience_id: str) -> None:
        """Delete an audience"""
        if not audience_id:
            raise ValidationError("audience_id is required", "audience_id")
        self.http_client.delete(f"/api/audiences/{audience_id}")

