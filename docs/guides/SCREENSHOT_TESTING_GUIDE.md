# Screenshot Testing Guide for PyDevelop-Docs

**Version**: 1.0
**Created**: 2025-08-17
**Purpose**: Comprehensive guide for visual testing documentation with screenshot analysis and feedback loops

## 🎯 Overview

Visual testing ensures your documentation renders correctly across different themes, browsers, and screen sizes. This guide covers:

- Setting up screenshot testing
- Running automated visual tests
- Analyzing results and feedback
- Implementing fixes based on visual issues
- Creating continuous feedback loops

## 📸 Screenshot Testing Tools

### Built-in Tools

PyDevelop-Docs includes powerful screenshot utilities:

1. **`comprehensive_screenshot.py`** - Full documentation session
2. **`screenshot_specific.py`** - Single page testing
3. **`visual_test_runner.py`** - Automated testing with feedback (create this)

### Prerequisites

```bash
# Install Playwright for screenshots
pip install playwright rich
playwright install chromium

# Install PyDevelop-Docs with dev dependencies
poetry install --with dev
```

## 🔄 Visual Testing Workflow

### 1. Build Documentation

```bash
# Using PyDevelop-Docs
poetry run pydvlp-docs build

# Or directly with Sphinx
poetry run sphinx-build -b html docs/source docs/build
```

### 2. Start Test Server

```bash
# Start local server
python -m http.server 8003 --directory docs/build

# Keep running in background
```

### 3. Run Screenshot Tests

```bash
# Comprehensive test (all pages)
poetry run python scripts/debug/comprehensive_screenshot.py 8003

# Specific page test
poetry run python scripts/debug/screenshot_specific.py \
  "http://localhost:8003/autoapi/index.html" \
  "api_index"
```

### 4. Analyze Results

Screenshot results are saved in `debug/screenshots/` with:

- Full page screenshots (entire content)
- Viewport screenshots (above the fold)
- Issue reports for each page
- Summary report with all findings

## 📊 Understanding Screenshot Analysis

### Issue Detection

The screenshot tools automatically detect:

```python
COMMON_ISSUES = {
    "missing_navigation": "No sidebar navigation found",
    "missing_toc": "No table of contents",
    "white_on_white": "Potential visibility issues in dark mode",
    "css_not_loaded": "Styling appears broken",
    "missing_content": "Expected content not found",
    "layout_broken": "Page layout issues detected"
}
```

### Reading Issue Reports

Each page generates an issues file:

```
01_index_light_issues.txt
01_index_dark_issues.txt
```

Example issues:

```
Missing navigation sidebar
White-on-white text detected in code blocks
TOC tree not visible
```

## 🔧 Feedback Loop Implementation

### 1. Automated Feedback Script

Create `scripts/visual_test_runner.py`:

```python
#!/usr/bin/env python3
"""Visual testing with automated feedback."""

import subprocess
import json
from pathlib import Path
from datetime import datetime

class VisualFeedbackTester:
    def __init__(self):
        self.results = []
        self.feedback = []

    def run_tests(self):
        """Run screenshot tests and collect results."""
        # Build docs
        subprocess.run(["poetry", "run", "pydvlp-docs", "build"])

        # Start server
        server = subprocess.Popen([
            "python", "-m", "http.server", "8003",
            "--directory", "docs/build"
        ])

        try:
            # Run screenshots
            result = subprocess.run([
                "poetry", "run", "python",
                "scripts/debug/comprehensive_screenshot.py"
            ], capture_output=True)

            # Parse results
            self.parse_results()

        finally:
            server.terminate()

    def parse_results(self):
        """Parse screenshot results and generate feedback."""
        screenshot_dir = Path("debug/screenshots")
        latest = max(screenshot_dir.glob("comprehensive_*"))

        # Check for issues
        for issue_file in latest.glob("*_issues.txt"):
            if issue_file.stat().st_size > 0:
                with open(issue_file) as f:
                    issues = f.read().strip().split("\n")
                    self.feedback.extend(issues)

    def suggest_fixes(self):
        """Suggest fixes based on detected issues."""
        fixes = {
            "missing navigation": "Check Furo theme configuration",
            "white-on-white": "Review dark mode CSS variables",
            "css not loaded": "Verify CSS files in _static directory",
            "missing content": "Check AutoAPI configuration"
        }

        for issue in self.feedback:
            for pattern, fix in fixes.items():
                if pattern in issue.lower():
                    print(f"Issue: {issue}")
                    print(f"Fix: {fix}\n")
```

