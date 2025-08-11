"""ML Pipeline implementation for Haive."""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from haive.core import DataProcessor, BaseModel
from .model import MLModel

@dataclass 
class PipelineResult:
    """Result from ML pipeline execution.
    
    Attributes:
        predictions: Model predictions
        confidence: Confidence scores for predictions
        metadata: Pipeline execution metadata
        model_version: Version of the model used
    """
    predictions: List[Any]
    confidence: Optional[List[float]] = None
    metadata: Optional[Dict[str, Any]] = None
    model_version: Optional[str] = None

class MLPipeline:
    """Machine Learning pipeline integrating with Haive Core.
    
    This class provides a complete ML pipeline that integrates with
    the Haive ecosystem, using DataProcessor for preprocessing and
    MLModel for predictions.
    
    Args:
        data_processor: Haive core data processor for preprocessing
        model: ML model for making predictions
        config: Pipeline configuration
        
    Examples:
        Basic usage:
        
        >>> from haive.core import DataProcessor
        >>> from haive.ml import MLPipeline, MLModel
        >>> 
        >>> processor = DataProcessor()
        >>> model = MLModel(model_type="classifier")
        >>> pipeline = MLPipeline(processor, model)
        >>> 
        >>> result = pipeline.predict([{"feature1": 1.0, "feature2": 2.0}])
        >>> print(result.predictions)
        [0.85]
        
        With custom configuration:
        
        >>> config = {"batch_size": 100, "enable_caching": True}
        >>> pipeline = MLPipeline(processor, model, config=config)
    """
    
    def __init__(
        self, 
        data_processor: DataProcessor,
        model: Optional[MLModel] = None,
        config: Optional[Dict[str, Any]] = None
    ):
        self.data_processor = data_processor
        self.model = model
        self.config = config or {}
        self._pipeline_stats = {"predictions_made": 0, "errors": 0}
    
    def predict(self, data: List[Dict[str, Any]]) -> PipelineResult:
        """Make predictions on input data.
        
        Args:
            data: List of data samples for prediction
            
        Returns:
            PipelineResult: Contains predictions and metadata
            
        Raises:
            ValueError: If model is not set or data is invalid
        """
        if not self.model:
            raise ValueError("Model must be set before making predictions")
        
        if not data:
            raise ValueError("Input data cannot be empty")
        
        try:
            # Preprocess data using core processor
            processed_samples = []
            for sample in data:
                result = self.data_processor.process(sample)
                if result.status == "success":
                    processed_samples.append(result.data)
            
            # Make predictions
            predictions = self.model.predict(processed_samples)
            confidence_scores = self.model.predict_confidence(processed_samples)
            
            self._pipeline_stats["predictions_made"] += len(predictions)
            
            return PipelineResult(
                predictions=predictions,
                confidence=confidence_scores,
                metadata={
                    "samples_processed": len(processed_samples),
                    "pipeline_version": "0.1.0",
                    "preprocessing_config": self.data_processor.config
                },
                model_version=self.model.version
            )
            
        except Exception as e:
            self._pipeline_stats["errors"] += 1
            raise
    
    def train(self, training_data: List[Dict[str, Any]], labels: List[Any]) -> Dict[str, Any]:
        """Train the ML model with provided data.
        
        Args:
            training_data: Training samples
            labels: Target labels for training
            
        Returns:
            Training results and metrics
        """
        if not self.model:
            raise ValueError("Model must be set before training")
        
        # Preprocess training data
        processed_training_data = []
        for sample in training_data:
            result = self.data_processor.process(sample)
            if result.status == "success":
                processed_training_data.append(result.data)
        
        # Train model
        training_result = self.model.train(processed_training_data, labels)
        
        return {
            "training_samples": len(processed_training_data),
            "model_metrics": training_result,
            "preprocessing_stats": self.data_processor.stats
        }
    
    def set_model(self, model: MLModel) -> None:
        """Set or replace the ML model.
        
        Args:
            model: New ML model to use in the pipeline
        """
        self.model = model
    
    @property
    def stats(self) -> Dict[str, int]:
        """Get pipeline statistics."""
        return {
            **self._pipeline_stats,
            "preprocessing_stats": self.data_processor.stats
        }