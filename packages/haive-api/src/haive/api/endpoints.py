"""Endpoint implementations for Haive API."""

from typing import Dict, Any, List
from abc import ABC, abstractmethod
import logging
from threading import Lock
from collections import defaultdict
import time
from haive.core import DataProcessor, ProcessingError
from haive.ml import MLPipeline

logger = logging.getLogger(__name__)

# Rate limiting configuration
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX_REQUESTS = 100  # max requests per window

class RateLimiter:
    """Simple rate limiter for API endpoints."""
    
    def __init__(self, window: int = RATE_LIMIT_WINDOW, max_requests: int = RATE_LIMIT_MAX_REQUESTS):
        self.window = window
        self.max_requests = max_requests
        self.requests = defaultdict(list)
        self.lock = Lock()
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed for given identifier."""
        with self.lock:
            now = time.time()
            # Clean old entries
            self.requests[identifier] = [
                timestamp for timestamp in self.requests[identifier]
                if now - timestamp < self.window
            ]
            
            # Check rate limit
            if len(self.requests[identifier]) >= self.max_requests:
                return False
            
            # Record new request
            self.requests[identifier].append(now)
            return True
    
    def cleanup(self):
        """Clean up old request records."""
        with self.lock:
            now = time.time()
            for identifier in list(self.requests.keys()):
                self.requests[identifier] = [
                    timestamp for timestamp in self.requests[identifier]
                    if now - timestamp < self.window
                ]
                if not self.requests[identifier]:
                    del self.requests[identifier]

# Global rate limiter instance
rate_limiter = RateLimiter()

class BaseEndpoint(ABC):
    """Base class for API endpoints.
    
    This abstract class defines the interface that all
    Haive API endpoints must implement.
    """
    
    @abstractmethod
    def handle_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle an incoming API request.
        
        Args:
            data: Request data dictionary
            
        Returns:
            Response data dictionary
        """
        pass

class MLEndpoint(BaseEndpoint):
    """Endpoint for ML model predictions.
    
    This endpoint integrates with ML pipelines to provide
    prediction capabilities via REST API.
    
    Args:
        pipeline: ML pipeline for making predictions
        
    Examples:
        >>> from haive.ml import MLPipeline
        >>> from haive.core import DataProcessor
        >>> 
        >>> processor = DataProcessor()
        >>> pipeline = MLPipeline(processor)
        >>> endpoint = MLEndpoint(pipeline)
        >>> 
        >>> request_data = {
        ...     "samples": [{"feature1": 1.0, "feature2": 2.0}]
        ... }
        >>> response = endpoint.handle_request(request_data)
        >>> print(response["predictions"])
    """
    
    def __init__(self, pipeline: MLPipeline):
        self.pipeline = pipeline
        self._request_count = 0
        self._request_lock = Lock()
    
    def handle_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle ML prediction request.
        
        Args:
            data: Request data containing 'samples' field
            
        Returns:
            Response with predictions and metadata
            
        Raises:
            ValueError: If request data is invalid
        """
        # Thread-safe request counting
        with self._request_lock:
            # Thread-safe request counting
        with self._request_lock:
            self._request_count += 1
            request_id = self._request_count
            request_id = self._request_count
        
        try:
            # Validate request format
            if "samples" not in data:
                raise ValueError("Request must contain 'samples' field")
            
            samples = data["samples"]
            if not isinstance(samples, list):
                raise ValueError("'samples' must be a list")
            
            # Size validation
            if len(samples) > 100:
                raise ValueError("Too many samples (max 100)")
            
            # Deep validation of sample structure
            for i, sample in enumerate(samples):
                if not isinstance(sample, dict):
                    raise ValueError(f"Sample {i} must be a dictionary")
                if len(str(sample)) > 10000:
                    raise ValueError(f"Sample {i} is too large")
            
            # Make predictions
            result = self.pipeline.predict(samples)
            
            return {
                "success": True,
                "predictions": result.predictions,
                "confidence": result.confidence,
                "model_version": result.model_version,
                "metadata": {
                    **result.metadata,
                    "endpoint": "ml",
                    "request_id": request_id,
                    "samples_count": len(samples)
                }
            }
            
        except ValueError as e:
            # Client errors - safe to expose
            logger.warning(f"ML endpoint validation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "ValidationError",
                "metadata": {
                    "endpoint": "ml",
                    "request_id": request_id
                }
            }
        except Exception as e:
            # Server errors - don't expose details
            logger.error(f"ML endpoint error: {e}", exc_info=True)
            return {
                "success": False,
                "error": "Internal server error",
                "error_type": "InternalError",
                "metadata": {
                    "endpoint": "ml",
                    "request_id": request_id
                }
            }
    
    @property
    def request_count(self) -> int:
        """Get total number of requests handled."""
        with self._request_lock:
            return self._request_count

class DataEndpoint(BaseEndpoint):
    """Endpoint for data processing operations.
    
    This endpoint provides data processing capabilities
    via REST API using Haive Core DataProcessor.
    
    Args:
        processor: Data processor for handling requests
        
    Examples:
        >>> from haive.core import DataProcessor
        >>> 
        >>> processor = DataProcessor()
        >>> endpoint = DataEndpoint(processor)
        >>> 
        >>> request_data = {
        ...     "data": {"field1": "value1", "field2": 42}
        ... }
        >>> response = endpoint.handle_request(request_data)
        >>> print(response["processed_data"])
    """
    
    def __init__(self, processor: DataProcessor):
        self.processor = processor
        self._request_count = 0
        self._request_lock = Lock()
    
    def handle_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle data processing request.
        
        Args:
            data: Request data containing 'data' field
            
        Returns:
            Response with processed data and status
        """
        # Thread-safe request counting
        with self._request_lock:
            self._request_count += 1
            request_id = self._request_count
        
        try:
            # Validate request format
            if "data" not in data:
                raise ValueError("Request must contain 'data' field")
            
            input_data = data["data"]
            
            # Size validation
            if not isinstance(input_data, dict):
                raise ValueError("'data' field must be a dictionary")
            if len(str(input_data)) > 50000:
                raise ValueError("Input data too large")
            
            # Process data
            result = self.processor.process(input_data)
            
            if result.status == "success":
                return {
                    "success": True,
                    "processed_data": result.data,
                    "metadata": {
                        **result.metadata,
                        "endpoint": "data",
                        "request_id": request_id,
                        "processor_stats": self.processor.stats
                    }
                }
            else:
                return {
                    "success": False,
                    "error": result.error,
                    "metadata": {
                        "endpoint": "data", 
                        "request_id": request_id,
                        "status": result.status
                    }
                }
                
        except ValueError as e:
            # Client errors - safe to expose
            logger.warning(f"Data endpoint validation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "ValidationError",
                "metadata": {
                    "endpoint": "data",
                    "request_id": request_id
                }
            }
        except Exception as e:
            # Server errors - don't expose details
            logger.error(f"Data endpoint error: {e}", exc_info=True)
            return {
                "success": False,
                "error": "Internal server error",
                "error_type": "InternalError",
                "metadata": {
                    "endpoint": "data",
                    "request_id": request_id
                }
            }
    
    @property
    def request_count(self) -> int:
        """Get total number of requests handled."""
        with self._request_lock:
            return self._request_count

