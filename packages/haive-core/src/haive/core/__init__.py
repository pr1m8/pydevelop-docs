"""
Haive Core Package

This package provides the foundational classes and utilities for the Haive ecosystem.
All other Haive packages build upon the core functionality provided here.

Examples:
    Basic usage of the core DataProcessor:

    >>> from haive.core import DataProcessor
    >>> processor = DataProcessor()
    >>> result = processor.process({"data": "sample"})
    >>> print(result.status)
    'success'
"""

from .data_processor import DataProcessor
from .base_model import BaseModel
from .exceptions import HaiveError, ProcessingError

__version__ = "0.1.0"
__all__ = ["DataProcessor", "BaseModel", "HaiveError", "ProcessingError"]