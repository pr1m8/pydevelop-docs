"""
Template manager for generating documentation content.

Handles rendering of Jinja2 templates for documentation sections.
"""

from pathlib import Path
from typing import Any, Dict, Optional

from jinja2 import Environment, FileSystemLoader, Template


class TemplateManager:
    """Manages documentation templates and rendering."""

    def __init__(self, project_path: Path, project_info: Dict[str, Any]):
        """Initialize template manager.

        Args:
            project_path: Root path of the project
            project_info: Project metadata (name, structure, etc.)
        """
        self.project_path = project_path
        self.project_info = project_info
        self.template_dir = Path(__file__).parent / "templates" / "doc_templates"

        # Set up Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Common context for all templates
        self.base_context = {
            "project_name": project_info.get("name", "Project"),
            "package_name": self._get_package_name(),
            "github_org": self._extract_github_org(),
            "github_repo": project_info.get("name", "repo"),
        }

    def _get_package_name(self) -> str:
        """Get the package name for pip install."""
        name = self.project_info.get("name", "project")
        return name.lower().replace(" ", "-")

    def _extract_github_org(self) -> str:
        """Extract GitHub organization from git remote or use default."""
        # TODO: Implement git remote parsing
        return "your-org"

    def render_template(
        self, template_name: str, context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Render a template with the given context.

        Args:
            template_name: Name of the template file
            context: Additional context to merge with base context

        Returns:
            Rendered template content
        """
        template = self.env.get_template(template_name)
        full_context = {**self.base_context, **(context or {})}
        return template.render(**full_context)

    def write_template(
        self,
        template_name: str,
        output_path: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Render and write a template to a file.

        Args:
            template_name: Name of the template file
            output_path: Relative path from project root for output
            context: Additional context to merge with base context
        """
        content = self.render_template(template_name, context)

        output_file = self.project_path / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(content)

    def create_section_index(self, section_type: str, output_dir: str) -> None:
        """Create an index.rst for a documentation section.

        Args:
            section_type: Type of section ('guides', 'examples', 'tutorials', 'cli')
            output_dir: Directory path relative to project root
        """
        section_configs = {
            "guides": {
                "title": "User Guides",
                "name": "guides",
                "has_quickstart": True,
            },
            "examples": {
                "title": "Examples",
                "name": "examples",
            },
            "tutorials": {
                "title": "Tutorials",
                "name": "tutorials",
            },
            "cli": {
                "title": "CLI Reference",
                "name": "CLI reference",
            },
        }

        config = section_configs.get(section_type, {})
        context = {
            "section_title": config.get("title", section_type.title()),
            "section_name": config.get("name", section_type),
            "section_type": section_type,
            "has_quickstart": config.get("has_quickstart", False),
        }

        self.write_template(
            "section_index.rst.jinja2", f"{output_dir}/index.rst", context
        )

    def create_quickstart(
        self, output_path: str = "docs/source/guides/quickstart.rst"
    ) -> None:
        """Create a quickstart guide.

        Args:
            output_path: Path for the quickstart file
        """
        self.write_template("quickstart.rst.jinja2", output_path)

    def create_installation(
        self, output_path: str = "docs/source/guides/installation.rst"
    ) -> None:
        """Create an installation guide.

        Args:
            output_path: Path for the installation file
        """
        self.write_template("installation.rst.jinja2", output_path)

    def create_configuration(
        self, output_path: str = "docs/source/guides/configuration.rst"
    ) -> None:
        """Create a configuration guide.

        Args:
            output_path: Path for the configuration file
        """
        self.write_template("configuration.rst.jinja2", output_path)

    def create_all_sections(self, doc_config: Dict[str, bool]) -> None:
        """Create all enabled documentation sections.

        Args:
            doc_config: Configuration dict with section flags
        """
        if doc_config.get("with_guides", False):
            self.create_section_index("guides", "docs/source/guides")
            self.create_quickstart()
            self.create_installation()
            self.create_configuration()

        if doc_config.get("with_examples", False):
            self.create_section_index("examples", "docs/source/examples")

        if doc_config.get("with_cli", False):
            self.create_section_index("cli", "docs/source/cli")

        if doc_config.get("with_tutorials", False):
            self.create_section_index("tutorials", "docs/source/tutorials")
