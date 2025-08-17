#!/usr/bin/env python3
"""
Automated visual testing for documentation with feedback loop.

This script builds documentation, runs screenshot tests, analyzes results,
and provides actionable feedback for improvements.
"""

import asyncio
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.table import Table
except ImportError:
    print("Please install rich: pip install rich")
    sys.exit(1)

console = Console()


class VisualTestRunner:
    """Runs visual tests on documentation with feedback analysis."""

    def __init__(self, project_path: Path = Path.cwd()):
        self.project_path = project_path
        self.build_dir = project_path / "docs" / "build"
        self.screenshot_dir = project_path / "debug" / "screenshots"
        self.results_file = project_path / "visual_test_results.json"
        self.server_process = None
        self.port = 8003

    def build_documentation(self) -> bool:
        """Build the documentation."""
        console.print("\n[bold blue]📚 Building documentation...[/bold blue]")

        # Check if pydevelop-docs is available
        check_cmd = ["poetry", "run", "which", "pydevelop-docs"]
        check_result = subprocess.run(check_cmd, capture_output=True)

        if check_result.returncode == 0:
            # Use pydevelop-docs
            build_cmd = ["poetry", "run", "pydevelop-docs", "build"]
        else:
            # Fallback to sphinx-build
            build_cmd = [
                "poetry",
                "run",
                "sphinx-build",
                "-b",
                "html",
                "docs/source",
                "docs/build",
            ]

        result = subprocess.run(build_cmd, capture_output=True, text=True)

        if result.returncode != 0:
            console.print(f"[red]❌ Build failed:[/red]\n{result.stderr}")
            return False

        console.print("[green]✅ Documentation built successfully[/green]")
        return True

    def start_server(self) -> bool:
        """Start the documentation server."""
        console.print(
            f"\n[bold blue]🌐 Starting server on port {self.port}...[/bold blue]"
        )

        # Check if build directory exists
        if not self.build_dir.exists():
            console.print(f"[red]❌ Build directory not found: {self.build_dir}[/red]")
            return False

        self.server_process = subprocess.Popen(
            [
                "python",
                "-m",
                "http.server",
                str(self.port),
                "--directory",
                str(self.build_dir),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Wait for server to start
        time.sleep(2)

        if self.server_process.poll() is not None:
            console.print("[red]❌ Failed to start server[/red]")
            return False

        console.print(
            f"[green]✅ Server running on http://localhost:{self.port}[/green]"
        )
        return True

    def stop_server(self):
        """Stop the documentation server."""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            console.print("[yellow]🛑 Server stopped[/yellow]")

    def run_screenshots(self) -> Dict:
        """Run comprehensive screenshot tests."""
        console.print("\n[bold blue]📸 Running screenshot tests...[/bold blue]")

        # Check if screenshot script exists
        screenshot_script = (
            self.project_path / "scripts" / "debug" / "comprehensive_screenshot.py"
        )
        if not screenshot_script.exists():
            return {
                "success": False,
                "error": f"Screenshot script not found: {screenshot_script}",
            }

        # Create timestamp for this session
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Run comprehensive screenshots
        result = subprocess.run(
            ["poetry", "run", "python", str(screenshot_script), str(self.port)],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            console.print(f"[red]❌ Screenshot tests failed:[/red]\n{result.stderr}")
            return {"success": False, "error": result.stderr}

        # Find the created session directory
        if not self.screenshot_dir.exists():
            return {"success": False, "error": "Screenshot directory not created"}

        sessions = list(self.screenshot_dir.glob("comprehensive_*"))
        if not sessions:
            return {"success": False, "error": "No screenshot session found"}

        latest_session = max(sessions, key=lambda p: p.stat().st_mtime)

        # Parse results
        summary_file = latest_session / "SUMMARY.md"
        if summary_file.exists():
            return self.parse_results(latest_session)
        else:
            return {"success": False, "error": "No summary file generated"}

    def parse_results(self, session_dir: Path) -> Dict:
        """Parse screenshot test results."""
        results = {
            "success": True,
            "session_dir": str(session_dir),
            "timestamp": (
                session_dir.name.split("_", 1)[1]
                if "_" in session_dir.name
                else "unknown"
            ),
            "pages_tested": 0,
            "issues": [],
            "theme_issues": {"light": [], "dark": []},
            "critical_issues": [],
            "css_issues": [],
            "navigation_issues": [],
            "content_issues": [],
        }

        # Count pages and collect issues
        for issue_file in session_dir.glob("*_issues.txt"):
            results["pages_tested"] += 1

            if issue_file.stat().st_size > 0:
                page_name = issue_file.stem.replace("_light_issues", "").replace(
                    "_dark_issues", ""
                )
                theme = "dark" if "_dark_" in issue_file.name else "light"

                with open(issue_file) as f:
                    issues = f.read().strip().split("\n")

                for issue in issues:
                    if not issue:
                        continue

                    issue_data = {"page": page_name, "theme": theme, "issue": issue}

                    results["issues"].append(issue_data)
                    results["theme_issues"][theme].append(issue_data)

                    # Categorize issues
                    issue_lower = issue.lower()
                    if any(
                        critical in issue_lower
                        for critical in ["missing", "error", "failed", "not found"]
                    ):
                        results["critical_issues"].append(issue_data)

                    if any(
                        css in issue_lower
                        for css in ["css", "style", "color", "background"]
                    ):
                        results["css_issues"].append(issue_data)

                    if any(
                        nav in issue_lower
                        for nav in ["navigation", "sidebar", "toc", "menu"]
                    ):
                        results["navigation_issues"].append(issue_data)

                    if any(
                        content in issue_lower
                        for content in ["content", "autoapi", "empty", "blank"]
                    ):
                        results["content_issues"].append(issue_data)

        return results

    def analyze_feedback(self, results: Dict) -> List[Dict]:
        """Analyze results and generate actionable feedback."""
        feedback = []

        # Check for critical issues
        if results.get("critical_issues"):
            feedback.append(
                {
                    "severity": "critical",
                    "category": "rendering",
                    "message": f"Found {len(results['critical_issues'])} critical rendering issues",
                    "action": "Review and fix missing elements immediately",
                    "details": results["critical_issues"][:3],  # Show first 3
                    "fix_suggestion": self.get_fix_for_critical(
                        results["critical_issues"]
                    ),
                }
            )

        # Check CSS issues
        if results.get("css_issues"):
            feedback.append(
                {
                    "severity": "high",
                    "category": "css",
                    "message": f"{len(results['css_issues'])} CSS-related issues found",
                    "action": "Review CSS configuration and file loading",
                    "details": results["css_issues"][:3],
                    "fix_suggestion": self.get_fix_for_css(results["css_issues"]),
                }
            )

        # Check navigation issues
        if results.get("navigation_issues"):
            feedback.append(
                {
                    "severity": "high",
                    "category": "navigation",
                    "message": f"{len(results['navigation_issues'])} navigation issues found",
                    "action": "Check Furo theme configuration",
                    "details": results["navigation_issues"][:3],
                    "fix_suggestion": self.get_fix_for_navigation(
                        results["navigation_issues"]
                    ),
                }
            )

        # Check theme-specific issues
        for theme in ["light", "dark"]:
            theme_issues = results.get("theme_issues", {}).get(theme, [])
            if len(theme_issues) > 5:  # Only report if significant
                feedback.append(
                    {
                        "severity": "medium",
                        "category": f"{theme}_theme",
                        "message": f"{len(theme_issues)} issues specific to {theme} theme",
                        "action": f"Test and fix {theme} theme compatibility",
                        "details": theme_issues[:3],
                        "fix_suggestion": self.get_fix_for_theme(theme, theme_issues),
                    }
                )

        # Success case
        if not feedback:
            feedback.append(
                {
                    "severity": "info",
                    "category": "success",
                    "message": "All visual tests passed! 🎉",
                    "action": "Documentation is ready for deployment",
                    "details": [],
                    "fix_suggestion": "No fixes needed - great job!",
                }
            )

        return feedback

    def get_fix_for_critical(self, issues: List[Dict]) -> str:
        """Get fix suggestions for critical issues."""
        fixes = []

        for issue in issues[:3]:  # Analyze first 3
            issue_text = issue["issue"].lower()

            if "navigation" in issue_text or "sidebar" in issue_text:
                fixes.append("Check html_theme_options['sidebar_hide_name'] = False")
            elif "autoapi" in issue_text:
                fixes.append("Verify autoapi_dirs points to correct source directory")
            elif "css" in issue_text:
                fixes.append("Check that CSS files exist in _static directory")

        return " | ".join(fixes) if fixes else "Review build logs for detailed errors"

    def get_fix_for_css(self, issues: List[Dict]) -> str:
        """Get fix suggestions for CSS issues."""
        return """
1. Check pydevelop_docs/config.py html_css_files list
2. Verify CSS files exist in docs/source/_static/
3. Review CSS load order in setup() function
4. Test with minimal CSS configuration"""

    def get_fix_for_navigation(self, issues: List[Dict]) -> str:
        """Get fix suggestions for navigation issues."""
        return """
1. In config.py, set: html_theme_options['sidebar_hide_name'] = False
2. Ensure navigation_with_keys = True
3. Check that toctree directives are properly formatted
4. Verify navigation_depth setting (should be 3-4)"""

    def get_fix_for_theme(self, theme: str, issues: List[Dict]) -> str:
        """Get fix suggestions for theme-specific issues."""
        if theme == "dark":
            return """
1. Check dark mode CSS variables in custom.css
2. Test color contrast for readability
3. Ensure code blocks have proper background colors
4. Review Furo's dark mode documentation"""
        else:
            return """
1. Verify light theme color values
2. Check for hardcoded dark colors
3. Test with browser's light mode preference
4. Review custom CSS overrides"""

    def display_results(self, results: Dict, feedback: List[Dict]):
        """Display test results and feedback."""
        # Results summary
        console.print("\n")
        console.print(
            Panel.fit(
                f"[bold]Visual Test Results[/bold]\n"
                f"Session: {results.get('timestamp', 'unknown')}\n"
                f"Pages tested: {results['pages_tested']}\n"
                f"Total issues: {len(results['issues'])}\n"
                f"Critical issues: [red]{len(results['critical_issues'])}[/red]\n"
                f"CSS issues: [yellow]{len(results['css_issues'])}[/yellow]\n"
                f"Navigation issues: [yellow]{len(results['navigation_issues'])}[/yellow]",
                title="📊 Test Summary",
            )
        )

        # Feedback table
        if feedback:
            table = Table(title="\n📋 Actionable Feedback", show_lines=True)
            table.add_column("Severity", style="bold", width=10)
            table.add_column("Category", width=15)
            table.add_column("Issue", width=40)
            table.add_column("Action Required", width=40)

            severity_colors = {
                "critical": "red",
                "high": "yellow",
                "medium": "cyan",
                "low": "green",
                "info": "blue",
            }

            for item in feedback:
                if item["severity"] != "info":  # Skip success message in table
                    table.add_row(
                        f"[{severity_colors.get(item['severity'], 'white')}]{item['severity'].upper()}[/]",
                        item["category"],
                        item["message"],
                        item["action"],
                    )

            if len(table.rows) > 0:
                console.print(table)

        # Detailed fixes
        console.print("\n[bold]🔧 Detailed Fix Suggestions:[/bold]\n")
        for item in feedback:
            if item["severity"] in ["critical", "high"] and item.get("fix_suggestion"):
                console.print(f"[yellow]➤ {item['category'].upper()}:[/yellow]")
                console.print(item["fix_suggestion"])
                console.print()

        # Save results
        self.save_results(results, feedback)

    def save_results(self, results: Dict, feedback: List[Dict]):
        """Save test results to JSON file."""
        output = {
            "results": results,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_issues": len(results["issues"]),
                "critical_count": len(results["critical_issues"]),
                "requires_fixes": any(
                    f["severity"] in ["critical", "high"] for f in feedback
                ),
            },
        }

        with open(self.results_file, "w") as f:
            json.dump(output, f, indent=2)

        console.print(f"\n[green]💾 Results saved to {self.results_file}[/green]")

    def run_full_test(self) -> bool:
        """Run the complete visual testing workflow."""
        try:
            # Build documentation
            if not self.build_documentation():
                return False

            # Start server
            if not self.start_server():
                return False

            # Run screenshots
            results = self.run_screenshots()

            if not results.get("success", False):
                console.print(
                    f"[red]❌ Screenshot tests failed: {results.get('error')}[/red]"
                )
                return False

            # Analyze feedback
            feedback = self.analyze_feedback(results)

            # Display results
            self.display_results(results, feedback)

            # Return success if no critical issues
            has_critical = any(f["severity"] == "critical" for f in feedback)

            if has_critical:
                console.print(
                    "\n[bold red]❌ Critical issues found - fixes required![/bold red]"
                )
                return False
            else:
                console.print(
                    "\n[bold green]✅ Visual tests completed successfully![/bold green]"
                )
                return True

        finally:
            self.stop_server()


def main():
    """Main entry point for visual testing."""
    console.print(
        Panel.fit(
            "[bold]📸 Documentation Visual Testing[/bold]\n"
            "Automated screenshot testing with feedback loop\n\n"
            "This tool will:\n"
            "1. Build your documentation\n"
            "2. Start a local server\n"
            "3. Take screenshots of all pages\n"
            "4. Analyze for visual issues\n"
            "5. Provide actionable feedback",
            title="PyDevelop-Docs Visual Tester",
        )
    )

    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        console.print("\nUsage: poetry run python scripts/visual_test_runner.py")
        console.print(
            "\nThis script runs visual tests on your documentation and provides feedback."
        )
        return 0

    tester = VisualTestRunner()
    success = tester.run_full_test()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
