"""Utility functions and helpers.

This module provides various utility functions, decorators,
and helper classes used throughout the application.
"""

import hashlib
import json
import logging
import random
import re
import string
import time
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

logger = logging.getLogger(__name__)


def generate_id(prefix: str = "", length: int = 8) -> str:
    """Generate a random ID with optional prefix.

    Args:
        prefix: Optional prefix for the ID
        length: Length of random part (default: 8)

    Returns:
        Generated ID string

    Example:
        >>> generate_id("user", 6)
        'user_a3k9x2'
    """
    chars = string.ascii_lowercase + string.digits
    random_part = "".join(random.choices(chars, k=length))
    return f"{prefix}_{random_part}" if prefix else random_part


def slugify(text: str, max_length: Optional[int] = None) -> str:
    """Convert text to URL-friendly slug.

    Args:
        text: Input text to slugify
        max_length: Maximum length of slug

    Returns:
        URL-friendly slug

    Example:
        >>> slugify("Hello World! 123")
        'hello-world-123'
    """
    # Convert to lowercase and replace spaces
    slug = text.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[-\s]+", "-", slug)

    # Trim to max length if specified
    if max_length:
        slug = slug[:max_length].rstrip("-")

    return slug


def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    """Hash password with salt using SHA-256.

    Args:
        password: Plain text password
        salt: Optional salt (generated if not provided)

    Returns:
        Tuple of (hashed_password, salt)

    Note:
        This is a simple example. Use bcrypt or similar
        for production password hashing.
    """
    if not salt:
        salt = generate_id(length=16)

    salted = f"{password}{salt}"
    hashed = hashlib.sha256(salted.encode()).hexdigest()
    return hashed, salt


def timedelta_to_human(td: timedelta) -> str:
    """Convert timedelta to human-readable string.

    Args:
        td: Timedelta object

    Returns:
        Human-readable duration string

    Example:
        >>> timedelta_to_human(timedelta(days=2, hours=3, minutes=15))
        '2 days, 3 hours, 15 minutes'
    """
    parts = []

    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds and not parts:  # Only show seconds if nothing else
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    return ", ".join(parts) if parts else "0 seconds"


def parse_size(size_str: str) -> int:
    """Parse human-readable size string to bytes.

    Args:
        size_str: Size string (e.g., "10MB", "1.5GB")

    Returns:
        Size in bytes

    Example:
        >>> parse_size("10MB")
        10485760
        >>> parse_size("1.5GB")
        1610612736
    """
    units = {
        "B": 1,
        "KB": 1024,
        "MB": 1024**2,
        "GB": 1024**3,
        "TB": 1024**4,
    }

    match = re.match(r"([\d.]+)\s*([A-Z]+)", size_str.upper())
    if not match:
        raise ValueError(f"Invalid size format: {size_str}")

    value, unit = match.groups()
    if unit not in units:
        raise ValueError(f"Unknown unit: {unit}")

    return int(float(value) * units[unit])


