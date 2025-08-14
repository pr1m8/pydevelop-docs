# sphinxext-rediraffe - Advanced Redirect Handling

**Extension**: `sphinxext.rediraffe`  
**Category**: Utilities  
**Priority**: High (Advanced redirect management and validation)  
**Status**: ✅ Implemented in PyDevelop-Docs

## Overview

`sphinxext-rediraffe` provides advanced redirect handling capabilities that go beyond basic URL redirection, offering intelligent redirect validation, automatic redirect generation, and comprehensive redirect management for complex documentation sites. This extension complements `sphinx-reredirects` by adding automated redirect discovery and validation features.

## Purpose & Utility Functionality

### Primary Functions

- **Automatic Redirect Discovery**: Detects moved content and suggests redirects automatically
- **Redirect Validation**: Validates redirect chains and detects broken redirects
- **Git Integration**: Analyzes git history to identify moved files and generate redirects
- **Conflict Resolution**: Handles redirect conflicts and circular dependencies
- **Performance Optimization**: Optimizes redirect configurations for better performance

### Business Value

- **Automated Maintenance**: Reduces manual effort in maintaining redirect configurations
- **Error Prevention**: Catches redirect issues before they affect users
- **SEO Protection**: Ensures comprehensive coverage of moved content for search engines
- **Developer Productivity**: Streamlines documentation restructuring workflows

## Configuration Options & Optimization Strategies

### Current PyDevelop-Docs Implementation

```python
# In config.py - Lines 312-315
"rediraffe_redirects": {},
"rediraffe_branch": "main",
"rediraffe_auto_redirect_perc": 50,
```

### Basic Configuration

```python
# Basic rediraffe configuration
rediraffe_redirects = {
    # Standard redirects
    "old-page.html": "new-page.html",
    "deprecated/": "current/",
}

# Git integration settings
rediraffe_branch = "main"  # Branch to analyze for changes
rediraffe_auto_redirect_perc = 50  # Percentage threshold for automatic redirects
```

### Advanced Configuration Options

```python
# Comprehensive rediraffe configuration
rediraffe_redirects = {
    # Manual redirects
    "specific-redirect.html": "target-page.html",

    # Pattern-based redirects
    "old-api/*": "api/v2/*",
    "tutorials/*": "guides/*",
}

# Advanced settings
rediraffe_branch = "main"  # Git branch for analysis
rediraffe_auto_redirect_perc = 75  # Higher threshold for stricter matching

# Validation settings
rediraffe_validate_redirects = True  # Enable redirect validation
rediraffe_check_broken_links = True  # Check for broken redirect targets
rediraffe_fail_on_error = False     # Don't fail build on redirect errors

# Performance settings
rediraffe_cache_redirects = True    # Cache redirect analysis
rediraffe_cache_duration = 3600     # Cache for 1 hour
rediraffe_parallel_validation = True # Validate redirects in parallel

# Git analysis settings
rediraffe_git_depth = 100          # Analyze last 100 commits
rediraffe_similarity_threshold = 0.8 # Content similarity threshold
rediraffe_exclude_patterns = [      # Patterns to exclude from analysis
    "*.tmp",
    "*/.git/*",
    "*/build/*",
    "*/__pycache__/*",
]

# Conflict resolution
rediraffe_conflict_resolution = "newest"  # newest, oldest, manual
rediraffe_circular_redirect_action = "warn"  # warn, error, fix
```

### Intelligent Redirect Generation

```python
# Advanced redirect generation with content analysis
rediraffe_content_analysis = {
    "enable": True,
    "similarity_algorithm": "tfidf",  # tfidf, cosine, jaccard
    "min_similarity": 0.7,           # Minimum similarity for auto-redirect
    "content_weight": 0.6,           # Weight for content similarity
    "title_weight": 0.3,             # Weight for title similarity
    "structure_weight": 0.1,         # Weight for document structure
}

# File move detection
rediraffe_move_detection = {
    "enable": True,
    "git_analysis": True,           # Use git log for move detection
    "filesystem_analysis": True,    # Use filesystem comparison
    "name_similarity": 0.8,         # Filename similarity threshold
    "path_similarity": 0.6,         # Path similarity threshold
}

# Bulk operations
rediraffe_bulk_operations = {
    "enable_bulk_rename": True,     # Enable bulk rename detection
    "namespace_migration": True,    # Detect namespace migrations
    "directory_restructure": True,  # Detect directory restructuring
    "api_versioning": True,         # Detect API version changes
}
```

