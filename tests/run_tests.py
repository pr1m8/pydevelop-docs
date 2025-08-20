#!/usr/bin/env python3
"""Test runner script for PyDevelop-Docs.

This script provides a convenient way to run tests with various options,
matching the CLI test command functionality.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description, verbose=False):
    """Run a command and handle output."""
    if verbose:
        print(f"\n🔄 {description}")
        print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=not verbose,
            text=True,
            check=True
        )
        
        if verbose and result.stdout:
            print(result.stdout)
            
        print(f"✅ {description} - PASSED")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        if e.stdout:
            print(f"STDOUT:\n{e.stdout}")
        if e.stderr:
            print(f"STDERR:\n{e.stderr}")
        return False


def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(
        description="Run PyDevelop-Docs tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Run all tests
  %(prog)s --unit             # Run only unit tests
  %(prog)s --integration      # Run only integration tests
  %(prog)s --coverage         # Run with coverage
  %(prog)s --fast             # Skip slow tests
  %(prog)s --lint             # Run linting only
  %(prog)s --verbose          # Verbose output
        """
    )
    
    # Test type selection
    parser.add_argument(
        "--unit", 
        action="store_true",
        help="Run unit tests only"
    )
    parser.add_argument(
        "--integration",
        action="store_true", 
        help="Run integration tests only"
    )
    parser.add_argument(
        "--slow",
        action="store_true",
        help="Include slow tests"
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Skip slow tests (default)"
    )
    
    # Coverage options
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Run with coverage reporting"
    )
    parser.add_argument(
        "--no-cov", 
        action="store_true",
        help="Disable coverage"
    )
    
    # Quality checks
    parser.add_argument(
        "--lint",
        action="store_true",
        help="Run linting checks"
    )
    parser.add_argument(
        "--format-check",
        action="store_true", 
        help="Check code formatting"
    )
    parser.add_argument(
        "--type-check",
        action="store_true",
        help="Run type checking"
    )
    
    # Output options
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Quiet output"
    )
    parser.add_argument(
        "--failed-first",
        action="store_true",
        help="Run failed tests first"
    )
    
    # Test selection
    parser.add_argument(
        "--pattern", "-k",
        help="Run tests matching pattern"
    )
    parser.add_argument(
        "--file",
        help="Run specific test file"
    )
    
    args = parser.parse_args()
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root / "src"))
    
    # Default to fast tests unless slow is explicitly requested
    if not args.slow:
        args.fast = True
    
    success = True
    
    print("🧪 PyDevelop-Docs Test Suite")
    print("=" * 50)
    
    # Run linting if requested
    if args.lint or (not args.unit and not args.integration and not args.file):
        lint_cmd = ["ruff", "check", "src", "tests"]
        if not run_command(lint_cmd, "Code linting", args.verbose):
            success = False
    
    # Run format checking if requested
    if args.format_check:
        format_cmd = ["ruff", "format", "--check", "src", "tests"]
        if not run_command(format_cmd, "Format checking", args.verbose):
            success = False
    
    # Run type checking if requested
    if args.type_check:
        type_cmd = ["mypy", "src"]
        if not run_command(type_cmd, "Type checking", args.verbose):
            success = False
    
    # Build pytest command
    pytest_cmd = ["python", "-m", "pytest"]
    
    # Add coverage if requested and not disabled
    if args.coverage or (not args.no_cov and not args.lint and not args.format_check):
        pytest_cmd.extend([
            "--cov=pydevelop_docs",
            "--cov-report=term-missing",
            "--cov-report=html"
        ])
    
    # Add verbosity
    if args.verbose:
        pytest_cmd.append("-v")
    elif args.quiet:
        pytest_cmd.append("-q")
    
    # Add failed first
    if args.failed_first:
        pytest_cmd.append("--failed-first")
    
    # Add test selection
    if args.unit:
        pytest_cmd.extend(["-m", "unit"])
    elif args.integration:
        pytest_cmd.extend(["-m", "integration"])
    
    # Add speed selection
    if args.fast:
        pytest_cmd.extend(["-m", "not slow"])
    elif args.slow:
        pytest_cmd.extend(["-m", "slow"])
    
    # Add pattern matching
    if args.pattern:
        pytest_cmd.extend(["-k", args.pattern])
    
    # Add specific file
    if args.file:
        pytest_cmd.append(args.file)
    else:
        pytest_cmd.append("tests/")
    
    # Run pytest unless only linting was requested
    if not (args.lint and not args.unit and not args.integration and not args.file):
        if not run_command(pytest_cmd, "Running tests", args.verbose):
            success = False
    
    # Summary
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed!")
        return 0
    else:
        print("💥 Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())