def format_bytes(num_bytes: int, precision: int = 2) -> str:
    """Format bytes to human-readable string.

    Args:
        num_bytes: Number of bytes
        precision: Decimal precision

    Returns:
        Formatted size string

    Example:
        >>> format_bytes(1536)
        '1.50 KB'
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:.{precision}f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.{precision}f} PB"


class Timer:
    """Context manager for timing code execution.

    Example:
        >>> with Timer() as timer:
        ...     time.sleep(1)
        >>> print(f"Elapsed: {timer.elapsed:.2f}s")
        Elapsed: 1.00s
    """

    def __init__(self):
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None

    def __enter__(self) -> "Timer":
        self.start_time = time.time()
        return self

    def __exit__(self, *args) -> None:
        self.end_time = time.time()

    @property
    def elapsed(self) -> float:
        """Get elapsed time in seconds."""
        if self.start_time is None:
            return 0.0
        end = self.end_time or time.time()
        return end - self.start_time


def memoize(maxsize: int = 128):
    """Decorator for memoizing function results.

    Args:
        maxsize: Maximum cache size

    Example:
        >>> @memoize(maxsize=100)
        ... def expensive_function(x):
        ...     return x ** 2
    """

    def decorator(func: Callable) -> Callable:
        cache: Dict[Any, Any] = {}
        cache_order: List[Any] = []

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from args and kwargs
            key = (args, tuple(sorted(kwargs.items())))

            # Return cached result if available
            if key in cache:
                logger.debug(f"Cache hit for {func.__name__}")
                return cache[key]

            # Compute result
            result = func(*args, **kwargs)

            # Update cache
            cache[key] = result
            cache_order.append(key)

            # Evict oldest entry if cache is full
            if len(cache) > maxsize:
                oldest_key = cache_order.pop(0)
                del cache[oldest_key]

            return result

        wrapper.cache_clear = lambda: (cache.clear(), cache_order.clear())
        wrapper.cache_info = lambda: {"size": len(cache), "maxsize": maxsize}

        return wrapper

    return decorator


def validate_email(email: str) -> bool:
    """Validate email address format.

    Args:
        email: Email address to validate

    Returns:
        True if valid email format

    Example:
        >>> validate_email("user@example.com")
        True
        >>> validate_email("invalid.email")
        False
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def deep_merge(dict1: Dict, dict2: Dict) -> Dict:
    """Deep merge two dictionaries.

    Args:
        dict1: Base dictionary
        dict2: Dictionary to merge in

    Returns:
        Merged dictionary (dict1 is modified)

    Example:
        >>> d1 = {"a": 1, "b": {"c": 2}}
        >>> d2 = {"b": {"d": 3}, "e": 4}
        >>> deep_merge(d1, d2)
        {'a': 1, 'b': {'c': 2, 'd': 3}, 'e': 4}
    """
    for key, value in dict2.items():
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
            deep_merge(dict1[key], value)
        else:
            dict1[key] = value
    return dict1


def batch(iterable, size: int):
    """Split iterable into batches.

    Args:
        iterable: Input iterable
        size: Batch size

    Yields:
        Batches of specified size

    Example:
        >>> list(batch([1, 2, 3, 4, 5], 2))
        [[1, 2], [3, 4], [5]]
    """
    iterator = iter(iterable)
    while True:
        batch_items = []
        for _ in range(size):
            try:
                batch_items.append(next(iterator))
            except StopIteration:
                if batch_items:
                    yield batch_items
                return
        yield batch_items


def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """Safely parse JSON with default fallback.

    Args:
        json_str: JSON string to parse
        default: Default value if parsing fails

    Returns:
        Parsed JSON or default value
    """
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        logger.warning(f"Failed to parse JSON: {json_str[:50]}...")
        return default


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate string to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to append if truncated

    Returns:
        Truncated string

    Example:
        >>> truncate_string("Hello, World!", 10)
        'Hello, ...'
    """
    if len(text) <= max_length:
        return text

    truncate_at = max_length - len(suffix)
    return text[:truncate_at] + suffix


def find_files(
    directory: Union[str, Path], pattern: str = "*", recursive: bool = True
) -> List[Path]:
    """Find files matching pattern in directory.

    Args:
        directory: Directory to search
        pattern: Glob pattern (default: "*")
        recursive: Search subdirectories

    Returns:
        List of matching file paths

    Example:
        >>> find_files("src", "*.py")
        [Path('src/main.py'), Path('src/utils.py'), ...]
    """
    path = Path(directory)
    if not path.exists():
        return []

    if recursive:
        return list(path.rglob(pattern))
    else:
        return list(path.glob(pattern))


class RateLimiter:
    """Simple rate limiter using token bucket algorithm.

    Example:
        >>> limiter = RateLimiter(rate=10, per=60)  # 10 per minute
        >>> if limiter.allow():
        ...     # Perform rate-limited operation
        ...     pass
    """

    def __init__(self, rate: int, per: float):
        """
        Args:
            rate: Number of allowed requests
            per: Time period in seconds
        """
        self.rate = rate
        self.per = per
        self.allowance = float(rate)
        self.last_check = time.time()

    def allow(self) -> bool:
        """Check if request is allowed."""
        current = time.time()
        time_passed = current - self.last_check
        self.last_check = current

        # Add tokens based on time passed
        self.allowance += time_passed * (self.rate / self.per)

        # Cap at maximum rate
        if self.allowance > self.rate:
            self.allowance = float(self.rate)

        # Check if we have tokens
        if self.allowance < 1.0:
            return False

        # Consume one token
        self.allowance -= 1.0
        return True