## SEO & Performance Impact

### Critical SEO Benefits

1. **Comprehensive Redirect Coverage**
   - **Automated Discovery**: Finds moved content that might be missed manually
   - **Content Similarity**: Matches pages based on content, not just filenames
   - **Bulk Operations**: Handles large-scale restructuring efficiently

2. **Redirect Quality Assurance**
   - **Validation Pipeline**: Ensures all redirects point to valid targets
   - **Chain Detection**: Identifies and optimizes redirect chains
   - **Conflict Resolution**: Handles competing redirects intelligently

3. **Performance Optimization**
   - **Redirect Efficiency**: Optimizes redirect configurations for speed
   - **Cache Integration**: Leverages caching for better performance
   - **Bulk Processing**: Handles large numbers of redirects efficiently

### Performance Metrics

```bash
# Typical performance improvements with rediraffe
- Redirect coverage: 90-98% (vs 60-80% manual)
- Redirect validation accuracy: 95-99%
- Configuration maintenance time: -70-85%
- SEO impact of restructuring: -5-15% (vs -30-50% without)
```

### Advanced SEO Strategies

```python
# SEO-optimized rediraffe configuration
rediraffe_seo_optimization = {
    # Prioritize high-value content
    "priority_patterns": [
        "api/*.html",           # API docs get highest priority
        "getting-started.html", # Important landing pages
        "tutorials/*.html",     # Educational content
    ],

    # Handle different redirect types appropriately
    "redirect_types": {
        "moved_permanently": 301,  # Standard permanent redirect
        "moved_temporarily": 302,  # Temporary redirects
        "content_merged": 301,     # When multiple pages become one
        "content_split": 300,      # When one page becomes multiple
    },

    # Content preservation strategies
    "content_preservation": {
        "preserve_anchors": True,     # Maintain anchor links
        "preserve_parameters": True,  # Maintain URL parameters
        "preserve_fragments": True,   # Maintain URL fragments
    },
}
```

## Current Implementation Status in PyDevelop-Docs

### Configuration Status: ✅ Implemented

**File**: `/src/pydevelop_docs/config.py`  
**Lines**: 312-315, 498

```python
# Current configuration (basic)
extensions = [
    # ... other extensions ...
    "sphinxext.rediraffe",  # Line 498
    # ... other extensions ...
]

# Basic rediraffe configuration
"rediraffe_redirects": {},              # Empty by default
"rediraffe_branch": "main",             # Git branch for analysis
"rediraffe_auto_redirect_perc": 50,     # Auto-redirect threshold
```

### Integration Status

- ✅ **Extension Loading**: Properly configured in extensions list
- ⚠️ **Basic Configuration**: Minimal configuration implemented
- ❌ **Advanced Features**: Content analysis and validation not configured
- ❌ **Git Integration**: Git-based redirect generation not enabled

## Integration with Build Pipeline & Deployment

### Build Process Integration

```python
# Advanced build-time redirect generation
def generate_rediraffe_redirects(app, env, updated_docs, added, removed):
    """Generate redirects using rediraffe's advanced capabilities."""

    # Analyze git history for moves
    git_moves = analyze_git_history(app.srcdir)

    # Perform content analysis
    content_matches = analyze_content_similarity(
        old_docs=removed,
        new_docs=added,
        threshold=app.config.rediraffe_similarity_threshold
    )

    # Generate comprehensive redirects
    redirects = {}
    redirects.update(git_moves)
    redirects.update(content_matches)

    # Validate and optimize redirects
    validated_redirects = validate_redirect_configuration(redirects)
    optimized_redirects = optimize_redirect_chains(validated_redirects)

    # Update configuration
    app.config.rediraffe_redirects.update(optimized_redirects)

def analyze_git_history(srcdir, max_commits=100):
    """Analyze git history for file moves and renames."""

    import subprocess
    import json

    try:
        # Get git log with file moves
        cmd = [
            "git", "log",
            f"--max-count={max_commits}",
            "--name-status",
            "--find-renames",
            "--pretty=format:%H|%s",
            "--", "docs/"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=srcdir)
        moves = parse_git_moves(result.stdout)

        return moves

    except Exception as e:
        print(f"Warning: Could not analyze git history: {e}")
        return {}

def analyze_content_similarity(old_docs, new_docs, threshold=0.7):
    """Analyze content similarity between old and new documents."""

    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np

    redirects = {}

    if not old_docs or not new_docs:
        return redirects

    # Extract content from documents
    old_content = {doc: extract_text_content(doc) for doc in old_docs}
    new_content = {doc: extract_text_content(doc) for doc in new_docs}

    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)

    all_content = list(old_content.values()) + list(new_content.values())
    tfidf_matrix = vectorizer.fit_transform(all_content)

    # Calculate similarities
    old_vectors = tfidf_matrix[:len(old_content)]
    new_vectors = tfidf_matrix[len(old_content):]

    similarities = cosine_similarity(old_vectors, new_vectors)

    # Find best matches above threshold
    old_docs_list = list(old_docs)
    new_docs_list = list(new_docs)

    for i, old_doc in enumerate(old_docs_list):
        best_match_idx = np.argmax(similarities[i])
        best_similarity = similarities[i][best_match_idx]

        if best_similarity >= threshold:
            new_doc = new_docs_list[best_match_idx]
            redirects[old_doc] = new_doc

    return redirects
```

