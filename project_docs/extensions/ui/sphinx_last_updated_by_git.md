# Sphinx Last Updated by Git - Intelligent Change Tracking and Attribution

**Extension**: `sphinx_last_updated_by_git`  
**Purpose**: Git-based timestamps and author attribution for documentation  
**Category**: UI Enhancement  
**Installation**: `pip install sphinx-last-updated-by-git`

## Overview

Sphinx Last Updated by Git transforms static documentation into a dynamic, transparent system that automatically tracks and displays when content was last modified, by whom, and provides complete change history. This extension bridges the gap between documentation and development workflow, providing accountability, freshness indicators, and collaborative transparency that builds trust with documentation users.

## User Experience Improvements

### Trust and Transparency

- **Freshness Indicators**: Users know immediately how current the information is
- **Author Attribution**: Clear responsibility and contact points for content
- **Change Tracking**: Complete history of modifications and improvements
- **Quality Assurance**: Recent updates suggest actively maintained content

### Navigation and Discovery

- **Recency Sorting**: Find the most recently updated content first
- **Change Notifications**: Visual indicators for recently modified pages
- **Author-Based Browsing**: Discover content by specific contributors
- **Maintenance Insights**: Identify outdated content that needs attention

### Collaborative Documentation

- **Contributor Recognition**: Acknowledge documentation authors and maintainers
- **Review Workflow**: Integration with code review and approval processes
- **Change Context**: Link documentation updates to code changes
- **Team Coordination**: Understand who's working on what documentation

## Current PyDevelop-Docs Configuration

```python
# Git last updated configuration - Intelligent change tracking
"git_last_updated_show_commit_hash": True,      # Show abbreviated commit hash
"git_last_updated_format": "%Y-%m-%d %H:%M",    # Human-readable timestamp format
```

## Configuration Options and Visual Customization

### Basic Configuration

```python
# Core git tracking settings
"git_last_updated_show_commit_hash": True,      # Display commit hash
"git_last_updated_format": "%Y-%m-%d %H:%M",    # Timestamp format
"git_last_updated_timezone": "UTC",             # Timezone for timestamps
"git_last_updated_show_author": True,           # Show commit author
"git_last_updated_show_email": False,           # Hide email addresses
```

### Advanced Display Options

```python
# Enhanced information display
"git_last_updated_detailed": {
    "show_commit_message": True,                 # Include commit message
    "show_branch_info": True,                    # Display source branch
    "show_tag_info": True,                       # Show related tags
    "show_file_stats": True,                     # Lines added/removed
    "max_commit_message_length": 80,             # Truncate long messages
    "author_format": "name_only",                # name_only, email, full
    "link_to_commit": True,                      # Link to repository commit
}
```

### Time and Date Formatting

```python
# Flexible timestamp presentation
"git_timestamp_formats": {
    "detailed": "%A, %B %d, %Y at %I:%M %p %Z",  # Full human format
    "standard": "%Y-%m-%d %H:%M",                # ISO-like format
    "relative": "relative",                      # "2 days ago" format
    "compact": "%m/%d/%Y",                       # Short format
    "iso": "%Y-%m-%dT%H:%M:%SZ",                # ISO 8601 format
}

# Multi-language date support
"git_date_localization": {
    "locale": "auto",                            # Auto-detect user locale
    "fallback_locale": "en_US",                  # Fallback language
    "custom_formats": {
        "en": "%B %d, %Y",
        "es": "%d de %B de %Y",
        "fr": "%d %B %Y",
        "de": "%d. %B %Y",
    }
}
```

### Repository Integration

```python
# Repository connection settings
"git_repository_config": {
    "repository_url": "https://github.com/user/repo",   # Base repository URL
    "branch": "main",                            # Default branch
    "commit_url_template": "{repo}/commit/{hash}",       # Commit link template
    "file_history_template": "{repo}/commits/{branch}/{path}",  # File history link
    "blame_url_template": "{repo}/blame/{branch}/{path}",      # Git blame link
}
```

## Template Integration for Enhanced UX

### Page Header Integration

**File**: `_templates/page.html`

