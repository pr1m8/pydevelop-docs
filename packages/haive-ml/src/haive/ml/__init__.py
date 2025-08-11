"""
Haive ML Package

Machine learning capabilities built on top of haive-core.
Provides ML pipelines, model training, and prediction functionality.

Examples:
    Basic ML pipeline:

    >>> from haive.ml import MLPipeline
    >>> from haive.core import DataProcessor
    >>> 
    >>> processor = DataProcessor()
    >>> pipeline = MLPipeline(processor)
    >>> result = pipeline.train(training_data)
"""

from .pipeline import MLPipeline
from .model import MLModel
from .trainer import ModelTrainer

__version__ = "0.1.0"
__all__ = ["MLPipeline", "MLModel", "ModelTrainer"]