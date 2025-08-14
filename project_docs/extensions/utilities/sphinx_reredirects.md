# sphinx-reredirects - URL Redirection Management

**Extension**: `sphinx_reredirects`  
**Category**: Utilities  
**Priority**: High (Critical for SEO and user experience)  
**Status**: ✅ Implemented in PyDevelop-Docs

## Overview

`sphinx-reredirects` provides comprehensive URL redirection management for Sphinx documentation sites, ensuring that moved, renamed, or restructured content remains accessible to users and search engines. This extension is essential for maintaining SEO rankings and providing seamless user experience during documentation evolution.

## Purpose & Utility Functionality

### Primary Functions

- **URL Preservation**: Maintains access to old URLs when documentation structure changes
- **SEO Protection**: Prevents loss of search engine rankings when pages are moved or renamed
- **User Experience**: Ensures bookmarks and shared links continue to work after site reorganization
- **Traffic Retention**: Redirects preserve referral traffic from external sites and social media

### Business Value

- **SEO Continuity**: Maintains search engine rankings worth thousands of dollars in organic traffic
- **User Satisfaction**: Prevents frustrating 404 errors that drive users away
- **Professional Image**: Shows attention to detail and consideration for user experience
- **Analytics Preservation**: Maintains historical traffic data and user journey tracking

## Configuration Options & Optimization Strategies

### Current PyDevelop-Docs Implementation

```python
# In config.py - Lines 310-311
"redirects": {},  # Empty by default
```

### Basic Configuration

```python
# Simple redirect configuration
redirects = {
    # Old path: New path
    "old-page.html": "new-page.html",
    "deprecated/": "current/",
    "v1/api.html": "api/v2/index.html",
}
```

### Advanced Configuration Options

```python
# Comprehensive redirection configuration
redirects = {
    # Simple page redirects
    "getting-started.html": "quickstart.html",
    "installation.html": "setup/installation.html",

    # Directory redirects
    "old-api/": "api/",
    "tutorials/": "guides/",

    # Version-specific redirects
    "v1/": "latest/",
    "v2/deprecated.html": "latest/migration.html",

    # API endpoint redirects
    "api/old-endpoint.html": "api/v3/new-endpoint.html",
    "reference/": "api/reference/",

    # External redirects (use carefully)
    "external-resource.html": "https://external-site.com/resource/",
}

# Advanced redirect configuration with HTTP status codes
redirects_status_codes = {
    "temporary-move.html": (302, "new-location.html"),  # Temporary redirect
    "permanent-move.html": (301, "final-location.html"), # Permanent redirect
    "gone-forever.html": (410, None),  # Gone (removed content)
}

# Pattern-based redirects for bulk operations
redirects_patterns = [
    # Redirect all old API docs to new structure
    (r"^old-api/(.+)\.html$", r"api/v3/\1.html"),

    # Redirect version-specific docs to latest
    (r"^v[12]/(.+)$", r"latest/\1"),

    # Redirect tutorial format changes
    (r"^tutorial-(.+)\.html$", r"guides/\1/index.html"),
]
```

### Intelligent Redirect Strategies

```python
# Content-aware redirect configuration
def setup_intelligent_redirects():
    """Setup redirects based on content analysis."""

    redirects = {}

    # Auto-detect moved content
    content_mappings = analyze_content_similarity()
    for old_path, new_path in content_mappings.items():
        redirects[old_path] = new_path

    # Handle API version redirects
    api_versions = detect_api_versions()
    for old_version, new_version in api_versions.items():
        redirects[f"api/{old_version}/"] = f"api/{new_version}/"

    # Setup maintenance redirects
    maintenance_pages = get_maintenance_pages()
    for page in maintenance_pages:
        redirects[page] = "maintenance.html"

    return redirects

# Dynamic redirects based on user context
def setup_contextual_redirects(user_agent, referrer):
    """Setup redirects based on user context."""

    redirects = {}

    # Mobile-specific redirects
    if is_mobile_user_agent(user_agent):
        redirects.update({
            "desktop-specific.html": "mobile/index.html",
            "complex-visualization.html": "mobile/simple-view.html",
        })

    # Search engine specific redirects
    if is_search_engine_bot(user_agent):
        redirects.update({
            "duplicate-content.html": "canonical-content.html",
            "thin-content.html": "comprehensive-guide.html",
        })

    return redirects
```

## SEO & Performance Impact

