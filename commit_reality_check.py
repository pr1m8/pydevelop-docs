#!/usr/bin/env python3
"""Compare commit messages with actual changes."""

import re
import subprocess


def run_git_command(cmd):
    """Run a git command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()


def get_commit_diff_summary(commit):
    """Get diff summary for a commit."""
    # Get files changed and their stats
    output = run_git_command(f"git show --stat {commit}")

    css_added = 0
    css_removed = 0
    css_files_changed = []

    lines = output.split("\n")
    for line in lines:
        if ".css" in line and "|" in line:
            # Parse lines like: "file.css | 885 +++++"
            parts = line.split("|")
            if len(parts) == 2:
                filename = parts[0].strip()
                changes = parts[1].strip()

                # Extract numbers from changes
                added_match = re.search(r"(\d+)\s*\+", changes)
                removed_match = re.search(r"(\d+)\s*-", changes)

                if added_match:
                    css_added += int(added_match.group(1))
                if removed_match:
                    css_removed += int(removed_match.group(1))

                css_files_changed.append(filename)

    return css_files_changed, css_added, css_removed


def analyze_commit_reality():
    """Analyze what commits actually did vs what they claimed."""

    # Save current state
    current_branch = run_git_command("git branch --show-current")

    # Switch to feature branch
    run_git_command("git checkout feat/universal-docs-init 2>/dev/null")

    # Key commits to analyze
    commits = [
        ("06:32", "3497afe", "FINAL FIX - replace broken templates"),
        ("07:34", "090d988", "enhance AutoAPI templates with modern design"),
        ("07:52", "16c6b50", "simplify AutoAPI module template"),
        ("15:21", "20907a1", "implement breadcrumb navigation"),
        ("16:30", "3c56087", "enhance documentation layout and styling"),
        ("20:34", "c0d09bb", "remove admonition over-styling"),
    ]

    print("COMMIT MESSAGES vs REALITY - CSS Analysis")
    print("=" * 120)
    print(f"{'Time':<6} {'Message':<50} {'CSS Changes':<30} {'Reality Check'}")
    print("=" * 120)

    for time, commit, message in commits:
        files, added, removed = get_commit_diff_summary(commit)

        css_summary = ""
        if files:
            css_summary = f"{len(files)} files, +{added}/-{removed}"
        else:
            css_summary = "No CSS changes"

        # Reality check
        reality = ""
        if "FINAL FIX" in message and added > 0:
            reality = "🤔 'Final' but still adding CSS"
        elif "enhance" in message and "modern" in message:
            if added > 500:
                reality = f"💥 MAJOR: Added {added} lines of 'modern' CSS"
            else:
                reality = "📝 Enhanced templates (not just CSS)"
        elif "simplify" in message:
            if removed > added:
                reality = f"✅ Actually simplified (-{removed} lines)"
            elif removed == 0:
                reality = "❌ Claimed to simplify but removed nothing"
            else:
                reality = "🔄 Refactored but didn't reduce"
        elif "remove" in message and "styling" in message:
            if removed > 0:
                reality = f"✅ Removed {removed} lines"
            else:
                reality = "❌ Said 'remove' but didn't remove CSS"
        elif "breadcrumb" in message and added > 0:
            reality = f"✅ Added breadcrumb CSS ({added} lines)"
        elif added > 0:
            reality = f"➕ Added {added} lines"
        else:
            reality = "↔️ No CSS impact"

        print(f"{time:<6} {message:<50} {css_summary:<30} {reality}")

        if files:
            for f in files[:3]:  # Show first 3 files
                print(f"       └─ {f}")
            if len(files) > 3:
                print(f"       └─ ... and {len(files)-3} more files")

    # Get overall stats for the day
    print("\n" + "=" * 120)
    print("FULL DAY ANALYSIS (Aug 15):")

    # Check CSS at start and end of day
    run_git_command("git checkout b2d6733 2>/dev/null")  # First commit
    start_css = run_git_command("find . -name '*.css' | wc -l")

    run_git_command("git checkout 469103a 2>/dev/null")  # Last commit
    end_css = run_git_command("find . -name '*.css' | wc -l")

    print(f"- Started with {start_css} CSS files")
    print(f"- Ended with {end_css} CSS files")
    print(f"- Net change: +{int(end_css) - int(start_css)} CSS files")

    # Check for enhanced-design.css specifically
    enhanced = run_git_command("find . -name 'enhanced-design.css' 2>/dev/null")
    if enhanced:
        size = run_git_command(f"wc -l {enhanced} | awk '{{print $1}}'")
        print(f"\nenhanced-design.css: {size} lines (THE PROBLEM FILE)")

    # Return to original state
    run_git_command(f"git checkout {current_branch} 2>/dev/null")

    print("\n" + "=" * 120)
    print("KEY FINDINGS:")
    print("1. Commit messages often didn't match actual changes")
    print("2. 'Simplify' commits didn't remove CSS")
    print("3. 'Fix' commits added more CSS instead of removing it")
    print("4. The 885-line enhanced-design.css was the main problem")


if __name__ == "__main__":
    analyze_commit_reality()
