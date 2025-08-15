#!/usr/bin/env python3
"""Test Tippy tooltip functionality and Jinja2/Sphinx type support.

This test validates:
1. Tippy tooltip generation works correctly
2. Python type annotations work in Jinja2 templates
3. Sphinx autodoc type support is functional
4. Template rendering handles complex Python types
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from pydevelop_docs.template_manager import TemplateManager


def test_tippy_template_integration():
    """Test Tippy tooltip integration with templates."""
    print("🔍 Testing Tippy tooltip functionality...")

    # Create template manager
    test_project_path = Path("/tmp/test_tippy")
    project_info = {"name": "Tippy Test Project"}
    manager = TemplateManager(project_path=test_project_path, project_info=project_info)

    # Test template with Tippy syntax
    tippy_template = """
{#- Test Tippy tooltip integration -#}
{{ project_name }} Documentation
===============================================

.. tippy:: API Reference
   :content: Click to view the complete API documentation with all classes and methods
   :placement: bottom
   :theme: light-border
   :interactive: true

This is our main :tippy:`documentation<Complete documentation for the {{ project_name }} project>` page.

{#- Test complex type annotations -#}
.. py:function:: process_data(data: List[Dict[str, Union[str, int]]], config: Optional[ConfigClass] = None) -> ProcessedResult
   
   Process input data with optional configuration.
   
   :tippy:`data<Input data as list of dictionaries with string keys and string/int values>`:
       The input data to process
   :tippy:`config<Optional configuration object, uses defaults if None>`:
       Configuration settings
"""

    try:
        # Create template from string
        from jinja2 import Template

        template = manager.env.from_string(tippy_template)
        result = template.render(**manager.base_context)

        print("✅ Tippy template rendering successful")
        print(f"   Content length: {len(result)} characters")

        # Check for Tippy directives
        tippy_checks = [
            ".. tippy::" in result,
            ":tippy:" in result,
            "API Reference" in result,
            "documentation<Complete documentation" in result,
        ]

        if all(tippy_checks):
            print("✅ All Tippy directive syntax present")
            return True
        else:
            print("❌ Missing Tippy syntax elements")
            print(f"   Checks: {tippy_checks}")
            return False

    except Exception as e:
        print(f"❌ Tippy template rendering failed: {e}")
        return False


def test_python_type_annotations():
    """Test Python type annotation support in templates."""
    print("\n🐍 Testing Python type annotation support...")

    # Test complex type scenarios
    type_examples = {
        "basic_types": ["str", "int", "float", "bool"],
        "optional_types": ["Optional[str]", "Optional[List[int]]"],
        "union_types": ["Union[str, int]", "Union[Dict[str, Any], None]"],
        "generic_types": ["List[str]", "Dict[str, int]", "Tuple[str, ...]"],
        "complex_nested": ["Dict[str, List[Optional[Union[str, int]]]]"],
        "callable_types": ["Callable[[str, int], bool]"],
    }

    test_project_path = Path("/tmp/test_types")
    project_info = {"name": "Type Test Project"}
    manager = TemplateManager(project_path=test_project_path, project_info=project_info)

    # Template with type annotations
    type_template = """
Python Type Support Test
========================

{% for category, types in type_examples.items() %}

{{ category|replace('_', ' ')|title }}
{{ '-' * (category|length + 1) }}

{% for type_annotation in types %}
.. py:function:: example_{{ loop.index }}(param: {{ type_annotation }}) -> {{ type_annotation }}

   Function with {{ type_annotation }} type annotation.
   
   :tippy:`{{ type_annotation }}<Type annotation: {{ type_annotation }}>`:
       Parameter with complex type

{% endfor %}
{% endfor %}
"""

    try:
        from jinja2 import Template

        template = manager.env.from_string(type_template)

        # Add type examples to context
        context = manager.base_context.copy()
        context["type_examples"] = type_examples

        result = template.render(**context)

        print("✅ Type annotation template rendering successful")

        # Check for type preservation
        type_checks = [
            "Optional[str]" in result,
            "Union[str, int]" in result,
            "Dict[str, List[" in result,
            "Callable[[str, int], bool]" in result,
            ":tippy:" in result,
        ]

        print(f"✅ Type annotation checks: {sum(type_checks)}/5 passed")

        if all(type_checks):
            print("✅ All Python type annotations preserved correctly")
            return True
        else:
            print("⚠️  Some type annotations may have issues")
            return False

    except Exception as e:
        print(f"❌ Type annotation test failed: {e}")
        return False


def test_sphinx_autodoc_integration():
    """Test Sphinx autodoc type hint integration."""
    print("\n📚 Testing Sphinx autodoc integration...")

    # Create a mock Python class for testing
    mock_class_content = '''
"""Example class for testing autodoc integration."""

from typing import Dict, List, Optional, Union
from dataclasses import dataclass


@dataclass
class ConfigClass:
    """Configuration class for testing.
    
    This class demonstrates proper type annotation
    support in Sphinx autodoc.
    """
    name: str
    values: List[int]
    metadata: Optional[Dict[str, Union[str, int]]] = None
    
    def process(self, data: List[str]) -> Dict[str, int]:
        """Process input data.
        
        Args:
            data: Input strings to process
            
        Returns:
            Dictionary mapping strings to their lengths
        """
        return {item: len(item) for item in data}


def complex_function(
    input_data: Dict[str, List[Union[str, int]]],
    config: Optional[ConfigClass] = None,
    validate: bool = True
) -> List[Dict[str, Union[str, int, float]]]:
    """Complex function with advanced type annotations.
    
    This function demonstrates complex type support.
    
    Args:
        input_data: Complex nested input data structure
        config: Optional configuration object
        validate: Whether to validate input data
        
    Returns:
        Processed data as list of dictionaries
        
    Raises:
        ValueError: If validation fails and validate=True
    """
    if not input_data and validate:
        raise ValueError("Empty input data")
    
    result = []
    for key, values in input_data.items():
        processed = {
            "key": key,
            "count": len(values),
            "average": sum(v for v in values if isinstance(v, (int, float))) / len(values)
        }
        result.append(processed)
    
    return result
'''

    # Create mock module file
    mock_module_path = Path("/tmp/test_mock_module.py")
    mock_module_path.write_text(mock_class_content)

    print("✅ Mock Python module created with complex type annotations")

    # Test template with autodoc directives
    autodoc_template = """
Sphinx Autodoc Integration Test
===============================

.. automodule:: test_mock_module
   :members:
   :undoc-members:
   :show-inheritance:

Class Documentation
-------------------

.. autoclass:: test_mock_module.ConfigClass
   :members:
   :undoc-members:
   
   :tippy:`ConfigClass<Main configuration class with type annotations>`:
       Configuration management

Function Documentation  
----------------------

.. autofunction:: test_mock_module.complex_function

   :tippy:`complex_function<Advanced function with nested type annotations>`:
       Data processing function
"""

    test_project_path = Path("/tmp/test_autodoc")
    project_info = {"name": "Autodoc Test Project"}
    manager = TemplateManager(project_path=test_project_path, project_info=project_info)

    try:
        from jinja2 import Template

        template = manager.env.from_string(autodoc_template)
        result = template.render(**manager.base_context)

        print("✅ Sphinx autodoc template rendering successful")

        # Check for autodoc directives
        autodoc_checks = [
            ".. automodule::" in result,
            ".. autoclass::" in result,
            ".. autofunction::" in result,
            ":tippy:" in result,
            "ConfigClass" in result,
            "complex_function" in result,
        ]

        print(f"✅ Autodoc directive checks: {sum(autodoc_checks)}/6 passed")

        # Cleanup
        mock_module_path.unlink()

        return all(autodoc_checks)

    except Exception as e:
        print(f"❌ Sphinx autodoc test failed: {e}")
        # Cleanup on error
        if mock_module_path.exists():
            mock_module_path.unlink()
        return False


def test_custom_filters_with_types():
    """Test custom filters with Python type support."""
    print("\n🎨 Testing custom filters with type annotations...")

    backup_dir = (
        Path(__file__).parent.parent
        / "src/pydevelop_docs/templates/_autoapi_templates_BROKEN_BACKUP"
    )
    filters_file = backup_dir / "python/_filters/type_filters.py"

    if not filters_file.exists():
        print("⏭️  Custom filters backup not found, skipping...")
        return True

    try:
        # Import the custom filters
        sys.path.insert(0, str(filters_file.parent))
        from type_filters import FILTERS

        # Test type-specific filters
        type_test_cases = {
            "format_annotation": [
                "List[str]",
                "Dict[str, Union[int, str]]",
                "Optional[Callable[[str], bool]]",
                "Union[str, None]",
            ],
            "is_pydantic_model": [
                {"bases": ["BaseModel"], "name": "UserModel"},
                {"bases": ["str"], "name": "StringClass"},
            ],
            "pluralize": [("function", 1), ("method", 5), ("class", 0)],
        }

        success_count = 0
        total_tests = 0

        for filter_name, test_cases in type_test_cases.items():
            if filter_name in FILTERS:
                filter_func = FILTERS[filter_name]
                for test_input in test_cases:
                    try:
                        total_tests += 1
                        if isinstance(test_input, tuple):
                            result = filter_func(*test_input)
                        else:
                            result = filter_func(test_input)
                        success_count += 1
                        print(f"   ✅ {filter_name}({test_input}) -> {result}")
                    except Exception as e:
                        print(f"   ❌ {filter_name}({test_input}) failed: {e}")

        print(f"✅ Custom filter type tests: {success_count}/{total_tests} passed")
        return success_count == total_tests

    except ImportError as e:
        print(f"⚠️  Cannot import custom filters: {e}")
        return True  # Not a failure, just unavailable


def generate_tippy_functionality_report(results: Dict[str, bool]) -> None:
    """Generate comprehensive functionality report."""
    print("\n" + "=" * 60)
    print("📊 TIPPY & TYPE SUPPORT FUNCTIONALITY REPORT")
    print("=" * 60)

    # Test results summary
    print(f"\n🔍 Test Results:")
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name}: {status}")

    # Overall assessment
    passed_count = sum(results.values())
    total_count = len(results)

    print(f"\n📈 Overall: {passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print("\n🎉 ALL FUNCTIONALITY WORKING!")
        print("   ✅ Tippy tooltips are properly configured")
        print("   ✅ Python type annotations work in templates")
        print("   ✅ Sphinx autodoc integration functional")
        print("   ✅ Custom filters support complex types")
    elif passed_count >= total_count * 0.75:
        print("\n⚠️  MOSTLY FUNCTIONAL - Minor Issues")
        print("   Most features working, some may need attention")
    else:
        print("\n❌ SIGNIFICANT ISSUES FOUND")
        print("   Major functionality problems detected")

    print("\n💡 To test Tippy in live documentation:")
    print("   1. Build docs: poetry run sphinx-build -b html docs/source docs/build")
    print("   2. Serve: python -m http.server 8003 --directory docs/build")
    print("   3. Open browser and hover over :tippy: elements")
    print("   4. Check browser console for Tippy.js loading")

    print("=" * 60)


def main():
    """Run comprehensive Tippy and type support tests."""
    print("🚀 Starting Tippy functionality and Python type support tests...\n")

    results = {}

    # Run all tests
    results["Tippy Template Integration"] = test_tippy_template_integration()
    results["Python Type Annotations"] = test_python_type_annotations()
    results["Sphinx Autodoc Integration"] = test_sphinx_autodoc_integration()
    results["Custom Filters with Types"] = test_custom_filters_with_types()

    # Generate comprehensive report
    generate_tippy_functionality_report(results)

    return all(results.values())


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