### Critical SEO Benefits

1. **PageRank Preservation**
   - **Link Equity Transfer**: 301 redirects pass 85-90% of link authority to new URLs
   - **Ranking Continuity**: Maintains search engine rankings during site reorganization
   - **Crawl Budget Optimization**: Helps search engines efficiently crawl updated content

2. **User Experience Benefits**
   - **Reduced Bounce Rate**: Prevents 404 errors that cause users to leave immediately
   - **Session Continuity**: Maintains user flow through documentation
   - **Bookmark Preservation**: Keeps user bookmarks functional after site changes

3. **Traffic Retention**
   - **Referral Traffic**: Maintains incoming links from external sites
   - **Social Media Links**: Preserves traffic from social media shares
   - **Email Links**: Keeps documentation links in emails functional

### Performance Metrics

```bash
# Typical performance improvements with proper redirects
- Reduced 404 error rate: 80-95%
- Maintained organic traffic during restructuring: 85-95%
- User satisfaction scores: +20-30%
- Search engine crawl efficiency: +15-25%
```

### SEO-Optimized Redirect Strategies

```python
# SEO-optimized redirect configuration
redirects_seo_optimized = {
    # 301 (Permanent) redirects for moved content
    "old-important-page.html": "new-important-page.html",  # 301 by default

    # Consolidate duplicate content
    "duplicate-1.html": "canonical-page.html",
    "duplicate-2.html": "canonical-page.html",

    # Redirect outdated content to updated versions
    "outdated-tutorial.html": "updated-tutorial.html",
    "deprecated-api.html": "current-api.html",

    # Handle URL structure changes
    "category/subcategory/page.html": "new-structure/page.html",
}

# Redirect chains optimization (avoid multiple redirects)
def optimize_redirect_chains(redirects):
    """Optimize redirect chains to improve performance."""

    optimized = {}

    for source, target in redirects.items():
        # Follow redirect chain to final destination
        final_target = target
        visited = set()

        while final_target in redirects and final_target not in visited:
            visited.add(final_target)
            final_target = redirects[final_target]

        optimized[source] = final_target

    return optimized
```

## Current Implementation Status in PyDevelop-Docs

### Configuration Status: ✅ Implemented

**File**: `/src/pydevelop_docs/config.py`  
**Lines**: 310-311, 497

```python
# Current configuration (basic)
extensions = [
    # ... other extensions ...
    "sphinx_reredirects",  # Line 497
    # ... other extensions ...
]

# Basic redirect configuration
"redirects": {},  # Empty by default - needs population
```

### Integration Status

- ✅ **Extension Loading**: Properly configured in extensions list
- ⚠️ **Redirect Rules**: No redirects configured by default
- ❌ **Pattern Matching**: Advanced pattern-based redirects not implemented
- ❌ **Analytics Integration**: Redirect tracking not configured

## Integration with Build Pipeline & Deployment

### Build Process Integration

```python
# Automatic redirect generation during build
def generate_redirects_from_history(app, env, updated_docs, added, removed):
    """Generate redirects based on documentation history."""

    redirects = {}

    # Analyze git history for moved files
    moved_files = analyze_git_moves()
    for old_path, new_path in moved_files.items():
        redirects[old_path] = new_path

    # Check for renamed sections
    renamed_sections = detect_renamed_sections(env)
    for old_section, new_section in renamed_sections.items():
        redirects[f"{old_section}/"] = f"{new_section}/"

    # Update redirect configuration
    app.config.redirects.update(redirects)

def setup(app):
    app.connect("env-before-resolve-references", generate_redirects_from_history)
```

### CI/CD Pipeline Integration

```yaml
# GitHub Actions redirect validation
- name: Build Documentation with Redirects
  run: |
    poetry run sphinx-build -b html docs/source docs/build

- name: Validate Redirect Configuration
  run: |
    # Check that redirect targets exist
    python scripts/validate-redirects.py docs/build/

- name: Test Redirect Functionality
  run: |
    # Test that redirects work correctly
    python scripts/test-redirects.py https://docs.yourproject.ai/

- name: Generate Redirect Report
  run: |
    # Generate report of all active redirects
    python scripts/redirect-report.py > redirect-summary.txt
```

### Web Server Integration

