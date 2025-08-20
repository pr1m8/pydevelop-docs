#!/usr/bin/env python3
"""
Screenshot a specific documentation page.
"""
import asyncio
import sys
from datetime import datetime
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Playwright not installed. Run: pip install playwright")
    print("Then run: playwright install chromium")
    exit(1)


async def screenshot_specific_page(url: str, output_prefix: str = "screenshot"):
    """Take screenshots of a specific documentation page in both themes."""

    # Setup paths
    screenshots_dir = Path("debug/screenshots")
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(
            headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"]
        )

        print(f"📸 Screenshotting: {url}")
        print(f"📁 Output directory: {screenshots_dir}")
        print("-" * 80)

        # Light theme
        print("🌞 Capturing light theme...")
        light_context = await browser.new_context(
            viewport={"width": 1920, "height": 1080}, color_scheme="light"
        )
        light_page = await light_context.new_page()

        await light_page.goto(url, wait_until="networkidle", timeout=30000)
        await light_page.wait_for_timeout(2000)

        # Full page screenshot
        light_full_path = (
            screenshots_dir / f"{output_prefix}_{timestamp}_light_full.png"
        )
        await light_page.screenshot(path=str(light_full_path), full_page=True)
        print(f"✅ Saved: {light_full_path}")

        # Viewport screenshot
        light_viewport_path = (
            screenshots_dir / f"{output_prefix}_{timestamp}_light_viewport.png"
        )
        await light_page.screenshot(path=str(light_viewport_path), full_page=False)
        print(f"✅ Saved: {light_viewport_path}")

        # Check for issues
        light_issues = await check_issues(light_page)
        print(f"   Issues: {light_issues}")

        await light_context.close()

        # Dark theme
        print("\n🌙 Capturing dark theme...")
        dark_context = await browser.new_context(
            viewport={"width": 1920, "height": 1080}, color_scheme="dark"
        )
        dark_page = await dark_context.new_page()

        await dark_page.goto(url, wait_until="networkidle", timeout=30000)
        await dark_page.wait_for_timeout(2000)

        # Full page screenshot
        dark_full_path = screenshots_dir / f"{output_prefix}_{timestamp}_dark_full.png"
        await dark_page.screenshot(path=str(dark_full_path), full_page=True)
        print(f"✅ Saved: {dark_full_path}")

        # Viewport screenshot
        dark_viewport_path = (
            screenshots_dir / f"{output_prefix}_{timestamp}_dark_viewport.png"
        )
        await dark_page.screenshot(path=str(dark_viewport_path), full_page=False)
        print(f"✅ Saved: {dark_viewport_path}")

        # Check for issues
        dark_issues = await check_issues(dark_page)
        print(f"   Issues: {dark_issues}")

        await dark_context.close()
        await browser.close()

        print("-" * 80)
        print(f"🎯 Screenshots complete!")
        print(f"\nView with:")
        print(f"  xdg-open {light_full_path}  # Linux")
        print(f"  open {light_full_path}      # macOS")


async def check_issues(page):
    """Quick check for common issues."""
    issues = []

    # Check navigation
    nav = await page.locator(".sidebar, .bd-sidebar, .wy-nav-side").count()
    if nav == 0:
        issues.append("No sidebar")

    # Check toctree
    toc = await page.locator(".toctree, .toctree-wrapper").count()
    if toc == 0:
        issues.append("No toctree")

    # Check for content
    content = await page.locator("h1, h2, h3").count()
    if content == 0:
        issues.append("No headings")

    return ", ".join(issues) if issues else "None detected"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python screenshot_specific.py <url> [output_prefix]")
        print(
            "Example: python screenshot_specific.py http://localhost:8003/autoapi/mcp/downloader/config/index.html downloader_config"
        )
        exit(1)

    url = sys.argv[1]
    output_prefix = sys.argv[2] if len(sys.argv) > 2 else "specific_page"

    asyncio.run(screenshot_specific_page(url, output_prefix))
