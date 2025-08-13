"""Base schema classes for the testhaive framework.

This module provides foundational schema classes that all other schemas inherit from.
It includes validation mixins, serialization support, and state management patterns.
"""

import json
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel, Field, root_validator, validator


class ValidationLevel(str, Enum):
    """Validation levels for schema validation.

    Attributes:
        STRICT: Strict validation with no tolerance for errors
        NORMAL: Standard validation with reasonable error tolerance
        PERMISSIVE: Permissive validation allowing most inputs
        DISABLED: No validation performed
    """

    STRICT = "strict"
    NORMAL = "normal"
    PERMISSIVE = "permissive"
    DISABLED = "disabled"


class SerializationFormat(str, Enum):
    """Supported serialization formats.

    Attributes:
        JSON: JSON serialization
        YAML: YAML serialization
        DICT: Python dictionary format
        COMPRESSED: Compressed binary format
    """

    JSON = "json"
    YAML = "yaml"
    DICT = "dict"
    COMPRESSED = "compressed"


T = TypeVar("T", bound="BaseSchema")


class ValidationMixin(ABC):
    """Mixin class providing validation capabilities to schemas.

    This mixin adds comprehensive validation functionality including custom validators,
    field-level validation, cross-field validation, and validation reporting.

    Examples:
        Using validation mixin::

            class MySchema(BaseSchema, ValidationMixin):
                name: str
                age: int

                def validate_age(self, value: int) -> int:
                    if value < 0:
                        raise ValueError("Age cannot be negative")
                    return value

        Custom validation levels::

            schema = MySchema(name="test", age=25)
            schema.set_validation_level(ValidationLevel.STRICT)
            result = schema.validate_all()
    """

    def __init__(self, *args, **kwargs):
        """Initialize validation mixin with default settings."""
        super().__init__(*args, **kwargs)
        self._validation_level = ValidationLevel.NORMAL
        self._validation_errors: List[str] = []
        self._validation_warnings: List[str] = []

    @abstractmethod
    def validate_all(self) -> bool:
        """Validate all fields and relationships.

        Returns:
            True if validation passes, False otherwise

        Note:
            Subclasses must implement this method to define their validation logic.
        """
        pass

    def set_validation_level(self, level: ValidationLevel) -> None:
        """Set the validation level for this schema.

        Args:
            level: Validation level to use

        Examples:
            Setting strict validation::

                schema.set_validation_level(ValidationLevel.STRICT)

            Disabling validation for performance::

                schema.set_validation_level(ValidationLevel.DISABLED)
        """
        self._validation_level = level

    def get_validation_errors(self) -> List[str]:
        """Get list of validation errors.

        Returns:
            List of validation error messages
        """
        return self._validation_errors.copy()

    def get_validation_warnings(self) -> List[str]:
        """Get list of validation warnings.

        Returns:
            List of validation warning messages
        """
        return self._validation_warnings.copy()

    def clear_validation_messages(self) -> None:
        """Clear all validation errors and warnings."""
        self._validation_errors.clear()
        self._validation_warnings.clear()

    def add_validation_error(self, message: str) -> None:
        """Add a validation error message.

        Args:
            message: Error message to add
        """
        self._validation_errors.append(message)

    def add_validation_warning(self, message: str) -> None:
        """Add a validation warning message.

        Args:
            message: Warning message to add
        """
        self._validation_warnings.append(message)


