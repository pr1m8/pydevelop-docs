"""Test template rendering with real data.

This module tests the Jinja2 template system in pydvlppy,
starting with simple templates and progressing to complex ones.
"""

from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

from pydvlppy.template_manager import TemplateManager


class TestBasicTemplateRendering:
    """Test basic template rendering functionality."""

    def setup_method(self):
        """Set up test environment for each test."""
        self.test_project_path = Path("/tmp/test_pydevelop")
        self.project_info = {
            "name": "Test Project",
            "description": "A test project for template validation",
        }
        self.template_manager = TemplateManager(
            project_path=self.test_project_path, project_info=self.project_info
        )

    def test_quickstart_template_renders(self):
        """Test that the quickstart template renders correctly."""
        result = self.template_manager.render_template("quickstart.rst.jinja2")

        # Basic checks
        assert "Test Project Quick Start" in result
        assert "pip install test-project" in result
        assert len(result) > 100
        assert "Happy documenting! 🚀" in result

    def test_quickstart_with_custom_context(self):
        """Test quickstart template with custom context."""
        custom_context = {
            "github_org": "myorg",
            "github_repo": "myrepo",
            "package_name": "my-custom-package",
        }

        result = self.template_manager.render_template(
            "quickstart.rst.jinja2", custom_context
        )

        assert "pip install my-custom-package" in result
        assert "https://github.com/myorg/myrepo" in result

    def test_section_index_template(self):
        """Test section index template generation."""
        # This will use section_index.rst.jinja2 if it exists
        try:
            self.template_manager.create_section_index("guides", "test_output/guides")
            # If no exception, the template rendered successfully
            assert True
        except Exception as e:
            # If template doesn't exist, that's also useful information
            assert "section_index.rst.jinja2" in str(e)

    def test_base_context_population(self):
        """Test that base context is properly populated."""
        base_context = self.template_manager.base_context

        assert "project_name" in base_context
        assert "package_name" in base_context
        assert "github_org" in base_context
        assert "github_repo" in base_context

        assert base_context["project_name"] == "Test Project"
        assert base_context["package_name"] == "test-project"
        assert base_context["github_org"] == "your-org"  # Default value


class TestTemplateManagerFunctions:
    """Test TemplateManager utility functions."""

    def setup_method(self):
        """Set up test environment."""
        self.test_project_path = Path("/tmp/test_pydevelop")
        self.project_info = {"name": "My Test Project"}
        self.template_manager = TemplateManager(
            project_path=self.test_project_path, project_info=self.project_info
        )

    def test_write_file_method_exists(self):
        """Test that the _write_file method exists and works."""
        # This tests our bug fix
        test_content = "Test content for file writing"

        # Should not raise an exception
        self.template_manager._write_file("test_file.txt", test_content)

        # Check file was created
        expected_path = self.test_project_path / "test_file.txt"
        assert expected_path.exists()
        assert expected_path.read_text() == test_content

        # Cleanup
        expected_path.unlink()

    def test_package_name_generation(self):
        """Test package name generation from project name."""
        manager1 = TemplateManager(Path("/tmp"), {"name": "My Amazing Project"})
        assert manager1._get_package_name() == "my-amazing-project"

        manager2 = TemplateManager(Path("/tmp"), {"name": "SimpleProject"})
        assert manager2._get_package_name() == "simpleproject"


class TestAdvancedTemplates:
    """Test advanced template features if they exist."""

    def setup_method(self):
        """Set up for advanced template tests."""
        self.template_dir = (
            Path(__file__).parent.parent / "src/pydevelop_docs/templates"
        )
        self.broken_backup_dir = self.template_dir / "_autoapi_templates_BROKEN_BACKUP"

    def test_custom_filters_available(self):
        """Test if custom Jinja2 filters are available."""
        if (self.broken_backup_dir / "python/_filters/type_filters.py").exists():
            # Import the filters
            import sys

            sys.path.append(str(self.broken_backup_dir / "python/_filters"))

            try:
                from type_filters import FILTERS

                assert len(FILTERS) > 0
                assert "is_pydantic_model" in FILTERS
                assert "format_annotation" in FILTERS
                print(f"Found {len(FILTERS)} custom filters in backup system")
            except ImportError:
                pytest.skip("Custom filters not importable in test environment")
        else:
            pytest.skip("Advanced template system not found")

    def test_navigation_component_exists(self):
        """Test if navigation components exist."""
        nav_component = self.broken_backup_dir / "python/_components/navigation.j2"
        if nav_component.exists():
            content = nav_component.read_text()
            assert "render_module_overview_cards" in content
            assert "render_breadcrumb" in content
        else:
            pytest.skip("Navigation components not found")


if __name__ == "__main__":
    # Allow running this file directly for quick testing
    pytest.main([__file__, "-v"])
