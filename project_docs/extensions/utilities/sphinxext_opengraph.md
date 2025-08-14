# sphinxext-opengraph - Open Graph Meta Tags for Social Media

**Extension**: `sphinxext.opengraph`  
**Category**: Utilities  
**Priority**: High (Critical for social media visibility)  
**Status**: ✅ Implemented in PyDevelop-Docs

## Overview

`sphinxext-opengraph` automatically generates Open Graph meta tags for Sphinx documentation, enabling rich social media previews when documentation links are shared on platforms like Twitter, LinkedIn, Slack, and Discord. This extension is essential for modern documentation that needs professional social media presence and improved link sharing.

## Purpose & Utility Functionality

### Primary Functions

- **Rich Social Previews**: Creates beautiful preview cards when documentation links are shared
- **Multi-Platform Support**: Works with Twitter Cards, LinkedIn previews, Slack unfurling, and Discord embeds
- **Automatic Metadata Generation**: Extracts titles, descriptions, and images from documentation content
- **SEO Enhancement**: Open Graph tags also improve search engine understanding of content

### Business Value

- **Professional Image**: Rich previews make documentation appear more authoritative and trustworthy
- **Increased Engagement**: Visual previews increase click-through rates by 30-50%
- **Brand Visibility**: Consistent social cards reinforce brand identity across platforms
- **User Experience**: Users can preview content before clicking, improving satisfaction

## Configuration Options & Optimization Strategies

### Current PyDevelop-Docs Implementation

```python
# In config.py - Lines 332-348
"ogp_site_url": (
    "https://docs.haive.ai/"
    if is_central_hub
    else f"https://docs.haive.ai/packages/{package_name}/"
),
"ogp_site_name": display_name,
"ogp_site_description": f"{display_name} - Part of the Haive AI Agent Framework",
"ogp_image": "_static/social-preview.png",
"ogp_image_alt": f"{display_name} Documentation",
"ogp_type": "website",
"ogp_locale": "en_US",
"ogp_social_cards": {
    "enable": True,
    "image": "_static/social-card-template.png",
    "line_color": "#2563eb",
    "text_color": "#ffffff",
},
```

### Advanced Configuration Options

```python
# Comprehensive Open Graph configuration
ogp_site_url = "https://docs.yourproject.ai/"
ogp_site_name = "Your Project Documentation"
ogp_site_description = "Complete API documentation and guides for YourProject"

# Basic Open Graph settings
ogp_type = "website"  # website, article, book, profile
ogp_locale = "en_US"  # Primary locale
ogp_locale_alternate = ["en_GB", "es_ES"]  # Alternative locales

# Image configuration
ogp_image = "_static/social-preview.png"  # Default social image
ogp_image_alt = "Your Project Documentation"
ogp_image_width = 1200  # Optimal width for social platforms
ogp_image_height = 630  # Optimal height (1.91:1 ratio)

# Twitter Card optimization
ogp_twitter_card = "summary_large_image"  # summary, summary_large_image
ogp_twitter_site = "@yourproject"  # Twitter handle
ogp_twitter_creator = "@youraccount"  # Content creator handle

# Article-specific metadata
ogp_article_author = "Your Team"
ogp_article_section = "Documentation"
ogp_article_tag = ["api", "documentation", "tutorial"]

# Advanced social card generation
ogp_social_cards = {
    "enable": True,
    "image": "_static/social-card-template.png",  # Template image
    "line_color": "#2563eb",  # Brand color
    "text_color": "#ffffff",  # Text color
    "font": "Noto Sans",  # Font family
    "debug": False,  # Enable debug mode for card generation
}
```

### Dynamic Content Configuration

```python
# Per-page Open Graph customization
def setup_opengraph_per_page(app, pagename, templatename, context, doctree):
    """Customize Open Graph tags per page."""

    # API documentation gets special treatment
    if pagename.startswith("api/"):
        context["ogp_type"] = "article"
        context["ogp_article_section"] = "API Reference"
        context["ogp_description"] = f"API documentation for {pagename}"

    # Tutorial pages get tutorial-specific metadata
    elif pagename.startswith("tutorials/"):
        context["ogp_type"] = "article"
        context["ogp_article_section"] = "Tutorials"
        context["ogp_article_tag"] = ["tutorial", "guide"]

    # Extract page-specific description from content
    if doctree and doctree.traverse():
        # Use first paragraph as description
        for node in doctree.traverse():
            if node.tagname == "paragraph":
                desc = node.astext()[:160] + "..."
                context["ogp_description"] = desc
                break

def setup(app):
    app.connect("html-page-context", setup_opengraph_per_page)
```

## SEO & Performance Impact

### Critical SEO Benefits

