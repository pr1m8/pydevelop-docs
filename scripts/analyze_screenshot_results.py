#!/usr/bin/env python3
"""
Analyze screenshot results and provide actionable feedback.

This script demonstrates the feedback loop by analyzing the screenshot
session and providing specific recommendations.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

console = Console()


def analyze_session(session_dir: Path) -> Dict:
    """Analyze a screenshot session directory."""
    results = {
        "session": session_dir.name,
        "timestamp": datetime.now().isoformat(),
        "total_pages": 0,
        "total_issues": 0,
        "critical_issues": [],
        "navigation_issues": [],
        "404_errors": [],
        "css_issues": [],
        "recommendations": [],
    }

    # Count issue files
    issue_files = list(session_dir.glob("*_issues.txt"))
    results["total_pages"] = len(issue_files) // 2  # Light and dark themes

    # Analyze each issue file
    for issue_file in issue_files:
        if issue_file.stat().st_size > 0:
            page_name = issue_file.stem.replace("_light_issues", "").replace(
                "_dark_issues", ""
            )
            theme = "dark" if "_dark_" in issue_file.name else "light"

            with open(issue_file) as f:
                issues = [line.strip() for line in f if line.strip()]

            for issue in issues:
                results["total_issues"] += 1

                # Categorize issues
                if "No navigation sidebar found" in issue:
                    results["navigation_issues"].append(
                        {"page": page_name, "theme": theme, "issue": issue}
                    )
                    if theme == "light":  # Count once per page
                        results["critical_issues"].append(
                            f"Missing navigation on {page_name}"
                        )

                if "No TOC tree found" in issue:
                    results["navigation_issues"].append(
                        {"page": page_name, "theme": theme, "issue": issue}
                    )

                if "404" in str(issue_file.parent / f"{page_name}_{theme}_full.png"):
                    results["404_errors"].append(page_name)

    # Check for 404s in the console output
    summary_file = session_dir / "SUMMARY.md"
    if summary_file.exists():
        with open(summary_file) as f:
            content = f.read()
            if "HTTP 404" in content:
                # Extract 404 pages
                for line in content.split("\n"):
                    if "HTTP 404" in line and "URL:" in line:
                        url = line.split("URL:")[1].strip()
                        page = (
                            url.split("/")[-2]
                            if url.endswith("/")
                            else url.split("/")[-1]
                        )
                        if page not in results["404_errors"]:
                            results["404_errors"].append(page)

    # Generate recommendations
    if results["navigation_issues"]:
        results["recommendations"].append(
            {
                "severity": "critical",
                "category": "navigation",
                "title": "Missing Navigation Sidebar",
                "description": f"Navigation sidebar is missing on {len(set(i['page'] for i in results['navigation_issues']))} pages",
                "fix": """
1. Check Furo theme configuration in conf.py:
   ```python
   html_theme_options = {
       "sidebar_hide_name": False,
       "navigation_with_keys": True,
   }
   ```

2. Verify toctree directives in index.rst

3. Ensure _static/css files aren't hiding the sidebar
""",
            }
        )

    if results["404_errors"]:
        results["recommendations"].append(
            {
                "severity": "high",
                "category": "content",
                "title": "Missing Pages (404 Errors)",
                "description": f"{len(results['404_errors'])} pages returned 404 errors",
                "fix": """
1. The screenshot tool is looking for 'mcp' module but docs might be for 'pydevelop_docs'

2. Check autoapi_dirs configuration:
   ```python
   autoapi_dirs = ["../../src"]  # Should point to actual source
   ```

3. Verify the module structure matches expected URLs
""",
            }
        )

    # CSS-specific recommendations based on our recent fixes
    results["recommendations"].append(
        {
            "severity": "info",
            "category": "css",
            "title": "CSS Configuration Check",
            "description": "Verify CSS files after recent simplification",
            "fix": """
1. Ensure these CSS files were removed:
   - enhanced-design.css (marketing style)
   - api-docs.css (aggressive badges)
   - furo-intense.css (dark mode overrides)

2. Verify minimal CSS set is active:
   - breadcrumb-navigation.css
   - mermaid-custom.css
   - tippy-enhancements.css
   - css/custom.css

3. Run `pydevelop-docs init --force` to update configuration
""",
        }
    )

    return results


def display_feedback(results: Dict):
    """Display analysis results with actionable feedback."""
    # Header
    console.print(
        Panel.fit(
            f"[bold]📸 Visual Test Analysis[/bold]\n"
            f"Session: {results['session']}\n"
            f"Pages tested: {results['total_pages']}\n"
            f"Total issues: {results['total_issues']}\n"
            f"Critical issues: {len(results['critical_issues'])}",
            title="Test Summary",
        )
    )

    # Critical issues
    if results["critical_issues"]:
        console.print("\n[bold red]🚨 Critical Issues:[/bold red]")
        for issue in results["critical_issues"][:5]:
            console.print(f"  • {issue}")

    # Recommendations table
    if results["recommendations"]:
        console.print("\n[bold]📋 Actionable Recommendations:[/bold]\n")

        for i, rec in enumerate(results["recommendations"], 1):
            severity_colors = {
                "critical": "red",
                "high": "yellow",
                "medium": "cyan",
                "low": "green",
                "info": "blue",
            }

            color = severity_colors.get(rec["severity"], "white")

            console.print(
                f"[{color}]### {i}. {rec['title']} [{rec['severity'].upper()}][/{color}]"
            )
            console.print(f"**Category**: {rec['category']}")
            console.print(f"**Issue**: {rec['description']}")
            console.print("\n**Fix**:")
            console.print(Markdown(rec["fix"]))
            console.print()

    # Save results
    output_file = Path("visual_test_analysis.json")
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    console.print(f"\n[green]💾 Full analysis saved to {output_file}[/green]")

    # Next steps
    console.print("\n[bold]🎯 Next Steps:[/bold]")
    console.print("1. Apply the recommended fixes above")
    console.print("2. Rebuild documentation: `poetry run pydevelop-docs build`")
    console.print(
        "3. Re-run visual tests: `poetry run python scripts/visual_test_runner.py`"
    )
    console.print(
        "4. Use continuous testing: `poetry run python scripts/watch_and_test.py`"
    )


def main():
    """Main entry point."""
    console.print(
        Panel.fit(
            "[bold]📸 Screenshot Analysis & Feedback Loop[/bold]\n"
            "Analyzing visual test results to provide actionable feedback",
            title="Visual Testing Feedback",
        )
    )

    # Find latest session
    screenshot_dir = Path("debug/screenshots")
    if not screenshot_dir.exists():
        console.print("[red]❌ No screenshot directory found[/red]")
        return 1

    sessions = list(screenshot_dir.glob("comprehensive_*"))
    if not sessions:
        console.print("[red]❌ No screenshot sessions found[/red]")
        return 1

    latest_session = max(sessions, key=lambda p: p.stat().st_mtime)
    console.print(f"\n[cyan]Analyzing session: {latest_session.name}[/cyan]\n")

    # Analyze the session
    results = analyze_session(latest_session)

    # Display feedback
    display_feedback(results)

    return 0


if __name__ == "__main__":
    exit(main())
