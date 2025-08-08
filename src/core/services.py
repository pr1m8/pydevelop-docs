"""Core service classes and utilities.

This module provides service layer implementations including
abstract base classes, concrete services, and utility functions.
"""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache, wraps
from typing import Any, Dict, Generic, List, Optional, Protocol, TypeVar

from .data_structures import Priority, Result, Status, Task
from .exceptions import NotFoundError, ValidationError

# Configure module logger
logger = logging.getLogger(__name__)


class CacheProtocol(Protocol):
    """Protocol for cache implementations."""

    def get(self, key: str) -> Optional[Any]:
        """Retrieve value from cache."""
        ...

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Store value in cache with optional TTL."""
        ...

    def delete(self, key: str) -> None:
        """Remove value from cache."""
        ...

    def clear(self) -> None:
        """Clear all cached values."""
        ...


T = TypeVar("T")


class Repository(ABC, Generic[T]):
    """Abstract base class for repository pattern.

    Provides a standard interface for data access operations.
    Concrete implementations should handle specific storage backends.

    Type Parameters:
        T: The entity type this repository manages
    """

    @abstractmethod
    async def get(self, id: str) -> Optional[T]:
        """Retrieve entity by ID."""
        pass

    @abstractmethod
    async def get_all(self) -> List[T]:
        """Retrieve all entities."""
        pass

    @abstractmethod
    async def save(self, entity: T) -> T:
        """Save or update entity."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete entity by ID."""
        pass

    @abstractmethod
    async def exists(self, id: str) -> bool:
        """Check if entity exists."""
        pass


class InMemoryTaskRepository(Repository[Task]):
    """In-memory implementation of task repository.

    A simple in-memory storage for tasks, useful for testing
    and development. Not suitable for production use.

    Attributes:
        _storage: Internal task storage
        _lock: Async lock for thread-safe operations
    """

    def __init__(self):
        self._storage: Dict[str, Task] = {}
        self._lock = asyncio.Lock()

    async def get(self, id: str) -> Optional[Task]:
        """Retrieve task by ID."""
        async with self._lock:
            return self._storage.get(id)

    async def get_all(self) -> List[Task]:
        """Retrieve all tasks."""
        async with self._lock:
            return list(self._storage.values())

    async def save(self, task: Task) -> Task:
        """Save or update task."""
        async with self._lock:
            task.updated_at = datetime.utcnow()
            self._storage[task.id] = task
            logger.info(f"Task saved: {task.id}")
            return task

    async def delete(self, id: str) -> bool:
        """Delete task by ID."""
        async with self._lock:
            if id in self._storage:
                del self._storage[id]
                logger.info(f"Task deleted: {id}")
                return True
            return False

    async def exists(self, id: str) -> bool:
        """Check if task exists."""
        async with self._lock:
            return id in self._storage

    async def find_by_status(self, status: Status) -> List[Task]:
        """Find all tasks with given status."""
        async with self._lock:
            return [t for t in self._storage.values() if t.status == status]

    async def find_by_priority(self, priority: Priority) -> List[Task]:
        """Find all tasks with given priority."""
        async with self._lock:
            return [t for t in self._storage.values() if t.priority == priority]


