#!/usr/bin/env python3
"""
Watch documentation files and run visual tests on changes.

This script monitors documentation source files and automatically
runs visual tests when changes are detected.
"""

import asyncio
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Set

try:
    from rich.console import Console
    from rich.live import Live
    from rich.panel import Panel
    from rich.table import Table
    from watchdog.events import FileModifiedEvent, FileSystemEventHandler
    from watchdog.observers import Observer
except ImportError:
    print("Please install dependencies: pip install watchdog rich")
    sys.exit(1)

console = Console()


class DocumentationWatcher(FileSystemEventHandler):
    """Watches documentation files and triggers visual tests."""

    def __init__(self):
        self.console = console
        self.last_test_time = None
        self.test_in_progress = False
        self.pending_changes: Set[str] = set()
        self.test_results = {
            "last_run": None,
            "status": "waiting",
            "issues_found": 0,
            "files_changed": [],
        }
        # Debounce settings
        self.debounce_seconds = 3
        self.last_change_time = None

    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return

        # Filter relevant files
        path = Path(event.src_path)
        if self.is_relevant_file(path):
            self.pending_changes.add(str(path))
            self.last_change_time = time.time()
            self.console.print(f"[yellow]📝 Change detected:[/yellow] {path.name}")

    def is_relevant_file(self, path: Path) -> bool:
        """Check if file is relevant for documentation."""
        relevant_extensions = {".py", ".rst", ".md", ".css", ".js", ".html"}
        relevant_dirs = {"docs", "source", "_static", "_templates", "src"}

        # Check extension
        if path.suffix not in relevant_extensions:
            return False

        # Check if in relevant directory
        path_parts = path.parts
        return any(part in path_parts for part in relevant_dirs)

    def should_run_tests(self) -> bool:
        """Check if we should run tests (with debouncing)."""
        if not self.pending_changes:
            return False

        if self.test_in_progress:
            return False

        if self.last_change_time is None:
            return False

        # Check if enough time has passed since last change
        time_since_change = time.time() - self.last_change_time
        return time_since_change >= self.debounce_seconds

    async def run_visual_tests(self):
        """Run visual tests and update results."""
        if not self.pending_changes:
            return

        self.test_in_progress = True
        self.test_results["status"] = "running"
        self.test_results["files_changed"] = list(self.pending_changes)

        self.console.print("\n[bold blue]🔄 Running visual tests...[/bold blue]")
        self.console.print(f"Changed files: {len(self.pending_changes)}")

        try:
            # Run the visual test runner
            result = subprocess.run(
                ["poetry", "run", "python", "scripts/visual_test_runner.py"],
                capture_output=True,
                text=True,
            )

            # Parse results
            if result.returncode == 0:
                self.test_results["status"] = "passed"
                self.test_results["issues_found"] = 0
                self.console.print("[green]✅ Visual tests passed![/green]")
            else:
                self.test_results["status"] = "failed"
                # Try to parse issue count from output
                output = result.stdout + result.stderr
                if "Critical issues:" in output:
                    try:
                        line = [
                            l for l in output.split("\n") if "Critical issues:" in l
                        ][0]
                        count = int(line.split(":")[-1].strip())
                        self.test_results["issues_found"] = count
                    except:
                        self.test_results["issues_found"] = -1

                self.console.print("[red]❌ Visual tests failed![/red]")
                if result.stderr:
                    self.console.print(f"[red]Error: {result.stderr[:200]}...[/red]")

            self.test_results["last_run"] = datetime.now().strftime("%H:%M:%S")

        except Exception as e:
            self.console.print(f"[red]❌ Error running tests: {e}[/red]")
            self.test_results["status"] = "error"

        finally:
            self.test_in_progress = False
            self.pending_changes.clear()
            self.last_test_time = time.time()

    def get_status_table(self) -> Table:
        """Create a status table for the live display."""
        table = Table(title="Documentation Watch Status", box=None)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")

        # Status with color
        status = self.test_results["status"]
        status_colors = {
            "waiting": "yellow",
            "running": "blue",
            "passed": "green",
            "failed": "red",
            "error": "red",
        }
        status_display = f"[{status_colors.get(status, 'white')}]{status.upper()}[/]"

        table.add_row("Status", status_display)
        table.add_row("Last Run", self.test_results["last_run"] or "Never")
        table.add_row("Issues Found", str(self.test_results["issues_found"]))
        table.add_row("Pending Changes", str(len(self.pending_changes)))

        if self.pending_changes:
            files = "\n".join(
                f"  • {Path(f).name}" for f in list(self.pending_changes)[:5]
            )
            if len(self.pending_changes) > 5:
                files += f"\n  • ... and {len(self.pending_changes) - 5} more"
            table.add_row("Changed Files", files)

        return table


async def watch_loop(watcher: DocumentationWatcher):
    """Main watch loop that checks for changes and runs tests."""
    with Live(
        Panel(watcher.get_status_table(), title="📸 Visual Test Watcher"),
        refresh_per_second=2,
        console=console,
    ) as live:
        while True:
            # Update display
            live.update(
                Panel(watcher.get_status_table(), title="📸 Visual Test Watcher")
            )

            # Check if we should run tests
            if watcher.should_run_tests():
                await watcher.run_visual_tests()

            # Small delay to prevent busy waiting
            await asyncio.sleep(1)


def main():
    """Main entry point for the watch script."""
    console.print(
        Panel.fit(
            "[bold]📸 Documentation Visual Test Watcher[/bold]\n"
            "Monitoring documentation files for changes\n\n"
            "This tool will:\n"
            "• Watch for changes in documentation files\n"
            "• Automatically run visual tests\n"
            "• Report issues in real-time\n"
            "• Provide continuous feedback\n\n"
            "Press Ctrl+C to stop",
            title="PyDevelop-Docs Watcher",
        )
    )

    # Paths to watch
    watch_paths = [
        Path("docs/source"),
        Path("src"),  # For autodoc changes
    ]

    # Filter out non-existent paths
    existing_paths = [p for p in watch_paths if p.exists()]

    if not existing_paths:
        console.print("[red]❌ No documentation directories found to watch![/red]")
        console.print("Expected directories: docs/source, src")
        return 1

    console.print(f"\n[green]👀 Watching directories:[/green]")
    for path in existing_paths:
        console.print(f"  • {path}")

    # Create watcher
    watcher = DocumentationWatcher()
    observer = Observer()

    # Schedule watchers for each path
    for path in existing_paths:
        observer.schedule(watcher, str(path), recursive=True)

    # Start watching
    observer.start()
    console.print("\n[green]✅ Watcher started![/green]")
    console.print("[yellow]Waiting for changes...[/yellow]\n")

    try:
        # Run the async watch loop
        asyncio.run(watch_loop(watcher))
    except KeyboardInterrupt:
        console.print("\n[yellow]🛑 Stopping watcher...[/yellow]")
        observer.stop()
        observer.join()
        console.print("[green]✅ Watcher stopped![/green]")
        return 0
    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]")
        observer.stop()
        observer.join()
        return 1


if __name__ == "__main__":
    sys.exit(main())
