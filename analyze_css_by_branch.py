#!/usr/bin/env python3
"""Analyze CSS files across branches on August 15, 2025."""

import json
import subprocess
from datetime import datetime
from pathlib import Path


def run_git_command(cmd):
    """Run a git command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()


def get_branches():
    """Get all local branches."""
    output = run_git_command("git branch | sed 's/\\*//g' | sed 's/^[ \\t]*//'")
    return [b.strip() for b in output.split("\n") if b.strip()]


def get_commits_on_date(branch, date="2025-08-15"):
    """Get commits for a branch on specific date."""
    cmd = f'git log {branch} --since="{date} 00:00" --until="{date} 23:59" --format="%h|%ad|%s" --date=format:"%H:%M"'
    output = run_git_command(cmd)
    if not output:
        return []

    commits = []
    for line in output.split("\n"):
        if line:
            parts = line.split("|", 2)
            if len(parts) == 3:
                commits.append(
                    {"hash": parts[0], "time": parts[1], "message": parts[2]}
                )
    return commits


def check_css_files_at_commit(commit_hash):
    """Check CSS files at a specific commit."""
    # Stash current changes
    run_git_command("git stash push -m 'temp-analysis' 2>/dev/null")

    # Checkout commit
    run_git_command(f"git checkout {commit_hash} 2>/dev/null")

    css_info = {}

    # Check template CSS files
    template_css = Path("src/pydevelop_docs/templates/static")
    if template_css.exists():
        css_files = list(template_css.glob("*.css"))
        css_info["template_css"] = []
        for css_file in css_files:
            lines = len(css_file.read_text().splitlines())
            css_info["template_css"].append({"name": css_file.name, "lines": lines})

    # Check docs CSS files
    docs_css = Path("docs/source/_static")
    if docs_css.exists():
        css_files = list(docs_css.glob("*.css")) + list(docs_css.glob("css/*.css"))
        css_info["docs_css"] = []
        for css_file in css_files:
            lines = len(css_file.read_text().splitlines())
            css_info["docs_css"].append(
                {"name": str(css_file.relative_to(docs_css)), "lines": lines}
            )

    # Check config.py for CSS configuration
    config_path = Path("src/pydevelop_docs/config.py")
    if config_path.exists():
        config_text = config_path.read_text()
        if "html_css_files" in config_text:
            # Extract CSS files from config
            start = config_text.find('"html_css_files":')
            if start != -1:
                end = config_text.find("],", start) + 1
                css_config = config_text[start:end]
                css_info["config_css"] = css_config

    return css_info


def analyze_branch(branch, date="2025-08-15"):
    """Analyze a branch for CSS evolution on specific date."""
    print(f"\n{'='*60}")
    print(f"Branch: {branch}")
    print(f"{'='*60}")

    commits = get_commits_on_date(branch, date)

    if not commits:
        print(f"No commits on {date}")
        return

    print(f"Total commits on {date}: {len(commits)}")

    # Key commits to analyze
    key_times = ["06:32", "07:34", "16:30", "20:34", "20:47"]

    for commit in commits:
        if (
            any(time in commit["time"] for time in key_times)
            or "css" in commit["message"].lower()
            or "design" in commit["message"].lower()
        ):
            print(f"\n{commit['time']} - {commit['hash']}: {commit['message']}")

            css_info = check_css_files_at_commit(commit["hash"])

            if css_info.get("template_css"):
                print("\n  Template CSS files:")
                total_lines = 0
                for css in css_info["template_css"]:
                    print(f"    - {css['name']}: {css['lines']} lines")
                    total_lines += css["lines"]
                print(f"  Total template CSS: {total_lines} lines")

            if css_info.get("docs_css"):
                print("\n  Docs CSS files:")
                total_lines = 0
                for css in css_info["docs_css"]:
                    print(f"    - {css['name']}: {css['lines']} lines")
                    total_lines += css["lines"]
                print(f"  Total docs CSS: {total_lines} lines")

            if css_info.get("config_css"):
                print("\n  Config CSS setting:")
                print("    " + css_info["config_css"].replace("\n", "\n    "))


def main():
    """Main analysis function."""
    print("CSS Evolution Analysis - August 15, 2025")
    print("=" * 60)

    # Save current branch
    current_branch = run_git_command("git branch --show-current")

    # Get all branches
    branches = get_branches()

    # Focus on key branches
    key_branches = [
        "main",
        "feat/universal-docs-init",
        "feature/optional-template-styles",
    ]

    for branch in branches:
        if branch in key_branches:
            analyze_branch(branch)

    # Return to original branch
    run_git_command(f"git checkout {current_branch} 2>/dev/null")
    run_git_command("git stash pop 2>/dev/null")

    print(f"\n{'='*60}")
    print("Analysis complete!")


if __name__ == "__main__":
    main()
