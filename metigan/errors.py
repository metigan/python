"""Error classes for Metigan SDK"""


class MetiganError(Exception):
    """Base exception for Metigan SDK"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ApiError(MetiganError):
    """Exception raised for API errors"""

    def __init__(self, status_code: int, message: str, error: str = None):
        self.status_code = status_code
        self.error = error
        super().__init__(message)

    def __str__(self):
        if self.error:
            return f"API error {self.status_code}: {self.error} - {self.message}"
        return f"API error {self.status_code}: {self.message}"


class ValidationError(MetiganError):
    """Exception raised for validation errors"""

    def __init__(self, message: str, field: str = None):
        self.field = field
        super().__init__(message)

    def __str__(self):
        if self.field:
            return f"Validation error in field '{self.field}': {self.message}"
        return f"Validation error: {self.message}"