### 2. Continuous Testing Loop

```bash
#!/bin/bash
# continuous_visual_test.sh

while true; do
    echo "🔄 Running visual tests..."

    # Run tests
    poetry run python scripts/visual_test_runner.py

    # Check for changes
    if git diff --quiet docs/source; then
        echo "✅ No changes needed"
    else
        echo "📝 Changes detected, rebuilding..."
        continue
    fi

    # Wait before next run
    sleep 300  # 5 minutes
done
```

## 🎨 CSS Testing Strategies

### 1. Theme Testing

Test both light and dark themes:

```python
# In screenshot script
for theme in ["light", "dark"]:
    # Take screenshot with theme
    page.emulate_media(color_scheme=theme)
    screenshot = page.screenshot(full_page=True)

    # Check for theme-specific issues
    if theme == "dark":
        check_dark_mode_visibility(screenshot)
```

### 2. Responsive Testing

Test different viewport sizes:

```python
VIEWPORTS = [
    {"width": 1920, "height": 1080},  # Desktop
    {"width": 768, "height": 1024},   # Tablet
    {"width": 375, "height": 667},    # Mobile
]

for viewport in VIEWPORTS:
    page.set_viewport_size(viewport)
    # Take screenshot and analyze
```

### 3. CSS Regression Testing

Compare before/after CSS changes:

```bash
# Before changes
poetry run python scripts/screenshot_specific.py "$URL" "before"

# Make CSS changes

# After changes
poetry run python scripts/screenshot_specific.py "$URL" "after"

# Compare visually
compare before_light_full.png after_light_full.png diff.png
```

## 📋 Common Issues and Fixes

### 1. Missing Navigation

**Issue**: Sidebar navigation not visible

```
Missing navigation sidebar
```

**Fix**:

```python
# In config.py
html_theme_options = {
    "navigation_with_keys": True,
    "sidebar_hide_name": False,  # Ensure sidebar visible
}
```

### 2. Dark Mode Visibility

**Issue**: White text on white background

```
White-on-white text detected in dark mode
```

**Fix**:

```css
/* In css/custom.css */
[data-theme="dark"] {
  --color-code-background: #2d2d2d !important;
  --color-code-foreground: #f8f8f2 !important;
}
```

### 3. CSS Not Loading

**Issue**: Styles not applied

```
CSS files appear to be missing
```

**Fix**:

1. Check `_static/` directory for CSS files
2. Verify `html_css_files` in config.py
3. Check CSS file paths are correct

### 4. AutoAPI Issues

**Issue**: API documentation missing

```
AutoAPI content not found
```

**Fix**:

```python
# In config.py
autoapi_dirs = ["../../src"]  # Correct path
autoapi_own_page_level = "module"  # Hierarchical structure
```

## 🔄 Feedback Loop Best Practices

### 1. Automated Testing

```yaml
# .github/workflows/visual-test.yml
name: Visual Documentation Test
on: [push, pull_request]

jobs:
  visual-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: |
          pip install playwright
          playwright install chromium
      - name: Run visual tests
        run: |
          poetry run python scripts/visual_test_runner.py
      - name: Upload screenshots
        uses: actions/upload-artifact@v3
        with:
          name: screenshots
          path: debug/screenshots/
```

### 2. Quick Feedback Loop

```python
# watch_and_test.py
import watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DocChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(('.css', '.py', '.rst', '.md')):
            print(f"Change detected: {event.src_path}")
            subprocess.run(["poetry", "run", "pydvlp-docs", "build"])
            # Run screenshot of affected page

observer = Observer()
observer.schedule(DocChangeHandler(), "docs/source", recursive=True)
observer.start()
```

