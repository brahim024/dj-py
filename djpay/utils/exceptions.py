class CustomError(Exception):
    """Base class for custom exceptions."""
    pass

class TokenAppNotFound(CustomError):
    """Exception raised for validation errors."""
    def __init__(self, message=None):
        self.message = "Invalid App token info or not exist"
        super().__init__(self.message)