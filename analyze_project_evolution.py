#!/usr/bin/env python3
"""Analyze project structure evolution across branches and commits."""

import os
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


def get_project_structure(commit_hash=None):
    """Get project structure at a specific commit."""
    if commit_hash:
        # Checkout specific commit
        run_git_command(f"git checkout {commit_hash} 2>/dev/null")

    structure = {}

    # Key directories to analyze
    dirs_to_check = [
        "src/pydevelop_docs",
        "src/pydevelop_docs/templates",
        "src/pydevelop_docs/templates/static",
        "src/pydevelop_docs/templates/_autoapi_templates",
        "docs/source",
        "docs/source/_static",
        "docs/source/_static/css",
        "docs/source/_templates",
        "test-projects",
        "scripts",
        "project_docs",
    ]

    for dir_path in dirs_to_check:
        path = Path(dir_path)
        if path.exists():
            # Count files by type
            py_files = list(path.glob("*.py"))
            css_files = list(path.glob("*.css"))
            js_files = list(path.glob("*.js"))
            rst_files = list(path.glob("*.rst"))
            md_files = list(path.glob("*.md"))

            if any([py_files, css_files, js_files, rst_files, md_files]):
                structure[dir_path] = {
                    "py": len(py_files),
                    "css": len(css_files),
                    "js": len(js_files),
                    "rst": len(rst_files),
                    "md": len(md_files),
                    "total": len(list(path.glob("*"))),
                }

                # Get CSS details
                if css_files:
                    structure[dir_path]["css_files"] = {}
                    for css_file in css_files:
                        lines = len(css_file.read_text().splitlines())
                        structure[dir_path]["css_files"][css_file.name] = lines

    return structure


def get_all_commits_for_date(branch, date="2025-08-15"):
    """Get all commits for a branch on specific date."""
    cmd = f'git log {branch} --since="{date} 00:00" --until="{date} 23:59" --format="%h|%ad|%an|%s" --date=format:"%Y-%m-%d %H:%M"'
    output = run_git_command(cmd)
    if not output:
        return []

    commits = []
    for line in output.split("\n"):
        if line:
            parts = line.split("|", 3)
            if len(parts) == 4:
                commits.append(
                    {
                        "hash": parts[0],
                        "datetime": parts[1],
                        "author": parts[2],
                        "message": parts[3],
                    }
                )
    return commits


def analyze_branch_evolution(branch):
    """Analyze how a branch evolved."""
    print(f"\n{'='*80}")
    print(f"BRANCH: {branch}")
    print(f"{'='*80}")

    # Get commits
    commits = get_all_commits_for_date(branch, "2025-08-15")

    if not commits:
        print("No commits on August 15, 2025")
        return

    print(f"\nTotal commits on Aug 15: {len(commits)}")
    print("\nCommit Timeline:")
    print("-" * 80)

    for commit in commits:
        time = commit["datetime"].split(" ")[1]
        print(f"{time} - {commit['hash']} - {commit['message'][:60]}...")

    # Analyze key commits
    key_commits = [
        ("06:32", "3497afe", "FINAL FIX - before enhanced-design.css"),
        ("07:34", "090d988", "Added enhanced-design.css"),
        ("16:30", "3c56087", "Peak CSS complexity"),
        ("20:47", "469103a", "Evening state"),
    ]

    print(f"\n{'='*80}")
    print("KEY COMMIT ANALYSIS")
    print(f"{'='*80}")

    # Save current state
    current_branch = run_git_command("git branch --show-current")
    run_git_command("git stash push -m 'analysis-temp' 2>/dev/null")

    # Checkout branch
    run_git_command(f"git checkout {branch} 2>/dev/null")

    for time, hash_prefix, description in key_commits:
        # Find full commit hash
        full_hash = None
        for commit in commits:
            if commit["hash"].startswith(hash_prefix):
                full_hash = commit["hash"]
                break

        if full_hash:
            print(f"\n{'-'*80}")
            print(f"{time} - {full_hash} - {description}")
            print(f"{'-'*80}")

            structure = get_project_structure(full_hash)

            # Show structure summary
            total_css_lines = 0
            css_file_count = 0

            for dir_path, info in sorted(structure.items()):
                if info.get("css_files"):
                    print(f"\n{dir_path}:")
                    for css_name, lines in info["css_files"].items():
                        print(f"  - {css_name}: {lines} lines")
                        total_css_lines += lines
                        css_file_count += 1

            print(f"\nTOTAL: {css_file_count} CSS files, {total_css_lines} lines")

    # Return to original state
    run_git_command(f"git checkout {current_branch} 2>/dev/null")
    run_git_command("git stash pop 2>/dev/null")


def main():
    """Main analysis function."""
    print("PROJECT EVOLUTION ANALYSIS - AUGUST 15, 2025")
    print("=" * 80)

    # Get all branches
    branches = get_branches()

    # Analyze key branches
    key_branches = [
        "main",
        "feat/universal-docs-init",
        "feature/optional-template-styles",
    ]

    for branch in branches:
        if branch in key_branches:
            analyze_branch_evolution(branch)

    print(f"\n{'='*80}")
    print("SUMMARY:")
    print(f"{'='*80}")
    print("- main branch: No August 15 activity (clean state)")
    print("- feat/universal-docs-init: 32 commits, CSS explosion")
    print("- feature/optional-template-styles: Attempted recovery")


if __name__ == "__main__":
    main()