### 3. Visual Regression Testing

```python
# visual_regression.py
from PIL import Image
import imagehash

def compare_screenshots(before, after):
    """Compare screenshots for visual regression."""
    img1 = Image.open(before)
    img2 = Image.open(after)

    hash1 = imagehash.average_hash(img1)
    hash2 = imagehash.average_hash(img2)

    difference = hash1 - hash2
    if difference > 5:  # Threshold
        print(f"Visual regression detected: {difference}")
        return False
    return True
```

## 📊 Reporting and Metrics

### 1. Test Summary Report

```python
def generate_report(results):
    """Generate HTML report of visual tests."""
    html = f"""
    <html>
    <head><title>Visual Test Report</title></head>
    <body>
        <h1>Documentation Visual Test Report</h1>
        <p>Generated: {datetime.now()}</p>

        <h2>Summary</h2>
        <ul>
            <li>Pages Tested: {results['pages_tested']}</li>
            <li>Issues Found: {len(results['issues'])}</li>
            <li>Critical Issues: {results['critical_count']}</li>
        </ul>

        <h2>Screenshots</h2>
        {"".join(f'<img src="{img}" width="400">' for img in results['screenshots'])}
    </body>
    </html>
    """

    with open("visual_test_report.html", "w") as f:
        f.write(html)
```

### 2. Metrics Tracking

Track visual quality over time:

```python
METRICS = {
    "render_time": [],
    "issue_count": [],
    "theme_issues": {"light": 0, "dark": 0},
    "page_load_errors": 0,
    "css_conflicts": 0
}

# Save metrics after each test run
with open("visual_metrics.json", "w") as f:
    json.dump(METRICS, f, indent=2)
```

## 🚀 Advanced Testing

### 1. Cross-Browser Testing

```python
BROWSERS = ["chromium", "firefox", "webkit"]

for browser_type in BROWSERS:
    browser = playwright[browser_type].launch()
    page = browser.new_page()
    # Run tests
```

### 2. Performance Testing

```python
# Measure page load performance
performance_timing = page.evaluate("""
    () => {
        const timing = performance.timing;
        return {
            domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
            loadComplete: timing.loadEventEnd - timing.navigationStart
        }
    }
""")
```

### 3. Accessibility Testing

```python
# Check color contrast
def check_contrast(page):
    """Check WCAG color contrast requirements."""
    contrast_issues = page.evaluate("""
        () => {
            // Check text contrast ratios
            const elements = document.querySelectorAll('*');
            const issues = [];
            // Contrast checking logic
            return issues;
        }
    """)
    return contrast_issues
```

## 💡 Tips and Tricks

### 1. Debug Mode

```python
# Enable debug screenshots
DEBUG = True

if DEBUG:
    page.screenshot(path=f"debug_{step_name}.png")
    print(f"Debug screenshot saved: {step_name}")
```

### 2. Selective Testing

```bash
# Test only specific pages
poetry run python scripts/screenshot_specific.py \
  "http://localhost:8003/autoapi/mymodule/index.html" \
  --themes "dark" \
  --viewports "mobile,desktop"
```

### 3. Parallel Testing

```python
# Run tests in parallel
import concurrent.futures

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    futures = []
    for page_url in page_urls:
        future = executor.submit(test_page, page_url)
        futures.append(future)
```

## 🎯 Next Steps

1. **Set up automated visual testing** in your CI/CD pipeline
2. **Create custom issue detectors** for your specific needs
3. **Build a visual regression suite** for critical pages
4. **Integrate with monitoring** for production documentation
5. **Create dashboards** for visual quality metrics

## 📚 Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [Visual Regression Testing](https://github.com/garris/BackstopJS)
- [Accessibility Testing](https://www.w3.org/WAI/test-evaluate/)
- [CSS Testing Best Practices](https://css-tricks.com/visual-regression-testing/)

---

**Remember**: Visual testing is not just about catching bugs - it's about ensuring a consistent, professional documentation experience for your users across all platforms and themes.