```python
# Generate web server redirect rules
def generate_server_redirects(redirects, server_type="nginx"):
    """Generate server-specific redirect rules."""

    if server_type == "nginx":
        return generate_nginx_redirects(redirects)
    elif server_type == "apache":
        return generate_apache_redirects(redirects)
    elif server_type == "cloudflare":
        return generate_cloudflare_redirects(redirects)

def generate_nginx_redirects(redirects):
    """Generate nginx redirect configuration."""

    nginx_config = []

    for source, target in redirects.items():
        # Handle different redirect types
        if target.startswith("http"):
            # External redirect
            nginx_config.append(f"rewrite ^/{source}$ {target} permanent;")
        else:
            # Internal redirect
            nginx_config.append(f"rewrite ^/{source}$ /{target} permanent;")

    return "\n".join(nginx_config)

def generate_apache_redirects(redirects):
    """Generate Apache .htaccess redirect rules."""

    htaccess_rules = ["RewriteEngine On"]

    for source, target in redirects.items():
        if target.startswith("http"):
            htaccess_rules.append(f"RewriteRule ^{source}$ {target} [R=301,L]")
        else:
            htaccess_rules.append(f"RewriteRule ^{source}$ /{target} [R=301,L]")

    return "\n".join(htaccess_rules)
```

## Monitoring & Analytics Capabilities

### Redirect Analytics Integration

```python
# Enhanced analytics for redirect performance
def track_redirect_usage(app, pagename, templatename, context, doctree):
    """Track redirect usage and performance."""

    # Add redirect tracking to pages
    redirect_tracking = {
        "source_page": pagename,
        "referrer": context.get("referrer", ""),
        "user_agent": context.get("user_agent", ""),
        "timestamp": datetime.now().isoformat(),
    }

    # Send to analytics service
    if app.config.redirect_analytics_enabled:
        send_redirect_analytics(redirect_tracking)

def setup(app):
    app.add_config_value("redirect_analytics_enabled", False, "html")
    app.connect("html-page-context", track_redirect_usage)
```

### Performance Monitoring

```python
# Redirect performance monitoring
def monitor_redirect_performance():
    """Monitor redirect performance and issues."""

    metrics = {
        "redirect_count": count_active_redirects(),
        "redirect_chains": detect_redirect_chains(),
        "broken_redirects": find_broken_redirects(),
        "redirect_performance": measure_redirect_speed(),
    }

    return metrics

def detect_redirect_chains():
    """Detect and report redirect chains."""

    chains = []
    redirects = get_current_redirects()

    for source in redirects:
        chain = trace_redirect_chain(source, redirects)
        if len(chain) > 2:  # More than one redirect
            chains.append(chain)

    return chains

def find_broken_redirects():
    """Find redirects pointing to non-existent pages."""

    broken = []
    redirects = get_current_redirects()

    for source, target in redirects.items():
        if not target.startswith("http") and not page_exists(target):
            broken.append((source, target))

    return broken
```

### Real-time Redirect Testing

```bash
# Test redirect functionality
#!/bin/bash

BASE_URL="https://docs.yourproject.ai"

# Test specific redirects
test_redirect() {
    local source=$1
    local expected_target=$2

    # Follow redirect and get final URL
    final_url=$(curl -s -L -o /dev/null -w "%{url_effective}" "$BASE_URL/$source")

    if [[ "$final_url" == "$BASE_URL/$expected_target" ]]; then
        echo "✅ Redirect $source -> $expected_target working"
    else
        echo "❌ Redirect $source -> $expected_target failed (got: $final_url)"
    fi
}

# Test common redirects
test_redirect "old-page.html" "new-page.html"
test_redirect "deprecated/" "current/"
test_redirect "v1/api.html" "api/v2/index.html"

# Test redirect response codes
test_redirect_code() {
    local source=$1
    local expected_code=$2

    http_code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/$source")

    if [[ "$http_code" == "$expected_code" ]]; then
        echo "✅ Redirect $source returns $expected_code"
    else
        echo "❌ Redirect $source returns $http_code (expected: $expected_code)"
    fi
}

# Test redirect status codes
test_redirect_code "permanent-move.html" "301"
test_redirect_code "temporary-move.html" "302"
```

## Code Examples for Advanced Usage

### Intelligent Redirect Generation

