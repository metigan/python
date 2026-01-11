"""Contacts service for managing contacts"""

from typing import Optional, List, Dict, Any
from urllib.parse import urlencode
from ..errors import ValidationError
from ..http_client import HttpClient


class ContactsService:
    """Service for managing contacts"""

    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    def create(
        self,
        email: str,
        audience_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        tags: Optional[List[str]] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        status: str = "subscribed",
    ) -> Dict[str, Any]:
        """
        Create a new contact

        Args:
            email: Contact email address
            audience_id: Audience ID
            first_name: Optional first name
            last_name: Optional last name
            phone: Optional phone number
            tags: Optional list of tags
            custom_fields: Optional custom fields
            status: Contact status (default: "subscribed")

        Returns:
            Contact dictionary
        """
        if not email:
            raise ValidationError("email is required", "email")
        if not audience_id:
            raise ValidationError("audience_id is required", "audience_id")

        body = {
            "email": email,
            "audienceId": audience_id,
            "status": status,
        }

        if first_name:
            body["firstName"] = first_name
        if last_name:
            body["lastName"] = last_name
        if phone:
            body["phone"] = phone
        if tags:
            body["tags"] = tags
        if custom_fields:
            body["customFields"] = custom_fields

        return self.http_client.post("/api/contacts", body)

    def get(self, contact_id: str) -> Dict[str, Any]:
        """Get contact by ID"""
        if not contact_id:
            raise ValidationError("contact_id is required", "contact_id")
        return self.http_client.get(f"/api/contacts/{contact_id}")

    def get_by_email(self, email: str, audience_id: str) -> Dict[str, Any]:
        """Get contact by email address"""
        if not email:
            raise ValidationError("email is required", "email")
        if not audience_id:
            raise ValidationError("audience_id is required", "audience_id")
        # Query string already in URL, don't pass params
        return self.http_client.get(f"/api/contacts/email/{email}?audienceId={audience_id}", None)

    def update(
        self,
        contact_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        tags: Optional[List[str]] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update an existing contact"""
        if not contact_id:
            raise ValidationError("contact_id is required", "contact_id")

        body = {}
        if first_name is not None:
            body["firstName"] = first_name
        if last_name is not None:
            body["lastName"] = last_name
        if phone is not None:
            body["phone"] = phone
        if tags is not None:
            body["tags"] = tags
        if custom_fields is not None:
            body["customFields"] = custom_fields
        if status is not None:
            body["status"] = status

        return self.http_client.patch(f"/api/contacts/{contact_id}", body)

    def list(
        self,
        audience_id: Optional[str] = None,
        status: Optional[str] = None,
        tag: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """List contacts with optional filters"""
        params = {}
        if audience_id:
            params["audienceId"] = audience_id
        if status:
            params["status"] = status
        if tag:
            params["tag"] = tag
        if search:
            params["search"] = search
        if page:
            params["page"] = page
        if limit:
            params["limit"] = limit

        if params:
            query_string = urlencode(params)
            endpoint = f"/api/contacts?{query_string}"
            # Params already in URL, don't pass again
            return self.http_client.get(endpoint, None)
        return self.http_client.get("/api/contacts", None)

    def delete(self, contact_id: str) -> None:
        """Delete a contact"""
        if not contact_id:
            raise ValidationError("contact_id is required", "contact_id")
        self.http_client.delete(f"/api/contacts/{contact_id}")

    def subscribe(self, contact_id: str) -> None:
        """Subscribe a contact"""
        if not contact_id:
            raise ValidationError("contact_id is required", "contact_id")
        self.http_client.post(f"/api/contacts/{contact_id}/subscribe", {})

    def unsubscribe(self, contact_id: str) -> None:
        """Unsubscribe a contact"""
        if not contact_id:
            raise ValidationError("contact_id is required", "contact_id")
        self.http_client.post(f"/api/contacts/{contact_id}/unsubscribe", {})

    def add_tags(self, contact_id: str, tags: List[str]) -> None:
        """Add tags to a contact"""
        if not contact_id:
            raise ValidationError("contact_id is required", "contact_id")
        if not tags or len(tags) == 0:
            raise ValidationError("at least one tag is required", "tags")
        self.http_client.post(f"/api/contacts/{contact_id}/tags", {"tags": tags})

    def remove_tags(self, contact_id: str, tags: List[str]) -> None:
        """Remove tags from a contact"""
        if not contact_id:
            raise ValidationError("contact_id is required", "contact_id")
        if not tags or len(tags) == 0:
            raise ValidationError("at least one tag is required", "tags")
        self.http_client.delete(f"/api/contacts/{contact_id}/tags", {"tags": tags})