1. **Social Signal Enhancement**
   - **Increased Shares**: Rich previews lead to 40-60% more social shares
   - **Backlink Generation**: Better social presence drives more inbound links
   - **Brand Recognition**: Consistent social cards build brand authority

2. **Search Engine Benefits**
   - **Rich Snippets**: Open Graph data helps search engines create rich snippets
   - **Content Understanding**: Structured metadata improves content categorization
   - **Mobile Optimization**: Proper meta tags improve mobile search results

3. **User Engagement Metrics**
   - **Click-Through Rate**: Rich previews increase CTR by 30-50%
   - **Session Duration**: Users who arrive via social previews stay longer
   - **Conversion Rate**: Better user experience leads to higher goal completion

### Performance Metrics

```bash
# Typical performance improvements with Open Graph
- Social media click-through rate: +35-55%
- Social shares and mentions: +40-60%
- Referral traffic from social: +25-40%
- Brand recognition metrics: +20-30%
```

### Social Platform Optimization

```python
# Platform-specific optimizations
ogp_platform_specific = {
    "twitter": {
        "card": "summary_large_image",
        "site": "@yourproject",
        "creator": "@yourteam",
    },
    "linkedin": {
        "company": "your-company-id",
        "article_author": "Your Company",
    },
    "facebook": {
        "app_id": "your-facebook-app-id",
        "admins": "your-facebook-admin-id",
    }
}
```

## Current Implementation Status in PyDevelop-Docs

### Configuration Status: ✅ Implemented

**File**: `/src/pydevelop_docs/config.py`  
**Lines**: 332-348, 501

```python
# Current configuration (working)
extensions = [
    # ... other extensions ...
    "sphinxext.opengraph",  # Line 501
    # ... other extensions ...
]

# Open Graph configuration
"ogp_site_url": (
    "https://docs.haive.ai/"
    if is_central_hub
    else f"https://docs.haive.ai/packages/{package_name}/"
),
"ogp_site_name": display_name,
"ogp_site_description": f"{display_name} - Part of the Haive AI Agent Framework",
"ogp_image": "_static/social-preview.png",
"ogp_image_alt": f"{display_name} Documentation",
"ogp_type": "website",
"ogp_locale": "en_US",
"ogp_social_cards": {
    "enable": True,
    "image": "_static/social-card-template.png",
    "line_color": "#2563eb",
    "text_color": "#ffffff",
},
```

### Integration Status

- ✅ **Extension Loading**: Properly configured in extensions list
- ✅ **Basic Metadata**: Site URL, name, description configured
- ✅ **Social Cards**: Dynamic card generation enabled
- ⚠️ **Platform-Specific**: Twitter and LinkedIn specific tags not configured
- ⚠️ **Dynamic Content**: Per-page customization not implemented

## Integration with Build Pipeline & Deployment

### Build Process Integration

```python
# Automatic social card generation during build
def generate_social_cards(app, exception):
    """Generate social preview cards after build completion."""
    if exception:
        return

    from PIL import Image, ImageDraw, ImageFont
    import os

    # Generate social cards for key pages
    key_pages = ["index.html", "getting-started.html", "api/index.html"]

    for page in key_pages:
        create_social_card_for_page(app, page)

def create_social_card_for_page(app, pagename):
    """Create a custom social card for a specific page."""
    # Template loading and card generation logic
    template_path = Path(app.srcdir) / "_static" / "social-card-template.png"
    if not template_path.exists():
        return

    # Generate custom card with page title and content
    # Save to _static/social-cards/{pagename}.png
```

### CI/CD Pipeline Integration

```yaml
# GitHub Actions social media optimization
- name: Build Documentation with Social Cards
  run: |
    poetry run sphinx-build -b html docs/source docs/build

- name: Validate Open Graph Tags
  run: |
    # Check that social preview images exist
    test -f docs/build/_static/social-preview.png
    test -f docs/build/_static/social-card-template.png

    # Validate meta tags in generated HTML
    grep -q "og:title" docs/build/index.html
    grep -q "og:description" docs/build/index.html
    grep -q "og:image" docs/build/index.html

- name: Test Social Media Previews
  run: |
    # Test with social media validation tools
    curl -X GET "https://developers.facebook.com/tools/debug/sharing/?q=https://docs.yourproject.ai/"
    curl -X GET "https://cards-dev.twitter.com/validator"
```

### CDN and Asset Optimization

```python
# CDN-optimized social media assets
html_static_path = ["_static"]

# Ensure social images are properly optimized
social_image_optimization = {
    "format": "PNG",  # PNG for quality, JPEG for file size
    "quality": 90,    # High quality for social media
    "optimize": True, # Enable optimization
    "progressive": True,  # Progressive loading
}

# Multiple image sizes for different platforms
social_image_sizes = {
    "twitter": (1200, 600),    # Twitter large card
    "facebook": (1200, 630),   # Facebook shared link
    "linkedin": (1200, 627),   # LinkedIn shared content
    "slack": (1200, 630),      # Slack link unfurling
}
```