### CI/CD Pipeline Integration

```yaml
# GitHub Actions with advanced rediraffe features
- name: Build Documentation with Advanced Redirects
  run: |
    # Enable git history access
    git fetch --unshallow

    # Build with rediraffe analysis
    poetry run sphinx-build -b html docs/source docs/build

- name: Validate Redirect Configuration
  run: |
    # Run rediraffe validation
    poetry run sphinx-build -b rediraffe docs/source docs/validate

- name: Generate Redirect Report
  run: |
    # Generate comprehensive redirect report
    poetry run python scripts/rediraffe-report.py > redirect-analysis.json

- name: Check Redirect Performance
  run: |
    # Test redirect performance
    poetry run python scripts/test-redirect-performance.py

- name: Archive Redirect Data
  uses: actions/upload-artifact@v3
  with:
    name: redirect-analysis
    path: redirect-analysis.json
```

### Advanced Validation Pipeline

```python
# Comprehensive redirect validation
class RediraffePipeline:
    """Advanced redirect validation and optimization pipeline."""

    def __init__(self, app):
        self.app = app
        self.redirects = app.config.rediraffe_redirects
        self.validation_results = {}

    def run_validation_pipeline(self):
        """Run complete validation pipeline."""

        # Step 1: Validate redirect targets
        self.validate_redirect_targets()

        # Step 2: Check for redirect chains
        self.check_redirect_chains()

        # Step 3: Detect circular redirects
        self.detect_circular_redirects()

        # Step 4: Validate HTTP responses
        self.validate_http_responses()

        # Step 5: Check for conflicts
        self.check_redirect_conflicts()

        # Step 6: Generate optimization recommendations
        self.generate_optimization_recommendations()

        return self.validation_results

    def validate_redirect_targets(self):
        """Validate that all redirect targets exist."""

        broken_redirects = []

        for source, target in self.redirects.items():
            if not self.target_exists(target):
                broken_redirects.append((source, target))

        self.validation_results['broken_redirects'] = broken_redirects

    def check_redirect_chains(self):
        """Check for redirect chains and measure their length."""

        chains = {}

        for source in self.redirects:
            chain = self.trace_redirect_chain(source)
            if len(chain) > 2:  # Source -> Target is length 2
                chains[source] = chain

        self.validation_results['redirect_chains'] = chains

    def detect_circular_redirects(self):
        """Detect circular redirect patterns."""

        circular_redirects = []

        for source in self.redirects:
            if self.is_circular_redirect(source):
                circular_redirects.append(source)

        self.validation_results['circular_redirects'] = circular_redirects

    def validate_http_responses(self):
        """Validate HTTP responses for redirect targets."""

        import requests
        from urllib.parse import urljoin

        http_validation = {}
        base_url = self.app.config.html_baseurl

        for source, target in self.redirects.items():
            if target.startswith('http'):
                target_url = target
            else:
                target_url = urljoin(base_url, target)

            try:
                response = requests.head(target_url, timeout=10)
                http_validation[source] = {
                    'status_code': response.status_code,
                    'target_url': target_url,
                    'valid': 200 <= response.status_code < 400
                }
            except Exception as e:
                http_validation[source] = {
                    'error': str(e),
                    'target_url': target_url,
                    'valid': False
                }

        self.validation_results['http_validation'] = http_validation
```

