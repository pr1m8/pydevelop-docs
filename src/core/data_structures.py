"""Core data structures using dataclasses.

This module provides fundamental data structures used throughout
the application, implemented using Python's dataclasses for clean,
type-safe code.
"""

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, Generic, List, Optional, TypeVar


class Priority(Enum):
    """Task priority levels."""

    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()

    def __str__(self) -> str:
        return self.name.title()


class Status(Enum):
    """Generic status enumeration."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

    @classmethod
    def active_statuses(cls) -> List["Status"]:
        """Return statuses that indicate active work."""
        return [cls.PENDING, cls.IN_PROGRESS]

    @classmethod
    def terminal_statuses(cls) -> List["Status"]:
        """Return statuses that indicate completion."""
        return [cls.COMPLETED, cls.FAILED, cls.CANCELLED]


@dataclass(frozen=True)
class Point:
    """Immutable 2D point representation.

    A frozen dataclass representing a point in 2D space.
    Supports basic arithmetic operations.

    Attributes:
        x: X-coordinate
        y: Y-coordinate

    Example:
        >>> p1 = Point(1, 2)
        >>> p2 = Point(3, 4)
        >>> p1.distance_to(p2)
        2.8284271247461903
    """

    x: float
    y: float

    def distance_to(self, other: "Point") -> float:
        """Calculate Euclidean distance to another point."""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def __add__(self, other: "Point") -> "Point":
        """Add two points together."""
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        """Subtract one point from another."""
        return Point(self.x - other.x, self.y - other.y)


@dataclass
class Task:
    """Represents a task or work item.

    A comprehensive task representation with metadata, status tracking,
    and JSON serialization support.

    Attributes:
        id: Unique task identifier
        title: Task title/summary
        description: Detailed task description
        priority: Task priority level
        status: Current task status
        created_at: Task creation timestamp
        updated_at: Last update timestamp
        due_date: Optional due date
        tags: List of tags for categorization
        metadata: Additional task metadata
    """

    id: str
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    due_date: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate task data after initialization."""
        if not self.title.strip():
            raise ValueError("Task title cannot be empty")
        if self.due_date and self.due_date < self.created_at:
            raise ValueError("Due date cannot be before creation date")

    def update_status(self, new_status: Status) -> None:
        """Update task status and timestamp."""
        self.status = new_status
        self.updated_at = datetime.utcnow()

    def add_tag(self, tag: str) -> None:
        """Add a tag if not already present."""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        # Convert enums to strings
        data["priority"] = self.priority.name
        data["status"] = self.status.value
        # Convert datetimes to ISO format
        data["created_at"] = self.created_at.isoformat()
        if self.updated_at:
            data["updated_at"] = self.updated_at.isoformat()
        if self.due_date:
            data["due_date"] = self.due_date.isoformat()
        return data

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    @property
    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if not self.due_date:
            return False
        return (
            datetime.utcnow() > self.due_date
            and self.status in Status.active_statuses()
        )

    @property
    def days_until_due(self) -> Optional[int]:
        """Calculate days until due date."""
        if not self.due_date:
            return None
        delta = self.due_date - datetime.utcnow()
        return delta.days


T = TypeVar("T")


@dataclass
class Result(Generic[T]):
    """Generic result wrapper for operation outcomes.

    A Result type that can represent either success with a value
    or failure with an error message. Useful for error handling
    without exceptions.

    Type Parameters:
        T: The type of the success value

    Attributes:
        value: The success value (if success=True)
        error: Error message (if success=False)
        success: Whether the operation succeeded
        metadata: Additional result metadata

    Example:
        >>> result = Result.ok(42)
        >>> if result.is_ok():
        ...     print(result.value)
        42
    """

    value: Optional[T] = None
    error: Optional[str] = None
    success: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def ok(cls, value: T, **metadata) -> "Result[T]":
        """Create a successful result."""
        return cls(value=value, success=True, metadata=metadata)

    @classmethod
    def fail(cls, error: str, **metadata) -> "Result[T]":
        """Create a failed result."""
        return cls(error=error, success=False, metadata=metadata)

    def is_ok(self) -> bool:
        """Check if result is successful."""
        return self.success

    def is_error(self) -> bool:
        """Check if result is an error."""
        return not self.success

    def unwrap(self) -> T:
        """Get the value or raise an exception."""
        if not self.success:
            raise ValueError(f"Cannot unwrap error result: {self.error}")
        return self.value

    def unwrap_or(self, default: T) -> T:
        """Get the value or return default."""
        return self.value if self.success else default

    def map(self, func) -> "Result":
        """Transform the success value if present."""
        if self.success:
            return Result.ok(func(self.value), **self.metadata)
        return self
