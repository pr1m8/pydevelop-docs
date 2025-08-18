#!/usr/bin/env python
"""
Serve documentation and take screenshots for visual testing.
This script starts the documentation server and captures screenshots of key pages.
"""

import asyncio
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Error: playwright is not installed.")
    print("Please install it with: pip install playwright")
    print("Then run: playwright install chromium")
    sys.exit(1)


class DocServerScreenshotTester:
    def __init__(self, port=8004, docs_dir=None):
        self.port = port
        self.base_url = f"http://localhost:{port}"

        # Default to PyDevelop-Docs documentation
        if docs_dir is None:
            self.docs_dir = Path(__file__).parent.parent / "docs" / "build" / "html"
        else:
            self.docs_dir = Path(docs_dir)

        self.screenshot_dir = Path(__file__).parent.parent / "debug" / "screenshots"
        self.server_process = None

    def start_server(self):
        """Start the documentation server."""
        print(f"Starting documentation server on port {self.port}...")

        # Kill any existing server on this port
        subprocess.run(
            f"lsof -ti:{self.port} | xargs -r kill -9", shell=True, capture_output=True
        )

        # Start new server
        self.server_process = subprocess.Popen(
            ["python", "-m", "http.server", str(self.port)],
            cwd=self.docs_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Wait for server to start
        time.sleep(3)

        # Check if server is running
        try:
            import requests

            response = requests.get(self.base_url, timeout=5)
            if response.status_code == 200:
                print(f"✓ Server started successfully at {self.base_url}")
                return True
        except:
            pass

        print("✗ Failed to start server")
        return False

    def stop_server(self):
        """Stop the documentation server."""
        if self.server_process:
            print("Stopping documentation server...")
            self.server_process.terminate()
            self.server_process.wait()
            self.server_process = None

    async def take_screenshots(self):
        """Take screenshots of documentation pages."""
        # Create screenshot directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = self.screenshot_dir / f"pydevelop_docs_{timestamp}"
        session_dir.mkdir(parents=True, exist_ok=True)

        print(f"\nTaking screenshots to: {session_dir}")

        # Define pages to screenshot
        pages = [
            ("index", "/", "PyDevelop-Docs Home"),
            ("getting_started", "/getting_started.html", "Getting Started"),
            ("api_reference", "/autoapi/index.html", "API Reference"),
            (
                "api_config",
                "/autoapi/pydevelop_docs/config/index.html",
                "Config Module",
            ),
            ("api_cli", "/autoapi/pydevelop_docs/cli/index.html", "CLI Module"),
            (
                "api_builders",
                "/autoapi/pydevelop_docs/builders/index.html",
                "Builders Module",
            ),
            ("configuration", "/configuration.html", "Configuration Guide"),
            ("themes", "/themes.html", "Themes Guide"),
            ("search", "/search.html", "Search Page"),
        ]

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)

            # Test both light and dark themes
            for theme in ["light", "dark"]:
                print(f"\n{theme.upper()} THEME:")
                print("-" * 40)

                # Create new context for each theme
                context = await browser.new_context(
                    viewport={"width": 1920, "height": 1080}, color_scheme=theme
                )
                page = await context.new_page()

                for page_name, path, description in pages:
                    url = self.base_url + path
                    print(f"Screenshotting {description}... ", end="", flush=True)

                    try:
                        # Navigate to page
                        await page.goto(url, wait_until="networkidle")

                        # Wait for content to load
                        await page.wait_for_timeout(1000)

                        # Take full page screenshot
                        screenshot_path = session_dir / f"{page_name}_{theme}_full.png"
                        await page.screenshot(path=str(screenshot_path), full_page=True)

                        # Take viewport screenshot
                        viewport_path = (
                            session_dir / f"{page_name}_{theme}_viewport.png"
                        )
                        await page.screenshot(path=str(viewport_path), full_page=False)

                        # Check for common issues
                        issues = await self.check_page_issues(page)
                        if issues:
                            issues_path = (
                                session_dir / f"{page_name}_{theme}_issues.txt"
                            )
                            issues_path.write_text("\n".join(issues))
                            print(f"✓ (with {len(issues)} issues)")
                        else:
                            print("✓")

                    except Exception as e:
                        print(f"✗ Error: {e}")
                        error_path = session_dir / f"{page_name}_{theme}_error.txt"
                        error_path.write_text(f"Error capturing {url}:\n{str(e)}")

                await context.close()

            await browser.close()

        # Create summary report
        await self.create_summary_report(session_dir)
        print(f"\n✓ Screenshots complete! View them at:\n  {session_dir}")

    async def check_page_issues(self, page):
        """Check for common documentation issues."""
        issues = []

        # Check for missing navigation
        nav = await page.query_selector(".sidebar-tree")
        if not nav:
            issues.append("Missing navigation sidebar")

        # Check for missing TOC
        toc = await page.query_selector(".toc-tree")
        if not toc:
            # Furo theme uses different selector
            toc = await page.query_selector(".toctree-wrapper")
            if not toc:
                issues.append("Missing table of contents")

        # Check for white-on-white text in dark mode
        body_style = await page.evaluate("window.getComputedStyle(document.body)")
        if body_style.get("background-color") == "rgb(255, 255, 255)":
            text_elements = await page.query_selector_all("p, span, div")
            for elem in text_elements[:5]:  # Check first 5 elements
                color = await elem.evaluate("el => window.getComputedStyle(el).color")
                if color == "rgb(255, 255, 255)":
                    issues.append("Possible white-on-white text issue")
                    break

        # Check if AutoAPI content loaded
        if "autoapi" in page.url:
            api_content = await page.query_selector(".autoapi-summary")
            if not api_content:
                # Try Furo-specific selectors
                api_content = await page.query_selector("dl.py")
                if not api_content:
                    issues.append("AutoAPI content may not be loading")

        return issues

    async def create_summary_report(self, session_dir):
        """Create a summary report of the screenshot session."""
        report_lines = [
            "# PyDevelop-Docs Screenshot Test Report",
            f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"URL: {self.base_url}",
            f"Output: {session_dir}",
            "\n## Screenshots Taken\n",
        ]

        # List all screenshots
        screenshots = sorted(session_dir.glob("*.png"))
        for theme in ["light", "dark"]:
            report_lines.append(f"\n### {theme.title()} Theme\n")
            theme_shots = [s for s in screenshots if f"_{theme}_" in s.name]
            for shot in theme_shots:
                page_name = shot.stem.replace(f"_{theme}_full", "").replace(
                    f"_{theme}_viewport", ""
                )
                shot_type = "Full Page" if "_full" in shot.name else "Viewport"
                report_lines.append(f"- **{page_name}** ({shot_type}): `{shot.name}`")

                # Check for issues file
                issues_file = session_dir / f"{page_name}_{theme}_issues.txt"
                if issues_file.exists():
                    issues = issues_file.read_text().strip()
                    report_lines.append(f"  - ⚠️ Issues: {issues}")

        # Write report
        report_path = session_dir / "REPORT.md"
        report_path.write_text("\n".join(report_lines))

    async def run(self):
        """Run the complete serve and screenshot test."""
        try:
            # Start server
            if not self.start_server():
                print("Failed to start server. Exiting.")
                return 1

            # Take screenshots
            await self.take_screenshots()

            return 0

        finally:
            # Always stop server
            self.stop_server()


async def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Serve docs and take screenshots")
    parser.add_argument("--port", type=int, default=8004, help="Port to serve on")
    parser.add_argument("--docs-dir", help="Documentation directory to serve")
    parser.add_argument("--package", help="Haive package name (e.g., haive-core)")

    args = parser.parse_args()

    # If package specified, use its docs
    docs_dir = args.docs_dir
    if args.package and not docs_dir:
        package_docs = Path(
            f"/home/will/Projects/haive/backend/haive/packages/{args.package}/docs/build/html"
        )
        if package_docs.exists():
            docs_dir = package_docs
            print(f"Using {args.package} documentation at: {docs_dir}")

    tester = DocServerScreenshotTester(port=args.port, docs_dir=docs_dir)
    return await tester.run()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