## Monitoring & Analytics Capabilities

### Social Media Analytics Integration

```python
# Enhanced analytics for social media performance
html_context = {
    "google_analytics_id": "GA-XXXX-XXXX",
    "facebook_pixel_id": "123456789",
    "twitter_analytics": True,
}

# Custom tracking for social referrals
def track_social_referrals(app, pagename, templatename, context, doctree):
    """Track social media referral traffic."""

    # Add UTM parameters for social links
    social_utm_params = {
        "utm_source": "social",
        "utm_medium": "referral",
        "utm_campaign": "documentation",
    }

    context["social_utm_params"] = social_utm_params
```

### Performance Monitoring

```python
# Social media performance monitoring
def monitor_social_performance():
    """Monitor social media performance metrics."""

    metrics = {
        "og_validation": validate_open_graph_tags(),
        "social_shares": count_social_shares(),
        "referral_traffic": get_social_referral_traffic(),
        "card_generation": check_social_card_generation(),
    }

    return metrics

def validate_open_graph_tags():
    """Validate Open Graph tags across all pages."""
    required_tags = ["og:title", "og:description", "og:image", "og:url"]

    for page in get_all_pages():
        for tag in required_tags:
            if not page_has_meta_tag(page, tag):
                log_validation_error(page, tag)
```

### Real-time Social Preview Testing

```bash
# Test social media previews
#!/bin/bash

# Test Facebook Open Graph
curl -X POST \
  "https://graph.facebook.com/v12.0/" \
  -d "id=https://docs.yourproject.ai/&scrape=true&access_token=$FB_ACCESS_TOKEN"

# Test Twitter Card validation
curl -X GET \
  "https://cards-dev.twitter.com/validator" \
  -d "url=https://docs.yourproject.ai/"

# Test LinkedIn preview
curl -X POST \
  "https://www.linkedin.com/post-inspector/inspect/" \
  -d "url=https://docs.yourproject.ai/"
```

## Code Examples for Advanced Usage

### Dynamic Social Card Generation

```python
# Advanced social card generation
from PIL import Image, ImageDraw, ImageFont
import textwrap

def generate_dynamic_social_card(title, description, output_path):
    """Generate a custom social card with dynamic content."""

    # Load template
    template = Image.open("_static/social-card-template.png")
    draw = ImageDraw.Draw(template)

    # Load fonts
    title_font = ImageFont.truetype("fonts/title.ttf", 60)
    desc_font = ImageFont.truetype("fonts/description.ttf", 30)

    # Add title (wrapped for long titles)
    title_lines = textwrap.wrap(title, width=40)
    y_offset = 200
    for line in title_lines:
        draw.text((100, y_offset), line, font=title_font, fill="#ffffff")
        y_offset += 70

    # Add description
    desc_lines = textwrap.wrap(description, width=80)
    y_offset = 400
    for line in desc_lines[:3]:  # Max 3 lines
        draw.text((100, y_offset), line, font=desc_font, fill="#e2e8f0")
        y_offset += 40

    # Save optimized for social media
    template.save(output_path, "PNG", optimize=True)

# Integration with Sphinx build
def setup(app):
    app.connect("build-finished", generate_all_social_cards)
```

### Platform-Specific Optimization

```python
# Platform-specific Open Graph optimization
def optimize_for_platform(context, platform):
    """Optimize Open Graph tags for specific platforms."""

    if platform == "twitter":
        context.update({
            "og_twitter_card": "summary_large_image",
            "og_twitter_site": "@yourproject",
            "og_twitter_creator": "@yourteam",
            "og_twitter_title": context.get("title", "")[:70],  # Twitter title limit
        })

    elif platform == "linkedin":
        context.update({
            "og_linkedin_company": "your-company-id",
            "og_article_author": "Your Company",
            "og_article_publisher": "https://www.linkedin.com/company/yourcompany",
        })

    elif platform == "facebook":
        context.update({
            "og_fb_app_id": "your-facebook-app-id",
            "og_fb_admins": "your-facebook-admin-id",
        })

# Auto-detect platform and optimize
def detect_and_optimize_platform(app, pagename, templatename, context, doctree):
    """Auto-detect referring platform and optimize accordingly."""

    # This would typically be done on the frontend with JavaScript
    # But we can prepare optimized tags for all platforms

    platforms = ["twitter", "linkedin", "facebook", "slack"]
    for platform in platforms:
        optimize_for_platform(context, platform)

def setup(app):
    app.connect("html-page-context", detect_and_optimize_platform)
```

