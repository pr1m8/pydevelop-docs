#!/usr/bin/env python3
"""Enhanced build logger for Sphinx documentation builds.

This script provides comprehensive logging, filtering, and analysis
of Sphinx build output with categorized warnings and errors.
"""

import argparse
import json
import re
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple

import click
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.table import Table


class SphinxBuildLogger:
    """Enhanced Sphinx build logger with real-time analysis."""

    def __init__(self, output_dir: Path = None, debug: bool = False):
        self.console = Console()
        self.debug = debug
        self.output_dir = output_dir or Path("logs")
        self.output_dir.mkdir(exist_ok=True)

        # Logging state
        self.start_time = datetime.now()
        self.log_file = (
            self.output_dir
            / f"sphinx-build-{self.start_time.strftime('%Y%m%d-%H%M%S')}.log"
        )
        self.analysis_file = (
            self.output_dir
            / f"build-analysis-{self.start_time.strftime('%Y%m%d-%H%M%S')}.json"
        )

        # Statistics
        self.stats = {
            "files_processed": 0,
            "warnings": defaultdict(list),
            "errors": defaultdict(list),
            "extensions_loaded": [],
            "progress_percent": 0,
            "build_phases": [],
            "import_errors": [],
            "deprecated_warnings": [],
        }

        # Pattern matchers
        self.patterns = {
            "autoapi_progress": re.compile(
                r"\[AutoAPI\] Reading files\.\.\. \[\s*(\d+)%\]"
            ),
            "warning": re.compile(r"WARNING: (.+)"),
            "error": re.compile(r"ERROR: (.+)"),
            "import_error": re.compile(r"Cannot resolve import of (.+) in (.+)"),
            "deprecated": re.compile(r"(.+) is deprecated"),
            "extension": re.compile(r"loading (.+) extension"),
            "sphinx_phase": re.compile(
                r"(reading sources|writing output|copying static files|building)"
            ),
        }

    def analyze_line(self, line: str) -> Dict[str, str]:
        """Analyze a single log line and categorize it."""
        line = line.strip()
        analysis = {"type": "info", "category": "general", "message": line}

        # Check for progress
        if match := self.patterns["autoapi_progress"].search(line):
            self.stats["progress_percent"] = int(match.group(1))
            analysis["type"] = "progress"
            analysis["category"] = "autoapi"
            analysis["progress"] = int(match.group(1))

        # Check for warnings
        elif match := self.patterns["warning"].search(line):
            warning_msg = match.group(1)
            analysis["type"] = "warning"

            # Categorize warnings
            if "Cannot resolve import" in warning_msg:
                analysis["category"] = "import_resolution"
                self.stats["import_errors"].append(warning_msg)
            elif "deprecated" in warning_msg.lower():
                analysis["category"] = "deprecated"
                self.stats["deprecated_warnings"].append(warning_msg)
            elif "extension" in warning_msg:
                analysis["category"] = "extension"
            else:
                analysis["category"] = "general"

            self.stats["warnings"][analysis["category"]].append(warning_msg)

        # Check for errors
        elif match := self.patterns["error"].search(line):
            error_msg = match.group(1)
            analysis["type"] = "error"
            analysis["category"] = "build_error"
            self.stats["errors"][analysis["category"]].append(error_msg)

        # Check for build phases
        elif match := self.patterns["sphinx_phase"].search(line):
            phase = match.group(1)
            analysis["type"] = "phase"
            analysis["category"] = "build_phase"
            if phase not in self.stats["build_phases"]:
                self.stats["build_phases"].append(phase)

        # Check for extensions
        elif "extension" in line and "loaded" in line:
            analysis["type"] = "extension"
            analysis["category"] = "extension_load"

        return analysis

    def create_live_dashboard(self) -> Table:
        """Create a live dashboard showing build progress."""
        table = Table(
            title="🔨 Sphinx Build Monitor",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")
        table.add_column("Details", style="yellow")

        # Progress
        progress_bar = "█" * (self.stats["progress_percent"] // 5) + "░" * (
            20 - self.stats["progress_percent"] // 5
        )
        table.add_row(
            "Progress", f"{self.stats['progress_percent']}%", f"[{progress_bar}]"
        )

        # Files processed
        table.add_row(
            "Files Processed", str(self.stats["files_processed"]), "AutoAPI reading"
        )

        # Build time
        elapsed = datetime.now() - self.start_time
        table.add_row("Elapsed Time", f"{elapsed.total_seconds():.1f}s", "")

        # Warnings summary
        total_warnings = sum(len(warns) for warns in self.stats["warnings"].values())
        warning_breakdown = ", ".join(
            [
                f"{cat}: {len(warns)}"
                for cat, warns in self.stats["warnings"].items()
                if warns
            ]
        )
        table.add_row("Warnings", str(total_warnings), warning_breakdown or "None")

        # Errors summary
        total_errors = sum(len(errs) for errs in self.stats["errors"].values())
        table.add_row(
            "Errors",
            str(total_errors),
            "None" if total_errors == 0 else "❌ Build issues",
        )

        # Current phase
        current_phase = (
            self.stats["build_phases"][-1] if self.stats["build_phases"] else "Starting"
        )
        table.add_row("Current Phase", current_phase, "")

        return table

    def run_build(self, build_command: List[str], cwd: Path = None) -> Tuple[int, Dict]:
        """Run the build command with enhanced logging."""
        self.console.print(f"🚀 Starting Sphinx build: {' '.join(build_command)}")
        self.console.print(f"📁 Working directory: {cwd or Path.cwd()}")
        self.console.print(f"📝 Logging to: {self.log_file}")

        # Start the process
        process = subprocess.Popen(
            build_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            cwd=cwd,
        )

        # Create live dashboard
        with Live(self.create_live_dashboard(), refresh_per_second=2) as live:
            with open(self.log_file, "w") as log_file:
                for line in process.stdout:
                    # Write to log file
                    log_file.write(line)
                    log_file.flush()

                    # Analyze line
                    analysis = self.analyze_line(line)

                    # Update file count for AutoAPI progress
                    if "Reading files" in line:
                        self.stats["files_processed"] += 1

                    # Update live dashboard
                    live.update(self.create_live_dashboard())

                    # Debug output
                    if self.debug and analysis["type"] in ["warning", "error"]:
                        self.console.print(
                            f"[{analysis['type'].upper()}] {analysis['message']}"
                        )

        # Wait for completion
        return_code = process.wait()

        # Generate final analysis
        self.generate_analysis_report()

        return return_code, self.stats

    def generate_analysis_report(self) -> None:
        """Generate comprehensive analysis report."""
        end_time = datetime.now()
        build_duration = (end_time - self.start_time).total_seconds()

        report = {
            "build_info": {
                "start_time": self.start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_seconds": build_duration,
                "log_file": str(self.log_file),
            },
            "statistics": {
                "files_processed": self.stats["files_processed"],
                "final_progress": self.stats["progress_percent"],
                "total_warnings": sum(
                    len(warns) for warns in self.stats["warnings"].values()
                ),
                "total_errors": sum(
                    len(errs) for errs in self.stats["errors"].values()
                ),
                "build_phases": self.stats["build_phases"],
            },
            "warning_breakdown": {
                category: len(warnings)
                for category, warnings in self.stats["warnings"].items()
            },
            "error_breakdown": {
                category: len(errors)
                for category, errors in self.stats["errors"].items()
            },
            "top_import_errors": self.stats["import_errors"][
                :20
            ],  # Top 20 import issues
            "deprecated_warnings": self.stats["deprecated_warnings"][
                :10
            ],  # Top 10 deprecated
            "recommendations": self.generate_recommendations(),
        }

        # Save analysis
        with open(self.analysis_file, "w") as f:
            json.dump(report, f, indent=2)

        # Display summary
        self.display_final_summary(report)

    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on build analysis."""
        recommendations = []

        # Import error recommendations
        if len(self.stats["import_errors"]) > 50:
            recommendations.append(
                "🔗 High number of import resolution warnings. Consider adding missing packages to autoapi_dirs or updating import paths."
            )

        # Deprecated warnings
        if len(self.stats["deprecated_warnings"]) > 5:
            recommendations.append(
                "⚠️ Multiple deprecated package warnings. Consider updating dependencies in pyproject.toml."
            )

        # Extension issues
        extension_warnings = len(self.stats["warnings"].get("extension", []))
        if extension_warnings > 0:
            recommendations.append(
                "🔌 Extension warnings detected. Check extension compatibility and configuration."
            )

        # Performance recommendations
        if self.stats["files_processed"] > 1000:
            recommendations.append(
                "⚡ Large codebase detected. Consider using autoapi_ignore_patterns to exclude unnecessary files."
            )

        if not recommendations:
            recommendations.append(
                "✅ Build completed successfully with minimal issues!"
            )

        return recommendations

    def display_final_summary(self, report: Dict) -> None:
        """Display final build summary."""
        stats = report["statistics"]

        # Create summary table
        summary_table = Table(
            title="📊 Build Summary", show_header=True, header_style="bold cyan"
        )
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="green")
        summary_table.add_column("Status", style="yellow")

        # Add rows
        summary_table.add_row(
            "Duration", f"{report['build_info']['duration_seconds']:.1f}s", ""
        )
        summary_table.add_row("Files Processed", str(stats["files_processed"]), "")
        summary_table.add_row(
            "Progress",
            f"{stats['final_progress']}%",
            "✅ Complete" if stats["final_progress"] == 100 else "⚠️ Partial",
        )
        summary_table.add_row(
            "Warnings",
            str(stats["total_warnings"]),
            "✅ Good" if stats["total_warnings"] < 50 else "⚠️ Review needed",
        )
        summary_table.add_row(
            "Errors",
            str(stats["total_errors"]),
            "✅ Success" if stats["total_errors"] == 0 else "❌ Issues found",
        )

        self.console.print(summary_table)

        # Warning breakdown
        if report["warning_breakdown"]:
            warning_table = Table(title="⚠️ Warning Breakdown", show_header=True)
            warning_table.add_column("Category", style="cyan")
            warning_table.add_column("Count", style="yellow")

            for category, count in sorted(
                report["warning_breakdown"].items(), key=lambda x: x[1], reverse=True
            ):
                warning_table.add_row(category.replace("_", " ").title(), str(count))

            self.console.print(warning_table)

        # Recommendations
        if report["recommendations"]:
            recommendations_panel = Panel(
                "\n".join(f"• {rec}" for rec in report["recommendations"]),
                title="💡 Recommendations",
                border_style="blue",
            )
            self.console.print(recommendations_panel)

        # File locations
        self.console.print(f"\n📄 Full log: {self.log_file}")
        self.console.print(f"📊 Analysis: {self.analysis_file}")


@click.command()
@click.option(
    "--command",
    "-c",
    default="poetry run sphinx-build -b html source build/html -v",
    help="Sphinx build command to run",
)
@click.option(
    "--directory",
    "-d",
    type=click.Path(exists=True, path_type=Path),
    default=Path.cwd(),
    help="Build directory",
)
@click.option(
    "--output", "-o", type=click.Path(path_type=Path), help="Output directory for logs"
)
@click.option("--debug", is_flag=True, help="Show debug output during build")
@click.option(
    "--filter-warnings",
    "-f",
    multiple=True,
    help="Filter out specific warning categories",
)
def main(
    command: str,
    directory: Path,
    output: Path,
    debug: bool,
    filter_warnings: Tuple[str],
):
    """Enhanced Sphinx build logger with real-time monitoring."""

    # Create logger
    logger = SphinxBuildLogger(output_dir=output, debug=debug)

    # Parse command
    build_command = command.split()

    # Run build with logging
    try:
        return_code, stats = logger.run_build(build_command, cwd=directory)

        # Exit with same code as build
        sys.exit(return_code)

    except KeyboardInterrupt:
        logger.console.print("\n🛑 Build interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.console.print(f"❌ Logger error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