class BaseSchema(BaseModel, ValidationMixin):
    """Base schema class for all testhaive schemas.

    This is the foundational schema class that provides common functionality
    including validation, serialization, metadata tracking, and lifecycle management.
    All other schemas in the testhaive framework should inherit from this class.

    Attributes:
        created_at: Timestamp when schema was created
        updated_at: Timestamp when schema was last updated
        version: Schema version for compatibility tracking
        metadata: Additional metadata dictionary

    Examples:
        Basic usage::

            class UserSchema(BaseSchema):
                name: str
                email: str
                age: int

            user = UserSchema(
                name="John Doe",
                email="john@example.com",
                age=30
            )

        With custom metadata::

            user = UserSchema(
                name="Jane Smith",
                email="jane@example.com",
                age=25,
                metadata={"department": "engineering", "role": "senior"}
            )

        Serialization example::

            # Export to JSON
            json_data = user.serialize(SerializationFormat.JSON)

            # Export to dictionary
            dict_data = user.serialize(SerializationFormat.DICT)

            # Load from data
            restored_user = UserSchema.deserialize(json_data, SerializationFormat.JSON)
    """

    created_at: datetime = Field(
        default_factory=datetime.now, description="Timestamp when schema was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp when schema was last updated",
    )
    version: str = Field(
        default="1.0.0", description="Schema version for compatibility tracking"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata dictionary"
    )

    class Config:
        """Pydantic configuration for BaseSchema."""

        use_enum_values = True
        validate_assignment = True
        extra = "forbid"
        json_encoders = {datetime: lambda v: v.isoformat()}

    def __init__(self, **kwargs):
        """Initialize BaseSchema with validation setup.

        Args:
            **kwargs: Keyword arguments for schema fields
        """
        super().__init__(**kwargs)
        self.clear_validation_messages()

    def validate_all(self) -> bool:
        """Validate all fields and relationships.

        Performs comprehensive validation including:
        - Field type validation
        - Value range validation
        - Cross-field relationship validation
        - Business logic validation

        Returns:
            True if validation passes, False otherwise

        Examples:
            Basic validation::

                if not schema.validate_all():
                    errors = schema.get_validation_errors()
                    print(f"Validation failed: {errors}")

            With different validation levels::

                schema.set_validation_level(ValidationLevel.STRICT)
                is_valid = schema.validate_all()
        """
        self.clear_validation_messages()

        if self._validation_level == ValidationLevel.DISABLED:
            return True

        try:
            # Validate field constraints
            self._validate_fields()

            # Validate business rules
            self._validate_business_rules()

            # Validate relationships
            self._validate_relationships()

            return len(self._validation_errors) == 0

        except Exception as e:
            self.add_validation_error(f"Validation exception: {str(e)}")
            return False

    def _validate_fields(self) -> None:
        """Validate individual field constraints."""
        # Override in subclasses for custom field validation
        pass

    def _validate_business_rules(self) -> None:
        """Validate business logic rules."""
        # Override in subclasses for business rule validation
        pass

    def _validate_relationships(self) -> None:
        """Validate relationships between fields."""
        # Override in subclasses for relationship validation
        pass

    def serialize(
        self, format: SerializationFormat = SerializationFormat.JSON
    ) -> Union[str, Dict[str, Any], bytes]:
        """Serialize schema to specified format.

        Args:
            format: Serialization format to use

        Returns:
            Serialized data in the specified format

        Raises:
            ValueError: If format is not supported

        Examples:
            JSON serialization::

                json_str = schema.serialize(SerializationFormat.JSON)

            Dictionary serialization::

                data_dict = schema.serialize(SerializationFormat.DICT)
        """
        if format == SerializationFormat.JSON:
            return self.json(indent=2)
        elif format == SerializationFormat.DICT:
            return self.dict()
        elif format == SerializationFormat.YAML:
            import yaml

            return yaml.dump(self.dict(), default_flow_style=False)
        elif format == SerializationFormat.COMPRESSED:
            import gzip

            json_data = self.json().encode("utf-8")
            return gzip.compress(json_data)
        else:
            raise ValueError(f"Unsupported serialization format: {format}")

    @classmethod
    def deserialize(
        cls: Type[T],
        data: Union[str, Dict[str, Any], bytes],
        format: SerializationFormat = SerializationFormat.JSON,
    ) -> T:
        """Deserialize data to create schema instance.

        Args:
            data: Data to deserialize
            format: Format of the input data

        Returns:
            New schema instance created from data

        Raises:
            ValueError: If format is not supported or data is invalid

        Examples:
            From JSON string::

                schema = MySchema.deserialize(json_str, SerializationFormat.JSON)

            From dictionary::

                schema = MySchema.deserialize(data_dict, SerializationFormat.DICT)
        """
        if format == SerializationFormat.JSON:
            if isinstance(data, str):
                return cls.parse_raw(data)
            else:
                return cls.parse_obj(data)
        elif format == SerializationFormat.DICT:
            return cls.parse_obj(data)
        elif format == SerializationFormat.YAML:
            import yaml

            if isinstance(data, str):
                yaml_data = yaml.safe_load(data)
            else:
                yaml_data = data
            return cls.parse_obj(yaml_data)
        elif format == SerializationFormat.COMPRESSED:
            import gzip

            if isinstance(data, bytes):
                json_data = gzip.decompress(data).decode("utf-8")
                return cls.parse_raw(json_data)
            else:
                raise ValueError("Compressed data must be bytes")
        else:
            raise ValueError(f"Unsupported deserialization format: {format}")

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp to current time."""
        self.updated_at = datetime.now()

    def set_metadata(self, key: str, value: Any) -> None:
        """Set a metadata value.

        Args:
            key: Metadata key
            value: Metadata value
        """
        self.metadata[key] = value
        self.update_timestamp()

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get a metadata value.

        Args:
            key: Metadata key
            default: Default value if key not found

        Returns:
            Metadata value or default
        """
        return self.metadata.get(key, default)

    def get_schema_info(self) -> Dict[str, Any]:
        """Get schema information summary.

        Returns:
            Dictionary containing schema metadata and status
        """
        return {
            "class_name": self.__class__.__name__,
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "field_count": len(self.__fields__),
            "metadata_keys": list(self.metadata.keys()),
            "validation_level": self._validation_level,
            "has_errors": len(self._validation_errors) > 0,
            "has_warnings": len(self._validation_warnings) > 0,
        }


