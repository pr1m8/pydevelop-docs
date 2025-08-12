#!/usr/bin/env python3
"""Analyze existing Sphinx build logs for patterns and issues."""

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class BuildLogAnalyzer:
    """Analyze Sphinx build logs."""

    def __init__(self, log_file: Path):
        self.log_file = log_file
        self.console = Console()

        # Statistics
        self.stats = {
            "total_lines": 0,
            "warnings": defaultdict(list),
            "errors": defaultdict(list),
            "progress_markers": [],
            "phases": [],
            "import_errors": defaultdict(int),
            "deprecated_packages": defaultdict(int),
            "file_processing": {"total": 0, "last_file": None},
        }

        # Patterns
        self.patterns = {
            "progress": re.compile(
                r"\[AutoAPI\] Reading files\.\.\. \[\s*(\d+)%\] (.+)"
            ),
            "phase": re.compile(
                r"(reading sources|writing output|copying static files|dumping object inventory)\.\.\. \[\s*(\d+)%\]"
            ),
            "warning": re.compile(r"WARNING: (.+)"),
            "error": re.compile(r"ERROR: (.+)"),
            "import_error": re.compile(
                r"Cannot resolve import of (?:unknown module )?(.+?) in (.+)"
            ),
            "deprecated": re.compile(r"(\S+) is deprecated"),
            "extension_load": re.compile(r"loading (.+) extension"),
            "pydantic_warning": re.compile(r"PydanticJsonSchemaWarning: (.+)"),
        }

    def analyze(self) -> Dict:
        """Analyze the log file."""
        if not self.log_file.exists():
            self.console.print(f"❌ Log file not found: {self.log_file}")
            return {}

        with open(self.log_file, "r") as f:
            for line_num, line in enumerate(f, 1):
                self.stats["total_lines"] = line_num
                self._analyze_line(line.strip())

        return self._generate_report()

    def _analyze_line(self, line: str):
        """Analyze a single log line."""
        # Progress tracking
        if match := self.patterns["progress"].search(line):
            percent = int(match.group(1))
            file_path = match.group(2)
            self.stats["progress_markers"].append(percent)
            self.stats["file_processing"]["total"] += 1
            self.stats["file_processing"]["last_file"] = file_path

        # Phase tracking
        elif match := self.patterns["phase"].search(line):
            phase = match.group(1)
            percent = int(match.group(2))
            self.stats["phases"].append((phase, percent))

        # Warning analysis
        elif match := self.patterns["warning"].search(line):
            warning = match.group(1)

            # Categorize warning
            if import_match := self.patterns["import_error"].search(warning):
                module = import_match.group(1)
                location = import_match.group(2)
                self.stats["import_errors"][module] += 1
                self.stats["warnings"]["import_resolution"].append(warning)

            elif dep_match := self.patterns["deprecated"].search(warning):
                package = dep_match.group(1)
                self.stats["deprecated_packages"][package] += 1
                self.stats["warnings"]["deprecation"].append(warning)

            elif pydantic_match := self.patterns["pydantic_warning"].search(line):
                self.stats["warnings"]["pydantic"].append(pydantic_match.group(1))

            else:
                self.stats["warnings"]["general"].append(warning)

        # Error tracking
        elif match := self.patterns["error"].search(line):
            error = match.group(1)
            self.stats["errors"]["build_error"].append(error)

    def _generate_report(self) -> Dict:
        """Generate analysis report."""
        # Calculate progress
        max_progress = (
            max(self.stats["progress_markers"]) if self.stats["progress_markers"] else 0
        )

        # Get top issues
        top_import_errors = sorted(
            self.stats["import_errors"].items(), key=lambda x: x[1], reverse=True
        )[:10]

        report = {
            "summary": {
                "total_lines": self.stats["total_lines"],
                "files_processed": self.stats["file_processing"]["total"],
                "max_progress": max_progress,
                "total_warnings": sum(len(w) for w in self.stats["warnings"].values()),
                "total_errors": sum(len(e) for e in self.stats["errors"].values()),
            },
            "warning_breakdown": {
                cat: len(warns) for cat, warns in self.stats["warnings"].items()
            },
            "top_import_errors": top_import_errors,
            "deprecated_packages": dict(self.stats["deprecated_packages"]),
            "phases_completed": self.stats["phases"],
        }

        return report

    def display_report(self, report: Dict):
        """Display the analysis report."""
        summary = report["summary"]

        # Title
        self.console.print(
            Panel(
                f"[bold cyan]Sphinx Build Log Analysis[/]\n{self.log_file.name}",
                style="bold",
            )
        )

        # Summary table
        summary_table = Table(title="📊 Build Summary", show_header=True)
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="green")

        summary_table.add_row("Total Lines", f"{summary['total_lines']:,}")
        summary_table.add_row("Files Processed", f"{summary['files_processed']:,}")
        summary_table.add_row("Max Progress", f"{summary['max_progress']}%")
        summary_table.add_row("Total Warnings", str(summary["total_warnings"]))
        summary_table.add_row("Total Errors", str(summary["total_errors"]))

        self.console.print(summary_table)

        # Warning breakdown
        if report["warning_breakdown"]:
            warning_table = Table(title="⚠️ Warning Categories", show_header=True)
            warning_table.add_column("Category", style="cyan")
            warning_table.add_column("Count", style="yellow")
            warning_table.add_column("Percentage", style="yellow")

            total_warnings = summary["total_warnings"]
            for cat, count in sorted(
                report["warning_breakdown"].items(), key=lambda x: x[1], reverse=True
            ):
                percentage = (count / total_warnings * 100) if total_warnings > 0 else 0
                warning_table.add_row(
                    cat.replace("_", " ").title(), str(count), f"{percentage:.1f}%"
                )

            self.console.print(warning_table)

        # Top import errors
        if report["top_import_errors"]:
            import_table = Table(
                title="🔗 Top Import Resolution Issues", show_header=True
            )
            import_table.add_column("Module", style="cyan", width=50)
            import_table.add_column("Count", style="red")

            for module, count in report["top_import_errors"]:
                import_table.add_row(module[:50], str(count))

            self.console.print(import_table)

        # Deprecated packages
        if report["deprecated_packages"]:
            dep_table = Table(title="📦 Deprecated Package Warnings", show_header=True)
            dep_table.add_column("Package", style="cyan")
            dep_table.add_column("Warnings", style="yellow")

            for package, count in sorted(
                report["deprecated_packages"].items(), key=lambda x: x[1], reverse=True
            ):
                dep_table.add_row(package, str(count))

            self.console.print(dep_table)

        # Recommendations
        self._print_recommendations(report)

    def _print_recommendations(self, report: Dict):
        """Print recommendations based on analysis."""
        recommendations = []

        # Import errors
        import_error_count = sum(
            count for _, count in report.get("top_import_errors", [])
        )
        if import_error_count > 100:
            recommendations.append(
                "🔗 High number of import errors. Consider:\n"
                "   - Adding missing packages to autoapi_ignore_patterns\n"
                "   - Fixing circular imports\n"
                "   - Using TYPE_CHECKING imports for type annotations"
            )

        # Progress
        if report["summary"]["max_progress"] < 100:
            recommendations.append(
                f"⚠️ Build only reached {report['summary']['max_progress']}% completion.\n"
                "   Check for errors that stopped the build."
            )

        # Deprecated packages
        if report["deprecated_packages"]:
            recommendations.append(
                "📦 Deprecated package warnings detected. Consider:\n"
                "   - Updating to newer package versions\n"
                "   - Replacing deprecated imports"
            )

        if recommendations:
            rec_panel = Panel(
                "\n\n".join(recommendations),
                title="💡 Recommendations",
                border_style="blue",
            )
            self.console.print(rec_panel)


@click.command()
@click.argument("log_file", type=click.Path(exists=True, path_type=Path))
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.option("--save", type=click.Path(path_type=Path), help="Save report to file")
def main(log_file: Path, output_json: bool, save: Path):
    """Analyze Sphinx build log files."""
    analyzer = BuildLogAnalyzer(log_file)
    report = analyzer.analyze()

    if output_json:
        print(json.dumps(report, indent=2))
    else:
        analyzer.display_report(report)

    if save:
        with open(save, "w") as f:
            json.dump(report, f, indent=2)
        analyzer.console.print(f"\n📄 Report saved to: {save}")


if __name__ == "__main__":
    main()