```python
# Intelligent redirect generation based on content analysis
import difflib
from pathlib import Path

def generate_intelligent_redirects(old_docs_path, new_docs_path):
    """Generate redirects by analyzing content similarity."""

    redirects = {}

    # Get all old and new files
    old_files = list(Path(old_docs_path).rglob("*.html"))
    new_files = list(Path(new_docs_path).rglob("*.html"))

    # Extract content for comparison
    old_content = {f: extract_content(f) for f in old_files}
    new_content = {f: extract_content(f) for f in new_files}

    # Find best matches
    for old_file, old_text in old_content.items():
        best_match = None
        best_similarity = 0.0

        for new_file, new_text in new_content.items():
            similarity = difflib.SequenceMatcher(None, old_text, new_text).ratio()

            if similarity > best_similarity and similarity > 0.7:  # 70% threshold
                best_similarity = similarity
                best_match = new_file

        if best_match:
            old_path = str(old_file.relative_to(old_docs_path))
            new_path = str(best_match.relative_to(new_docs_path))
            redirects[old_path] = new_path

    return redirects

def extract_content(file_path):
    """Extract meaningful content from HTML file."""

    from bs4 import BeautifulSoup

    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Remove navigation, scripts, styles
    for element in soup(['nav', 'script', 'style', 'header', 'footer']):
        element.decompose()

    # Extract main content
    main_content = soup.find('main') or soup.find('article') or soup.find('body')

    return main_content.get_text(strip=True) if main_content else ""
```

### Bulk Redirect Management

```python
# Bulk redirect management utilities
class RedirectManager:
    """Manage large numbers of redirects efficiently."""

    def __init__(self, base_redirects=None):
        self.redirects = base_redirects or {}
        self.patterns = []

    def add_bulk_redirects(self, prefix, mappings):
        """Add multiple redirects with common prefix."""

        for old_suffix, new_suffix in mappings.items():
            old_path = f"{prefix}/{old_suffix}"
            new_path = f"{prefix}/{new_suffix}"
            self.redirects[old_path] = new_path

    def add_pattern_redirect(self, pattern, replacement):
        """Add pattern-based redirect rule."""

        self.patterns.append((pattern, replacement))

    def generate_version_redirects(self, old_version, new_version):
        """Generate redirects for version migration."""

        version_redirects = {}

        # Redirect all old version URLs to new version
        for path in self.get_version_paths(old_version):
            new_path = path.replace(f"/{old_version}/", f"/{new_version}/")
            version_redirects[path] = new_path

        self.redirects.update(version_redirects)

    def optimize_redirects(self):
        """Optimize redirect configuration for performance."""

        # Remove redirect chains
        optimized = {}

        for source, target in self.redirects.items():
            # Follow chain to final destination
            final_target = self.follow_redirect_chain(target)
            optimized[source] = final_target

        self.redirects = optimized

    def follow_redirect_chain(self, target, visited=None):
        """Follow redirect chain to final destination."""

        if visited is None:
            visited = set()

        if target in visited or target not in self.redirects:
            return target

        visited.add(target)
        return self.follow_redirect_chain(self.redirects[target], visited)

    def export_redirects(self, format="dict"):
        """Export redirects in various formats."""

        if format == "dict":
            return self.redirects
        elif format == "nginx":
            return self.generate_nginx_config()
        elif format == "apache":
            return self.generate_apache_config()
        elif format == "json":
            import json
            return json.dumps(self.redirects, indent=2)
```

### Conditional Redirects

```python
# Conditional redirect system
def setup_conditional_redirects(app):
    """Setup redirects based on various conditions."""

    def conditional_redirect_handler(app, pagename, templatename, context, doctree):
        """Handle conditional redirects based on context."""

        # Time-based redirects
        current_time = datetime.now()
        if current_time > datetime(2024, 12, 31):  # After deprecation date
            if pagename.startswith("deprecated/"):
                context["redirect_to"] = pagename.replace("deprecated/", "current/")

        # User-based redirects
        user_agent = context.get("HTTP_USER_AGENT", "")
        if "bot" in user_agent.lower():
            # Special handling for search engine bots
            if pagename in app.config.bot_redirects:
                context["redirect_to"] = app.config.bot_redirects[pagename]

        # Geographic redirects
        user_country = context.get("HTTP_CF_IPCOUNTRY", "")
        if user_country in app.config.geo_redirects:
            geo_redirects = app.config.geo_redirects[user_country]
            if pagename in geo_redirects:
                context["redirect_to"] = geo_redirects[pagename]

    app.connect("html-page-context", conditional_redirect_handler)
```

## Best Practices for Production Deployment