### A/B Testing for Social Cards

```python
# A/B testing framework for social cards
def setup_social_card_ab_testing(app, pagename, templatename, context, doctree):
    """Setup A/B testing for social card designs."""

    import hashlib
    import random

    # Generate consistent variant based on page URL
    page_hash = hashlib.md5(pagename.encode()).hexdigest()
    variant = "A" if int(page_hash, 16) % 2 == 0 else "B"

    # Configure different social card styles
    if variant == "A":
        context["ogp_social_cards"].update({
            "line_color": "#2563eb",  # Blue theme
            "text_color": "#ffffff",
            "template": "_static/social-card-blue.png",
        })
    else:
        context["ogp_social_cards"].update({
            "line_color": "#dc2626",  # Red theme
            "text_color": "#ffffff",
            "template": "_static/social-card-red.png",
        })

    # Track variant for analytics
    context["social_card_variant"] = variant
```

## Best Practices for Production Deployment

### 1. Image Optimization Strategy

```python
# Optimal social media image configuration
ogp_image_width = 1200   # Standard width for all platforms
ogp_image_height = 630   # Standard height (1.91:1 ratio)
ogp_image_type = "image/png"  # PNG for quality, JPEG for file size

# Multiple image sizes for different contexts
social_image_variants = {
    "large": (1200, 630),    # Primary social card
    "square": (600, 600),    # Square format for some platforms
    "small": (600, 315),     # Smaller format for mobile
}
```

### 2. Content Strategy

```python
# Strategic content optimization
def optimize_social_content(title, description):
    """Optimize content for social media."""

    # Title optimization (Facebook: 95 chars, Twitter: 70 chars)
    optimized_title = title[:60] + "..." if len(title) > 60 else title

    # Description optimization (Facebook: 300 chars, Twitter: 200 chars)
    optimized_desc = description[:150] + "..." if len(description) > 150 else description

    return optimized_title, optimized_desc
```

### 3. Performance Optimization

```python
# Performance-optimized configuration
ogp_cache_duration = 3600  # Cache social cards for 1 hour
ogp_lazy_loading = True    # Enable lazy loading for images
ogp_image_compression = {
    "quality": 85,         # Balance quality vs file size
    "progressive": True,   # Progressive JPEG loading
    "optimize": True,      # Enable optimization
}
```

### 4. Monitoring and Maintenance

```bash
# Regular social media optimization checks
#!/bin/bash

# Check social image accessibility
for image in social-preview.png social-card-template.png; do
    if curl -s -f "https://docs.yourproject.ai/_static/$image" > /dev/null; then
        echo "✅ $image accessible"
    else
        echo "❌ $image not accessible"
    fi
done

# Validate Open Graph tags on key pages
for page in "" "getting-started/" "api/"; do
    URL="https://docs.yourproject.ai/$page"

    # Check required Open Graph tags
    for tag in "og:title" "og:description" "og:image" "og:url"; do
        if curl -s "$URL" | grep -q "$tag"; then
            echo "✅ $tag found on $URL"
        else
            echo "❌ $tag missing on $URL"
        fi
    done
done

# Test social media preview generation
curl -X POST "https://developers.facebook.com/tools/debug/clear_cache/" \
  -d "id=https://docs.yourproject.ai/"
```

## Troubleshooting Common Issues

### Issue: Social Preview Not Showing

**Cause**: Missing or incorrect Open Graph image  
**Solution**:

```python
# Ensure image exists and is accessible
ogp_image = "_static/social-preview.png"  # Must exist in _static/
# Image should be 1200x630 pixels for best results
```

### Issue: Incorrect Social Card Content

**Cause**: Missing or malformed meta tags  
**Solution**:

```python
# Validate required Open Graph tags
required_tags = {
    "ogp_site_url": "https://docs.yourproject.ai/",
    "ogp_site_name": "Your Project",
    "ogp_site_description": "Description",
    "ogp_image": "_static/social-preview.png",
    "ogp_type": "website",
}
```

### Issue: Platform-Specific Problems

**Cause**: Platform-specific tag requirements not met  
**Solution**:

```python
# Add platform-specific tags
ogp_twitter_card = "summary_large_image"  # For Twitter
ogp_fb_app_id = "your-app-id"             # For Facebook
```

## Next Steps for PyDevelop-Docs

### Immediate Improvements

1. **Add Twitter Card Support**: Implement Twitter-specific meta tags
2. **Dynamic Description Generation**: Extract page-specific descriptions automatically
3. **Social Card Templates**: Create multiple social card design variants

### Future Enhancements

1. **A/B Testing Framework**: Test different social card designs for optimization
2. **Platform Analytics**: Track social media performance metrics
3. **Automated Card Generation**: Generate cards automatically based on page content
