#!/usr/bin/env python3
"""Debug intersphinx mappings during Sphinx build."""

from sphinx.application import Sphinx


def debug_intersphinx(app: Sphinx, env, docnames):
    """Print intersphinx mappings during build."""
    print("\n" + "=" * 70)
    print("INTERSPHINX MAPPINGS AT BUILD TIME:")
    print("=" * 70)

    mapping = app.config.intersphinx_mapping
    print(f"Total mappings: {len(mapping)}")
    print("\nMappings:")
    for name, (url, inv) in sorted(mapping.items()):
        print(f"  {name:30} -> {url}")

    print("=" * 70 + "\n")


def setup(app: Sphinx):
    """Setup the debug extension."""
    app.connect("env-before-read-docs", debug_intersphinx)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
