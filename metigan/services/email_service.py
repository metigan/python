"""Email service for sending emails"""

from typing import List, Optional, Dict, Any
import base64
from ..errors import ValidationError
from ..http_client import HttpClient


class EmailService:
    """Service for sending emails"""

    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    def send_email(
        self,
        from_address: str,
        recipients: List[str],
        subject: str,
        content: str,
        attachments: Optional[List[Dict[str, Any]]] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        reply_to: Optional[str] = None,
        tracking_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send an email

        Args:
            from_address: Sender email address (or "Name <email>")
            recipients: List of recipient email addresses
            subject: Email subject
            content: Email content (HTML supported)
            attachments: Optional list of attachments
            cc: Optional CC recipients
            bcc: Optional BCC recipients
            reply_to: Optional reply-to address
            tracking_id: Optional tracking ID

        Returns:
            Email response dictionary
        """
        # Validate required fields
        if not from_address:
            raise ValidationError("from_address is required", "from_address")
        if not recipients or len(recipients) == 0:
            raise ValidationError("at least one recipient is required", "recipients")
        if not subject:
            raise ValidationError("subject is required", "subject")
        if not content:
            raise ValidationError("content is required", "content")

        # Prepare request body
        body = {
            "from": from_address,
            "recipients": recipients,
            "subject": subject,
            "content": content,
        }

        # Process attachments - encode to base64
        if attachments:
            processed_attachments = []
            for att in attachments:
                if isinstance(att.get("content"), bytes):
                    content_b64 = base64.b64encode(att["content"]).decode("utf-8")
                else:
                    content_b64 = att["content"]
                
                processed_attachments.append({
                    "content": content_b64,
                    "filename": att.get("filename", "file"),
                    "contentType": att.get("content_type", "application/octet-stream"),
                })
            body["attachments"] = processed_attachments

        if cc:
            body["cc"] = cc
        if bcc:
            body["bcc"] = bcc
        if reply_to:
            body["replyTo"] = reply_to
        if tracking_id:
            body["trackingId"] = tracking_id

        return self.http_client.post("/api/email/send", body)

    def send_email_with_template(
        self,
        template_id: str,
        variables: Dict[str, Any],
        from_address: str,
        recipients: List[str],
        reply_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send an email using a template

        Args:
            template_id: Template ID
            variables: Template variables
            from_address: Sender email address
            recipients: List of recipient email addresses
            reply_to: Optional reply-to address

        Returns:
            Email response dictionary
        """
        if not template_id:
            raise ValidationError("template_id is required", "template_id")

        body = {
            "templateId": template_id,
            "variables": variables,
            "from": from_address,
            "recipients": recipients,
        }

        if reply_to:
            body["replyTo"] = reply_to

        return self.http_client.post("/api/email/send", body)

