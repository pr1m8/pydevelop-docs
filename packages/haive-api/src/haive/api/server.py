"""API Server implementation for Haive."""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from haive.core import BaseModel, DataProcessor
from haive.ml import MLPipeline
from .endpoints import MLEndpoint, DataEndpoint
from .middleware import BaseMiddleware

@dataclass
class ServerConfig:
    """Configuration for the API server.
    
    Attributes:
        host: Server host address
        port: Server port number
        debug: Enable debug mode
        cors_enabled: Enable CORS support
        rate_limit: Requests per minute limit
        timeout: Request timeout in seconds
    """
    host: str = "localhost"
    port: int = 8000
    debug: bool = False
    cors_enabled: bool = True
    rate_limit: int = 1000
    timeout: int = 30

class APIServer:
    """REST API server for the Haive ecosystem.
    
    This class provides a complete API server that can integrate
    ML pipelines, data processors, and custom endpoints with
    built-in middleware support.
    
    Args:
        config: Server configuration
        data_processor: Optional default data processor
        
    Examples:
        Basic server setup:
        
        >>> from haive.api import APIServer
        >>> from haive.core import DataProcessor
        >>> 
        >>> processor = DataProcessor()
        >>> server = APIServer(data_processor=processor)
        >>> server.add_endpoint("/health", lambda: {"status": "ok"})
        >>> server.run()
        
        With ML integration:
        
        >>> from haive.ml import MLPipeline, MLModel, ModelType
        >>> 
        >>> model = MLModel(id="api-model", model_type=ModelType.CLASSIFIER)
        >>> pipeline = MLPipeline(processor, model)
        >>> 
        >>> server.add_ml_endpoint("/predict", pipeline)
        >>> server.run()
    """
    
    def __init__(
        self, 
        config: Optional[ServerConfig] = None,
        data_processor: Optional[DataProcessor] = None
    ):
        self.config = config or ServerConfig()
        self.data_processor = data_processor
        self.endpoints = {}
        self.middleware = []
        self._server_stats = {"requests_handled": 0, "errors": 0}
        
        # Add default endpoints
        self._setup_default_endpoints()
    
    def add_endpoint(
        self, 
        path: str, 
        handler: Callable,
        methods: List[str] = ["GET"]
    ) -> None:
        """Add a custom endpoint to the server.
        
        Args:
            path: URL path for the endpoint
            handler: Function to handle requests
            methods: HTTP methods supported (default: GET)
            
        Examples:
            >>> def health_check():
            ...     return {"status": "healthy", "timestamp": "2025-01-01T00:00:00Z"}
            >>> 
            >>> server.add_endpoint("/health", health_check)
            >>> server.add_endpoint("/status", health_check, methods=["GET", "POST"])
        """
        self.endpoints[path] = {
            "handler": handler,
            "methods": methods,
            "type": "custom"
        }
    
    def add_ml_endpoint(
        self, 
        path: str, 
        pipeline: MLPipeline,
        methods: List[str] = ["POST"]
    ) -> None:
        """Add an ML prediction endpoint.
        
        Args:
            path: URL path for the ML endpoint
            pipeline: ML pipeline for making predictions
            methods: HTTP methods supported (default: POST)
            
        Examples:
            >>> ml_endpoint = server.add_ml_endpoint("/predict", pipeline)
            >>> # Now POST /predict will accept data and return predictions
        """
        ml_endpoint = MLEndpoint(pipeline)
        self.endpoints[path] = {
            "handler": ml_endpoint.handle_request,
            "methods": methods,
            "type": "ml"
        }
    
    def add_data_endpoint(
        self, 
        path: str,
        processor: Optional[DataProcessor] = None,
        methods: List[str] = ["POST"]
    ) -> None:
        """Add a data processing endpoint.
        
        Args:
            path: URL path for the data endpoint
            processor: Data processor (uses default if None)
            methods: HTTP methods supported (default: POST)
        """
        processor = processor or self.data_processor
        if not processor:
            raise ValueError("Data processor required for data endpoints")
        
        data_endpoint = DataEndpoint(processor)
        self.endpoints[path] = {
            "handler": data_endpoint.handle_request,
            "methods": methods,
            "type": "data"
        }
    
    def add_middleware(self, middleware: BaseMiddleware) -> None:
        """Add middleware to the server.
        
        Args:
            middleware: Middleware instance to add
            
        Examples:
            >>> from haive.api import AuthMiddleware, LoggingMiddleware
            >>> 
            >>> server.add_middleware(LoggingMiddleware())
            >>> server.add_middleware(AuthMiddleware(api_key="secret"))
        """
        self.middleware.append(middleware)
    
    def remove_endpoint(self, path: str) -> bool:
        """Remove an endpoint from the server.
        
        Args:
            path: URL path to remove
            
        Returns:
            True if endpoint was removed, False if not found
        """
        if path in self.endpoints:
            del self.endpoints[path]
            return True
        return False
    
    def run(self, host: Optional[str] = None, port: Optional[int] = None) -> None:
        """Start the API server.
        
        Args:
            host: Override config host
            port: Override config port
            
        Note:
            This is a mock implementation. In a real scenario,
            this would start an actual web server (Flask, FastAPI, etc.)
        """
        actual_host = host or self.config.host
        actual_port = port or self.config.port
        
        print(f"🚀 Starting Haive API Server on {actual_host}:{actual_port}")
        print(f"📊 Debug mode: {self.config.debug}")
        print(f"🔧 Registered endpoints: {len(self.endpoints)}")
        
        for path, info in self.endpoints.items():
            methods_str = ", ".join(info["methods"])
            print(f"   {methods_str} {path} ({info['type']})")
        
        print(f"🛡️  Middleware: {len(self.middleware)} active")
        print("🎉 Server started successfully!")
        
        # In a real implementation, this would start the actual server
        # For demo purposes, we'll just simulate it
        self._simulate_server_requests()
    
    def stop(self) -> None:
        """Stop the API server."""
        print("🛑 Stopping Haive API Server...")
        print(f"📈 Total requests handled: {self._server_stats['requests_handled']}")
        print(f"❌ Total errors: {self._server_stats['errors']}")
    
    def _setup_default_endpoints(self) -> None:
        """Set up default server endpoints."""
        self.add_endpoint("/", self._root_handler)
        self.add_endpoint("/health", self._health_handler)
        self.add_endpoint("/stats", self._stats_handler)
    
    def _root_handler(self) -> Dict[str, Any]:
        """Root endpoint handler."""
        return {
            "message": "Welcome to Haive API Server",
            "version": "0.1.0",
            "endpoints": list(self.endpoints.keys())
        }
    
    def _health_handler(self) -> Dict[str, Any]:
        """Health check endpoint handler."""
        return {
            "status": "healthy",
            "server": "haive-api",
            "version": "0.1.0",
            "endpoints_count": len(self.endpoints),
            "middleware_count": len(self.middleware)
        }
    
    def _stats_handler(self) -> Dict[str, Any]:
        """Server statistics endpoint handler."""
        return {
            "server_stats": self._server_stats,
            "config": {
                "host": self.config.host,
                "port": self.config.port,
                "debug": self.config.debug
            }
        }
    
    def _simulate_server_requests(self) -> None:
        """Simulate handling some requests (for demo purposes)."""
        # Simulate a few requests
        for i in range(5):
            self._server_stats["requests_handled"] += 1
            
        print(f"✅ Handled {self._server_stats['requests_handled']} demo requests")
    
    @property
    def stats(self) -> Dict[str, Any]:
        """Get server statistics."""
        return {
            **self._server_stats,
            "endpoints_registered": len(self.endpoints),
            "middleware_active": len(self.middleware),
            "config": self.config.__dict__
        }