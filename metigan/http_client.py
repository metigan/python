"""HTTP client for Metigan API"""

import time
from typing import Optional, Dict, Any
import requests
from .errors import ApiError


BASE_URL = "https://api.metigan.com"


class HttpClient:
    """HTTP client with retry logic and error handling"""

    def __init__(
        self,
        api_key: str,
        timeout: int = 30,
        retry_count: int = 3,
        retry_delay: int = 2,
        debug: bool = False,
        base_url: Optional[str] = None,
    ):
        self.api_key = api_key
        self.timeout = timeout
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.debug = debug
        self.base_url = base_url or BASE_URL

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "User-Agent": "Metigan-Python-SDK/1.0",
            }
        )

    def _request(
        self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request with retry logic"""
        url = f"{self.base_url}{endpoint}"

        for attempt in range(self.retry_count + 1):
            try:
                if method == "GET":
                    response = self.session.get(url, params=data, timeout=self.timeout)
                elif method == "POST":
                    response = self.session.post(url, json=data, timeout=self.timeout)
                elif method == "PATCH":
                    response = self.session.patch(url, json=data, timeout=self.timeout)
                elif method == "DELETE":
                    response = self.session.delete(url, json=data, timeout=self.timeout)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                # Success or client error - don't retry
                if response.status_code < 500:
                    if response.status_code >= 400:
                        self._handle_error(response)
                    return response.json() if response.content else {}

                # Server error - retry if attempts remaining
                if attempt < self.retry_count:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue

                # Last attempt failed
                self._handle_error(response)

            except requests.exceptions.RequestException as e:
                if attempt < self.retry_count:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise ApiError(0, str(e))

        # Should not reach here, but just in case
        raise ApiError(0, "Request failed after retries")

    def _handle_error(self, response: requests.Response):
        """Handle HTTP error responses"""
        try:
            error_data = response.json()
            message = error_data.get("message") or error_data.get("error", "")
            error = error_data.get("error")
        except Exception:
            message = f"HTTP {response.status_code}: {response.reason}"
            error = None

        raise ApiError(response.status_code, message, error)

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request"""
        return self._request("GET", endpoint, params)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make POST request"""
        return self._request("POST", endpoint, data)

    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make PATCH request"""
        return self._request("PATCH", endpoint, data)

    def delete(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make DELETE request"""
        return self._request("DELETE", endpoint, data)