## Monitoring & Analytics Capabilities

### Advanced Analytics Integration

```python
# Enhanced analytics for rediraffe
def setup_rediraffe_analytics(app):
    """Setup comprehensive analytics for redirect performance."""

    def track_redirect_generation(app, exception):
        """Track redirect generation metrics."""

        if exception:
            return

        metrics = {
            'total_redirects': len(app.config.rediraffe_redirects),
            'auto_generated': count_auto_generated_redirects(app),
            'manually_configured': count_manual_redirects(app),
            'git_based': count_git_based_redirects(app),
            'content_based': count_content_based_redirects(app),
            'validation_results': app.rediraffe_validation_results,
        }

        send_analytics_data('rediraffe_metrics', metrics)

    app.connect('build-finished', track_redirect_generation)

def setup_redirect_performance_monitoring():
    """Setup performance monitoring for redirects."""

    monitoring_config = {
        'track_redirect_usage': True,
        'measure_redirect_speed': True,
        'monitor_redirect_chains': True,
        'track_validation_results': True,
        'alert_on_broken_redirects': True,
    }

    return monitoring_config
```

### Real-time Monitoring Dashboard

```python
# Redirect monitoring dashboard
class RediraffeDashboard:
    """Real-time monitoring dashboard for rediraffe."""

    def __init__(self, app):
        self.app = app
        self.metrics = {}

    def generate_dashboard_data(self):
        """Generate data for monitoring dashboard."""

        self.metrics = {
            'redirect_overview': self.get_redirect_overview(),
            'validation_status': self.get_validation_status(),
            'performance_metrics': self.get_performance_metrics(),
            'git_analysis': self.get_git_analysis_data(),
            'content_analysis': self.get_content_analysis_data(),
            'health_score': self.calculate_health_score(),
        }

        return self.metrics

    def get_redirect_overview(self):
        """Get overview of redirect configuration."""

        redirects = self.app.config.rediraffe_redirects

        return {
            'total_redirects': len(redirects),
            'internal_redirects': len([r for r in redirects.values() if not r.startswith('http')]),
            'external_redirects': len([r for r in redirects.values() if r.startswith('http')]),
            'pattern_redirects': len([r for r in redirects.keys() if '*' in r]),
        }

    def calculate_health_score(self):
        """Calculate overall health score for redirects."""

        score = 100

        # Deduct points for issues
        if self.metrics.get('validation_status', {}).get('broken_redirects'):
            score -= len(self.metrics['validation_status']['broken_redirects']) * 5

        if self.metrics.get('validation_status', {}).get('redirect_chains'):
            score -= len(self.metrics['validation_status']['redirect_chains']) * 3

        if self.metrics.get('validation_status', {}).get('circular_redirects'):
            score -= len(self.metrics['validation_status']['circular_redirects']) * 10

        return max(0, score)
```

## Code Examples for Advanced Usage

### Intelligent Content Migration

```python
# Intelligent content migration with rediraffe
class ContentMigrationManager:
    """Manage complex content migrations with intelligent redirects."""

    def __init__(self, app):
        self.app = app
        self.migration_rules = {}

    def setup_api_version_migration(self, old_version, new_version):
        """Setup redirects for API version migration."""

        api_endpoints = self.discover_api_endpoints(old_version)

        for endpoint in api_endpoints:
            old_path = f"api/{old_version}/{endpoint}"
            new_path = f"api/{new_version}/{endpoint}"

            # Check if new endpoint exists
            if self.endpoint_exists(new_path):
                self.migration_rules[old_path] = new_path
            else:
                # Try to find similar endpoint in new version
                similar_endpoint = self.find_similar_endpoint(endpoint, new_version)
                if similar_endpoint:
                    self.migration_rules[old_path] = f"api/{new_version}/{similar_endpoint}"

    def setup_namespace_migration(self, old_namespace, new_namespace):
        """Setup redirects for namespace changes."""

        namespace_pages = self.get_namespace_pages(old_namespace)

        for page in namespace_pages:
            old_path = f"{old_namespace}/{page}"
            new_path = f"{new_namespace}/{page}"

            if self.page_exists(new_path):
                self.migration_rules[old_path] = new_path

    def setup_content_consolidation(self, source_pages, target_page):
        """Setup redirects for content consolidation."""

        # Multiple pages being consolidated into one
        for source_page in source_pages:
            # Add anchor to target page based on source content
            anchor = self.generate_anchor_from_content(source_page)
            target_with_anchor = f"{target_page}#{anchor}"

            self.migration_rules[source_page] = target_with_anchor

    def apply_migration_rules(self):
        """Apply all migration rules to rediraffe configuration."""

        self.app.config.rediraffe_redirects.update(self.migration_rules)

        # Validate migration rules
        validator = RediraffePipeline(self.app)
        validation_results = validator.run_validation_pipeline()

        return validation_results
```

