#!/usr/bin/env python3
"""
Quick build script for haive-core documentation with detailed logging.
"""
import subprocess
import sys
import os
from pathlib import Path
import time

def build_haive_core():
    """Build haive-core documentation with detailed analysis."""
    
    # Paths
    core_dir = Path("/home/will/Projects/haive/backend/haive/packages/haive-core")
    source_dir = core_dir / "docs" / "source" 
    build_dir = core_dir / "docs" / "build" / "html"
    log_file = core_dir / "docs" / "build.log"
    
    print("🚀 Building haive-core documentation...")
    print(f"Source: {source_dir}")
    print(f"Build: {build_dir}")
    print(f"Log: {log_file}")
    print()
    
    # Check if directories exist
    if not source_dir.exists():
        print(f"❌ Source directory not found: {source_dir}")
        return False
        
    if not (source_dir / "conf.py").exists():
        print(f"❌ conf.py not found: {source_dir / 'conf.py'}")
        return False
    
    # Create build directory
    build_dir.mkdir(parents=True, exist_ok=True)
    
    # Set up environment
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{core_dir / 'src'}:{source_dir}"
    
    # Build command
    cmd = [
        "poetry", "run", "sphinx-build",
        "-b", "html",           # HTML builder
        "-v",                   # Verbose
        "-W", "--keep-going",   # Treat warnings as errors but keep going
        "-E",                   # Don't use cached environment
        str(source_dir),
        str(build_dir)
    ]
    
    print(f"Running: {' '.join(cmd)}")
    print()
    
    start_time = time.time()
    
    try:
        # Run the build
        with open(log_file, "w") as f:
            process = subprocess.run(
                cmd,
                cwd=str(core_dir),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            # Write output to log file
            f.write(process.stdout)
            
            # Also show last part of output
            lines = process.stdout.split('\n')
            print("📋 Last 20 lines of output:")
            for line in lines[-20:]:
                if line.strip():
                    print(f"  {line}")
        
        end_time = time.time()
        duration = end_time - start_time
        
        print()
        print(f"⏱️  Build completed in {duration:.1f} seconds")
        print(f"📄 Full log: {log_file}")
        
        if process.returncode == 0:
            print("✅ Build successful!")
            print(f"📖 Documentation: {build_dir / 'index.html'}")
            
            # Check if key files exist
            if (build_dir / "autoapi" / "index.html").exists():
                print("✅ AutoAPI generated successfully")
            else:
                print("⚠️  AutoAPI may have issues")
                
            return True
        else:
            print(f"❌ Build failed with return code: {process.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Build timed out after 10 minutes")
        return False
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def analyze_log():
    """Analyze the build log for common issues."""
    log_file = Path("/home/will/Projects/haive/backend/haive/packages/haive-core/docs/build.log")
    
    if not log_file.exists():
        print("No log file found")
        return
        
    print("\n🔍 Analyzing build log...")
    
    with open(log_file, 'r') as f:
        content = f.read()
    
    # Count different types of issues
    warnings = content.count("WARNING:")
    errors = content.count("ERROR:")
    failed_imports = content.count("Failed to import")
    
    print(f"📊 Build Analysis:")
    print(f"  Warnings: {warnings}")
    print(f"  Errors: {errors}")
    print(f"  Failed imports: {failed_imports}")
    
    # Show failed imports
    if failed_imports > 0:
        print(f"\n⚠️  Failed Imports (first 10):")
        lines = content.split('\n')
        count = 0
        for line in lines:
            if "Failed to import" in line and count < 10:
                print(f"  {line.strip()}")
                count += 1

if __name__ == "__main__":
    success = build_haive_core()
    analyze_log()
    
    if success:
        print("\n🎉 haive-core documentation built successfully!")
    else:
        print("\n😞 Build had issues - check the log for details")