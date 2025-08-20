#!/usr/bin/env python3
"""
Documentation Build Recovery Tools

Simple utilities to check build status and recover from failures.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime


class BuildRecovery:
    """Simple build recovery utilities."""
    
    def __init__(self, haive_root="/home/will/Projects/haive/backend/haive"):
        self.haive_root = Path(haive_root)
        self.packages_dir = self.haive_root / "packages"
    
    def check_running_builds(self):
        """Check what documentation builds are currently running."""
        print("🔍 Checking running builds...")
        
        try:
            result = subprocess.run(
                ["ps", "aux"],
                capture_output=True, 
                text=True
            )
            
            sphinx_processes = []
            for line in result.stdout.split('\n'):
                if 'sphinx-build' in line or 'sphinx' in line:
                    parts = line.split()
                    if len(parts) > 10:
                        pid = parts[1]
                        cpu = parts[2]
                        mem = parts[3]
                        command = ' '.join(parts[10:])
                        
                        # Extract package name from path
                        package_name = "unknown"
                        for pkg in ["haive-core", "haive-agents", "haive-mcp", "haive-tools", "haive-games", "haive-dataflow"]:
                            if pkg in command:
                                package_name = pkg
                                break
                        
                        sphinx_processes.append({
                            'pid': pid,
                            'cpu': cpu,
                            'mem': mem,
                            'package': package_name,
                            'command': command[:80] + "..." if len(command) > 80 else command
                        })
            
            if sphinx_processes:
                print(f"📊 Found {len(sphinx_processes)} running builds:")
                print()
                for proc in sphinx_processes:
                    print(f"   📦 {proc['package']} (PID: {proc['pid']})")
                    print(f"      CPU: {proc['cpu']}% | Memory: {proc['mem']}%")
                    print(f"      Command: {proc['command']}")
                    print()
            else:
                print("   ✅ No running builds found")
            
            return sphinx_processes
            
        except Exception as e:
            print(f"❌ Error checking processes: {e}")
            return []
    
    def check_build_status(self):
        """Check status of all package builds."""
        print("📋 Checking build status for all packages...")
        print()
        
        package_status = {}
        
        for package_dir in self.packages_dir.glob("haive-*"):
            if not package_dir.is_dir():
                continue
            
            package_name = package_dir.name
            docs_dir = package_dir / "docs"
            
            if not docs_dir.exists():
                package_status[package_name] = {"status": "no_docs", "html_count": 0}
                continue
            
            build_dir = docs_dir / "build" / "html"
            if build_dir.exists():
                html_files = list(build_dir.rglob("*.html"))
                index_exists = (build_dir / "index.html").exists()
                
                if index_exists and len(html_files) > 10:
                    package_status[package_name] = {
                        "status": "complete",
                        "html_count": len(html_files),
                        "build_dir": str(build_dir)
                    }
                elif len(html_files) > 0:
                    package_status[package_name] = {
                        "status": "partial",
                        "html_count": len(html_files),
                        "build_dir": str(build_dir)
                    }
                else:
                    package_status[package_name] = {
                        "status": "empty",
                        "html_count": 0,
                        "build_dir": str(build_dir)
                    }
            else:
                package_status[package_name] = {"status": "not_started", "html_count": 0}
        
        # Display results
        for package, info in package_status.items():
            status_emoji = {
                "complete": "✅",
                "partial": "🔄", 
                "empty": "⚠️",
                "not_started": "❌",
                "no_docs": "🚫"
            }
            
            emoji = status_emoji.get(info["status"], "❓")
            print(f"   {emoji} {package}: {info['status']} ({info.get('html_count', 0)} HTML files)")
        
        return package_status
    
    def monitor_build_logs(self, package_name=None):
        """Monitor build logs for specific package or all."""
        print("📖 Checking recent build logs...")
        
        # Check for common log locations
        log_locations = [
            f"/tmp/{package_name}_build.log" if package_name else "/tmp/*_build*.log",
            f"/tmp/{package_name}_build_fixed.log" if package_name else "/tmp/*_build_fixed.log",
            "/tmp/haive-*_build*.log"
        ]
        
        found_logs = []
        for pattern in log_locations:
            try:
                import glob
                matches = glob.glob(pattern)
                found_logs.extend(matches)
            except Exception:
                continue
        
        if found_logs:
            print(f"   📁 Found {len(found_logs)} log files:")
            for log_file in found_logs:
                print(f"      📄 {log_file}")
                
                # Show last few lines
                try:
                    with open(log_file, 'r') as f:
                        lines = f.readlines()
                        if len(lines) > 5:
                            print("         Last 3 lines:")
                            for line in lines[-3:]:
                                print(f"         {line.strip()}")
                        print()
                except Exception as e:
                    print(f"         ❌ Could not read log: {e}")
        else:
            print("   ⚠️ No build logs found")
        
        return found_logs
    
    def suggest_recovery_actions(self):
        """Suggest recovery actions based on current state."""
        print("🔧 Recovery Suggestions:")
        print()
        
        # Check running processes
        running = self.check_running_builds()
        
        if running:
            print("📍 Active builds detected:")
            for proc in running:
                if proc['package'] != 'unknown':
                    print(f"   • {proc['package']}: Let it continue running (PID {proc['pid']})")
                    print(f"     Monitor with: tail -f /tmp/{proc['package']}_build_fixed.log")
            print()
        
        # Check build status  
        status = self.check_build_status()
        
        failed_packages = [pkg for pkg, info in status.items() 
                          if info['status'] in ['empty', 'not_started', 'partial']]
        
        if failed_packages:
            print("🔄 Packages needing attention:")
            for pkg in failed_packages:
                print(f"   • {pkg}: {status[pkg]['status']}")
                if status[pkg]['status'] == 'partial':
                    print(f"     - Has {status[pkg]['html_count']} files but incomplete")
                    print(f"     - Try resuming build with clean flag")
                elif status[pkg]['status'] == 'not_started':
                    print(f"     - Start fresh build")
                elif status[pkg]['status'] == 'empty':
                    print(f"     - Build failed, check logs and restart")
            print()
        
        completed = [pkg for pkg, info in status.items() if info['status'] == 'complete']
        if completed:
            print(f"✅ Successfully built packages: {', '.join(completed)}")
            total_files = sum(status[pkg]['html_count'] for pkg in completed)
            print(f"   📊 Total HTML files: {total_files}")
            print()
        
        print("🎯 Recommended next steps:")
        if running:
            print("   1. Wait for current builds to complete")
            print("   2. Monitor logs for any errors")
        if failed_packages:
            print("   3. Address failed packages one by one")
            print("   4. Use nohup for long-running builds")
        print("   5. Export completed documentation when ready")
        
    def export_completed_docs(self, output_dir="./completed_docs"):
        """Export all completed documentation."""
        print(f"📦 Exporting completed documentation to {output_dir}...")
        
        status = self.check_build_status()
        completed = [pkg for pkg, info in status.items() if info['status'] == 'complete']
        
        if not completed:
            print("   ❌ No completed documentation found")
            return False
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        exported = []
        for package in completed:
            package_info = status[package]
            source_dir = Path(package_info['build_dir'])
            target_dir = output_path / package
            
            try:
                import shutil
                if target_dir.exists():
                    shutil.rmtree(target_dir)
                shutil.copytree(source_dir, target_dir)
                exported.append(package)
                print(f"   ✅ Exported {package} ({package_info['html_count']} files)")
            except Exception as e:
                print(f"   ❌ Failed to export {package}: {e}")
        
        if exported:
            # Create simple index
            self._create_export_index(output_path, exported, status)
            print(f"\n🎉 Export complete! {len(exported)} packages exported to {output_path}")
            print(f"📁 Open {output_path}/index.html to browse documentation")
            return True
        else:
            print("   ❌ No packages successfully exported")
            return False
    
    def _create_export_index(self, output_path, packages, status):
        """Create a simple index for exported documentation."""
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Haive Documentation Export</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .package {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 8px; }}
        .package h3 {{ margin: 0 0 10px 0; color: #333; }}
        .package a {{ color: #007bff; text-decoration: none; }}
        .package a:hover {{ text-decoration: underline; }}
        .stats {{ color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <h1>🤖 Haive Documentation Export</h1>
    <p>Exported on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <h2>📦 Available Packages ({len(packages)})</h2>
"""
        
        for package in packages:
            info = status[package]
            html_content += f'''
    <div class="package">
        <h3><a href="{package}/index.html">📄 {package}</a></h3>
        <div class="stats">{info['html_count']} HTML files</div>
        <p><a href="{package}/index.html">Main Documentation</a> | 
           <a href="{package}/autoapi/index.html">API Reference</a></p>
    </div>
'''
        
        html_content += """
</body>
</html>"""
        
        index_path = output_path / "index.html"
        index_path.write_text(html_content)


def main():
    """Main recovery interface."""
    print("🚑 Haive Documentation Build Recovery")
    print("=" * 50)
    
    recovery = BuildRecovery()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "status":
            recovery.check_build_status()
        elif command == "running":
            recovery.check_running_builds()
        elif command == "logs":
            package = sys.argv[2] if len(sys.argv) > 2 else None
            recovery.monitor_build_logs(package)
        elif command == "export":
            output_dir = sys.argv[2] if len(sys.argv) > 2 else "./completed_docs"
            recovery.export_completed_docs(output_dir)
        elif command == "suggest":
            recovery.suggest_recovery_actions()
        else:
            print(f"Unknown command: {command}")
    else:
        # Full recovery check
        recovery.suggest_recovery_actions()


if __name__ == "__main__":
    main()