"""Pytest configuration and fixtures for pydvlppy tests.

This module provides common fixtures and configuration for all Pydvlppy tests.
"""

import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any

import pytest


@pytest.fixture
def temp_project_dir():
    """Create a temporary directory for test projects."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_project_info() -> Dict[str, Any]:
    """Provide sample project information for testing."""
    return {
        "name": "Test Project",
        "description": "A test project for Pydvlppy validation",
        "author": "Test Author",
        "version": "1.0.0",
        "python_requires": ">=3.12",
    }


@pytest.fixture  
def monorepo_structure(temp_project_dir):
    """Create a sample monorepo structure for testing."""
    project_dir = temp_project_dir / "test-monorepo"
    project_dir.mkdir()
    
    # Create packages directory
    packages_dir = project_dir / "packages"
    packages_dir.mkdir()
    
    # Create sample packages
    for pkg_name in ["package-a", "package-b", "package-c"]:
        pkg_dir = packages_dir / pkg_name
        pkg_dir.mkdir()
        
        # Create src structure
        src_dir = pkg_dir / "src" / pkg_name.replace("-", "_")
        src_dir.mkdir(parents=True)
        
        # Add __init__.py
        (src_dir / "__init__.py").write_text(f'"""Package {pkg_name}."""\n__version__ = "1.0.0"')
        
        # Add a module
        (src_dir / "core.py").write_text(f'''"""Core module for {pkg_name}."""

class {pkg_name.replace("-", "_").title()}Core:
    """Main class for {pkg_name}."""
    
    def __init__(self):
        """Initialize the core."""
        pass
        
    def process(self, data: str) -> str:
        """Process data.
        
        Args:
            data: Input data to process
            
        Returns:
            Processed data
        """
        return f"Processed: {{data}}"
''')
        
        # Create pyproject.toml
        (pkg_dir / "pyproject.toml").write_text(f'''[tool.poetry]
name = "{pkg_name}"
version = "1.0.0"
description = "Test package {pkg_name}"
authors = ["Test Author <test@example.com>"]

[tool.poetry.dependencies]
python = "^3.12"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
''')
    
    # Create main pyproject.toml
    (project_dir / "pyproject.toml").write_text('''[tool.poetry]
name = "test-monorepo"
version = "1.0.0"
description = "Test monorepo project"
authors = ["Test Author <test@example.com>"]

[tool.poetry.dependencies]
python = "^3.12"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
''')
    
    return project_dir


@pytest.fixture
def single_package_structure(temp_project_dir):
    """Create a sample single package structure for testing."""
    project_dir = temp_project_dir / "test-package"
    project_dir.mkdir()
    
    # Create src structure
    src_dir = project_dir / "src" / "test_package"
    src_dir.mkdir(parents=True)
    
    # Add __init__.py
    (src_dir / "__init__.py").write_text('''"""Test package."""
__version__ = "1.0.0"

from .core import TestCore

__all__ = ["TestCore"]
''')
    
    # Add core module
    (src_dir / "core.py").write_text('''"""Core functionality for test package."""

from typing import Optional


class TestCore:
    """Main test class with comprehensive docstrings.
    
    This class demonstrates proper Google-style docstrings
    for Pydvlppy testing.
    
    Attributes:
        name: The name of the test instance
        value: Optional numeric value
        
    Example:
        Basic usage::
        
            core = TestCore("test")
            result = core.process("data")
            print(result)
    """
    
    def __init__(self, name: str, value: Optional[int] = None):
        """Initialize TestCore.
        
        Args:
            name: Name for this test instance
            value: Optional numeric value for calculations
            
        Raises:
            ValueError: If name is empty
        """
        if not name:
            raise ValueError("Name cannot be empty")
        self.name = name
        self.value = value
        
    def process(self, data: str) -> str:
        """Process input data with test logic.
        
        Args:
            data: Input data to process
            
        Returns:
            Processed data with instance name prefix
            
        Example:
            >>> core = TestCore("test")
            >>> core.process("hello")
            'test: Processed hello'
        """
        return f"{self.name}: Processed {data}"
        
    def calculate(self, x: int, y: int) -> int:
        """Perform calculation with instance value.
        
        Args:
            x: First number
            y: Second number
            
        Returns:
            Result of calculation, optionally modified by instance value
            
        Note:
            If instance has a value, it will be added to the result.
        """
        result = x + y
        if self.value is not None:
            result += self.value
        return result
''')
    
    # Add utils module
    (src_dir / "utils.py").write_text('''"""Utility functions for test package."""

from typing import List, Dict, Any


def format_data(data: List[str], separator: str = ", ") -> str:
    """Format list of strings into a single string.
    
    Args:
        data: List of strings to format
        separator: String to use as separator
        
    Returns:
        Formatted string with all elements joined
        
    Example:
        >>> format_data(["a", "b", "c"])
        'a, b, c'
        >>> format_data(["x", "y"], " | ")
        'x | y'
    """
    return separator.join(data)


def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration dictionary.
    
    Args:
        config: Configuration dictionary to validate
        
    Returns:
        True if configuration is valid, False otherwise
        
    Note:
        A valid configuration must have 'name' and 'version' keys.
    """
    required_keys = {"name", "version"}
    return all(key in config for key in required_keys)


