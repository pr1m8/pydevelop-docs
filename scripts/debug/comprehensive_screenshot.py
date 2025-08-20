#!/usr/bin/env python3
"""
Comprehensive screenshot utility for PyDevelop-Docs documentation.
Takes screenshots of multiple pages including index and specific module pages.
"""
import asyncio
import os
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Playwright not installed. Run: pip install playwright")
    print("Then run: playwright install chromium")
    exit(1)


async def take_comprehensive_screenshots(port: int = 8003):
    """Take comprehensive screenshots of PyDevelop-Docs documentation."""

    # Setup paths
    screenshots_dir = Path("debug/screenshots")
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = screenshots_dir / f"comprehensive_{timestamp}"
    session_dir.mkdir(exist_ok=True)

    # Base URL
    base_url = f"http://localhost:{port}"

    # URLs to capture - comprehensive list
    urls_to_capture: List[Tuple[str, str]] = [
        # Main pages
        ("01_index", f"{base_url}/index.html"),
        ("02_autoapi_index", f"{base_url}/autoapi/index.html"),
        # Main module
        ("03_mcp_module", f"{base_url}/autoapi/mcp/index.html"),
        # Submodules
        ("04_agents", f"{base_url}/autoapi/mcp/agents/index.html"),
        ("05_cli", f"{base_url}/autoapi/mcp/cli/index.html"),
        ("06_config", f"{base_url}/autoapi/mcp/config/index.html"),
        ("07_discovery", f"{base_url}/autoapi/mcp/discovery/index.html"),
        ("08_documentation", f"{base_url}/autoapi/mcp/documentation/index.html"),
        ("09_downloader", f"{base_url}/autoapi/mcp/downloader/index.html"),
        # Specific requested page
        (
            "10_downloader_config",
            f"{base_url}/autoapi/mcp/downloader/config/index.html",
        ),
        # More submodules
        ("11_installers", f"{base_url}/autoapi/mcp/installers/index.html"),
        ("12_integration", f"{base_url}/autoapi/mcp/integration/index.html"),
        ("13_launcher", f"{base_url}/autoapi/mcp/launcher/index.html"),
        ("14_manager", f"{base_url}/autoapi/mcp/manager/index.html"),
        ("15_mixins", f"{base_url}/autoapi/mcp/mixins/index.html"),
        ("16_servers", f"{base_url}/autoapi/mcp/servers/index.html"),
        ("17_tools", f"{base_url}/autoapi/mcp/tools/index.html"),
        ("18_utils", f"{base_url}/autoapi/mcp/utils/index.html"),
        # Some specific classes/functions
        ("19_mcp_agent", f"{base_url}/autoapi/mcp/agents/mcp_agent/index.html"),
        ("20_mcp_manager", f"{base_url}/autoapi/mcp/cli/mcp_manager/index.html"),
    ]

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(
            headless=True,  # Set to False to see browser
            args=["--no-sandbox", "--disable-setuid-sandbox"],
        )

        # Create contexts for different themes
        contexts = {
            "light": await browser.new_context(
                viewport={"width": 1920, "height": 1080}, color_scheme="light"
            ),
            "dark": await browser.new_context(
                viewport={"width": 1920, "height": 1080}, color_scheme="dark"
            ),
        }

        print(f"📸 Starting comprehensive screenshot session: {timestamp}")
        print(f"📁 Screenshots will be saved to: {session_dir}")
        print(f"🌐 Base URL: {base_url}")
        print("-" * 80)

        # Capture each URL in both themes
        for name, url in urls_to_capture:
            for theme, context in contexts.items():
                page = await context.new_page()

                try:
                    print(f"📸 Capturing {name} ({theme} theme)")
                    print(f"   URL: {url}")

                    # Navigate to page
                    response = await page.goto(
                        url, wait_until="networkidle", timeout=30000
                    )

                    if response and response.status != 200:
                        print(f"   ⚠️ HTTP {response.status}")

                    # Wait for content to stabilize
                    await page.wait_for_timeout(2000)

                    # Take full page screenshot
                    full_path = session_dir / f"{name}_{theme}_full.png"
                    await page.screenshot(
                        path=str(full_path), full_page=True, type="png"
                    )
                    print(f"   ✅ Full page saved")

                    # Take viewport screenshot (above the fold)
                    viewport_path = session_dir / f"{name}_{theme}_viewport.png"
                    await page.screenshot(
                        path=str(viewport_path), full_page=False, type="png"
                    )
                    print(f"   ✅ Viewport saved")

                    # Check for specific issues
                    await check_page_issues(page, name, theme, session_dir)

                except Exception as e:
                    print(f"   ❌ Error: {e}")
                    error_path = session_dir / f"{name}_{theme}_error.txt"
                    error_path.write_text(f"Error: {e}\nURL: {url}\nTheme: {theme}\n")

                finally:
                    await page.close()

        # Close contexts
        for context in contexts.values():
            await context.close()

        await browser.close()

    # Create summary report
    create_summary_report(session_dir, timestamp, urls_to_capture)
    print("-" * 80)
    print(f"🎯 Session complete! Total screenshots: {len(urls_to_capture) * 2 * 2}")
    print(f"📁 Results saved to: {session_dir}")
    print(f"📊 View summary: {session_dir}/SUMMARY.md")