class BatchEndpoint(BaseEndpoint):
    """Endpoint for batch processing operations.
    
    This endpoint handles multiple requests in a single call,
    useful for processing large amounts of data efficiently.
    
    Args:
        ml_pipeline: Optional ML pipeline for predictions
        data_processor: Optional data processor
        
    Examples:
        >>> batch_endpoint = BatchEndpoint(ml_pipeline=pipeline)
        >>> 
        >>> request_data = {
        ...     "operations": [
        ...         {"type": "predict", "data": {"feature1": 1.0}},
        ...         {"type": "predict", "data": {"feature1": 2.0}}
        ...     ]
        ... }
        >>> response = batch_endpoint.handle_request(request_data)
    """
    
    def __init__(self, ml_pipeline: MLPipeline = None, data_processor: DataProcessor = None):
        self.ml_pipeline = ml_pipeline
        self.data_processor = data_processor
        self._request_count = 0
        self._batch_count = 0
        self._request_lock = Lock()
    
    def handle_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle batch processing request.
        
        Args:
            data: Request data containing 'operations' list
            
        Returns:
            Response with results for each operation
        """
        # Thread-safe request counting
        with self._request_lock:
            self._request_count += 1
            request_id = self._request_count
        
        try:
            if "operations" not in data:
                raise ValueError("Request must contain 'operations' field")
            
            operations = data["operations"]
            if not isinstance(operations, list):
                raise ValueError("'operations' must be a list")
            
            # Limit batch size
            if len(operations) > 50:
                raise ValueError("Too many operations in batch (max 50)")
            
            results = []
            
            for i, operation in enumerate(operations):
                try:
                    op_type = operation.get("type")
                    op_data = operation.get("data")
                    
                    if op_type == "predict" and self.ml_pipeline:
                        result = self.ml_pipeline.predict([op_data])
                        results.append({
                            "operation_index": i,
                            "success": True,
                            "result": {
                                "predictions": result.predictions,
                                "confidence": result.confidence
                            }
                        })
                    elif op_type == "process" and self.data_processor:
                        result = self.data_processor.process(op_data)
                        results.append({
                            "operation_index": i,
                            "success": result.status == "success",
                            "result": result.data if result.status == "success" else None,
                            "error": result.error if result.status != "success" else None
                        })
                    else:
                        results.append({
                            "operation_index": i,
                            "success": False,
                            "error": f"Unsupported operation type: {op_type}"
                        })
                        
                except Exception as e:
                    results.append({
                        "operation_index": i,
                        "success": False,
                        "error": str(e)
                    })
            
            with self._request_lock:
                self._batch_count += 1
                batch_id = self._batch_count
            
            return {
                "success": True,
                "results": results,
                "metadata": {
                    "endpoint": "batch",
                    "request_id": request_id,
                    "batch_id": batch_id,
                    "operations_count": len(operations),
                    "successful_operations": sum(1 for r in results if r["success"])
                }
            }
            
        except ValueError as e:
            # Client errors - safe to expose
            logger.warning(f"Batch endpoint validation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "ValidationError",
                "metadata": {
                    "endpoint": "batch",
                    "request_id": request_id
                }
            }
        except Exception as e:
            # Server errors - don't expose details
            logger.error(f"Batch endpoint error: {e}", exc_info=True)
            return {
                "success": False,
                "error": "Internal server error",
                "error_type": "InternalError",
                "metadata": {
                    "endpoint": "batch",
                    "request_id": request_id
                }
            }