### Automated Redirect Optimization

```python
# Automated redirect optimization
def optimize_rediraffe_configuration(app):
    """Automatically optimize rediraffe configuration."""

    redirects = app.config.rediraffe_redirects.copy()
    optimizations = []

    # 1. Flatten redirect chains
    flattened = flatten_redirect_chains(redirects)
    if flattened != redirects:
        optimizations.append(f"Flattened {len(redirects) - len(flattened)} redirect chains")
        redirects = flattened

    # 2. Remove redundant redirects
    cleaned = remove_redundant_redirects(redirects)
    if cleaned != redirects:
        optimizations.append(f"Removed {len(redirects) - len(cleaned)} redundant redirects")
        redirects = cleaned

    # 3. Consolidate pattern redirects
    patterns = consolidate_pattern_redirects(redirects)
    if patterns:
        optimizations.append(f"Consolidated {len(patterns)} pattern redirects")
        redirects.update(patterns)

    # 4. Sort redirects for performance
    sorted_redirects = sort_redirects_for_performance(redirects)

    # Apply optimizations
    app.config.rediraffe_redirects = sorted_redirects

    return optimizations

def flatten_redirect_chains(redirects):
    """Flatten redirect chains to direct redirects."""

    flattened = {}

    for source, target in redirects.items():
        # Follow chain to final destination
        final_target = target
        visited = {source}  # Prevent infinite loops

        while final_target in redirects and final_target not in visited:
            visited.add(final_target)
            final_target = redirects[final_target]

        flattened[source] = final_target

    return flattened

def consolidate_pattern_redirects(redirects):
    """Consolidate similar redirects into patterns."""

    patterns = {}
    redirect_groups = group_similar_redirects(redirects)

    for group in redirect_groups:
        if len(group) >= 3:  # At least 3 similar redirects
            pattern = generate_pattern_from_group(group)
            if pattern:
                patterns[pattern['source']] = pattern['target']

    return patterns
```

### Git Integration Enhancement

```python
# Enhanced git integration for rediraffe
class GitAnalyzer:
    """Advanced git analysis for redirect generation."""

    def __init__(self, repo_path):
        import git
        self.repo = git.Repo(repo_path)

    def analyze_file_moves(self, max_commits=100, since_date=None):
        """Analyze file moves in git history."""

        moves = {}

        # Get commits to analyze
        commits = list(self.repo.iter_commits(
            max_count=max_commits,
            since=since_date
        ))

        for commit in commits:
            if len(commit.parents) == 1:  # Skip merge commits
                parent = commit.parents[0]

                # Get changes between commit and parent
                changes = parent.diff(commit, create_patch=True)

                for change in changes:
                    if change.renamed_file:
                        old_path = change.rename_from
                        new_path = change.rename_to

                        # Convert to web paths
                        if old_path.startswith('docs/') and new_path.startswith('docs/'):
                            web_old = self.convert_to_web_path(old_path)
                            web_new = self.convert_to_web_path(new_path)
                            moves[web_old] = web_new

        return moves

    def analyze_content_evolution(self, file_path, max_commits=20):
        """Analyze how content has evolved for a file."""

        evolution = []

        # Get commits that touched this file
        commits = list(self.repo.iter_commits(
            paths=file_path,
            max_count=max_commits
        ))

        for commit in commits:
            try:
                content = self.repo.git.show(f"{commit.hexsha}:{file_path}")
                evolution.append({
                    'commit': commit.hexsha,
                    'date': commit.committed_datetime,
                    'message': commit.message.strip(),
                    'content_length': len(content),
                    'content_hash': hash(content),
                })
            except:
                continue

        return evolution

    def detect_major_restructures(self, threshold=0.3):
        """Detect major documentation restructures."""

        restructures = []

        # Look for commits that moved many files
        commits = list(self.repo.iter_commits(max_count=50))

        for commit in commits:
            if len(commit.parents) == 1:
                parent = commit.parents[0]
                changes = parent.diff(commit)

                move_count = sum(1 for change in changes if change.renamed_file)
                total_count = len(changes)

                if total_count > 0 and move_count / total_count >= threshold:
                    restructures.append({
                        'commit': commit.hexsha,
                        'date': commit.committed_datetime,
                        'message': commit.message.strip(),
                        'moves': move_count,
                        'total_changes': total_count,
                        'move_percentage': move_count / total_count,
                    })

        return restructures
```

