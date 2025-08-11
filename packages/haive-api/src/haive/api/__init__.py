"""
Haive API Package

REST API framework and tools for the Haive ecosystem.
Provides easy integration of ML models and data processing into web APIs.

Examples:
    Basic API server:

    >>> from haive.api import APIServer
    >>> from haive.ml import MLPipeline
    >>> 
    >>> server = APIServer()
    >>> server.add_ml_endpoint("/predict", ml_pipeline)
    >>> server.run()
"""

from .server import APIServer
from .endpoints import MLEndpoint, DataEndpoint
from .middleware import AuthMiddleware, LoggingMiddleware

__version__ = "0.1.0"
__all__ = ["APIServer", "MLEndpoint", "DataEndpoint", "AuthMiddleware", "LoggingMiddleware"]