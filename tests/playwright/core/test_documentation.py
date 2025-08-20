#!/usr/bin/env python3
"""Comprehensive Playwright tests for generated documentation.

Tests functionality, visual appearance, links, navigation, search, and more.
Generates timestamped reports and screenshots for each package.
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse

import click
from playwright.async_api import Browser, BrowserContext, Page, async_playwright


class DocumentationTester:
    """Comprehensive documentation testing with Playwright."""

    def __init__(self, base_dir: Path, output_dir: Path = None):
        """Initialize documentation tester.

        Args:
            base_dir: Root directory containing package documentation
            output_dir: Directory for test results (default: test_results_{timestamp})
        """
        self.base_dir = Path(base_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = output_dir or Path(f"test_results_{self.timestamp}")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Test results storage
        self.results = {
            "timestamp": self.timestamp,
            "base_dir": str(self.base_dir),
            "packages": {},
            "summary": {
                "total_packages": 0,
                "passed": 0,
                "failed": 0,
                "total_tests": 0,
                "total_issues": 0,
            },
        }

        # Configure test timeouts
        self.page_load_timeout = 30000  # 30 seconds
        self.navigation_timeout = 10000  # 10 seconds

    async def test_all_packages(self):
        """Test all package documentation."""
        packages = self._find_package_docs()
        self.results["summary"]["total_packages"] = len(packages)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)

            for package_name, doc_path in packages.items():
                click.echo(f"\n{'='*80}")
                click.echo(f"📦 Testing {package_name} documentation")
                click.echo(f"{'='*80}")

                package_results = await self._test_package(
                    browser, package_name, doc_path
                )
                self.results["packages"][package_name] = package_results

                if package_results["passed"]:
                    self.results["summary"]["passed"] += 1
                else:
                    self.results["summary"]["failed"] += 1

                self.results["summary"]["total_tests"] += package_results["total_tests"]
                self.results["summary"]["total_issues"] += len(
                    package_results["issues"]
                )

            await browser.close()

        # Save final results
        self._save_results()
        self._print_summary()

    def _find_package_docs(self) -> Dict[str, Path]:
        """Find all package documentation directories."""
        packages = {}

        # Look for packages/*/docs/build/html/index.html
        for package_dir in (self.base_dir / "packages").iterdir():
            if package_dir.is_dir():
                index_path = package_dir / "docs" / "build" / "html" / "index.html"
                if index_path.exists():
                    packages[package_dir.name] = index_path.parent

        return packages

    async def _test_package(
        self, browser: Browser, package_name: str, doc_path: Path
    ) -> Dict:
        """Test a single package documentation.

        Returns:
            Dictionary with test results for the package
        """
        # Create package output directory
        package_output = self.output_dir / package_name
        package_output.mkdir(exist_ok=True)

        # Initialize results
        results = {
            "package": package_name,
            "doc_path": str(doc_path),
            "timestamp": datetime.now().isoformat(),
            "tests": {},
            "issues": [],
            "screenshots": [],
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "passed": True,
        }

        # Create browser context with specific viewport
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080}, device_scale_factor=1
        )

        page = await context.new_page()

        # Run all tests
        test_methods = [
            ("homepage", self._test_homepage),
            ("navigation", self._test_navigation),
            ("api_reference", self._test_api_reference),
            ("search", self._test_search_functionality),
            ("links", self._test_all_links),
            ("images", self._test_images),
            ("code_blocks", self._test_code_blocks),
            ("responsive", self._test_responsive_design),
            ("dark_mode", self._test_dark_mode),
            ("performance", self._test_page_performance),
        ]

        for test_name, test_method in test_methods:
            click.echo(f"  🧪 Running {test_name} test...")

            try:
                test_result = await test_method(page, doc_path, package_output)
                results["tests"][test_name] = test_result
                results["total_tests"] += 1

                if test_result["passed"]:
                    results["passed_tests"] += 1
                    click.echo(f"    ✅ {test_name}: PASSED")
                else:
                    results["failed_tests"] += 1
                    results["passed"] = False
                    click.echo(f"    ❌ {test_name}: FAILED - {test_result['error']}")

                # Collect issues
                if "issues" in test_result:
                    results["issues"].extend(test_result["issues"])

                # Collect screenshots
                if "screenshot" in test_result:
                    results["screenshots"].append(test_result["screenshot"])

            except Exception as e:
                results["tests"][test_name] = {
                    "passed": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
                results["failed_tests"] += 1
                results["passed"] = False
                click.echo(f"    ❌ {test_name}: ERROR - {e}")

        await context.close()

        # Save package results
        package_results_file = package_output / "test_results.json"
        with open(package_results_file, "w") as f:
            json.dump(results, f, indent=2)

        return results

    async def _test_homepage(
        self, page: Page, doc_path: Path, output_dir: Path
    ) -> Dict:
        """Test the documentation homepage."""
        result = {
            "passed": True,
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "issues": [],
        }

        # Load homepage
        homepage_url = f"file://{doc_path}/index.html"
        await page.goto(
            homepage_url, wait_until="networkidle", timeout=self.page_load_timeout
        )

        # Take screenshot
        screenshot_path = output_dir / f"homepage_{self.timestamp}.png"
        await page.screenshot(path=str(screenshot_path), full_page=True)
        result["screenshot"] = str(screenshot_path)

        # Check title
        title = await page.title()
        result["checks"]["has_title"] = bool(title)
        if not title:
            result["issues"].append("Missing page title")
            result["passed"] = False

        # Check main heading
        h1_elements = await page.query_selector_all("h1")
        result["checks"]["has_h1"] = len(h1_elements) > 0
        if not h1_elements:
            result["issues"].append("Missing main heading (h1)")

        # Check navigation sidebar
        sidebar = await page.query_selector(".sidebar-container, .bd-sidebar, nav")
        result["checks"]["has_sidebar"] = sidebar is not None
        if not sidebar:
            result["issues"].append("Missing navigation sidebar")
            result["passed"] = False

        # Check search box
        search = await page.query_selector(
            "input[type='search'], .search-field, #searchbox"
        )
        result["checks"]["has_search"] = search is not None
        if not search:
            result["issues"].append("Missing search functionality")

        # Check footer
        footer = await page.query_selector("footer, .footer")
        result["checks"]["has_footer"] = footer is not None

        # Check for broken images
        images = await page.query_selector_all("img")
        broken_images = []
        for img in images:
            src = await img.get_attribute("src")
            if src:
                # Check if image loads
                is_broken = await page.evaluate(
                    """
                    (img) => {
                        return !img.complete || img.naturalWidth === 0;
                    }
                """,
                    img,
                )
                if is_broken:
                    broken_images.append(src)

        result["checks"]["broken_images"] = len(broken_images)
        if broken_images:
            result["issues"].extend([f"Broken image: {img}" for img in broken_images])
            result["passed"] = False

        return result

    async def _test_navigation(
        self, page: Page, doc_path: Path, output_dir: Path
    ) -> Dict:
        """Test navigation functionality."""
        result = {
            "passed": True,
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "issues": [],
        }

        # Load homepage
        homepage_url = f"file://{doc_path}/index.html"
        await page.goto(homepage_url, wait_until="networkidle")

        # Find all navigation links
        nav_links = await page.query_selector_all("nav a, .sidebar a, .toctree a")
        result["checks"]["nav_link_count"] = len(nav_links)

        if not nav_links:
            result["issues"].append("No navigation links found")
            result["passed"] = False
            return result

        # Test first 5 navigation links
        tested_links = []
        for i, link in enumerate(nav_links[:5]):
            href = await link.get_attribute("href")
            text = await link.text_content()

            if href and not href.startswith("#"):
                try:
                    # Click the link
                    await link.click(timeout=self.navigation_timeout)
                    await page.wait_for_load_state("networkidle")

                    # Check if navigation worked
                    current_url = page.url
                    tested_links.append(
                        {
                            "text": text.strip(),
                            "href": href,
                            "success": True,
                            "url": current_url,
                        }
                    )

                    # Go back
                    await page.go_back()

                except Exception as e:
                    tested_links.append(
                        {
                            "text": text.strip(),
                            "href": href,
                            "success": False,
                            "error": str(e),
                        }
                    )
                    result["issues"].append(f"Navigation failed for '{text}': {e}")

        result["checks"]["tested_links"] = tested_links

        # Check for navigation hierarchy
        toc_tree = await page.query_selector(".toctree-wrapper, .toc-tree")
        result["checks"]["has_toc_tree"] = toc_tree is not None

        # Take navigation screenshot
        screenshot_path = output_dir / f"navigation_{self.timestamp}.png"
        await page.screenshot(path=str(screenshot_path))
        result["screenshot"] = str(screenshot_path)

        return result

    async def _test_api_reference(
        self, page: Page, doc_path: Path, output_dir: Path
    ) -> Dict:
        """Test API reference documentation."""
        result = {
            "passed": True,
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "issues": [],
        }

        # Look for API reference link
        homepage_url = f"file://{doc_path}/index.html"
        await page.goto(homepage_url, wait_until="networkidle")

        # Find API reference link
        api_link = await page.query_selector(
            "a[href*='autoapi'], a[href*='api'], a:text('API Reference')"
        )

        if not api_link:
            result["issues"].append("No API reference link found")
            result["checks"]["has_api_link"] = False
            return result

        result["checks"]["has_api_link"] = True

        # Navigate to API reference
        await api_link.click()
        await page.wait_for_load_state("networkidle")

        # Check for class/function documentation
        classes = await page.query_selector_all(".class, .py-class, [class*='class']")
        functions = await page.query_selector_all(
            ".function, .py-function, [class*='function']"
        )
        modules = await page.query_selector_all(
            ".module, .py-module, [class*='module']"
        )

        result["checks"]["class_count"] = len(classes)
        result["checks"]["function_count"] = len(functions)
        result["checks"]["module_count"] = len(modules)

        if not classes and not functions:
            result["issues"].append(
                "No API documentation found (no classes or functions)"
            )
            result["passed"] = False

        # Check for code examples
        code_blocks = await page.query_selector_all("pre, .highlight, .codehilite")
        result["checks"]["code_example_count"] = len(code_blocks)

        # Take API screenshot
        screenshot_path = output_dir / f"api_reference_{self.timestamp}.png"
        await page.screenshot(path=str(screenshot_path), full_page=True)
        result["screenshot"] = str(screenshot_path)

        return result

    async def _test_search_functionality(
        self, page: Page, doc_path: Path, output_dir: Path
    ) -> Dict:
        """Test search functionality."""
        result = {
            "passed": True,
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "issues": [],
        }

        homepage_url = f"file://{doc_path}/index.html"
        await page.goto(homepage_url, wait_until="networkidle")

        # Find search input
        search_input = await page.query_selector(
            "input[type='search'], .search-field, #searchbox input"
        )

        if not search_input:
            result["issues"].append("No search input found")
            result["passed"] = False
            result["checks"]["has_search_input"] = False
            return result

        result["checks"]["has_search_input"] = True

        # Try searching
        search_term = "class"
        await search_input.fill(search_term)
        await search_input.press("Enter")

        # Wait for search results
        await page.wait_for_timeout(2000)  # Wait 2 seconds for results

        # Check for search results
        search_results = await page.query_selector_all(
            ".search-results li, .search-result-item, [class*='search-result']"
        )
        result["checks"]["search_result_count"] = len(search_results)

        if not search_results:
            result["issues"].append(f"No search results found for '{search_term}'")

        # Take search screenshot
        screenshot_path = output_dir / f"search_results_{self.timestamp}.png"
        await page.screenshot(path=str(screenshot_path))
        result["screenshot"] = str(screenshot_path)

        return result

    async def _test_all_links(
        self, page: Page, doc_path: Path, output_dir: Path
    ) -> Dict:
        """Test all internal links."""
        result = {
            "passed": True,
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "issues": [],
        }

        homepage_url = f"file://{doc_path}/index.html"
        await page.goto(homepage_url, wait_until="networkidle")

        # Collect all links
        all_links = await page.query_selector_all("a[href]")
        result["checks"]["total_links"] = len(all_links)

        broken_links = []
        external_links = []
        checked_urls = set()

        for link in all_links[:50]:  # Check first 50 links
            href = await link.get_attribute("href")
            if not href or href in checked_urls:
                continue

            checked_urls.add(href)

            # Skip anchors and external links
            if href.startswith("#"):
                continue
            if href.startswith(("http://", "https://", "mailto:")):
                external_links.append(href)
                continue

            # Test internal link
            try:
                full_url = urljoin(homepage_url, href)
                response = await page.request.get(full_url)
                if response.status >= 400:
                    broken_links.append(
                        {
                            "href": href,
                            "status": response.status,
                            "text": await link.text_content(),
                        }
                    )
            except Exception as e:
                broken_links.append(
                    {"href": href, "error": str(e), "text": await link.text_content()}
                )

        result["checks"]["broken_links"] = len(broken_links)
        result["checks"]["external_links"] = len(external_links)

        if broken_links:
            result["issues"].extend(
                [f"Broken link: {link['href']}" for link in broken_links]
            )
            result["passed"] = False
            result["broken_link_details"] = broken_links

        return result

    async def _test_images(self, page: Page, doc_path: Path, output_dir: Path) -> Dict:
        """Test all images load correctly."""
        result = {
            "passed": True,
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "issues": [],
        }

        homepage_url = f"file://{doc_path}/index.html"
        await page.goto(homepage_url, wait_until="networkidle")

        # Find all images
        images = await page.query_selector_all("img")
        result["checks"]["total_images"] = len(images)

        missing_alt = []
        broken_images = []

        for img in images:
            src = await img.get_attribute("src")
            alt = await img.get_attribute("alt")

            # Check alt text
            if not alt:
                missing_alt.append(src or "unknown")

            # Check if image loads
            if src:
                is_broken = await page.evaluate(
                    """
                    (img) => {
                        return !img.complete || img.naturalWidth === 0;
                    }
                """,
                    img,
                )

                if is_broken:
                    broken_images.append(src)

        result["checks"]["missing_alt_text"] = len(missing_alt)
        result["checks"]["broken_images"] = len(broken_images)

        if missing_alt:
            result["issues"].append(f"{len(missing_alt)} images missing alt text")

        if broken_images:
            result["issues"].extend([f"Broken image: {img}" for img in broken_images])
            result["passed"] = False

        return result

    async def _test_code_blocks(
        self, page: Page, doc_path: Path, output_dir: Path
    ) -> Dict:
        """Test code blocks and syntax highlighting."""
        result = {
            "passed": True,
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "issues": [],
        }

        # Navigate to API reference for code blocks
        homepage_url = f"file://{doc_path}/index.html"
        await page.goto(homepage_url, wait_until="networkidle")

        # Find API link and navigate
        api_link = await page.query_selector("a[href*='autoapi'], a[href*='api']")
        if api_link:
            await api_link.click()
            await page.wait_for_load_state("networkidle")

        # Find code blocks
        code_blocks = await page.query_selector_all(
            "pre, .highlight, .codehilite, .code-block"
        )
        result["checks"]["code_block_count"] = len(code_blocks)

        if not code_blocks:
            result["issues"].append("No code blocks found")
            return result

        # Check syntax highlighting
        highlighted_blocks = 0
        copy_buttons = 0

        for block in code_blocks[:10]:  # Check first 10
            # Check for syntax highlighting classes
            classes = await block.get_attribute("class") or ""
            if any(
                lang in classes
                for lang in ["python", "bash", "json", "yaml", "language-"]
            ):
                highlighted_blocks += 1

            # Check for copy button
            parent = await block.evaluate_handle("el => el.parentElement")
            copy_btn = await parent.query_selector(
                ".copybtn, .copy-button, button[aria-label*='copy']"
            )
            if copy_btn:
                copy_buttons += 1

        result["checks"]["highlighted_blocks"] = highlighted_blocks
        result["checks"]["copy_buttons"] = copy_buttons

        if highlighted_blocks == 0:
            result["issues"].append("No syntax highlighting found")

        # Take code block screenshot
        if code_blocks:
            screenshot_path = output_dir / f"code_blocks_{self.timestamp}.png"
            await code_blocks[0].screenshot(path=str(screenshot_path))
            result["screenshot"] = str(screenshot_path)

        return result

    async def _test_responsive_design(
        self, page: Page, doc_path: Path, output_dir: Path
    ) -> Dict:
        """Test responsive design at different viewport sizes."""
        result = {
            "passed": True,
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "issues": [],
            "screenshots": [],
        }

        homepage_url = f"file://{doc_path}/index.html"

        # Test different viewport sizes
        viewports = [
            {"name": "mobile", "width": 375, "height": 667},
            {"name": "tablet", "width": 768, "height": 1024},
            {"name": "desktop", "width": 1920, "height": 1080},
        ]

        for viewport in viewports:
            await page.set_viewport_size(
                {"width": viewport["width"], "height": viewport["height"]}
            )

            await page.goto(homepage_url, wait_until="networkidle")

            # Take screenshot
            screenshot_path = (
                output_dir / f"responsive_{viewport['name']}_{self.timestamp}.png"
            )
            await page.screenshot(path=str(screenshot_path))
            result["screenshots"].append(str(screenshot_path))

            # Check if content is visible
            content = await page.query_selector("main, .content, #content")
            if content:
                is_visible = await content.is_visible()
                result["checks"][f"{viewport['name']}_content_visible"] = is_visible
                if not is_visible:
                    result["issues"].append(
                        f"Content not visible on {viewport['name']}"
                    )
                    result["passed"] = False

            # Check if navigation is accessible
            if viewport["name"] == "mobile":
                # Look for hamburger menu
                hamburger = await page.query_selector(
                    ".navbar-toggler, .menu-toggle, .mobile-menu"
                )
                result["checks"]["mobile_menu_present"] = hamburger is not None

        return result

    async def _test_dark_mode(
        self, page: Page, doc_path: Path, output_dir: Path
    ) -> Dict:
        """Test dark mode functionality if available."""
        result = {
            "passed": True,
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "issues": [],
        }

        homepage_url = f"file://{doc_path}/index.html"
        await page.goto(homepage_url, wait_until="networkidle")

        # Look for theme toggle
        theme_toggle = await page.query_selector(
            "[aria-label*='theme'], .theme-toggle, button[title*='theme']"
        )

        if not theme_toggle:
            result["checks"]["has_theme_toggle"] = False
            return result

        result["checks"]["has_theme_toggle"] = True

        # Take light mode screenshot
        light_screenshot = output_dir / f"theme_light_{self.timestamp}.png"
        await page.screenshot(path=str(light_screenshot))

        # Toggle to dark mode
        await theme_toggle.click()
        await page.wait_for_timeout(500)  # Wait for transition

        # Take dark mode screenshot
        dark_screenshot = output_dir / f"theme_dark_{self.timestamp}.png"
        await page.screenshot(path=str(dark_screenshot))

        result["screenshots"] = [str(light_screenshot), str(dark_screenshot)]

        # Check if theme actually changed
        body_classes = await page.evaluate("document.body.className")
        html_attrs = await page.evaluate(
            "document.documentElement.getAttribute('data-theme')"
        )

        result["checks"]["theme_changed"] = (
            "dark" in body_classes or html_attrs == "dark"
        )

        if not result["checks"]["theme_changed"]:
            result["issues"].append("Theme toggle doesn't appear to work")
            result["passed"] = False

        return result

    async def _test_page_performance(
        self, page: Page, doc_path: Path, output_dir: Path
    ) -> Dict:
        """Test page load performance."""
        result = {
            "passed": True,
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "issues": [],
        }

        homepage_url = f"file://{doc_path}/index.html"

        # Measure load time
        start_time = datetime.now()
        await page.goto(homepage_url, wait_until="networkidle")
        load_time = (datetime.now() - start_time).total_seconds()

        result["checks"]["load_time_seconds"] = load_time

        # Get performance metrics
        metrics = await page.evaluate(
            """
            () => {
                const timing = performance.timing;
                return {
                    domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
                    fullLoad: timing.loadEventEnd - timing.navigationStart
                };
            }
        """
        )

        result["checks"]["dom_content_loaded_ms"] = metrics.get("domContentLoaded", 0)
        result["checks"]["full_load_ms"] = metrics.get("fullLoad", 0)

        # Check file sizes
        resource_sizes = await page.evaluate(
            """
            () => {
                const resources = performance.getEntriesByType('resource');
                let totalSize = 0;
                let largeFiles = [];
                
                resources.forEach(resource => {
                    if (resource.transferSize) {
                        totalSize += resource.transferSize;
                        if (resource.transferSize > 1024 * 1024) {  // > 1MB
                            largeFiles.push({
                                name: resource.name,
                                size: resource.transferSize
                            });
                        }
                    }
                });
                
                return {
                    totalSize: totalSize,
                    largeFiles: largeFiles
                };
            }
        """
        )

        result["checks"]["total_resource_size_bytes"] = resource_sizes.get(
            "totalSize", 0
        )
        result["checks"]["large_files"] = resource_sizes.get("largeFiles", [])

        # Performance thresholds
        if load_time > 5:
            result["issues"].append(f"Slow page load: {load_time:.2f} seconds")
            result["passed"] = False

        if resource_sizes.get("largeFiles"):
            result["issues"].append(
                f"{len(resource_sizes['largeFiles'])} files larger than 1MB"
            )

        return result

    def _save_results(self):
        """Save test results to JSON file."""
        results_file = self.output_dir / f"test_results_{self.timestamp}.json"
        with open(results_file, "w") as f:
            json.dump(self.results, f, indent=2)

        click.echo(f"\n💾 Results saved to: {results_file}")

    def _print_summary(self):
        """Print test summary."""
        summary = self.results["summary"]

        click.echo("\n" + "=" * 80)
        click.echo("📊 DOCUMENTATION TEST SUMMARY")
        click.echo("=" * 80)
        click.echo(f"Timestamp:        {self.timestamp}")
        click.echo(f"Packages Tested:  {summary['total_packages']}")
        click.echo(f"Passed:           {summary['passed']} ✅")
        click.echo(f"Failed:           {summary['failed']} ❌")
        click.echo(f"Total Tests:      {summary['total_tests']}")
        click.echo(f"Total Issues:     {summary['total_issues']}")
        click.echo()

        # Package details
        click.echo("Package Results:")
        for pkg_name, pkg_results in self.results["packages"].items():
            status = "✅" if pkg_results["passed"] else "❌"
            click.echo(
                f"  {status} {pkg_name}: {pkg_results['passed_tests']}/{pkg_results['total_tests']} tests passed"
            )
            if pkg_results["issues"]:
                click.echo(f"     Issues: {len(pkg_results['issues'])}")


@click.command()
@click.option(
    "--base-dir",
    "-b",
    default="/home/will/Projects/haive/backend/haive",
    help="Base directory containing packages",
)
@click.option("--output-dir", "-o", help="Output directory for test results")
@click.option("--package", "-p", help="Test specific package only")
def main(base_dir: str, output_dir: Optional[str], package: Optional[str]):
    """Run comprehensive documentation tests with Playwright."""
    base_path = Path(base_dir)

    if not base_path.exists():
        click.echo(f"❌ Base directory not found: {base_path}")
        return

    output_path = Path(output_dir) if output_dir else None

    tester = DocumentationTester(base_path, output_path)

    click.echo("🧪 Starting Documentation Tests with Playwright")
    click.echo(f"📁 Base directory: {base_path}")
    click.echo(f"📁 Output directory: {tester.output_dir}")
    click.echo()

    # Run tests
    asyncio.run(tester.test_all_packages())


if __name__ == "__main__":
    main()