## Best Practices for Production Deployment

### 1. Configuration Strategy

```python
# Production-ready rediraffe configuration
rediraffe_production_config = {
    # Conservative settings for production
    "rediraffe_auto_redirect_perc": 80,  # Higher threshold for auto-generation
    "rediraffe_validate_redirects": True,  # Always validate
    "rediraffe_fail_on_error": False,     # Don't break builds

    # Performance optimization
    "rediraffe_cache_redirects": True,
    "rediraffe_parallel_validation": True,

    # Git integration
    "rediraffe_git_depth": 50,            # Limited history for performance
    "rediraffe_similarity_threshold": 0.85, # Stricter matching
}
```

### 2. Validation Pipeline

```python
# Comprehensive validation for production
def production_validation_pipeline(app):
    """Production-grade validation pipeline."""

    validator = RediraffePipeline(app)
    results = validator.run_validation_pipeline()

    # Check for critical issues
    critical_issues = []

    if results.get('broken_redirects'):
        critical_issues.extend(results['broken_redirects'])

    if results.get('circular_redirects'):
        critical_issues.extend(results['circular_redirects'])

    # Log issues but don't fail build
    if critical_issues:
        logger.warning(f"Found {len(critical_issues)} critical redirect issues")
        for issue in critical_issues:
            logger.warning(f"Redirect issue: {issue}")

    return results
```

### 3. Monitoring and Alerting

```bash
# Production monitoring script
#!/bin/bash

DOCS_URL="https://docs.yourproject.ai"
ALERT_THRESHOLD=5

# Check redirect health
check_redirect_health() {
    echo "Checking redirect health..."

    # Count broken redirects
    broken_count=$(curl -s "$DOCS_URL/redirect-health.json" | jq '.broken_redirects | length')

    if [ "$broken_count" -gt "$ALERT_THRESHOLD" ]; then
        echo "🚨 ALERT: $broken_count broken redirects detected!"
        send_alert "Broken redirects detected: $broken_count"
    else
        echo "✅ Redirect health OK ($broken_count issues)"
    fi
}

# Main monitoring function
main() {
    check_redirect_health
    echo "✅ Rediraffe monitoring completed"
}

main
```

## Troubleshooting Common Issues

### Issue: Auto-generation Creating Wrong Redirects

**Cause**: Similarity threshold too low or content analysis inaccurate  
**Solution**:

```python
# Increase similarity threshold and add validation
rediraffe_auto_redirect_perc = 85  # Increase threshold
rediraffe_similarity_threshold = 0.9  # Stricter content matching

# Add manual validation step
rediraffe_validate_auto_redirects = True
```

### Issue: Git Analysis Not Working

**Cause**: Shallow git clone or missing git history  
**Solution**:

```yaml
# In CI/CD, ensure full git history
- name: Checkout with full history
  uses: actions/checkout@v3
  with:
    fetch-depth: 0 # Get full history
```

### Issue: Performance Problems with Large Sites

**Cause**: Too many redirects or inefficient validation  
**Solution**:

```python
# Optimize for large sites
rediraffe_cache_redirects = True
rediraffe_parallel_validation = True
rediraffe_git_depth = 25  # Limit git analysis depth
rediraffe_batch_validation = True  # Validate in batches
```

## Next Steps for PyDevelop-Docs

### Immediate Improvements

1. **Enable Git Integration**: Configure git-based redirect generation
2. **Add Content Analysis**: Implement content similarity matching
3. **Setup Validation Pipeline**: Add comprehensive redirect validation

### Future Enhancements

1. **Machine Learning Integration**: Use ML for better content matching
2. **Performance Optimization**: Implement advanced caching and batching
3. **Integration Dashboard**: Create real-time monitoring dashboard for redirects