class TaskService:
    """High-level task management service.

    Provides business logic for task operations, coordinating
    between repositories, validation, and other services.

    Attributes:
        repository: Task repository for data access
        cache: Optional cache for performance optimization
    """

    def __init__(
        self, repository: Repository[Task], cache: Optional[CacheProtocol] = None
    ):
        self.repository = repository
        self.cache = cache
        self._validators = []

    async def create_task(
        self,
        id: str,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        due_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
    ) -> Result[Task]:
        """Create a new task with validation."""
        try:
            # Validate ID uniqueness
            if await self.repository.exists(id):
                return Result.fail(f"Task with ID '{id}' already exists")

            # Create task
            task = Task(
                id=id,
                title=title,
                description=description,
                priority=priority,
                due_date=due_date,
                tags=tags or [],
            )

            # Run validators
            for validator in self._validators:
                if not validator(task):
                    return Result.fail("Task validation failed")

            # Save to repository
            saved_task = await self.repository.save(task)

            # Cache if available
            if self.cache:
                self.cache.set(f"task:{id}", saved_task, ttl=300)

            logger.info(f"Task created: {id}")
            return Result.ok(saved_task)

        except Exception as e:
            logger.error(f"Failed to create task: {e}")
            return Result.fail(str(e))

    async def get_task(self, id: str) -> Result[Task]:
        """Retrieve task by ID with caching."""
        # Check cache first
        if self.cache:
            cached = self.cache.get(f"task:{id}")
            if cached:
                logger.debug(f"Task retrieved from cache: {id}")
                return Result.ok(cached)

        # Fetch from repository
        task = await self.repository.get(id)
        if not task:
            return Result.fail(f"Task not found: {id}")

        # Update cache
        if self.cache:
            self.cache.set(f"task:{id}", task, ttl=300)

        return Result.ok(task)

    async def update_task_status(self, id: str, new_status: Status) -> Result[Task]:
        """Update task status with validation."""
        result = await self.get_task(id)
        if result.is_error():
            return result

        task = result.value
        old_status = task.status

        # Validate status transition
        if not self._is_valid_transition(old_status, new_status):
            return Result.fail(
                f"Invalid status transition: {old_status} -> {new_status}"
            )

        # Update status
        task.update_status(new_status)
        saved_task = await self.repository.save(task)

        # Invalidate cache
        if self.cache:
            self.cache.delete(f"task:{id}")

        logger.info(f"Task {id} status updated: {old_status} -> {new_status}")
        return Result.ok(saved_task)

    def _is_valid_transition(self, old: Status, new: Status) -> bool:
        """Validate status transitions."""
        # Cannot transition from terminal states
        if old in Status.terminal_statuses() and new != old:
            return False

        # Specific transition rules
        transitions = {
            Status.PENDING: [Status.IN_PROGRESS, Status.CANCELLED],
            Status.IN_PROGRESS: [Status.COMPLETED, Status.FAILED, Status.CANCELLED],
            Status.COMPLETED: [Status.COMPLETED],
            Status.FAILED: [Status.PENDING, Status.FAILED],
            Status.CANCELLED: [Status.CANCELLED],
        }

        return new in transitions.get(old, [])

    def add_validator(self, validator):
        """Add a task validator function."""
        self._validators.append(validator)


def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Decorator for retrying failed operations.

    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Backoff multiplier for each retry

    Example:
        >>> @retry(max_attempts=3, delay=0.5)
        ... async def flaky_operation():
        ...     # Operation that might fail
        ...     pass
    """

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay

            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Attempt {attempt + 1} failed: {e}. "
                            f"Retrying in {current_delay}s..."
                        )
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(f"All {max_attempts} attempts failed")

            raise last_exception

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Attempt {attempt + 1} failed: {e}. "
                            f"Retrying in {current_delay}s..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(f"All {max_attempts} attempts failed")

            raise last_exception

        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


class MetricsCollector:
    """Simple metrics collection service.

    Collects and aggregates application metrics for monitoring
    and analysis purposes.
    """

    def __init__(self):
        self._metrics: Dict[str, List[float]] = {}
        self._counters: Dict[str, int] = {}

    def record_value(self, metric_name: str, value: float) -> None:
        """Record a metric value."""
        if metric_name not in self._metrics:
            self._metrics[metric_name] = []
        self._metrics[metric_name].append(value)

    def increment_counter(self, counter_name: str, amount: int = 1) -> None:
        """Increment a counter."""
        if counter_name not in self._counters:
            self._counters[counter_name] = 0
        self._counters[counter_name] += amount

    def get_average(self, metric_name: str) -> Optional[float]:
        """Calculate average for a metric."""
        values = self._metrics.get(metric_name, [])
        return sum(values) / len(values) if values else None

    def get_counter(self, counter_name: str) -> int:
        """Get counter value."""
        return self._counters.get(counter_name, 0)

    @lru_cache(maxsize=128)
    def get_percentile(self, metric_name: str, percentile: float) -> Optional[float]:
        """Calculate percentile for a metric."""
        values = sorted(self._metrics.get(metric_name, []))
        if not values:
            return None

        index = int(len(values) * percentile / 100)
        return values[min(index, len(values) - 1)]

    def reset(self) -> None:
        """Reset all metrics."""
        self._metrics.clear()
        self._counters.clear()
        self.get_percentile.cache_clear()
