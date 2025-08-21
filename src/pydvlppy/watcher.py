"""File watcher and auto-rebuild system for PyDevelop-Docs."""

import asyncio
from datetime import datetime
import hashlib
from pathlib import Path
from typing import Any

import click
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .autofix import DocumentationAutoFixer
from .builders import MonorepoBuilder, SinglePackageBuilder
from .config_discovery import PyDevelopConfig


class DocumentationWatcher(FileSystemEventHandler):
    """Watch for changes and trigger selective rebuilds."""

    def __init__(
        self,
        project_path: Path,
        config: dict[str, Any],
        auto_fix: bool = True,
        selective: bool = True,
    ):
        self.project_path = project_path
        self.config = config
        self.auto_fix = auto_fix
        self.selective = selective
        self.file_hashes: dict[str, str] = {}
        self.package_states: dict[str, dict[str, Any]] = {}
        self.rebuild_queue: set[str] = set()
        self.last_build_time: dict[str, datetime] = {}

        # Initialize auto-fixer
        self.fixer = DocumentationAutoFixer(project_path) if auto_fix else None

        # Load .pydevelop configuration
        self.pydevelop = PyDevelopConfig(project_path)
        self.docs_config = self.pydevelop.load_config().get("documentation", {})
        self.watch_config = self.pydevelop.load_config().get("watch", {})

        # Determine project type
        self.is_monorepo = (project_path / "packages").exists()

        # Initialize file hashes
        self._initialize_hashes()

    def _initialize_hashes(self):
        """Initialize file hashes for change detection."""
        patterns = [
            "**/*.py",
            "**/*.rst",
            "**/*.md",
            "**/conf.py",
            "**/.pydevelop.yaml",
        ]

        for pattern in patterns:
            for file_path in self.project_path.rglob(pattern):
                if ".venv" not in str(file_path) and "build" not in str(file_path):
                    self.file_hashes[str(file_path)] = self._get_file_hash(file_path)

    def _get_file_hash(self, file_path: Path) -> str:
        """Get hash of file contents."""
        if not file_path.exists():
            return ""

        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            hasher.update(f.read())
        return hasher.hexdigest()

    def _get_affected_package(self, file_path: str) -> str | None:
        """Determine which package is affected by a file change."""
        path = Path(file_path)

        # Check if it's in a package
        if "packages" in path.parts:
            try:
                pkg_index = path.parts.index("packages")
                if pkg_index + 1 < len(path.parts):
                    return path.parts[pkg_index + 1]
            except ValueError:
                pass

        # Check if it's a root-level change
        if path.is_relative_to(self.project_path):
            rel_path = path.relative_to(self.project_path)
            if len(rel_path.parts) == 1 or rel_path.parts[0] == "docs":
                return "_root_"

        return None

    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Skip certain paths
        if any(skip in str(file_path) for skip in [".venv", "build", "__pycache__", ".git"]):
            return

        # Check if file actually changed
        new_hash = self._get_file_hash(file_path)
        old_hash = self.file_hashes.get(str(file_path), "")

        if new_hash == old_hash:
            return

        self.file_hashes[str(file_path)] = new_hash

        # Auto-fix if enabled
        if self.auto_fix and self.fixer:
            if file_path.suffix in [".py", ".rst", ".md"]:
                click.echo(f"🔧 Auto-fixing {file_path.name}...")
                self.fixer.fix_file(file_path)

        # Determine what needs rebuilding
        if self.selective:
            affected_package = self._get_affected_package(str(file_path))
            if affected_package:
                self.rebuild_queue.add(affected_package)
                click.echo(f"📝 Queued {affected_package} for rebuild (changed: {file_path.name})")
        else:
            self.rebuild_queue.add("_all_")
            click.echo(f"📝 Queued full rebuild (changed: {file_path.name})")

    def on_created(self, event):
        """Handle file creation events."""
        self.on_modified(event)

    def on_deleted(self, event):
        """Handle file deletion events."""
        if not event.is_directory:
            file_path = str(event.src_path)
            self.file_hashes.pop(file_path, None)

            # Queue rebuild for affected package
            affected_package = self._get_affected_package(file_path)
            if affected_package:
                self.rebuild_queue.add(affected_package)

    async def process_rebuild_queue(self):
        """Process the rebuild queue."""
        while True:
            if self.rebuild_queue:
                # Get items to rebuild
                to_rebuild = list(self.rebuild_queue)
                self.rebuild_queue.clear()

                # Rebuild each item
                for item in to_rebuild:
                    await self._rebuild_item(item)

            await asyncio.sleep(2)  # Check every 2 seconds

    async def _rebuild_item(self, item: str):
        """Rebuild a specific item (package or all)."""
        click.echo(f"\n🔨 Rebuilding {item}...")

        try:
            if item == "_all_":
                # Full rebuild
                if self.is_monorepo:
                    builder = MonorepoBuilder(self.project_path, self.config)
                    builder.build_all(clean=False)
                else:
                    builder = SinglePackageBuilder(self.project_path, self.config)
                    builder.build()

            elif item == "_root_":
                # Rebuild root docs only
                if self.is_monorepo:
                    builder = MonorepoBuilder(self.project_path, self.config)
                    builder.build_aggregate()

            else:
                # Rebuild specific package
                package_path = self.project_path / "packages" / item
                if package_path.exists():
                    pkg_config = {"name": item}
                    builder = SinglePackageBuilder(package_path, pkg_config)
                    builder.build()

            self.last_build_time[item] = datetime.now()
            click.echo(f"✅ Successfully rebuilt {item}")

        except Exception as e:
            click.echo(f"❌ Failed to rebuild {item}: {e}", err=True)


async def watch_documentation(
    project_path: Path,
    auto_fix: bool = True,
    selective: bool = True,
):
    """Watch for changes and rebuild documentation."""
    # Load configuration
    from .config_discovery import ConfigDiscovery

    discovery = ConfigDiscovery(project_path)
    config = discovery.discover_all()

    # Create watcher
    watcher = DocumentationWatcher(
        project_path,
        config,
        auto_fix=auto_fix,
        selective=selective,
    )

    # Create observer
    observer = Observer()
    observer.schedule(watcher, str(project_path), recursive=True)

    click.echo("👀 Watching for changes...")
    click.echo(f"   Auto-fix: {'✅' if auto_fix else '❌'}")
    click.echo(f"   Selective rebuild: {'✅' if selective else '❌'}")
    click.echo("   Press Ctrl+C to stop\n")

    # Start watching
    observer.start()

    try:
        # Process rebuild queue
        await watcher.process_rebuild_queue()
    except KeyboardInterrupt:
        observer.stop()
        click.echo("\n👋 Stopped watching")

    observer.join()


if __name__ == "__main__":
    # Test the watcher
    asyncio.run(watch_documentation(Path.cwd()))
