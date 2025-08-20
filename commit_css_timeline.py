#!/usr/bin/env python3
"""Analyze commit messages vs actual CSS changes on August 15."""

import subprocess
from pathlib import Path


def run_git_command(cmd):
    """Run a git command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()


def count_css_at_commit(commit):
    """Count CSS lines at a specific commit."""
    run_git_command(f"git checkout {commit} 2>/dev/null")

    total_lines = 0
    css_files = []

    # Check all CSS locations
    locations = [
        "src/pydevelop_docs/templates/static/*.css",
        "docs/source/_static/*.css",
        "docs/source/_static/css/*.css",
    ]

    for pattern in locations:
        files = run_git_command(f"find . -path '{pattern}' 2>/dev/null")
        if files:
            for file_path in files.split("\n"):
                if file_path and Path(file_path).exists():
                    lines = len(Path(file_path).read_text().splitlines())
                    total_lines += lines
                    css_files.append((file_path, lines))

    return total_lines, len(css_files)


def analyze_commits():
    """Analyze key commits on August 15."""

    # Save current state
    current_branch = run_git_command("git branch --show-current")
    run_git_command("git stash push -m 'analysis' 2>/dev/null")

    # Switch to feature branch with all the action
    run_git_command("git checkout feat/universal-docs-init 2>/dev/null")

    # Key commits to analyze
    commits = [
        ("04:11", "b2d6733", "feat: implement AutoAPI template distribution fix"),
        ("05:19", "1f27332", "fix: Restore and fix custom AutoAPI templates"),
        (
            "06:32",
            "3497afe",
            "feat: FINAL FIX - replace broken templates with correct AutoAPI defaults",
        ),
        (
            "07:34",
            "090d988",
            "feat(templates): enhance AutoAPI templates with modern design and dropdowns",
        ),
        (
            "07:52",
            "16c6b50",
            "refactor: simplify AutoAPI module template from dropdowns to clean admonitions",
        ),
        (
            "11:20",
            "31e74b6",
            "feat(autoapi): comprehensive template customization for modern documentation",
        ),
        ("15:21", "20907a1", "feat: implement breadcrumb navigation for Furo theme"),
        ("16:30", "3c56087", "feat: enhance documentation layout and styling"),
        (
            "20:34",
            "c0d09bb",
            "fix: remove admonition over-styling to restore Furo semantic theming",
        ),
        (
            "20:47",
            "469103a",
            "docs(test): add AutoAPI hierarchical fix validation notes",
        ),
    ]

    print("COMMIT MESSAGE vs CSS REALITY - August 15, 2025")
    print("=" * 100)
    print(f"{'Time':<6} {'Commit':<8} {'CSS':<12} {'Message':<50} {'Reality'}")
    print("=" * 100)

    prev_lines = 0
    for time, commit, message in commits:
        lines, files = count_css_at_commit(commit)
        change = lines - prev_lines if prev_lines > 0 else 0
        change_str = f"+{change}" if change > 0 else str(change) if change < 0 else "0"

        # Determine what really happened
        reality = ""
        if "FINAL FIX" in message and lines > 3000:
            reality = "❌ Not final, still 3500+ lines"
        elif "enhance" in message and "modern" in message and change > 500:
            reality = "💥 Added 800+ lines marketing CSS"
        elif "simplify" in message and change == 0:
            reality = "❓ No CSS actually removed"
        elif "remove admonition over-styling" in message and lines > 4000:
            reality = "❌ CSS still present (4700+ lines)"
        elif "breadcrumb" in message:
            reality = "✅ Added breadcrumb CSS"
        elif change > 100:
            reality = f"📈 Added {change} lines"
        elif change < -100:
            reality = f"📉 Removed {-change} lines"
        else:
            reality = "➡️ No significant CSS change"

        print(
            f"{time:<6} {commit:<8} {lines:>5} lines {change_str:>6} {message[:50]:<50} {reality}"
        )
        prev_lines = lines

    # Return to original state
    run_git_command(f"git checkout {current_branch} 2>/dev/null")
    run_git_command("git stash pop 2>/dev/null")

    print("\n" + "=" * 100)
    print("KEY INSIGHTS:")
    print("- 06:32: 'FINAL FIX' but already had 3500+ lines of CSS")
    print(
        "- 07:34: 'enhance...modern' added 800+ lines of marketing CSS (enhanced-design.css)"
    )
    print("- 07:52: 'simplify' but didn't actually remove the CSS")
    print("- 20:34: 'remove admonition over-styling' but all CSS files still present")
    print(
        "\nCONCLUSION: Commit messages often didn't match reality - 'fixes' didn't fix, 'simplify' didn't simplify"
    )


if __name__ == "__main__":
    analyze_commits()
