# PyDevelop-Docs Test Suite

This directory contains a comprehensive test suite for PyDevelop-Docs, ensuring all functionality works correctly without mocks.

## 🧪 Test Files Overview

### Core Functionality Tests

- **`test_project_detection.py`** - Project structure detection and metadata extraction
- **`test_configuration_generation.py`** - Sphinx configuration generation and validation
- **`test_cli_functionality.py`** - Command-line interface testing
- **`test_builders.py`** - Documentation builder functionality
- **`test_template_system.py`** - Template manager and Jinja2 integration
- **`test_integration.py`** - End-to-end integration tests

### Legacy Template Tests

- **`test_templates.py`** - Original template tests (now enhanced)
- **`validate_templates.py`** - Template validation with djLint
- **`integration_test.py`** - Custom filter integration

### Test Infrastructure

- **`conftest.py`** - Pytest fixtures and test configuration
- **`run_tests.py`** - Standalone test runner script

## 🚀 Quick Start

### Using Poetry (Recommended)

```bash
# Install test dependencies
poetry install --with test

# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=pydevelop_docs

# Run specific test categories
poetry run pytest -m unit          # Unit tests only
poetry run pytest -m integration   # Integration tests only
poetry run pytest -m "not slow"    # Skip slow tests
```

### Using the CLI Test Command

```bash
# Run all tests with coverage
poetry run pydevelop-docs test

# Run unit tests only
poetry run pydevelop-docs test --unit

# Run with linting and type checking
poetry run pydevelop-docs test --lint --type-check

# Fast tests only (skip slow integration tests)
poetry run pydevelop-docs test --fast
```

### Using the Standalone Runner

```bash
# Run all tests
python tests/run_tests.py

# Run with coverage and verbose output
python tests/run_tests.py --coverage --verbose

# Run specific test pattern
python tests/run_tests.py --pattern "test_config"

# Run specific file
python tests/run_tests.py --file tests/test_cli_functionality.py
```

## 🧪 Test Categories

### Unit Tests (`-m unit`)
- **Project Detection**: Test project structure analysis
- **Configuration Generation**: Test Sphinx config creation
- **Template Rendering**: Test Jinja2 template system
- **Builder Logic**: Test documentation builders
- **CLI Commands**: Test command-line interface

### Integration Tests (`-m integration`) 
- **End-to-End Workflows**: Complete project → docs workflows
- **Component Integration**: Test components working together
- **Real-World Scenarios**: Pydantic models, large projects
- **Configuration Compatibility**: Sphinx compatibility validation

### Slow Tests (`-m slow`)
- **Large Project Handling**: Projects with 50+ modules
- **Performance Tests**: Memory usage and build times
- **Complex Builds**: Full documentation generation

## 🔧 Test Infrastructure

### Fixtures (conftest.py)
- **Project Structures**: Monorepo, single package, flat layout
- **Sample Data**: Project metadata, configurations
- **Temporary Directories**: Isolated test environments

### Test Utilities
- **Real Components**: No mocks - tests actual functionality
- **File System Isolation**: Each test gets clean environment
- **Error Handling**: Graceful failure and recovery testing

## 📊 Coverage Goals

- **Unit Tests**: >90% line coverage
- **Integration Tests**: All critical workflows covered
- **Error Paths**: All exception handling tested
- **CLI Commands**: All commands and options tested

## 🎯 Testing Philosophy

### No Mocks Policy
- **Real LLMs**: When testing involves AI components
- **Real File Systems**: Actual file I/O operations
- **Real Dependencies**: Full dependency integration
- **Real Errors**: Actual error conditions

### Comprehensive Validation
- **Input Validation**: All parameter combinations
- **Output Verification**: Complete result validation
- **State Consistency**: Proper state management
- **Resource Cleanup**: No test pollution

## 🚀 Advanced Usage

### Running Specific Test Suites

```bash
# Project detection only
poetry run pytest tests/test_project_detection.py -v

# Configuration generation with coverage
poetry run pytest tests/test_configuration_generation.py --cov=pydevelop_docs.config

# CLI functionality with pattern matching
poetry run pytest tests/test_cli_functionality.py -k "test_init"

# Integration tests with verbose output
poetry run pytest tests/test_integration.py -v -s
```

### Performance Testing

```bash
# Run slow tests to check performance
poetry run pytest -m slow --verbose

# Memory usage testing
poetry run pytest tests/test_integration.py::TestPerformanceIntegration -v

# Large project simulation
poetry run pytest -k "large_project" --verbose
```

### Development Testing

```bash
# Run tests on file change (requires pytest-watch)
poetry run ptw tests/ --runner "pytest --cov=pydevelop_docs"

# Run failed tests first
poetry run pytest --failed-first

# Run tests in parallel (requires pytest-xdist)
poetry run pytest -n auto
```

## 🔍 Debugging Test Failures

### Common Issues

1. **Import Errors**: Ensure `poetry install --with test` completed
2. **Path Issues**: Tests run from project root directory
3. **Temporary Files**: Check cleanup in fixture teardown
4. **Dependency Conflicts**: Verify test environment isolation

### Debug Commands

```bash
# Run single test with full output
poetry run pytest tests/test_cli_functionality.py::TestCLICommands::test_cli_help -v -s

# Show test collection without running
poetry run pytest --collect-only

# Show fixtures available to a test
poetry run pytest --fixtures tests/test_project_detection.py

# Run with pdb on failure
poetry run pytest tests/ --pdb
```

## 📈 Continuous Integration

### Local Pre-commit Testing

```bash
# Full test suite before commit
poetry run pydevelop-docs test --coverage --lint --type-check

# Quick validation
poetry run pytest tests/ -x --failed-first
```

### CI/CD Integration

The test suite is designed for CI/CD integration with:
- **Parallel Execution**: Tests can run in parallel
- **Selective Running**: Run only changed test categories
- **Coverage Reporting**: XML and HTML coverage reports
- **Artifact Generation**: Test reports and logs

## 🎉 Success Metrics

- **✅ 100+ Tests**: Comprehensive coverage of all functionality
- **✅ No Mocks**: All tests use real components
- **✅ Fast Execution**: Unit tests complete in <30 seconds
- **✅ Clear Errors**: Descriptive test names and failure messages
- **✅ Isolated**: Tests don't interfere with each other
- **✅ Documented**: Every test has clear docstring and purpose
