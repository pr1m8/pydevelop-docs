"""Exception classes for the Haive ecosystem."""

class HaiveError(Exception):
    """Base exception for all Haive-related errors.
    
    This is the root exception class for the Haive ecosystem.
    All other Haive exceptions should inherit from this class.
    
    Attributes:
        message: Error message
        error_code: Optional error code for categorization
        context: Optional context dictionary with additional error details
        
    Examples:
        Basic usage:
        
        >>> raise HaiveError("Something went wrong")
        
        With error code and context:
        
        >>> raise HaiveError(
        ...     "Validation failed",
        ...     error_code="VALIDATION_ERROR",
        ...     context={"field": "email", "value": "invalid"}
        ... )
    """
    
    def __init__(self, message: str, error_code: str = None, context: dict = None):
        self.message = message
        self.error_code = error_code
        self.context = context or {}
        super().__init__(self.message)
    
    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class ProcessingError(HaiveError):
    """Exception raised during data processing operations.
    
    This exception is raised when data processing fails in the
    DataProcessor or related components.
    
    Examples:
        >>> raise ProcessingError("Failed to process data")
        >>> raise ProcessingError(
        ...     "Invalid data format", 
        ...     error_code="INVALID_FORMAT"
        ... )
    """
    pass


class ValidationError(HaiveError):
    """Exception raised when data validation fails.
    
    This exception is raised when input validation fails,
    typically in model validation or API request validation.
    
    Examples:
        >>> raise ValidationError("Email format is invalid")
        >>> raise ValidationError(
        ...     "Required field missing",
        ...     context={"field": "name"}
        ... )
    """
    pass


class ConfigurationError(HaiveError):
    """Exception raised when configuration is invalid or missing.
    
    This exception is raised when there are issues with
    system configuration, environment variables, or settings.
    
    Examples:
        >>> raise ConfigurationError("Database URL not configured")
        >>> raise ConfigurationError(
        ...     "Invalid timeout value",
        ...     context={"timeout": -1, "expected": "> 0"}
        ... )
    """
    pass