```html
{%- block content -%}
<div class="document-meta">
  {%- if last_updated -%}
  <div class="last-updated-info">
    <div class="update-summary">
      <span class="update-icon">🕒</span>
      <span class="update-text">
        Last updated:
        <time
          datetime="{{ last_updated.isoformat() }}"
          title="{{ last_updated.strftime('%A, %B %d, %Y at %I:%M %p') }}"
        >
          {{ last_updated.strftime('%Y-%m-%d %H:%M') }}
        </time>
      </span>
    </div>

    {%- if git_author -%}
    <div class="author-info">
      <span class="author-icon">👤</span>
      <span class="author-text">
        by <strong>{{ git_author.name }}</strong> {%- if git_author.email and
        show_email -%} &lt;<a href="mailto:{{ git_author.email }}"
          >{{ git_author.email }}</a
        >&gt; {%- endif -%}
      </span>
    </div>
    {%- endif -%} {%- if git_commit_hash -%}
    <div class="commit-info">
      <span class="commit-icon">🔗</span>
      <span class="commit-text">
        Commit:
        <a
          href="{{ repository_url }}/commit/{{ git_commit_hash }}"
          class="commit-link"
          title="View this commit on GitHub"
        >
          <code>{{ git_commit_hash[:7] }}</code>
        </a>
      </span>
    </div>
    {%- endif -%} {%- if git_commit_message -%}
    <div class="commit-message">
      <span class="message-icon">💬</span>
      <span class="message-text">{{ git_commit_message | truncate(80) }}</span>
    </div>
    {%- endif -%}
  </div>
  {%- endif -%}
</div>

{{ super() }} {%- endblock -%}
```

### Footer Attribution

**File**: `_templates/layout.html`

```html
{%- block footer -%}
<footer class="documentation-footer">
  <div class="footer-content">
    <div class="footer-section">
      <h4>📚 Documentation Info</h4>
      {%- if page_source_date -%}
      <p>
        <strong>Last updated:</strong>
        <time datetime="{{ page_source_date.isoformat() }}">
          {{ page_source_date.strftime('%B %d, %Y') }}
        </time>
      </p>
      {%- endif -%} {%- if git_contributors -%}
      <p>
        <strong>Contributors:</strong>
        {%- for contributor in git_contributors[:3] -%}
        <span class="contributor">{{ contributor.name }}</span>
        {%- if not loop.last %}, {% endif -%} {%- endfor -%} {%- if
        git_contributors|length > 3 -%} and {{ git_contributors|length - 3 }}
        others {%- endif -%}
      </p>
      {%- endif -%}
    </div>

    <div class="footer-section">
      <h4>🔗 Source & History</h4>
      <ul class="source-links">
        <li>
          <a
            href="{{ repository_url }}/blob/{{ git_branch }}/{{ page_source_suffix }}"
          >
            📝 Edit this page
          </a>
        </li>
        <li>
          <a
            href="{{ repository_url }}/commits/{{ git_branch }}/{{ page_source_suffix }}"
          >
            📜 View page history
          </a>
        </li>
        <li>
          <a
            href="{{ repository_url }}/blame/{{ git_branch }}/{{ page_source_suffix }}"
          >
            🔍 View line-by-line attribution
          </a>
        </li>
      </ul>
    </div>
  </div>
</footer>
{%- endblock -%}
```

### AutoAPI Integration with Git Info

**File**: `_autoapi_templates/python/class.rst`

```jinja2
{%- if obj.source_file -%}
.. raw:: html

   <div class="api-source-info">
       <h4>📁 Source Information</h4>
       <div class="source-details">
           <div class="source-file">
               <strong>File:</strong>
               <a href="{{ repository_url }}/blob/{{ git_branch }}/{{ obj.source_file }}">
                   <code>{{ obj.source_file }}</code>
               </a>
           </div>

           {%- if obj.last_modified -%}
           <div class="source-modified">
               <strong>Last modified:</strong>
               <time datetime="{{ obj.last_modified.isoformat() }}">
                   {{ obj.last_modified.strftime('%Y-%m-%d') }}
               </time>
               by {{ obj.last_author or 'Unknown' }}
           </div>
           {%- endif -%}

           <div class="source-links">
               <a href="{{ repository_url }}/commits/{{ git_branch }}/{{ obj.source_file }}"
                  class="history-link">
                  📜 View history
               </a>
               <a href="{{ repository_url }}/blame/{{ git_branch }}/{{ obj.source_file }}#L{{ obj.line_number }}"
                  class="blame-link">
                  🔍 View blame
               </a>
           </div>
       </div>
   </div>

{%- endif -%}
```

### Recently Updated Content Widget