async def check_page_issues(page, name: str, theme: str, session_dir: Path):
    """Check for specific visual and structural issues on the page."""
    issues = []

    try:
        # Check for navigation elements
        nav_found = await page.locator(".sidebar, .bd-sidebar, .wy-nav-side").count()
        if nav_found > 0:
            issues.append(f"✅ Navigation found: {nav_found} elements")
        else:
            issues.append("❌ No navigation sidebar found")

        # Check for toctree
        toctree_found = await page.locator(".toctree, .toctree-wrapper").count()
        if toctree_found > 0:
            issues.append(f"✅ TOC tree found: {toctree_found} elements")
        else:
            issues.append("⚠️ No TOC tree found")

        # Check for white-on-white text issues
        if theme == "dark":
            white_text_elements = await page.evaluate(
                """
                () => {
                    const elements = Array.from(document.querySelectorAll('*'));
                    return elements.filter(el => {
                        const style = window.getComputedStyle(el);
                        const color = style.color;
                        const bgColor = style.backgroundColor;
                        
                        // Check for white text
                        const isWhiteText = color.includes('rgb(255, 255, 255)') || 
                                          color.includes('#fff') || 
                                          color.includes('#ffffff');
                        
                        // Check for white/light background
                        const isLightBg = bgColor.includes('rgb(255, 255, 255)') ||
                                        bgColor.includes('rgb(254, 254, 254)') ||
                                        bgColor.includes('rgb(253, 253, 253)');
                        
                        return isWhiteText && isLightBg;
                    }).length;
                }
            """
            )

            if white_text_elements > 0:
                issues.append(
                    f"⚠️ Potential white-on-white text: {white_text_elements} elements"
                )

        # Check for CSS loading
        css_count = await page.evaluate("() => document.styleSheets.length")
        issues.append(f"📊 CSS files loaded: {css_count}")

        # Check for AutoAPI content
        autoapi_content = await page.locator(".autoapi, [class*='autoapi']").count()
        if autoapi_content > 0:
            issues.append(f"✅ AutoAPI content found: {autoapi_content} elements")

        # Check for source links
        source_links = await page.locator(
            "a[href*='github'], a:has-text('[source]')"
        ).count()
        if source_links > 0:
            issues.append(f"✅ Source links found: {source_links}")
        else:
            issues.append("⚠️ No source links found")

        # Save issues report
        issues_path = session_dir / f"{name}_{theme}_issues.txt"
        issues_path.write_text("\n".join(issues))

        # Print critical issues
        critical = [i for i in issues if "❌" in i or "⚠️" in i]
        if critical:
            print(f"   ⚠️ Issues: {', '.join(critical)}")

    except Exception as e:
        print(f"   ❌ Error checking issues: {e}")


def create_summary_report(
    session_dir: Path, timestamp: str, urls: List[Tuple[str, str]]
):
    """Create a comprehensive summary report of the screenshot session."""

    summary = f"""# PyDevelop-Docs Screenshot Session Report

**Timestamp**: {timestamp}  
**Directory**: {session_dir}  
**Total Pages**: {len(urls)}  
**Total Screenshots**: {len(urls) * 2 * 2} (full + viewport × light + dark)

## Pages Captured

| Page | URL | Light Theme | Dark Theme |
|------|-----|-------------|------------|
"""

    for name, url in urls:
        # Check if files exist
        light_exists = (
            "✅" if (session_dir / f"{name}_light_full.png").exists() else "❌"
        )
        dark_exists = "✅" if (session_dir / f"{name}_dark_full.png").exists() else "❌"

        # Clean URL for display
        clean_url = url.replace("http://localhost:8003", "")

        summary += f"| {name.replace('_', ' ').title()} | `{clean_url}` | {light_exists} | {dark_exists} |\n"

    summary += f"""

## Quick Analysis

### Check for Issues
```bash
cd {session_dir}
grep -h "❌\\|⚠️" *_issues.txt | sort | uniq -c
```

### View Specific Screenshots
```bash
# View all index pages
ls -la *index*_full.png

# View the requested downloader config page
ls -la *downloader_config*.png

# Open in image viewer (Linux)
xdg-open 01_index_light_full.png

# Open in Preview (macOS)
open 01_index_light_full.png
```

### Compare Themes
```bash
# Compare light vs dark for same page
montage 01_index_light_full.png 01_index_dark_full.png -geometry +10+10 -tile 2x1 comparison_index.png
```

## Issues Summary

Check individual issue files for detailed analysis:
```bash
cat *_issues.txt | grep -E "(✅|❌|⚠️)" | sort | uniq -c
```

## Navigation Check

Pages with navigation issues:
```bash
grep -l "No navigation" *_issues.txt
```

## TOC Tree Check

Pages missing TOC tree:
```bash
grep -l "No TOC tree" *_issues.txt
```
"""

    summary_path = session_dir / "SUMMARY.md"
    summary_path.write_text(summary)


if __name__ == "__main__":
    import sys

    # Check if docs are being served
    port = 8003
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    print(f"📌 Make sure documentation is being served on port {port}")
    print(f"   Run: python -m http.server {port} --directory docs/build")
    print()

    try:
        import requests

        response = requests.get(f"http://localhost:{port}/", timeout=2)
        print(f"✅ Server is running on port {port}")
    except:
        print(f"❌ No server found on port {port}")
        print(f"   Please start the server first:")
        print(f"   cd /path/to/docs/build && python -m http.server {port}")
        exit(1)

    # Run the screenshot session
    asyncio.run(take_comprehensive_screenshots(port))
