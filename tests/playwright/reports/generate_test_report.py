#!/usr/bin/env python3
"""Generate comprehensive HTML report from documentation test results."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import click


class TestReportGenerator:
    """Generate beautiful HTML reports from test results."""

    def __init__(self, results_file: Path):
        """Initialize report generator with test results."""
        self.results_file = Path(results_file)
        with open(self.results_file, "r") as f:
            self.results = json.load(f)

        self.timestamp = self.results.get(
            "timestamp", datetime.now().strftime("%Y%m%d_%H%M%S")
        )
        self.output_dir = self.results_file.parent

    def generate_html_report(self) -> Path:
        """Generate comprehensive HTML report."""
        report_path = self.output_dir / f"test_report_{self.timestamp}.html"

        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Haive Documentation Test Report - {self.timestamp}</title>
    <style>
        :root {{
            --primary: #2563eb;
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
            --dark: #1f2937;
            --light: #f3f4f6;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: var(--dark);
            background: var(--light);
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        header {{
            background: white;
            padding: 2rem;
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }}
        
        h1 {{
            color: var(--primary);
            margin-bottom: 1rem;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        
        .stat-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }}
        
        .stat-label {{
            color: #6b7280;
            font-size: 0.875rem;
            text-transform: uppercase;
        }}
        
        .success {{ color: var(--success); }}
        .danger {{ color: var(--danger); }}
        .warning {{ color: var(--warning); }}
        
        .package-section {{
            background: white;
            padding: 2rem;
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }}
        
        .package-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--light);
        }}
        
        .package-name {{
            font-size: 1.5rem;
            font-weight: bold;
        }}
        
        .package-status {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 0.25rem;
            font-weight: 500;
        }}
        
        .status-passed {{
            background: #d1fae5;
            color: #065f46;
        }}
        
        .status-failed {{
            background: #fee2e2;
            color: #991b1b;
        }}
        
        .test-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-bottom: 1.5rem;
        }}
        
        .test-card {{
            border: 1px solid #e5e7eb;
            border-radius: 0.375rem;
            padding: 1rem;
        }}
        
        .test-name {{
            font-weight: 600;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .test-details {{
            font-size: 0.875rem;
            color: #6b7280;
        }}
        
        .issues-section {{
            margin-top: 1.5rem;
            padding: 1rem;
            background: #fef3c7;
            border-radius: 0.375rem;
            border: 1px solid #fbbf24;
        }}
        
        .issues-title {{
            font-weight: 600;
            color: #92400e;
            margin-bottom: 0.5rem;
        }}
        
        .issue-list {{
            list-style: none;
            font-size: 0.875rem;
        }}
        
        .issue-item {{
            padding: 0.25rem 0;
            color: #92400e;
        }}
        
        .screenshots {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }}
        
        .screenshot {{
            border: 1px solid #e5e7eb;
            border-radius: 0.375rem;
            overflow: hidden;
            cursor: pointer;
            transition: transform 0.2s;
        }}
        
        .screenshot:hover {{
            transform: scale(1.05);
        }}
        
        .screenshot img {{
            width: 100%;
            height: auto;
            display: block;
        }}
        
        .screenshot-label {{
            padding: 0.5rem;
            background: #f9fafb;
            font-size: 0.75rem;
            text-align: center;
        }}
        
        footer {{
            text-align: center;
            padding: 2rem;
            color: #6b7280;
            font-size: 0.875rem;
        }}
        
        .icon {{
            display: inline-block;
            width: 1.25rem;
            height: 1.25rem;
            vertical-align: middle;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Haive Documentation Test Report</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Test Suite: Playwright Documentation Tests</p>
        </header>
        
        {self._generate_summary_section()}
        
        <main>
            <h2>📦 Package Test Results</h2>
            {self._generate_package_sections()}
        </main>
        
        <footer>
            <p>Generated by PyDevelop Documentation Test Suite</p>
            <p>Timestamp: {self.timestamp}</p>
        </footer>
    </div>
</body>
</html>
"""

        with open(report_path, "w") as f:
            f.write(html)

        return report_path

    def _generate_summary_section(self) -> str:
        """Generate summary statistics section."""
        summary = self.results["summary"]

        return f"""
        <div class="summary">
            <div class="stat-card">
                <div class="stat-value">{summary['total_packages']}</div>
                <div class="stat-label">Total Packages</div>
            </div>
            <div class="stat-card">
                <div class="stat-value success">{summary['passed']}</div>
                <div class="stat-label">Passed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value danger">{summary['failed']}</div>
                <div class="stat-label">Failed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary['total_tests']}</div>
                <div class="stat-label">Total Tests</div>
            </div>
            <div class="stat-card">
                <div class="stat-value warning">{summary['total_issues']}</div>
                <div class="stat-label">Issues Found</div>
            </div>
        </div>
"""

    def _generate_package_sections(self) -> str:
        """Generate detailed sections for each package."""
        sections = []

        for package_name, package_results in self.results["packages"].items():
            status_class = "passed" if package_results["passed"] else "failed"
            status_text = "PASSED" if package_results["passed"] else "FAILED"
            status_icon = "✅" if package_results["passed"] else "❌"

            section = f"""
            <div class="package-section">
                <div class="package-header">
                    <div class="package-name">{package_name}</div>
                    <div class="package-status status-{status_class}">
                        {status_icon} {status_text}
                    </div>
                </div>
                
                <div class="test-grid">
                    {self._generate_test_cards(package_results["tests"])}
                </div>
                
                {self._generate_issues_section(package_results.get("issues", []))}
                {self._generate_screenshots_section(package_name, package_results.get("screenshots", []))}
            </div>
"""
            sections.append(section)

        return "\n".join(sections)

    def _generate_test_cards(self, tests: Dict) -> str:
        """Generate test result cards."""
        cards = []

        for test_name, test_result in tests.items():
            status_icon = "✅" if test_result.get("passed", False) else "❌"

            details = []
            if "checks" in test_result:
                for check_name, check_value in test_result["checks"].items():
                    if isinstance(check_value, (int, float, bool)):
                        details.append(f"{check_name}: {check_value}")

            card = f"""
            <div class="test-card">
                <div class="test-name">
                    {status_icon} {test_name.replace('_', ' ').title()}
                </div>
                <div class="test-details">
                    {' • '.join(details[:3]) if details else 'No details available'}
                </div>
            </div>
"""
            cards.append(card)

        return "\n".join(cards)

    def _generate_issues_section(self, issues: List[str]) -> str:
        """Generate issues section if any exist."""
        if not issues:
            return ""

        issue_items = "\n".join(
            [f'<li class="issue-item">• {issue}</li>' for issue in issues[:10]]
        )

        return f"""
        <div class="issues-section">
            <div class="issues-title">⚠️ Issues Found ({len(issues)})</div>
            <ul class="issue-list">
                {issue_items}
                {f'<li class="issue-item">... and {len(issues) - 10} more</li>' if len(issues) > 10 else ''}
            </ul>
        </div>
"""

    def _generate_screenshots_section(
        self, package_name: str, screenshots: List[str]
    ) -> str:
        """Generate screenshots section."""
        if not screenshots:
            return ""

        screenshot_items = []
        for screenshot_path in screenshots[:4]:  # Show max 4 screenshots
            path = Path(screenshot_path)
            if path.exists():
                rel_path = path.relative_to(self.output_dir)
                label = path.stem.replace("_", " ").title()

                screenshot_items.append(
                    f"""
                <div class="screenshot">
                    <img src="{rel_path}" alt="{label}" loading="lazy">
                    <div class="screenshot-label">{label}</div>
                </div>
"""
                )

        return f"""
        <div class="screenshots">
            {' '.join(screenshot_items)}
        </div>
"""


@click.command()
@click.argument("results_file", type=click.Path(exists=True))
def main(results_file: str):
    """Generate HTML report from test results JSON file."""
    generator = TestReportGenerator(Path(results_file))
    report_path = generator.generate_html_report()

    click.echo(f"✅ Report generated: {report_path}")
    click.echo(f"📊 Open in browser: file://{report_path.absolute()}")


if __name__ == "__main__":
    main()