```rst
.. raw:: html

   <div class="recently-updated-widget">
       <h3>🔄 Recently Updated</h3>
       <div class="update-list">
           {% for page in recently_updated_pages[:5] %}
           <div class="update-item">
               <div class="update-title">
                   <a href="{{ page.url }}">{{ page.title }}</a>
               </div>
               <div class="update-meta">
                   <time datetime="{{ page.last_updated.isoformat() }}">
                       {{ page.last_updated.strftime('%m/%d/%Y') }}
                   </time>
                   by {{ page.author }}
               </div>
           </div>
           {% endfor %}
       </div>
       <div class="update-actions">
           <a href="/changelog/" class="view-all-link">View all changes →</a>
       </div>
   </div>
```

## Accessibility Considerations and WCAG Compliance

### Semantic Time Elements

```html
<!-- Accessible timestamp markup -->
<time
  datetime="{{ timestamp.isoformat() }}"
  class="last-updated-time"
  aria-label="Last updated on {{ timestamp.strftime('%A, %B %d, %Y at %I:%M %p') }}"
>
  {{ timestamp.strftime('%Y-%m-%d %H:%M') }}
</time>

<!-- Extended accessibility information -->
<div class="update-info" role="complementary" aria-label="Document metadata">
  <h4 id="doc-meta-heading">Document Information</h4>
  <dl aria-labelledby="doc-meta-heading">
    <dt>Last updated:</dt>
    <dd>
      <time datetime="{{ last_updated.isoformat() }}">
        {{ last_updated.strftime('%B %d, %Y') }}
      </time>
    </dd>

    <dt>Author:</dt>
    <dd>{{ author_name }}</dd>

    <dt>Commit:</dt>
    <dd>
      <a
        href="{{ commit_url }}"
        aria-label="View commit {{ commit_hash }} on GitHub"
      >
        {{ commit_hash[:7] }}
      </a>
    </dd>
  </dl>
</div>
```

### Screen Reader Enhancements

```python
# Screen reader optimized configuration
"git_accessibility": {
    "provide_aria_labels": True,              # Add descriptive ARIA labels
    "use_semantic_time": True,                # Use <time> elements
    "verbose_descriptions": True,             # Detailed descriptions
    "skip_decorative_info": False,            # Include all information
}

# Custom ARIA label templates
"git_aria_templates": {
    "last_updated": "Last updated on {date} at {time}",
    "author_info": "Last modified by {author}",
    "commit_info": "Commit {hash} with message: {message}",
    "file_history": "View complete change history for this file",
}
```

### High Contrast Mode Support

```css
/* High contrast accessibility */
@media (prefers-contrast: high) {
  .last-updated-info {
    border: 2px solid CanvasText;
    background: Canvas;
    color: CanvasText;
  }

  .commit-link {
    color: LinkText;
    text-decoration: underline;
  }

  .author-info strong {
    color: CanvasText;
    font-weight: bold;
    background: Highlight;
    padding: 2px 4px;
  }
}

/* Focus indicators */
.commit-link:focus,
.history-link:focus {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
  border-radius: 4px;
}
```

## Mobile Optimization and Responsive Behavior

### Mobile-First Information Display

```css
/* Mobile-optimized git information */
.last-updated-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px;
  background: #f8fafc;
  border-left: 4px solid #2563eb;
  border-radius: 4px;
  margin: 1rem 0;
}

@media (max-width: 768px) {
  .last-updated-info {
    margin: 0.5rem -1rem;
    border-radius: 0;
    border-left-width: 3px;
    padding: 8px 16px;
  }

  /* Compact mobile display */
  .update-summary,
  .author-info,
  .commit-info {
    font-size: 14px;
    line-height: 1.4;
  }

  /* Stack elements vertically */
  .commit-info {
    flex-direction: column;
    align-items: flex-start;
  }

  /* Shorter commit hashes on mobile */
  .commit-link code {
    font-size: 12px;
  }
}

/* Ultra-mobile optimization */
@media (max-width: 480px) {
  .last-updated-info {
    font-size: 12px;
  }

  /* Hide less critical information on small screens */
  .commit-message {
    display: none;
  }

  /* Simplify timestamp format */
  .update-text time::after {
    content: " (" attr(data-relative) ")";
  }
}
```

### Touch-Friendly Links

```css
/* Touch-optimized interactive elements */
.source-links a,
.commit-link,
.history-link {
  display: inline-block;
  padding: 8px 12px;
  margin: 4px 2px;
  border-radius: 4px;
  background: #e2e8f0;
  color: #1e293b;
  text-decoration: none;
  min-width: 44px; /* Minimum touch target */
  min-height: 44px;
  text-align: center;
  transition: all 0.2s ease;
}

.source-links a:hover,
.commit-link:hover {
  background: #cbd5e1;
  transform: translateY(-1px);
}

.source-links a:active,
.commit-link:active {
  transform: translateY(0);
}
```