class StateSchema(BaseSchema):
    """Base class for all state schemas in the testhaive framework.

    StateSchema extends BaseSchema with state-specific functionality including
    state transitions, history tracking, rollback capabilities, and state validation.

    This class is designed for schemas that represent mutable state that changes
    over time, such as agent states, workflow states, and execution contexts.

    Attributes:
        state_id: Unique identifier for this state instance
        previous_state_id: ID of the previous state in the chain
        state_type: Type classification for this state
        is_final: Whether this is a final/terminal state
        transition_count: Number of transitions this state has undergone

    Examples:
        Basic state schema::

            class GameState(StateSchema):
                player_position: Tuple[int, int]
                score: int
                level: int

            state = GameState(
                player_position=(0, 0),
                score=0,
                level=1,
                state_type="game"
            )

        State transitions::

            # Create new state from current
            new_state = state.create_transition(
                player_position=(1, 0),
                score=100
            )

            # Rollback to previous state
            if new_state.can_rollback():
                previous = new_state.rollback()

        State history tracking::

            # Get transition history
            history = state.get_transition_history()

            # Check if state has changed
            if state.has_changed_since(previous_state_id):
                print("State has been modified")
    """

    state_id: str = Field(
        default_factory=lambda: f"state_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
        description="Unique identifier for this state instance",
    )
    previous_state_id: Optional[str] = Field(
        default=None, description="ID of the previous state in the chain"
    )
    state_type: str = Field(
        default="generic", description="Type classification for this state"
    )
    is_final: bool = Field(
        default=False, description="Whether this is a final/terminal state"
    )
    transition_count: int = Field(
        default=0, description="Number of transitions this state has undergone"
    )

    def create_transition(self: T, **changes) -> T:
        """Create a new state instance with the specified changes.

        This method creates a new state that inherits from the current state
        but with the specified field changes applied. The new state will
        reference this state as its previous state.

        Args:
            **changes: Field changes to apply to the new state

        Returns:
            New state instance with changes applied

        Examples:
            Simple field update::

                new_state = current_state.create_transition(score=150)

            Multiple field changes::

                new_state = current_state.create_transition(
                    player_position=(2, 3),
                    score=200,
                    level=2
                )
        """
        # Get current state data
        current_data = self.dict()

        # Apply changes
        current_data.update(changes)

        # Update state metadata
        current_data["previous_state_id"] = self.state_id
        current_data["state_id"] = (
            f"state_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        )
        current_data["transition_count"] = self.transition_count + 1
        current_data["updated_at"] = datetime.now()

        # Create new instance
        return self.__class__(**current_data)

    def can_rollback(self) -> bool:
        """Check if this state can be rolled back to its previous state.

        Returns:
            True if rollback is possible, False otherwise
        """
        return self.previous_state_id is not None and not self.is_final

    def rollback(self) -> Optional["StateSchema"]:
        """Attempt to rollback to the previous state.

        Note:
            This method returns None as it cannot reconstruct the previous state
            without access to a state store. In a real implementation, this would
            query a state repository to retrieve the previous state.

        Returns:
            Previous state instance if available, None otherwise

        Raises:
            ValueError: If rollback is not possible
        """
        if not self.can_rollback():
            raise ValueError("Cannot rollback: no previous state or state is final")

        # In a real implementation, this would query a state store
        # For now, return None to indicate the interface
        return None

    def get_transition_history(self) -> List[str]:
        """Get the history of state transitions.

        Returns:
            List of state IDs in the transition chain

        Note:
            This method only returns the current state ID. In a real implementation,
            this would traverse the state chain to build the complete history.
        """
        # In a real implementation, this would traverse the state chain
        return [self.state_id]

    def has_changed_since(self, state_id: str) -> bool:
        """Check if this state has changed since the specified state.

        Args:
            state_id: ID of the state to compare against

        Returns:
            True if state has changed, False otherwise
        """
        return self.state_id != state_id

    def mark_final(self) -> None:
        """Mark this state as final/terminal.

        Final states cannot be transitioned from or rolled back.
        """
        self.is_final = True
        self.update_timestamp()

    def get_state_summary(self) -> Dict[str, Any]:
        """Get a summary of this state's information.

        Returns:
            Dictionary containing state summary information
        """
        base_info = self.get_schema_info()
        base_info.update(
            {
                "state_id": self.state_id,
                "previous_state_id": self.previous_state_id,
                "state_type": self.state_type,
                "is_final": self.is_final,
                "transition_count": self.transition_count,
                "can_rollback": self.can_rollback(),
            }
        )
        return base_info
