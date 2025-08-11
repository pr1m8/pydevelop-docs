#!/usr/bin/env python3
"""Clean up PyAutoDoc project structure.

This script helps consolidate the configuration and remove redundant files.
Run with --dry-run first to see what would be changed.
"""

import argparse
import shutil
import sys
from pathlib import Path
from typing import List, Tuple

# Project root
PROJECT_ROOT = Path(__file__).parent.parent


class ProjectCleaner:
    """Clean up redundant files and directories in PyAutoDoc."""
    
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.actions: List[Tuple[str, Path, str]] = []
    
    def add_action(self, action: str, path: Path, reason: str):
        """Add an action to be performed."""
        self.actions.append((action, path, reason))
    
    def analyze(self):
        """Analyze project structure and identify cleanup actions."""
        
        # 1. Redundant documentation structure
        source_dir = PROJECT_ROOT / "docs" / "source"
        if source_dir.exists():
            self.add_action(
                "REMOVE_DIR",
                source_dir,
                "Redundant docs/source directory (using docs/ as root)"
            )
        
        # 2. Duplicate configuration files (after migration)
        old_configs = [
            (PROJECT_ROOT / "shared-docs-config" / "shared_config.py", 
             "Replaced by unified_config.py"),
            (PROJECT_ROOT / "shared-docs-config" / "shared_config_simple.py",
             "Replaced by unified_config.py"),
        ]
        
        for config_path, reason in old_configs:
            if config_path.exists():
                self.add_action("REMOVE_FILE", config_path, reason)
        
        # 3. Unused YAML configuration system
        yaml_config_dir = PROJECT_ROOT / "docs" / "config"
        if yaml_config_dir.exists():
            yaml_files = list(yaml_config_dir.glob("*.yaml"))
            if yaml_files and not self._yaml_configs_in_use():
                self.add_action(
                    "REMOVE_DIR",
                    yaml_config_dir,
                    "Unused YAML configuration system"
                )
        
        # 4. Build artifacts that shouldn't be in git
        build_dirs = [
            PROJECT_ROOT / "docs" / "build",
            PROJECT_ROOT / "docs" / "_build",
            PROJECT_ROOT / "_build",
        ]
        
        for build_dir in build_dirs:
            if build_dir.exists() and not self._has_gitkeep(build_dir):
                self.add_action(
                    "REMOVE_DIR",
                    build_dir,
                    "Build artifacts (should be git-ignored)"
                )
        
        # 5. __pycache__ directories (excluding .venv)
        for pycache in PROJECT_ROOT.rglob("__pycache__"):
            # Skip if in .venv directory
            if ".venv" in str(pycache):
                continue
            self.add_action(
                "REMOVE_DIR",
                pycache,
                "Python cache directory"
            )
        
        # 6. Empty or redundant directories
        empty_dirs = [
            PROJECT_ROOT / "docs" / "data",
            PROJECT_ROOT / "docs" / "logs",
            PROJECT_ROOT / "docs" / "docs",  # docs/docs is confusing
        ]
        
        for dir_path in empty_dirs:
            if dir_path.exists() and self._is_empty_dir(dir_path):
                self.add_action(
                    "REMOVE_DIR",
                    dir_path,
                    "Empty or redundant directory"
                )
    
    def _yaml_configs_in_use(self) -> bool:
        """Check if YAML configs are referenced in any conf.py."""
        conf_files = PROJECT_ROOT.rglob("conf.py")
        for conf in conf_files:
            if conf.is_file():
                content = conf.read_text()
                if "config_loader" in content or "yaml" in content.lower():
                    return True
        return False
    
    def _has_gitkeep(self, path: Path) -> bool:
        """Check if directory has .gitkeep file."""
        return (path / ".gitkeep").exists()
    
    def _is_empty_dir(self, path: Path) -> bool:
        """Check if directory is empty (ignoring .gitkeep)."""
        if not path.is_dir():
            return False
        
        files = list(path.iterdir())
        # Empty or only has .gitkeep
        return len(files) == 0 or (len(files) == 1 and files[0].name == ".gitkeep")
    
    def execute(self):
        """Execute the cleanup actions."""
        if not self.actions:
            print("✅ No cleanup actions needed!")
            return
        
        print(f"\n{'DRY RUN: ' if self.dry_run else ''}Cleanup Actions")
        print("=" * 80)
        
        for action, path, reason in self.actions:
            rel_path = path.relative_to(PROJECT_ROOT)
            print(f"\n{action}: {rel_path}")
            print(f"  Reason: {reason}")
            
            if not self.dry_run:
                try:
                    if action == "REMOVE_FILE":
                        path.unlink()
                        print(f"  ✓ Removed file")
                    elif action == "REMOVE_DIR":
                        shutil.rmtree(path)
                        print(f"  ✓ Removed directory")
                except Exception as e:
                    print(f"  ✗ Error: {e}")
        
        if self.dry_run:
            print("\n⚠️  This was a dry run. Use --execute to perform these actions.")
    
    def create_gitignore(self):
        """Update .gitignore with proper entries."""
        gitignore_path = PROJECT_ROOT / ".gitignore"
        
        required_entries = [
            "# Build directories",
            "_build/",
            "docs/build/",
            "docs/_build/",
            "**/build/",
            "",
            "# Python",
            "__pycache__/",
            "*.py[cod]",
            "*$py.class",
            "*.so",
            ".Python",
            "",
            "# Virtual environments",
            ".venv/",
            "venv/",
            "ENV/",
            "env/",
            "",
            "# IDE",
            ".vscode/",
            ".idea/",
            "*.swp",
            "*.swo",
            "*~",
            "",
            "# OS",
            ".DS_Store",
            "Thumbs.db",
            "",
            "# Documentation",
            "docs/_autosummary/",
            "docs/api/",
            ".doctrees/",
            "",
            "# Testing",
            ".coverage",
            "htmlcov/",
            ".pytest_cache/",
            ".tox/",
            "",
            "# Distribution",
            "dist/",
            "*.egg-info/",
            ".eggs/",
        ]
        
        if gitignore_path.exists():
            current = gitignore_path.read_text()
            # Check if our entries are missing
            missing = [e for e in required_entries if e and e not in current]
            
            if missing:
                print(f"\n📝 Updating .gitignore with {len(missing)} entries")
                if not self.dry_run:
                    with open(gitignore_path, 'a') as f:
                        f.write('\n\n# Added by cleanup script\n')
                        f.write('\n'.join(required_entries))
        else:
            print("\n📝 Creating .gitignore")
            if not self.dry_run:
                gitignore_path.write_text('\n'.join(required_entries) + '\n')


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Clean up PyAutoDoc project structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # See what would be cleaned up
  python scripts/cleanup-project.py
  
  # Actually perform cleanup
  python scripts/cleanup-project.py --execute
  
  # Update .gitignore
  python scripts/cleanup-project.py --gitignore
        """
    )
    
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Actually perform cleanup (default is dry run)'
    )
    
    parser.add_argument(
        '--gitignore',
        action='store_true',
        help='Update .gitignore file'
    )
    
    args = parser.parse_args()
    
    cleaner = ProjectCleaner(dry_run=not args.execute)
    
    print("🧹 PyAutoDoc Project Cleanup")
    print("=" * 80)
    
    # Analyze project
    cleaner.analyze()
    
    # Execute cleanup
    cleaner.execute()
    
    # Update gitignore if requested
    if args.gitignore:
        cleaner.create_gitignore()
    
    print("\n✨ Cleanup complete!")
    
    # Provide next steps
    if not args.execute:
        print("\nNext steps:")
        print("1. Review the proposed changes above")
        print("2. Run with --execute to perform cleanup")
        print("3. Run with --gitignore to update .gitignore")
        print("4. Migrate conf.py files to use unified_config.py")
        print("   See: docs/cleanup-migration-guide.md")


if __name__ == "__main__":
    main()