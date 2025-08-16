# PyDevelop-Docs Playwright Testing Suite

Comprehensive testing suite for generated documentation using Playwright.

## 📁 Directory Structure

```
tests/playwright/
├── __init__.py           # Package initialization
├── README.md            # This file
├── requirements.txt     # Testing dependencies
│
├── core/                # Core test modules
│   ├── __init__.py
│   ├── test_documentation.py    # Main comprehensive test suite
│   ├── test_accessibility.py   # Accessibility tests (future)
│   └── test_performance.py     # Performance tests (future)
│
├── reports/             # Report generation
│   ├── __init__.py
│   ├── generate_test_report.py  # HTML report generator
│   └── templates/              # Report templates (future)
│
├── runners/             # Test execution scripts
│   ├── __init__.py
│   ├── run_doc_tests.py        # Simple test runner
│   ├── run_package_test.py     # Single package tester (future)
│   └── run_ci_tests.py         # CI/CD runner (future)
│
├── fixtures/            # Test fixtures and data
│   └── __init__.py
│
└── results/             # Test results (gitignored)
    └── .gitkeep
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 2. Run Tests

```bash
# Run all documentation tests
python runners/run_doc_tests.py

# Or run directly
python core/test_documentation.py --base-dir /path/to/haive
```

### 3. Generate Report

```bash
# Generate HTML report from results
python reports/generate_test_report.py results/test_results_TIMESTAMP.json
```

## 🧪 Test Coverage

The test suite validates:

### ✅ Functionality Tests

- **Homepage**: Title, headings, navigation, footer
- **Navigation**: Link functionality, TOC tree, breadcrumbs
- **API Reference**: Class/function documentation, code examples
- **Search**: Search input, results display
- **Links**: Internal link validation, broken link detection
- **Images**: Alt text, loading validation

### 🎨 Visual Tests

- **Responsive Design**: Mobile, tablet, desktop viewports
- **Dark Mode**: Theme toggle functionality
- **Code Blocks**: Syntax highlighting, copy buttons
- **Screenshots**: Full page captures for each test

### ⚡ Performance Tests

- **Page Load Time**: DOM ready, full load metrics
- **Resource Size**: Total size, large file detection
- **Network Requests**: Request count and timing

## 📊 Test Results

Test results are saved with timestamps:

```
results/
├── doc_test_results_20250815_193000/
│   ├── test_results_20250815_193000.json    # Main results
│   ├── test_report_20250815_193000.html     # HTML report
│   │
│   ├── haive-agents/                         # Package results
│   │   ├── test_results.json                 # Package test data
│   │   ├── homepage_20250815_193000.png      # Screenshots
│   │   ├── navigation_20250815_193000.png
│   │   ├── api_reference_20250815_193000.png
│   │   └── ...
│   │
│   ├── haive-core/
│   └── ...
```

## 🔧 Configuration

### Test Timeouts

Edit in `core/test_documentation.py`:

```python
self.page_load_timeout = 30000  # 30 seconds
self.navigation_timeout = 10000  # 10 seconds
```

### Viewport Sizes

```python
viewports = [
    {"name": "mobile", "width": 375, "height": 667},
    {"name": "tablet", "width": 768, "height": 1024},
    {"name": "desktop", "width": 1920, "height": 1080}
]
```

## 📈 Extending Tests

### Add New Test Category

1. Create new test file in `core/`:

```python
# core/test_accessibility.py
async def _test_accessibility(self, page: Page, doc_path: Path, output_dir: Path) -> Dict:
    """Test accessibility features."""
    # Your test implementation
```

2. Add to test methods in main suite:

```python
test_methods = [
    # ... existing tests
    ("accessibility", self._test_accessibility),
]
```

### Add Custom Checks

Add to specific test methods:

```python
# Check custom element
custom_element = await page.query_selector(".my-custom-class")
result["checks"]["has_custom_element"] = custom_element is not None
```

## 🐛 Troubleshooting

### Common Issues

1. **Playwright not installed**

   ```bash
   pip install playwright
   playwright install chromium
   ```

2. **Tests timeout**
   - Increase timeouts in test configuration
   - Check if documentation server is running

3. **Screenshots not saving**
   - Ensure output directory has write permissions
   - Check disk space

### Debug Mode

Run with verbose output:

```bash
python core/test_documentation.py --base-dir /path/to/haive --debug
```

## 📝 CI/CD Integration

### GitHub Actions Example

```yaml
name: Documentation Tests
on: [push, pull_request]

jobs:
  test-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - name: Install dependencies
        run: |
          pip install -r tests/playwright/requirements.txt
          playwright install chromium
      - name: Build documentation
        run: python run_smart_build.py
      - name: Run tests
        run: python tests/playwright/runners/run_doc_tests.py
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: tests/playwright/results/
```

## 🤝 Contributing

1. Add tests for new documentation features
2. Ensure all tests pass before submitting PR
3. Update this README with new test categories
4. Follow existing code style and patterns

## 📄 License

Part of PyDevelop-Docs project. See main LICENSE file.
