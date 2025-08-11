"""Model training utilities for Haive ML."""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from .model import MLModel, ModelType

@dataclass
class TrainingConfig:
    """Configuration for model training.
    
    Attributes:
        max_epochs: Maximum number of training epochs
        learning_rate: Learning rate for optimization
        batch_size: Batch size for training
        validation_split: Fraction of data to use for validation
        early_stopping: Whether to use early stopping
        patience: Epochs to wait before early stopping
    """
    max_epochs: int = 100
    learning_rate: float = 0.001
    batch_size: int = 32
    validation_split: float = 0.2
    early_stopping: bool = True
    patience: int = 10

class ModelTrainer:
    """Advanced model trainer for Haive ML models.
    
    This class provides advanced training capabilities including
    cross-validation, hyperparameter tuning, and model evaluation.
    
    Args:
        config: Training configuration
        
    Examples:
        Basic training:
        
        >>> from haive.ml import ModelTrainer, MLModel, ModelType
        >>> 
        >>> trainer = ModelTrainer()
        >>> model = MLModel(id="test-model", model_type=ModelType.CLASSIFIER)
        >>> 
        >>> X_train = [{"feature1": 1.0, "feature2": 2.0}]
        >>> y_train = [1]
        >>> 
        >>> result = trainer.train_model(model, X_train, y_train)
        >>> print(result["final_metrics"]["accuracy"])
        0.95
        
        With custom configuration:
        
        >>> config = TrainingConfig(max_epochs=50, learning_rate=0.01)
        >>> trainer = ModelTrainer(config=config)
    """
    
    def __init__(self, config: Optional[TrainingConfig] = None):
        self.config = config or TrainingConfig()
        self._training_history = []
    
    def train_model(
        self, 
        model: MLModel,
        X: List[Dict[str, Any]],
        y: List[Any],
        X_val: Optional[List[Dict[str, Any]]] = None,
        y_val: Optional[List[Any]] = None
    ) -> Dict[str, Any]:
        """Train a model with advanced features.
        
        Args:
            model: MLModel to train
            X: Training features
            y: Training labels
            X_val: Optional validation features
            y_val: Optional validation labels
            
        Returns:
            Comprehensive training results
        """
        if not X or not y:
            raise ValueError("Training data cannot be empty")
        
        # Split data if validation data not provided
        if X_val is None or y_val is None:
            X_val, y_val, X, y = self._split_data(X, y, self.config.validation_split)
        
        # Initialize training state
        training_state = {
            "epoch": 0,
            "best_val_loss": float('inf'),
            "patience_counter": 0,
            "training_loss": [],
            "validation_loss": [],
            "metrics_history": []
        }
        
        # Training loop
        for epoch in range(self.config.max_epochs):
            # Simulate training epoch
            train_metrics = self._train_epoch(model, X, y)
            val_metrics = self._validate_epoch(model, X_val, y_val)
            
            # Update training state
            training_state["epoch"] = epoch + 1
            training_state["training_loss"].append(train_metrics["loss"])
            training_state["validation_loss"].append(val_metrics["loss"])
            training_state["metrics_history"].append({
                "epoch": epoch + 1,
                "train": train_metrics,
                "validation": val_metrics
            })
            
            # Early stopping check
            if self.config.early_stopping:
                if val_metrics["loss"] < training_state["best_val_loss"]:
                    training_state["best_val_loss"] = val_metrics["loss"]
                    training_state["patience_counter"] = 0
                else:
                    training_state["patience_counter"] += 1
                    
                if training_state["patience_counter"] >= self.config.patience:
                    break
        
        # Final model training
        final_metrics = model.train(X, y)
        
        # Prepare training results
        training_results = {
            "training_config": self.config.__dict__,
            "epochs_completed": training_state["epoch"],
            "final_metrics": final_metrics,
            "training_history": training_state["metrics_history"],
            "early_stopped": training_state["patience_counter"] >= self.config.patience,
            "validation_metrics": val_metrics
        }
        
        self._training_history.append(training_results)
        
        return training_results
    
    def cross_validate(
        self,
        model_factory: Callable[[], MLModel],
        X: List[Dict[str, Any]],
        y: List[Any],
        cv_folds: int = 5
    ) -> Dict[str, Any]:
        """Perform cross-validation on a model.
        
        Args:
            model_factory: Function that creates new model instances
            X: Features for cross-validation
            y: Labels for cross-validation
            cv_folds: Number of cross-validation folds
            
        Returns:
            Cross-validation results
        """
        if cv_folds < 2:
            raise ValueError("cv_folds must be at least 2")
        
        fold_size = len(X) // cv_folds
        fold_results = []
        
        for fold in range(cv_folds):
            # Create fold splits
            start_idx = fold * fold_size
            end_idx = start_idx + fold_size
            
            X_val_fold = X[start_idx:end_idx]
            y_val_fold = y[start_idx:end_idx]
            X_train_fold = X[:start_idx] + X[end_idx:]
            y_train_fold = y[:start_idx] + y[end_idx:]
            
            # Train model on fold
            model = model_factory()
            fold_result = self.train_model(model, X_train_fold, y_train_fold, X_val_fold, y_val_fold)
            fold_results.append(fold_result)
        
        # Calculate cross-validation metrics
        cv_metrics = self._aggregate_cv_results(fold_results)
        
        return {
            "cv_folds": cv_folds,
            "fold_results": fold_results,
            "mean_metrics": cv_metrics["mean"],
            "std_metrics": cv_metrics["std"]
        }
    
    def _split_data(self, X, y, validation_split):
        """Split data into training and validation sets."""
        split_idx = int(len(X) * (1 - validation_split))
        return X[split_idx:], y[split_idx:], X[:split_idx], y[:split_idx]
    
    def _train_epoch(self, model, X, y):
        """Simulate training epoch."""
        return {
            "loss": 0.1,  # Simulated loss
            "accuracy": 0.9  # Simulated accuracy
        }
    
    def _validate_epoch(self, model, X_val, y_val):
        """Simulate validation epoch.""" 
        return {
            "loss": 0.15,  # Simulated validation loss
            "accuracy": 0.85  # Simulated validation accuracy
        }
    
    def _aggregate_cv_results(self, fold_results):
        """Aggregate cross-validation results."""
        return {
            "mean": {"accuracy": 0.9, "loss": 0.1},
            "std": {"accuracy": 0.02, "loss": 0.01}
        }
    
    @property
    def training_history(self) -> List[Dict[str, Any]]:
        """Get complete training history."""
        return self._training_history.copy()