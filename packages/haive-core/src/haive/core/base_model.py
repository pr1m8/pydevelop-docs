"""Base model classes for the Haive ecosystem."""

from typing import Dict, Any, Optional
from pydantic import BaseModel as PydanticBaseModel, Field
from datetime import datetime

class BaseModel(PydanticBaseModel):
    """Base model for all Haive entities.
    
    This class provides common functionality and fields that are used
    across all Haive models, ensuring consistency and shared behavior.
    
    Attributes:
        id: Unique identifier for the entity
        created_at: Timestamp when the entity was created
        updated_at: Timestamp when the entity was last updated
        metadata: Additional metadata dictionary
        
    Examples:
        Creating a basic model:
        
        >>> from haive.core import BaseModel
        >>> model = BaseModel(id="test-123")
        >>> print(model.created_at)
        2025-01-01T00:00:00
        
        With custom metadata:
        
        >>> model = BaseModel(
        ...     id="test-456",
        ...     metadata={"source": "api", "version": "1.0"}
        ... )
        >>> print(model.metadata["source"])
        'api'
    """
    
    id: str = Field(..., description="Unique identifier for the entity")
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp when the entity was created"
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when the entity was last updated"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata dictionary"
    )
    
    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def update_metadata(self, key: str, value: Any) -> None:
        """Update a metadata field and set updated_at timestamp.
        
        Args:
            key: Metadata key to update
            value: New value for the metadata key
        """
        self.metadata[key] = value
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary representation.
        
        Returns:
            Dictionary representation of the model
        """
        return self.dict()
    
    def __str__(self) -> str:
        """String representation of the model."""
        return f"{self.__class__.__name__}(id={self.id})"