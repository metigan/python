"""Main Metigan client"""

from .http_client import HttpClient
from .errors import ValidationError
from .services.email_service import EmailService
from .services.contacts_service import ContactsService
from .services.audiences_service import AudiencesService
from .services.templates_service import TemplatesService
from .services.forms_service import FormsService


class MetiganClient:
    """Main Metigan client that provides access to all services"""

    def __init__(
        self,
        api_key: str,
        timeout: int = 30,
        retry_count: int = 3,
        retry_delay: int = 2,
        debug: bool = False,
    ):
        """
        Initialize the Metigan client

        Args:
            api_key: Your Metigan API key
            timeout: Request timeout in seconds (default: 30)
            retry_count: Number of retries on failure (default: 3)
            retry_delay: Delay between retries in seconds (default: 2)
            debug: Enable debug mode (default: False)
        """
        if not api_key:
            raise ValidationError("API key is required", "api_key")

        self.http_client = HttpClient(
            api_key=api_key,
            timeout=timeout,
            retry_count=retry_count,
            retry_delay=retry_delay,
            debug=debug,
        )

        # Initialize services
        self.email = EmailService(self.http_client)
        self.contacts = ContactsService(self.http_client)
        self.audiences = AudiencesService(self.http_client)
        self.templates = TemplatesService(self.http_client)
        self.forms = FormsService(self.http_client)