### 1. Redirect Strategy Planning

```python
# Strategic redirect planning
redirect_strategy = {
    # Permanent content moves (301)
    "permanent_redirects": {
        "old-important-page.html": "new-important-page.html",
        "deprecated-api/": "current-api/",
    },

    # Temporary redirects (302)
    "temporary_redirects": {
        "maintenance-page.html": "under-construction.html",
        "beta-feature.html": "coming-soon.html",
    },

    # External redirects (301)
    "external_redirects": {
        "external-tool.html": "https://external-site.com/tool/",
        "partner-docs.html": "https://partner.com/documentation/",
    },
}
```

### 2. Performance Optimization

```python
# Performance-optimized redirect configuration
redirect_performance_config = {
    "max_redirects": 1,        # Avoid redirect chains
    "cache_ttl": 3600,         # Cache redirects for 1 hour
    "preload_redirects": True, # Preload redirect mapping
    "compress_redirects": True, # Compress redirect data
}
```

### 3. Monitoring and Maintenance

```python
# Comprehensive redirect monitoring
def setup_redirect_monitoring():
    """Setup comprehensive redirect monitoring."""

    monitoring_config = {
        "track_redirect_usage": True,
        "monitor_redirect_performance": True,
        "alert_on_broken_redirects": True,
        "log_redirect_chains": True,
        "generate_redirect_reports": True,
    }

    return monitoring_config
```

### 4. SEO-Friendly Redirect Management

```bash
# SEO-friendly redirect validation
#!/bin/bash

# Check for redirect chains (bad for SEO)
check_redirect_chains() {
    echo "Checking for redirect chains..."

    for url in $(get_all_redirected_urls); do
        chain_length=$(get_redirect_chain_length "$url")
        if [ "$chain_length" -gt 1 ]; then
            echo "⚠️  Redirect chain detected: $url (length: $chain_length)"
        fi
    done
}

# Validate redirect HTTP status codes
validate_redirect_codes() {
    echo "Validating redirect status codes..."

    for url in $(get_all_redirected_urls); do
        status_code=$(curl -s -o /dev/null -w "%{http_code}" -L "$url")
        if [ "$status_code" -ne 200 ]; then
            echo "❌ Redirect target returns $status_code: $url"
        fi
    done
}

# Main redirect health check
main() {
    check_redirect_chains
    validate_redirect_codes
    echo "✅ Redirect health check completed"
}

main
```

## Troubleshooting Common Issues

### Issue: Redirect Loops

**Cause**: Circular redirects in configuration  
**Solution**:

```python
# Detect and prevent redirect loops
def detect_redirect_loops(redirects):
    """Detect circular redirects that create loops."""

    loops = []

    for source in redirects:
        visited = set()
        current = source

        while current in redirects:
            if current in visited:
                # Found a loop
                loops.append(list(visited) + [current])
                break

            visited.add(current)
            current = redirects[current]

    return loops
```

### Issue: Redirect Chains

**Cause**: Multiple successive redirects slowing performance  
**Solution**:

```python
# Optimize redirect chains
def flatten_redirect_chains(redirects):
    """Flatten redirect chains to direct redirects."""

    flattened = {}

    for source, target in redirects.items():
        # Follow chain to final destination
        final_target = target
        visited = set()

        while final_target in redirects and final_target not in visited:
            visited.add(final_target)
            final_target = redirects[final_target]

        flattened[source] = final_target

    return flattened
```

### Issue: Missing Redirect Targets

**Cause**: Redirects pointing to non-existent pages  
**Solution**:

```python
# Validate redirect targets
def validate_redirect_targets(redirects, site_pages):
    """Validate that all redirect targets exist."""

    invalid_redirects = []

    for source, target in redirects.items():
        if not target.startswith("http") and target not in site_pages:
            invalid_redirects.append((source, target))

    return invalid_redirects
```

## Next Steps for PyDevelop-Docs

### Immediate Improvements

1. **Add Common Redirects**: Implement typical redirects for documentation restructuring
2. **Pattern-Based Redirects**: Add support for bulk redirects using regex patterns
3. **Redirect Validation**: Implement build-time validation of redirect targets

### Future Enhancements

1. **Intelligent Redirect Generation**: Auto-generate redirects based on content analysis
2. **Analytics Integration**: Track redirect usage and performance metrics
3. **Dynamic Redirects**: Support for context-aware redirects based on user attributes
