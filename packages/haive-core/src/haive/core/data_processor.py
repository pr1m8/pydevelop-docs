"""Core data processing functionality."""

from typing import Dict, Any, Optional
from dataclasses import dataclass
import datetime
import logging
from threading import Lock
from .exceptions import ProcessingError

logger = logging.getLogger(__name__)

@dataclass
class ProcessingResult:
    """Result of a data processing operation.
    
    Attributes:
        status: Processing status ('success', 'failed', 'partial')
        data: Processed data
        metadata: Additional processing metadata
        error: Error message if processing failed
    """
    status: str
    data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class DataProcessor:
    """Core data processor for the Haive ecosystem.
    
    This class provides the fundamental data processing capabilities
    that are used throughout the Haive ecosystem. It handles data
    validation, transformation, and error management.
    
    Args:
        config: Configuration dictionary for the processor
        validate: Whether to validate input data (default: True)
        
    Examples:
        Basic usage:
        
        >>> processor = DataProcessor()
        >>> data = {"name": "test", "value": 42}
        >>> result = processor.process(data)
        >>> print(result.status)
        'success'
        
        With custom configuration:
        
        >>> config = {"strict_mode": True, "timeout": 30}
        >>> processor = DataProcessor(config=config)
        >>> result = processor.process(data)
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None, validate: bool = True):
        self.config = config or {}
        self.validate = validate
        self._processing_stats = {"total_processed": 0, "errors": 0}
        self._stats_lock = Lock()  # Thread-safe statistics
    
    def process(self, data: Dict[str, Any]) -> ProcessingResult:
        """Process input data and return results.
        
        Args:
            data: Input data dictionary to process
            
        Returns:
            ProcessingResult: Contains status, processed data, and metadata
            
        Raises:
            ProcessingError: If processing fails and strict_mode is enabled
        """
        try:
            if self.validate and not self._validate_input(data):
                raise ProcessingError("Invalid input data")
            
            # Simulate processing
            processed_data = self._transform_data(data)
            
            # Thread-safe statistics update
            with self._stats_lock:
                self._processing_stats["total_processed"] += 1
            
            return ProcessingResult(
                status="success",
                data=processed_data,
                metadata={"processor": "core", "version": "0.1.0"}
            )
            
        except ProcessingError:
            # Re-raise our own exceptions
            raise
        except ValueError as e:
            # Log and handle validation errors
            logger.error(f"Validation error: {e}")
            with self._stats_lock:
                self._processing_stats["errors"] += 1
            
            if self.config.get("strict_mode", False):
                raise ProcessingError(f"Validation failed: {e}")
            
            return ProcessingResult(
                status="failed",
                error=f"Validation error: {str(e)}"
            )
        except Exception as e:
            # Log unexpected errors
            logger.exception("Unexpected error during processing")
            with self._stats_lock:
                self._processing_stats["errors"] += 1
            
            if self.config.get("strict_mode", False):
                raise ProcessingError(f"Processing failed: {e}")
            
            return ProcessingResult(
                status="failed",
                error="Internal processing error"  # Don't expose internal details
            )
    
    def _validate_input(self, data: Dict[str, Any]) -> bool:
        """Validate input data structure with security checks.
        
        Args:
            data: Input data to validate
            
        Returns:
            bool: True if data is valid
            
        Raises:
            ValueError: If data contains invalid keys or is too large
        """
        if not isinstance(data, dict) or not data:
            return False
        
        # Size limit check
        max_size = self.config.get('max_input_size', 10_000)  # 10KB default
        data_str = str(data)
        if len(data_str) > max_size:
            raise ValueError(f"Input data too large: {len(data_str)} > {max_size}")
        
        # Key validation
        for key in data:
            if not isinstance(key, str):
                raise ValueError(f"Invalid key type: {type(key)}")
            # Simple check for potentially dangerous keys
            if key.startswith('_') or key.startswith('__'):
                logger.warning(f"Potentially dangerous key detected: {key}")
        
        return True
    
    def _transform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform input data."""
        return {
            **data,
            "_processed": True,
            "_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
    
    @property
    def stats(self) -> Dict[str, int]:
        """Get processing statistics (thread-safe)."""
        with self._stats_lock:
            return self._processing_stats.copy()
    
    def reset_stats(self) -> None:
        """Reset processing statistics (thread-safe)."""
        with self._stats_lock:
            self._processing_stats = {"total_processed": 0, "errors": 0}