"""Middleware implementations for Haive API."""

from typing import Dict, Any, Callable, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass
import time
import hashlib
from haive.core import BaseModel


@dataclass
class RequestContext:
    """Context information for API requests.
    
    Attributes:
        request_id: Unique identifier for the request
        start_time: Request start timestamp
        method: HTTP method
        path: Request path
        headers: Request headers dictionary
        user_id: Optional authenticated user ID
    """
    request_id: str
    start_time: float
    method: str
    path: str
    headers: Dict[str, str]
    user_id: Optional[str] = None


class BaseMiddleware(ABC):
    """Abstract base class for API middleware.
    
    All middleware in the Haive API system must inherit from this class
    and implement the process_request and process_response methods.
    
    Examples:
        Custom middleware implementation:
        
        >>> class CustomMiddleware(BaseMiddleware):
        ...     def process_request(self, context, data):
        ...         print(f"Processing request {context.request_id}")
        ...         return data
        ...     
        ...     def process_response(self, context, response):
        ...         print(f"Processing response for {context.request_id}")
        ...         return response
    """
    
    @abstractmethod
    def process_request(self, context: RequestContext, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming request.
        
        Args:
            context: Request context information
            data: Request data
            
        Returns:
            Modified request data
        """
        pass
    
    @abstractmethod
    def process_response(self, context: RequestContext, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process outgoing response.
        
        Args:
            context: Request context information
            response: Response data
            
        Returns:
            Modified response data
        """
        pass


class LoggingMiddleware(BaseMiddleware):
    """Middleware for request/response logging.
    
    This middleware logs detailed information about incoming requests
    and outgoing responses for debugging and monitoring purposes.
    
    Args:
        log_level: Logging level (debug, info, warning, error)
        include_data: Whether to include request/response data in logs
        
    Examples:
        Basic logging:
        
        >>> middleware = LoggingMiddleware()
        >>> server.add_middleware(middleware)
        
        Detailed logging with data:
        
        >>> middleware = LoggingMiddleware(
        ...     log_level="debug",
        ...     include_data=True
        ... )
    """
    
    def __init__(self, log_level: str = "info", include_data: bool = False):
        self.log_level = log_level
        self.include_data = include_data
        self._request_logs = []
    
    def process_request(self, context: RequestContext, data: Dict[str, Any]) -> Dict[str, Any]:
        """Log incoming request details.
        
        Args:
            context: Request context
            data: Request data
            
        Returns:
            Unmodified request data
        """
        log_entry = {
            "timestamp": context.start_time,
            "request_id": context.request_id,
            "method": context.method,
            "path": context.path,
            "user_id": context.user_id,
            "data_size": len(str(data)) if data else 0
        }
        
        if self.include_data:
            log_entry["request_data"] = data
        
        self._request_logs.append(log_entry)
        
        # Simulate logging output
        print(f"[{self.log_level.upper()}] REQUEST {context.request_id}: "
              f"{context.method} {context.path}")
        
        return data
    
    def process_response(self, context: RequestContext, response: Dict[str, Any]) -> Dict[str, Any]:
        """Log outgoing response details.
        
        Args:
            context: Request context
            response: Response data
            
        Returns:
            Unmodified response data
        """
        duration = time.time() - context.start_time
        
        log_entry = {
            "request_id": context.request_id,
            "duration_ms": duration * 1000,
            "success": response.get("success", True),
            "response_size": len(str(response))
        }
        
        if self.include_data:
            log_entry["response_data"] = response
            
        # Update existing request log
        for log in self._request_logs:
            if log["request_id"] == context.request_id:
                log.update(log_entry)
                break
        
        print(f"[{self.log_level.upper()}] RESPONSE {context.request_id}: "
              f"{'SUCCESS' if response.get('success', True) else 'ERROR'} "
              f"({duration*1000:.2f}ms)")
        
        return response
    
    @property
    def logs(self) -> list:
        """Get all request logs."""
        return self._request_logs.copy()


class AuthMiddleware(BaseMiddleware):
    """Authentication and authorization middleware.
    
    This middleware handles API key validation, user authentication,
    and request authorization based on user permissions.
    
    Args:
        api_key: Required API key for authentication
        require_auth: Whether authentication is required
        auth_header: Header name for authentication (default: "Authorization")
        
    Examples:
        API key authentication:
        
        >>> auth_middleware = AuthMiddleware(api_key="secret-key-123")
        >>> server.add_middleware(auth_middleware)
        
        Optional authentication:
        
        >>> auth_middleware = AuthMiddleware(
        ...     api_key="secret-key-123",
        ...     require_auth=False
        ... )
    """
    
    def __init__(
        self, 
        api_key: str,
        require_auth: bool = True,
        auth_header: str = "Authorization"
    ):
        self.api_key = api_key
        self.require_auth = require_auth
        self.auth_header = auth_header
        self._authenticated_users = {}
    
    def process_request(self, context: RequestContext, data: Dict[str, Any]) -> Dict[str, Any]:
        """Authenticate and authorize request.
        
        Args:
            context: Request context
            data: Request data
            
        Returns:
            Request data with authentication info
            
        Raises:
            ValueError: If authentication fails
        """
        auth_header = context.headers.get(self.auth_header, "")
        
        if not auth_header and self.require_auth:
            raise ValueError("Authentication required")
        
        if auth_header:
            # Extract API key from header
            if auth_header.startswith("Bearer "):
                provided_key = auth_header[7:]
            else:
                provided_key = auth_header
            
            # Validate API key
            if provided_key != self.api_key:
                raise ValueError("Invalid API key")
            
            # Generate user ID from API key
            user_id = hashlib.md5(provided_key.encode()).hexdigest()[:8]
            context.user_id = user_id
            
            # Track authenticated user
            self._authenticated_users[user_id] = {
                "first_seen": time.time(),
                "last_request": time.time(),
                "request_count": self._authenticated_users.get(user_id, {}).get("request_count", 0) + 1
            }
            
            print(f"[AUTH] Authenticated user {user_id} for request {context.request_id}")
        
        return data
    
    def process_response(self, context: RequestContext, response: Dict[str, Any]) -> Dict[str, Any]:
        """Add authentication metadata to response.
        
        Args:
            context: Request context
            response: Response data
            
        Returns:
            Response with authentication metadata
        """
        if context.user_id:
            response.setdefault("metadata", {})
            response["metadata"]["authenticated"] = True
            response["metadata"]["user_id"] = context.user_id
        else:
            response.setdefault("metadata", {})
            response["metadata"]["authenticated"] = False
        
        return response
    
    @property
    def authenticated_users(self) -> Dict[str, Dict]:
        """Get information about authenticated users."""
        return self._authenticated_users.copy()


class RateLimitMiddleware(BaseMiddleware):
    """Rate limiting middleware for API protection.
    
    This middleware implements rate limiting based on user ID or IP address
    to prevent abuse and ensure fair resource usage.
    
    Args:
        requests_per_minute: Maximum requests per minute per user
        window_size: Time window for rate limiting in seconds
        
    Examples:
        Basic rate limiting:
        
        >>> rate_limit = RateLimitMiddleware(requests_per_minute=60)
        >>> server.add_middleware(rate_limit)
        
        Custom window size:
        
        >>> rate_limit = RateLimitMiddleware(
        ...     requests_per_minute=100,
        ...     window_size=30  # 30-second window
        ... )
    """
    
    def __init__(self, requests_per_minute: int = 60, window_size: int = 60):
        self.requests_per_minute = requests_per_minute
        self.window_size = window_size
        self._request_counts = {}
    
    def process_request(self, context: RequestContext, data: Dict[str, Any]) -> Dict[str, Any]:
        """Check rate limit for request.
        
        Args:
            context: Request context
            data: Request data
            
        Returns:
            Unmodified request data
            
        Raises:
            ValueError: If rate limit exceeded
        """
        # Use user_id if available, otherwise use a default identifier
        identifier = context.user_id or "anonymous"
        current_time = time.time()
        
        # Initialize tracking for new users
        if identifier not in self._request_counts:
            self._request_counts[identifier] = []
        
        # Clean old requests outside the window
        self._request_counts[identifier] = [
            req_time for req_time in self._request_counts[identifier]
            if current_time - req_time < self.window_size
        ]
        
        # Check rate limit
        if len(self._request_counts[identifier]) >= self.requests_per_minute:
            raise ValueError(f"Rate limit exceeded: {self.requests_per_minute} requests per minute")
        
        # Add current request
        self._request_counts[identifier].append(current_time)
        
        return data
    
    def process_response(self, context: RequestContext, response: Dict[str, Any]) -> Dict[str, Any]:
        """Add rate limit information to response.
        
        Args:
            context: Request context
            response: Response data
            
        Returns:
            Response with rate limit headers
        """
        identifier = context.user_id or "anonymous"
        current_requests = len(self._request_counts.get(identifier, []))
        
        response.setdefault("metadata", {})
        response["metadata"]["rate_limit"] = {
            "limit": self.requests_per_minute,
            "remaining": max(0, self.requests_per_minute - current_requests),
            "window_seconds": self.window_size
        }
        
        return response
    
    @property
    def current_usage(self) -> Dict[str, int]:
        """Get current usage for all identifiers."""
        current_time = time.time()
        usage = {}
        
        for identifier, requests in self._request_counts.items():
            # Count recent requests
            recent_requests = [
                req_time for req_time in requests
                if current_time - req_time < self.window_size
            ]
            usage[identifier] = len(recent_requests)
        
        return usage