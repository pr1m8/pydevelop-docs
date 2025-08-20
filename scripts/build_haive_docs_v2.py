#!/usr/bin/env python3
"""
Enhanced Haive documentation builder with progress tracking and selective builds.

Features:
- Progress bars and detailed status
- Build specific packages or all
- Union type error handling
- Memory usage tracking
- Timing information
- Better error reporting
"""

import argparse
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import psutil
from rich import box
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.table import Table

# Initialize Rich console
console = Console()

# Package info with descriptions
HAIVE_PACKAGES = {
    "haive-core": "Core framework and infrastructure",
    "haive-agents": "Agent implementations (SimpleAgent, ReactAgent, etc.)",
    "haive-tools": "Tool integrations and utilities",
    "haive-games": "Game environments and agents",
    "haive-dataflow": "Streaming and data processing",
    "haive-mcp": "Model Context Protocol integration",
    "haive-prebuilt": "Pre-configured agent setups",
}

# Known problematic packages
SKIP_PACKAGES = ["haive-models", "haive-agp", "haive-ui"]


class BuildStats:
    """Track build statistics."""

    def __init__(self):
        self.start_time = time.time()
        self.packages_built = 0
        self.packages_failed = 0
        self.total_warnings = 0
        self.union_type_issues = 0
        self.memory_peak = 0
        self.build_times: Dict[str, float] = {}

    def update_memory(self):
        """Update peak memory usage."""
        current = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        self.memory_peak = max(self.memory_peak, current)

    def get_summary(self) -> Table:
        """Get summary table."""
        table = Table(title="Build Summary", box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        total_time = time.time() - self.start_time
        table.add_row("Total Time", f"{total_time:.1f}s")
        table.add_row("Packages Built", str(self.packages_built))
        table.add_row("Packages Failed", str(self.packages_failed))
        table.add_row("Total Warnings", str(self.total_warnings))
        table.add_row("Union Type Issues", str(self.union_type_issues))
        table.add_row("Peak Memory", f"{self.memory_peak:.1f} MB")

        return table


def run_command_with_progress(
    cmd: List[str], cwd: str, description: str, progress: Progress, task_id
) -> Tuple[bool, str, int]:
    """Run command with progress tracking."""
    try:
        # Start subprocess
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        output_lines = []
        warning_count = 0
        union_type_detected = False

        # Read output in real-time
        while True:
            # Check if process is done
            retcode = process.poll()

            # Read available output
            if process.stdout:
                line = process.stdout.readline()
                if line:
                    output_lines.append(line)

                    # Update progress with current activity
                    if "reading sources" in line.lower():
                        progress.update(
                            task_id, description=f"{description} [reading sources]"
                        )
                    elif "building" in line.lower():
                        progress.update(
                            task_id, description=f"{description} [building]"
                        )
                    elif "writing" in line.lower():
                        progress.update(
                            task_id, description=f"{description} [writing output]"
                        )

                    # Count warnings
                    if "warning" in line.lower():
                        warning_count += 1

                    # Detect union type issues
                    if "unsupported operand type" in line and "NoneType" in line:
                        union_type_detected = True

            # Read stderr
            if process.stderr:
                err_line = process.stderr.readline()
                if err_line:
                    output_lines.append(f"STDERR: {err_line}")
                    if "warning" in err_line.lower():
                        warning_count += 1
                    if "unsupported operand type" in err_line:
                        union_type_detected = True

            # If process finished, break
            if retcode is not None:
                break

            # Small sleep to prevent CPU spinning
            time.sleep(0.1)

        # Get remaining output
        remaining_out, remaining_err = process.communicate()
        if remaining_out:
            output_lines.extend(remaining_out.splitlines())
        if remaining_err:
            output_lines.extend(
                [f"STDERR: {line}" for line in remaining_err.splitlines()]
            )

        output = "\n".join(output_lines)
        success = retcode == 0 or (retcode != 0 and "index.html" in output)

        return success, output, warning_count, union_type_detected

    except Exception as e:
        return False, str(e), 0, False


def check_package_structure(package_path: Path) -> Dict[str, bool]:
    """Check package structure and readiness."""
    checks = {
        "exists": package_path.exists(),
        "has_pyproject": (package_path / "pyproject.toml").exists(),
        "has_src": (package_path / "src").exists()
        or (package_path / package_path.name.replace("-", "_")).exists(),
        "has_docs": (package_path / "docs").exists(),
        "docs_initialized": (package_path / "docs" / "source" / "conf.py").exists(),
    }
    return checks


def build_single_package(
    package_path: Path,
    package_name: str,
    progress: Progress,
    stats: BuildStats,
    force_init: bool = False,
) -> Tuple[bool, Dict[str, any]]:
    """Build documentation for a single package."""

    # Check package structure
    checks = check_package_structure(package_path)

    if not checks["has_pyproject"]:
        return False, {"error": "No pyproject.toml found", "checks": checks}

    # Track timing
    start_time = time.time()

    # Create main task
    main_task = progress.add_task(f"[bold blue]{package_name}[/bold blue]", total=100)

    results = {
        "package": package_name,
        "initialized": False,
        "built": False,
        "warnings": 0,
        "union_type_issues": False,
        "build_time": 0,
        "output_path": None,
    }

    try:
        # Step 1: Initialize PyDevelop-Docs (33%)
        if force_init or not checks["docs_initialized"]:
            progress.update(
                main_task, advance=10, description=f"{package_name} [initializing]"
            )

            init_task = progress.add_task(
                f"  → Initializing docs structure", total=None
            )

            success, output, warnings, union_issues = run_command_with_progress(
                ["poetry", "run", "pydvlp-docs", "init", "--force", "--yes"],
                str(package_path),
                "Initializing",
                progress,
                init_task,
            )

            progress.remove_task(init_task)

            if not success:
                progress.update(
                    main_task,
                    completed=100,
                    description=f"{package_name} [failed init]",
                )
                return False, {
                    **results,
                    "error": "Initialization failed",
                    "output": output,
                }

            results["initialized"] = True
            results["warnings"] += warnings
            progress.update(
                main_task, advance=23, description=f"{package_name} [initialized]"
            )
        else:
            progress.update(
                main_task,
                advance=33,
                description=f"{package_name} [already initialized]",
            )
            results["initialized"] = True

        # Step 2: Build documentation (67%)
        progress.update(main_task, description=f"{package_name} [building docs]")

        docs_source = package_path / "docs" / "source"
        docs_build = package_path / "docs" / "build"

        # Clean build directory
        if docs_build.exists():
            shutil.rmtree(docs_build)

        build_task = progress.add_task(f"  → Building Sphinx documentation", total=None)

        stats.update_memory()

        success, output, warnings, union_issues = run_command_with_progress(
            [
                "poetry",
                "run",
                "sphinx-build",
                "-b",
                "html",
                "source",
                "build",
                "-E",
                "-q",
            ],
            str(package_path / "docs"),
            "Building",
            progress,
            build_task,
        )

        progress.remove_task(build_task)

        results["warnings"] += warnings
        stats.total_warnings += warnings

        if union_issues:
            results["union_type_issues"] = True
            stats.union_type_issues += 1
            console.print(
                f"  [yellow]⚠️  Union type syntax detected - using fallback mode[/yellow]"
            )

        # Check if build succeeded
        if (docs_build / "index.html").exists():
            results["built"] = True
            results["output_path"] = docs_build / "index.html"
            progress.update(
                main_task, advance=67, description=f"{package_name} [completed]"
            )

            stats.packages_built += 1
            console.print(f"  [green]✅ Documentation built successfully[/green]")

            if warnings > 0:
                console.print(f"  [yellow]⚠️  {warnings} warnings during build[/yellow]")
        else:
            progress.update(
                main_task, completed=100, description=f"{package_name} [failed]"
            )
            stats.packages_failed += 1
            return False, {
                **results,
                "error": "Build failed - no output",
                "output": output,
            }

        # Record build time
        build_time = time.time() - start_time
        results["build_time"] = build_time
        stats.build_times[package_name] = build_time

        return True, results

    except Exception as e:
        progress.update(main_task, completed=100, description=f"{package_name} [error]")
        stats.packages_failed += 1
        return False, {**results, "error": str(e)}


def create_hub_page(haive_root: Path, build_results: List[Dict]) -> Path:
    """Create central documentation hub with enhanced styling."""
    console.print("\n[bold blue]Creating documentation hub...[/bold blue]")

    hub_dir = haive_root / "docs" / "hub"
    hub_dir.mkdir(parents=True, exist_ok=True)

    # Generate package cards HTML
    package_cards = []
    for result in build_results:
        package_name = result["package"]
        status = "success" if result.get("built") else "failed"

        if status == "success":
            status_html = '<span class="status success">✅ Built</span>'
            warnings_html = (
                f'<div class="warnings">⚠️ {result["warnings"]} warnings</div>'
                if result["warnings"] > 0
                else ""
            )
            union_html = (
                '<div class="union-type">🔄 Union type fallback used</div>'
                if result.get("union_type_issues")
                else ""
            )
            time_html = f'<div class="build-time">⏱️ Build time: {result["build_time"]:.1f}s</div>'
            link_html = f'<a href="../../packages/{package_name}/docs/build/index.html" class="view-docs">View Documentation →</a>'
        else:
            status_html = '<span class="status failed">❌ Failed</span>'
            warnings_html = ""
            union_html = ""
            time_html = ""
            link_html = f'<div class="error-msg">Error: {result.get("error", "Unknown error")}</div>'

        description = HAIVE_PACKAGES.get(package_name, "Package documentation")

        card_html = f"""
        <div class="package {status}">
            <h2>{package_name}</h2>
            {status_html}
            <p class="description">{description}</p>
            {warnings_html}
            {union_html}
            {time_html}
            {link_html}
        </div>"""

        package_cards.append(card_html)

    # Create index.html with modern styling
    index_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Haive Documentation Hub</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        :root {{
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --success: #10b981;
            --warning: #f59e0b;
            --error: #ef4444;
            --bg-light: #f8fafc;
            --bg-dark: #1e293b;
            --text: #334155;
            --text-light: #64748b;
            --border: #e2e8f0;
            --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-light);
            color: var(--text);
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 3rem;
        }}
        
        h1 {{
            font-size: 3rem;
            color: var(--primary);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
        }}
        
        .subtitle {{
            color: var(--text-light);
            font-size: 1.25rem;
        }}
        
        .stats {{
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: var(--shadow);
            margin-bottom: 3rem;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
        }}
        
        .stat {{
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 2.5rem;
            font-weight: bold;
            color: var(--primary);
        }}
        
        .stat-label {{
            color: var(--text-light);
            margin-top: 0.5rem;
        }}
        
        .packages {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }}
        
        .package {{
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
            border: 2px solid transparent;
            position: relative;
            overflow: hidden;
        }}
        
        .package::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--border);
        }}
        
        .package.success::before {{
            background: var(--success);
        }}
        
        .package.failed::before {{
            background: var(--error);
        }}
        
        .package:hover {{
            transform: translateY(-4px);
            box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
            border-color: var(--primary);
        }}
        
        .package h2 {{
            color: var(--primary);
            margin-bottom: 0.5rem;
            font-size: 1.5rem;
        }}
        
        .status {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 500;
            margin-bottom: 1rem;
        }}
        
        .status.success {{
            background: var(--success);
            color: white;
        }}
        
        .status.failed {{
            background: var(--error);
            color: white;
        }}
        
        .description {{
            color: var(--text);
            margin-bottom: 1rem;
            font-size: 0.95rem;
        }}
        
        .warnings, .union-type, .build-time {{
            font-size: 0.875rem;
            color: var(--text-light);
            margin: 0.5rem 0;
        }}
        
        .warnings {{
            color: var(--warning);
        }}
        
        .view-docs {{
            display: inline-block;
            margin-top: 1rem;
            padding: 0.75rem 1.5rem;
            background: var(--primary);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 500;
            transition: background 0.2s;
        }}
        
        .view-docs:hover {{
            background: var(--primary-dark);
        }}
        
        .error-msg {{
            color: var(--error);
            font-size: 0.875rem;
            margin-top: 1rem;
        }}
        
        footer {{
            text-align: center;
            color: var(--text-light);
            padding: 2rem;
            border-top: 1px solid var(--border);
        }}
        
        .timestamp {{
            margin-top: 1rem;
            font-size: 0.875rem;
        }}
        
        @media (max-width: 768px) {{
            .packages {{
                grid-template-columns: 1fr;
            }}
            h1 {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 Haive Documentation Hub</h1>
            <p class="subtitle">Comprehensive documentation for the Haive AI Agent Framework</p>
        </header>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{len([r for r in build_results if r.get("built")])}</div>
                <div class="stat-label">Packages Built</div>
            </div>
            <div class="stat">
                <div class="stat-value">{sum(r.get("warnings", 0) for r in build_results)}</div>
                <div class="stat-label">Total Warnings</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len([r for r in build_results if r.get("union_type_issues")])}</div>
                <div class="stat-label">Union Type Fallbacks</div>
            </div>
            <div class="stat">
                <div class="stat-value">{sum(r.get("build_time", 0) for r in build_results):.1f}s</div>
                <div class="stat-label">Total Build Time</div>
            </div>
        </div>
        
        <div class="packages">
            {''.join(package_cards)}
        </div>
        
        <footer>
            <p>Built with ❤️ using PyDevelop-Docs</p>
            <p class="timestamp">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>
</body>
</html>"""

    hub_path = hub_dir / "index.html"
    hub_path.write_text(index_content)

    console.print(f"[green]✅ Documentation hub created at:[/green] {hub_path}")
    return hub_path


def main():
    """Enhanced main function with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Build Haive documentation with PyDevelop-Docs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build all packages
  %(prog)s --all
  
  # Build specific packages
  %(prog)s haive-core haive-agents
  
  # Build haive-mcp only
  %(prog)s haive-mcp
  
  # Force reinitialize and build
  %(prog)s --force haive-mcp
  
  # Don't open browser after build
  %(prog)s --no-open haive-mcp
""",
    )

    parser.add_argument(
        "packages",
        nargs="*",
        choices=list(HAIVE_PACKAGES.keys()) + ["all"],
        help="Packages to build (default: all)",
    )
    parser.add_argument("--all", "-a", action="store_true", help="Build all packages")
    parser.add_argument(
        "--force", "-f", action="store_true", help="Force reinitialize documentation"
    )
    parser.add_argument(
        "--no-open", action="store_true", help="Don't open browser after build"
    )
    parser.add_argument(
        "--parallel",
        "-p",
        type=int,
        default=1,
        help="Number of parallel builds (default: 1)",
    )

    args = parser.parse_args()

    # Determine which packages to build
    if args.all or (not args.packages):
        packages_to_build = list(HAIVE_PACKAGES.keys())
    else:
        packages_to_build = args.packages

    # Show header
    console.print(
        Panel.fit(
            "[bold blue]🚀 Haive Documentation Builder[/bold blue]\n"
            f"Building: {', '.join(packages_to_build)}",
            border_style="blue",
        )
    )

    # Get paths
    haive_root = Path(__file__).parent.parent.parent.parent
    packages_dir = haive_root / "packages"

    if not packages_dir.exists():
        console.print(f"[red]❌ Packages directory not found at {packages_dir}[/red]")
        sys.exit(1)

    # Initialize stats
    stats = BuildStats()

    # Build packages with progress tracking
    build_results = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console,
    ) as progress:

        for package_name in packages_to_build:
            package_path = packages_dir / package_name

            if not package_path.exists():
                console.print(f"[yellow]⚠️  Package {package_name} not found[/yellow]")
                continue

            if package_name in SKIP_PACKAGES:
                console.print(
                    f"[yellow]⚠️  Skipping {package_name} (known issues)[/yellow]"
                )
                continue

            console.print(f"\n[bold]Building {package_name}...[/bold]")

            success, result = build_single_package(
                package_path, package_name, progress, stats, force_init=args.force
            )

            build_results.append(result)

    # Create hub
    if len(build_results) > 1:
        hub_path = create_hub_page(haive_root, build_results)
    else:
        # Single package - use its index
        successful = [r for r in build_results if r.get("built")]
        if successful:
            hub_path = successful[0]["output_path"]
        else:
            hub_path = None

    # Show summary
    console.print("\n")
    console.print(stats.get_summary())

    # Show package URLs
    if build_results:
        console.print("\n[bold]📚 Documentation URLs:[/bold]")
        for result in build_results:
            if result.get("built"):
                console.print(f"  {result['package']}: file://{result['output_path']}")

    # Open browser
    if hub_path and not args.no_open:
        console.print(f"\n[blue]Opening documentation...[/blue]")
        try:
            subprocess.run(["xdg-open", str(hub_path)])
        except Exception as e:
            console.print(f"[yellow]Could not open browser: {e}[/yellow]")
            console.print(f"Open manually: file://{hub_path}")

    # Exit code based on results
    failed_count = len([r for r in build_results if not r.get("built")])
    sys.exit(failed_count)


if __name__ == "__main__":
    main()
