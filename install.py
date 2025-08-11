#!/usr/bin/env python3
"""
PyAutoDoc Installer

Run this script to install PyAutoDoc in your project:
    curl -sSL https://raw.githubusercontent.com/yourusername/pyautodoc/main/install.py | python3

Or download and run:
    python install.py
"""

import os
import sys
import urllib.request
import urllib.error


SIMPLE_URL = "https://raw.githubusercontent.com/yourusername/pyautodoc/main/pyautodoc_simple.py"
LOCAL_NAME = "pyautodoc.py"


def download_pyautodoc():
    """Download PyAutoDoc to current directory."""
    print("📥 Downloading PyAutoDoc...")
    
    try:
        # For testing, use local file if in development
        if os.path.exists("/home/will/Projects/nonsense/pyautodoc/pyautodoc_simple.py"):
            with open("/home/will/Projects/nonsense/pyautodoc/pyautodoc_simple.py", "r") as src:
                content = src.read()
        else:
            # Download from GitHub
            response = urllib.request.urlopen(SIMPLE_URL)
            content = response.read().decode('utf-8')
        
        # Save to local file
        with open(LOCAL_NAME, "w") as f:
            f.write(content)
        
        # Make executable on Unix-like systems
        if hasattr(os, 'chmod'):
            os.chmod(LOCAL_NAME, 0o755)
        
        print(f"✅ Downloaded {LOCAL_NAME}")
        return True
        
    except urllib.error.URLError as e:
        print(f"❌ Failed to download: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Install PyAutoDoc and optionally set up documentation."""
    print("🚀 PyAutoDoc Installer\n")
    
    # Check if already exists
    if os.path.exists(LOCAL_NAME):
        print(f"ℹ️  {LOCAL_NAME} already exists")
        response = input("Overwrite? (y/N): ").lower()
        if response != 'y':
            print("❌ Installation cancelled")
            return
    
    # Download PyAutoDoc
    if not download_pyautodoc():
        sys.exit(1)
    
    print(f"\n✨ PyAutoDoc installed successfully!")
    print(f"\n📖 Usage:")
    print(f"   python {LOCAL_NAME}           # Set up and build docs")
    print(f"   python {LOCAL_NAME} serve     # Serve docs locally")
    print(f"   python {LOCAL_NAME} clean     # Remove docs")
    
    # Ask if user wants to set up now
    print("\n" + "="*50)
    response = input("\n📝 Set up documentation now? (Y/n): ").lower()
    if response != 'n':
        print("\n" + "="*50 + "\n")
        os.system(f"{sys.executable} {LOCAL_NAME} setup")


if __name__ == "__main__":
    main()