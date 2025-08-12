"""Enhanced CLI display utilities for pydevelop-docs."""

from typing import Any, Dict, List

import click


class EnhancedDisplay:
    """Enhanced display manager for CLI output."""

    def __init__(self, quiet: bool = False, debug: bool = False):
        self.quiet = quiet
        self.debug = debug

    def show_analysis(self, analysis: Dict[str, Any]) -> None:
        """Display detailed project analysis."""
        if self.quiet:
            return

        click.echo(f"🔍 Analyzing project at {analysis.get('path', 'unknown')}...")
        click.echo(f"📦 Project: {analysis['name']} ({analysis['type']})")
        click.echo(f"🔧 Package Manager: {analysis['package_manager']}")
        click.echo()

        # Show package detection
        if analysis["type"] == "monorepo":
            self._show_package_details(analysis)
            click.echo()

        # Show central hub status
        self._show_central_hub(analysis["central_hub"])
        click.echo()

        # Show dependency issues
        self._show_dependency_analysis(analysis["dependencies"])

    def _show_package_details(self, analysis: Dict[str, Any]) -> None:
        """Display detailed package analysis."""
        click.echo("📋 Detected Packages:")

        for pkg_name in analysis["packages"]:
            details = analysis["package_details"][pkg_name]

            # Status indicators
            src_status = "✅" if details["src_exists"] else "❌"
            docs_status = self._get_docs_status(details)
            config_status = "✅" if details["pyproject_exists"] else "❌"

            # Shared config indicator
            shared_indicator = (
                " (shared)" if details["uses_shared_config"] else " (embedded)"
            )

            click.echo(
                f"   {self._get_package_status(details)} {pkg_name:<15} │ "
                f"src: {src_status} │ docs: {docs_status} │ "
                f"pyproject.toml: {config_status}{shared_indicator}"
            )

    def _get_package_status(self, details: Dict[str, Any]) -> str:
        """Get overall package status indicator."""
        if (
            details["src_exists"]
            and details["docs_exists"]
            and details["conf_py_exists"]
            and details["uses_shared_config"]
        ):
            return "✅"
        elif details["src_exists"] and details["docs_exists"]:
            return "⚠️ "
        else:
            return "❌"

    def _get_docs_status(self, details: Dict[str, Any]) -> str:
        """Get detailed docs status."""
        if not details["docs_exists"]:
            return "❌"
        elif not details["conf_py_exists"]:
            return "⚠️ (no conf.py)"
        elif not details["changelog_exists"]:
            return "⚠️ (no changelog)"
        elif not details["uses_shared_config"]:
            return "⚠️ (embedded config)"
        else:
            return "✅"

    def _show_central_hub(self, hub_info: Dict[str, Any]) -> None:
        """Display central hub status."""
        status = "✅ exists" if hub_info["exists"] else "❌ missing"
        collections = (
            " (collections: ✅)"
            if hub_info.get("collections_configured")
            else " (collections: ❌)"
        )

        click.echo(
            f"🏗️  Central Hub: /docs ({status}{collections if hub_info['exists'] else ''})"
        )

    def _show_dependency_analysis(self, deps: Dict[str, Any]) -> None:
        """Display dependency analysis results."""
        if deps["valid"]:
            click.echo("✅ Dependencies: All valid")
        else:
            click.echo("⚠️  Dependency Issues Found:")
            for issue in deps["issues"]:
                click.echo(f"      - {issue}")

            if not self.quiet:
                click.echo()
                click.echo("🔧 Auto-fixes available:")
                for i, issue in enumerate(deps["issues"], 1):
                    if "Duplicate dependency" in issue:
                        click.echo(f"   [{i}] Remove duplicate entry")
                    elif "TOML parse error" in issue:
                        click.echo(f"   [{i}] Fix TOML syntax")

    def show_processing(self, packages: List[str]) -> None:
        """Display package processing status."""
        if self.quiet:
            return

        click.echo("📦 Processing Packages:")
        for pkg in packages:
            click.echo(
                f"   🔨 {pkg:<15} │ conf.py: ... │ changelog.rst: ... │ index.rst: ..."
            )

    def update_package_status(self, pkg_name: str, status: Dict[str, str]) -> None:
        """Update package processing status."""
        if self.quiet:
            return

        conf_status = status.get("conf_py", "...")
        changelog_status = status.get("changelog", "...")
        index_status = status.get("index", "...")

        # Use ANSI escape codes to update the line
        click.echo(
            f"\r   🔨 {pkg_name:<15} │ conf.py: {conf_status} │ "
            f"changelog.rst: {changelog_status} │ index.rst: {index_status}",
            nl=False,
        )

    def show_summary(self, summary: Dict[str, Any]) -> None:
        """Display final summary."""
        if self.quiet:
            return

        click.echo("\n✅ Documentation initialized successfully!")
        click.echo()
        click.echo("📊 Summary:")
        click.echo(f"   - {summary.get('packages_configured', 0)} packages configured")
        click.echo(
            f"   - {summary.get('packages_created', 0)} packages had docs created"
        )
        click.echo(
            f"   - {summary.get('packages_updated', 0)} packages had docs updated"
        )
        click.echo(f"   - {summary.get('central_hub_status', 'unknown')} central hub")
        click.echo(
            f"   - {summary.get('conflicts_resolved', 0)} dependency conflicts resolved"
        )

        click.echo()
        click.echo("📚 Next steps:")
        click.echo("   1. poetry lock && poetry install --with docs")
        click.echo("   2. poetry run pydevelop-docs build-all --clean")
        click.echo("   3. open docs/build/html/index.html")

    def show_fixes_prompt(self, fixes: List[str]) -> bool:
        """Show available fixes and prompt for confirmation."""
        if self.quiet:
            return True

        if not fixes:
            return True

        click.echo("🔧 Auto-fixes available:")
        for i, fix in enumerate(fixes, 1):
            click.echo(f"   [{i}] {fix}")

        return click.confirm("\nApply fixes?", default=True)

    def debug(self, message: str) -> None:
        """Show debug message if debug mode is enabled."""
        if self.debug:
            click.echo(f"🐛 DEBUG: {message}", err=True)

    def error(self, message: str) -> None:
        """Show error message."""
        click.echo(f"❌ ERROR: {message}", err=True)

    def success(self, message: str) -> None:
        """Show success message."""
        if not self.quiet:
            click.echo(f"✅ {message}")

    def warning(self, message: str) -> None:
        """Show warning message."""
        if not self.quiet:
            click.echo(f"⚠️  {message}")