class ConfigManager:
    """Manages configuration for the test package.
    
    This class provides configuration management functionality
    with validation and default values.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize ConfigManager.
        
        Args:
            config: Initial configuration dictionary
        """
        self.config = config or {}
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key to retrieve
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)
        
    def set(self, key: str, value: Any) -> None:
        """Set configuration value.
        
        Args:
            key: Configuration key to set
            value: Value to set
        """
        self.config[key] = value
        
    def is_valid(self) -> bool:
        """Check if current configuration is valid.
        
        Returns:
            True if configuration is valid
        """
        return validate_config(self.config)
''')
    
    # Create tests directory
    tests_dir = project_dir / "tests"
    tests_dir.mkdir()
    (tests_dir / "__init__.py").write_text("")
    
    # Add test file
    (tests_dir / "test_core.py").write_text('''"""Tests for core module."""

import pytest
from test_package.core import TestCore


def test_core_creation():
    """Test TestCore can be created."""
    core = TestCore("test")
    assert core.name == "test"
    assert core.value is None


def test_core_with_value():
    """Test TestCore with initial value."""
    core = TestCore("test", 42)
    assert core.value == 42


def test_process():
    """Test process method."""
    core = TestCore("test")
    result = core.process("hello")
    assert result == "test: Processed hello"


def test_calculate():
    """Test calculate method."""
    core = TestCore("test")
    result = core.calculate(5, 3)
    assert result == 8


def test_calculate_with_value():
    """Test calculate with instance value."""
    core = TestCore("test", 10)
    result = core.calculate(5, 3)
    assert result == 18


def test_empty_name_raises():
    """Test that empty name raises ValueError."""
    with pytest.raises(ValueError, match="Name cannot be empty"):
        TestCore("")
''')
    
    # Create pyproject.toml
    (project_dir / "pyproject.toml").write_text('''[tool.poetry]
name = "test-package"
version = "1.0.0"
description = "A test package for Pydvlppy"
authors = ["Test Author <test@example.com>"]
packages = [{include = "test_package", from = "src"}]

[tool.poetry.dependencies]
python = "^3.12"

[tool.poetry.group.test.dependencies]
pytest = "^8.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
''')
    
    # Create README
    (project_dir / "README.md").write_text('''# Test Package

A test package for Pydvlppy validation.

## Installation

```bash
pip install test-package
```

## Usage

```python
from test_package import TestCore

core = TestCore("my-test")
result = core.process("data")
print(result)
```
''')
    
    return project_dir


@pytest.fixture
def flat_package_structure(temp_project_dir):
    """Create a sample flat package structure for testing."""
    project_dir = temp_project_dir / "flat-project"
    project_dir.mkdir()
    
    # Create package directory directly in project root
    pkg_dir = project_dir / "flat_project"
    pkg_dir.mkdir()
    
    # Add __init__.py
    (pkg_dir / "__init__.py").write_text('''"""Flat project package."""
__version__ = "1.0.0"
''')
    
    # Add module
    (pkg_dir / "main.py").write_text('''"""Main module for flat project."""

def hello_world() -> str:
    """Return hello world message.
    
    Returns:
        A friendly greeting message
    """
    return "Hello, World!"


def add_numbers(a: int, b: int) -> int:
    """Add two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of the two numbers
    """
    return a + b
''')
    
    # Create pyproject.toml
    (project_dir / "pyproject.toml").write_text('''[tool.poetry]
name = "flat-project"
version = "1.0.0"
description = "A flat project structure for testing"
authors = ["Test Author <test@example.com>"]

[tool.poetry.dependencies]
python = "^3.12"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
''')
    
    return project_dir