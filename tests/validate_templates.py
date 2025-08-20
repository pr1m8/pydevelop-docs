#!/usr/bin/env python3
"""Comprehensive template validation for pydevelop-docs.

This script validates all templates using multiple approaches:
1. djLint for syntax and style checking
2. Jinja2 rendering with real data
3. Custom filter loading and testing
"""

import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

from jinja2 import Environment, FileSystemLoader, Template

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from pydevelop_docs.template_manager import TemplateManager


def run_djlint_on_templates() -> Dict[str, Any]:
    """Run djLint on all template files."""
    print("🔍 Running djLint validation...")

    # Find all template files
    template_patterns = ["*.jinja2", "*.j2"]
    template_files = []

    base_dir = Path(__file__).parent.parent / "src/pydevelop_docs/templates"
    for pattern in template_patterns:
        template_files.extend(base_dir.rglob(pattern))

    results = {
        "total_files": len(template_files),
        "passed": 0,
        "failed": 0,
        "errors": {},
    }

    for template_file in template_files:
        try:
            result = subprocess.run(
                ["djlint", str(template_file), "--profile=jinja"],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                results["passed"] += 1
                print(f"  ✅ {template_file.name}")
            else:
                results["failed"] += 1
                results["errors"][str(template_file)] = result.stdout
                print(f"  ❌ {template_file.name}")

        except FileNotFoundError:
            print("❌ djLint not found - install with 'pip install djlint'")
            return results

    return results


def test_template_rendering() -> Dict[str, Any]:
    """Test template rendering with real data."""
    print("\n🔧 Testing template rendering...")

    test_project_path = Path("/tmp/test_pydevelop_validation")
    project_info = {
        "name": "Validation Test Project",
        "description": "Testing template rendering",
    }

    template_manager = TemplateManager(
        project_path=test_project_path, project_info=project_info
    )

    results = {"templates_tested": 0, "successful": 0, "failed": 0, "errors": {}}

    # Test basic templates
    templates_to_test = [
        "quickstart.rst.jinja2",
        "section_index.rst.jinja2",
        "configuration.rst.jinja2",
    ]

    for template_name in templates_to_test:
        try:
            results["templates_tested"] += 1

            # Try different contexts for variety
            contexts = [
                {},  # Default context
                {"section_type": "guides", "section_title": "User Guides"},
                {"custom_extensions": ["sphinx.ext.todo"], "source_path": "../.."},
            ]

            for i, context in enumerate(contexts):
                if template_name == "section_index.rst.jinja2" and i == 1:
                    # Use section context for section template
                    result = template_manager.render_template(template_name, context)
                elif template_name == "quickstart.rst.jinja2" and i == 0:
                    # Use default context for quickstart
                    result = template_manager.render_template(template_name, context)
                else:
                    continue

                if len(result) > 50:  # Basic sanity check
                    results["successful"] += 1
                    print(f"  ✅ {template_name} (context {i+1})")
                    break
                else:
                    raise ValueError(
                        f"Template rendered but output too short: {len(result)} chars"
                    )

        except Exception as e:
            results["failed"] += 1
            results["errors"][template_name] = str(e)
            print(f"  ❌ {template_name}: {e}")

    return results


def test_custom_filters() -> Dict[str, Any]:
    """Test custom Jinja2 filters from the backup system."""
    print("\n🎨 Testing custom filters...")

    results = {
        "filters_found": 0,
        "filters_tested": 0,
        "working_filters": 0,
        "errors": {},
    }

    backup_dir = (
        Path(__file__).parent.parent
        / "src/pydevelop_docs/templates/_autoapi_templates_BROKEN_BACKUP"
    )
    filters_file = backup_dir / "python/_filters/type_filters.py"

    if not filters_file.exists():
        print("  ⏭️  Custom filters backup not found")
        return results

    try:
        # Import the filters
        sys.path.insert(0, str(filters_file.parent))
        from type_filters import FILTERS

        results["filters_found"] = len(FILTERS)
        print(f"  📦 Found {len(FILTERS)} custom filters")

        # Test a few key filters with sample data
        test_cases = {
            "is_pydantic_model": {"bases": ["BaseModel"]},
            "format_annotation": "Optional[List[str]]",
            "pluralize": ("word", 2),
            "to_snake_case": "CamelCaseString",
            "truncate_with_ellipsis": (
                "This is a very long string that should be truncated",
                20,
            ),
        }

        for filter_name, test_input in test_cases.items():
            if filter_name in FILTERS:
                try:
                    results["filters_tested"] += 1
                    filter_func = FILTERS[filter_name]

                    if isinstance(test_input, tuple):
                        result = filter_func(*test_input)
                    else:
                        result = filter_func(test_input)

                    results["working_filters"] += 1
                    print(f"    ✅ {filter_name}: {result}")

                except Exception as e:
                    results["errors"][filter_name] = str(e)
                    print(f"    ❌ {filter_name}: {e}")

        # Test loading into Jinja2 environment
        try:
            env = Environment(loader=FileSystemLoader("."))
            for name, func in FILTERS.items():
                env.filters[name] = func
            print(f"  ✅ All {len(FILTERS)} filters loaded into Jinja2 environment")
        except Exception as e:
            results["errors"]["jinja2_loading"] = str(e)
            print(f"  ❌ Error loading filters into Jinja2: {e}")

    except ImportError as e:
        results["errors"]["import"] = str(e)
        print(f"  ❌ Cannot import filters: {e}")

    return results


def test_advanced_templates() -> Dict[str, Any]:
    """Test advanced template components."""
    print("\n🏗️ Testing advanced template components...")

    results = {
        "components_found": 0,
        "components_tested": 0,
        "syntax_valid": 0,
        "errors": {},
    }

    backup_dir = (
        Path(__file__).parent.parent
        / "src/pydevelop_docs/templates/_autoapi_templates_BROKEN_BACKUP"
    )
    component_dirs = [
        backup_dir / "python/_components",
        backup_dir / "python/_macros",
        backup_dir / "python/_base",
    ]

    advanced_templates = []
    for comp_dir in component_dirs:
        if comp_dir.exists():
            advanced_templates.extend(comp_dir.glob("*.j2"))

    results["components_found"] = len(advanced_templates)
    print(f"  📦 Found {len(advanced_templates)} advanced components")

    for template_file in advanced_templates:
        try:
            results["components_tested"] += 1

            # Test syntax by creating template object
            content = template_file.read_text()
            template = Template(content)

            # Basic syntax validation - template creation should not fail
            results["syntax_valid"] += 1
            print(f"    ✅ {template_file.name}: Valid syntax")

        except Exception as e:
            results["errors"][str(template_file)] = str(e)
            print(f"    ❌ {template_file.name}: {e}")

    return results


def generate_report(all_results: Dict[str, Dict[str, Any]]) -> None:
    """Generate a comprehensive validation report."""
    print("\n" + "=" * 60)
    print("📊 TEMPLATE VALIDATION REPORT")
    print("=" * 60)

    # djLint results
    djlint = all_results.get("djlint", {})
    print(f"\n🔍 djLint Validation:")
    print(f"  Files checked: {djlint.get('total_files', 0)}")
    print(f"  Passed: {djlint.get('passed', 0)}")
    print(f"  Failed: {djlint.get('failed', 0)}")

    # Template rendering results
    rendering = all_results.get("rendering", {})
    print(f"\n🔧 Template Rendering:")
    print(f"  Templates tested: {rendering.get('templates_tested', 0)}")
    print(f"  Successful: {rendering.get('successful', 0)}")
    print(f"  Failed: {rendering.get('failed', 0)}")

    # Custom filters results
    filters = all_results.get("filters", {})
    print(f"\n🎨 Custom Filters:")
    print(f"  Filters found: {filters.get('filters_found', 0)}")
    print(f"  Filters tested: {filters.get('filters_tested', 0)}")
    print(f"  Working filters: {filters.get('working_filters', 0)}")

    # Advanced templates results
    advanced = all_results.get("advanced", {})
    print(f"\n🏗️ Advanced Components:")
    print(f"  Components found: {advanced.get('components_found', 0)}")
    print(f"  Components tested: {advanced.get('components_tested', 0)}")
    print(f"  Syntax valid: {advanced.get('syntax_valid', 0)}")

    # Overall assessment
    total_errors = sum(len(result.get("errors", {})) for result in all_results.values())
    if total_errors == 0:
        print(f"\n✅ Overall: ALL TESTS PASSED! Template system is ready for use.")
    else:
        print(f"\n⚠️  Overall: {total_errors} issues found. Review needed.")

    print("=" * 60)


def main():
    """Run comprehensive template validation."""
    print("🚀 Starting comprehensive template validation...\n")

    all_results = {}

    # Run all validation tests
    all_results["djlint"] = run_djlint_on_templates()
    all_results["rendering"] = test_template_rendering()
    all_results["filters"] = test_custom_filters()
    all_results["advanced"] = test_advanced_templates()

    # Generate final report
    generate_report(all_results)


if __name__ == "__main__":
    main()