### Progressive Information Disclosure

```javascript
// Mobile-friendly progressive disclosure
class MobileGitInfo {
  constructor() {
    this.initMobileOptimization();
  }

  initMobileOptimization() {
    if (window.innerWidth <= 768) {
      this.createCompactView();
      this.addExpandableDetails();
    }
  }

  createCompactView() {
    const gitInfo = document.querySelectorAll(".last-updated-info");

    gitInfo.forEach((info) => {
      const summary = info.querySelector(".update-summary");
      const details = info.querySelectorAll(
        ".author-info, .commit-info, .commit-message",
      );

      // Create toggle button
      const toggleButton = document.createElement("button");
      toggleButton.className = "git-info-toggle";
      toggleButton.innerHTML = "📋 Details";
      toggleButton.setAttribute("aria-expanded", "false");

      // Create collapsible container
      const detailsContainer = document.createElement("div");
      detailsContainer.className = "git-details-container collapsed";

      // Move detailed info to container
      details.forEach((detail) => {
        detailsContainer.appendChild(detail);
      });

      // Add toggle functionality
      toggleButton.addEventListener("click", () => {
        this.toggleDetails(toggleButton, detailsContainer);
      });

      // Insert into DOM
      summary.appendChild(toggleButton);
      info.appendChild(detailsContainer);
    });
  }

  toggleDetails(button, container) {
    const isExpanded = button.getAttribute("aria-expanded") === "true";

    button.setAttribute("aria-expanded", !isExpanded);
    container.classList.toggle("collapsed");

    button.innerHTML = isExpanded ? "📋 Details" : "🔼 Less";

    // Smooth animation
    if (!isExpanded) {
      container.style.maxHeight = container.scrollHeight + "px";
    } else {
      container.style.maxHeight = "0";
    }
  }
}
```

## Performance Impact and Optimization Strategies

### Performance Metrics

- **Git Operations**: ~10-50ms per file (depends on repository size)
- **Memory Usage**: <1MB for metadata of 1000+ files
- **Build Time Impact**: +5-15% depending on repository history depth
- **Caching Benefits**: 90%+ performance improvement with proper caching

### Optimization Techniques

#### Git Information Caching

```python
# Performance optimization configuration
"git_performance": {
    "enable_caching": True,               # Cache git information
    "cache_duration": 3600,               # Cache for 1 hour
    "cache_file": ".git_cache.json",      # Cache file location
    "max_cache_size": "50MB",             # Maximum cache size
    "parallel_processing": True,          # Process files in parallel
    "batch_size": 100,                    # Files per batch
}

# Selective information gathering
"git_optimization": {
    "shallow_clone_depth": 50,            # Limit history depth
    "exclude_merge_commits": True,        # Skip merge commits
    "author_email_privacy": True,         # Hash email addresses
    "commit_message_length": 100,         # Truncate long messages
}
```

#### Incremental Updates

```python
# Smart incremental processing
"git_incremental": {
    "enable_incremental": True,           # Only check changed files
    "track_file_changes": True,           # Monitor file modifications
    "update_strategy": "smart",           # Only update when needed
    "force_refresh_interval": "24h",      # Force refresh daily
}
```

#### Asynchronous Loading

```javascript
// Lazy load git information
class AsyncGitInfo {
  constructor() {
    this.loadGitInfo();
  }

  async loadGitInfo() {
    const gitContainers = document.querySelectorAll("[data-git-info]");

    // Use Intersection Observer for lazy loading
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          this.fetchGitData(entry.target);
          observer.unobserve(entry.target);
        }
      });
    });

    gitContainers.forEach((container) => {
      observer.observe(container);
    });
  }

  async fetchGitData(container) {
    const filePath = container.dataset.filePath;

    try {
      const response = await fetch(
        `/api/git-info/${encodeURIComponent(filePath)}`,
      );
      const gitData = await response.json();

      this.renderGitInfo(container, gitData);
    } catch (error) {
      console.warn("Failed to load git information:", error);
      container.style.display = "none";
    }
  }

  renderGitInfo(container, data) {
    container.innerHTML = `
            <div class="git-info-loaded">
                <time datetime="${data.lastUpdated}">${data.formattedDate}</time>
                <span class="author">by ${data.author}</span>
                <a href="${data.commitUrl}" class="commit-link">${data.shortHash}</a>
            </div>
        `;
  }
}
```

This extension provides comprehensive Git-based change tracking that enhances documentation transparency, builds user trust, and facilitates collaborative documentation workflows while maintaining excellent performance and accessibility across all devices.
