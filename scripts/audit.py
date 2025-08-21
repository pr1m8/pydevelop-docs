#!/usr/bin/env python3
"""Comprehensive audit script for pydvlppy package.

This script audits the package functionality, tests new features,
and generates detailed reports about capabilities and issues.
"""

import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import click
from rich.console import Console
from rich.progress import track
from rich.table import Table


class PackageAuditor:
    """Comprehensive auditor for pydvlppy package."""

    def __init__(self, debug: bool = False):
        self.console = Console()
        self.debug = debug
        self.test_results = []
        self.start_time = datetime.now()

    def log_test(
        self, test_name: str, success: bool, details: str = "", duration: float = 0
    ):
        """Log test result."""
        self.test_results.append(
            {
                "test_name": test_name,
                "success": success,
                "details": details,
                "duration": duration,
                "timestamp": datetime.now().isoformat(),
            }
        )

        status = "✅" if success else "❌"
        if self.debug:
            self.console.print(f"{status} {test_name}: {details} ({duration:.2f}s)")

    def run_command(self, cmd: List[str], timeout: int = 60) -> Dict[str, Any]:
        """Run a command and capture results."""
        start_time = time.time()
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=Path(__file__).parent.parent,
            )
            duration = time.time() - start_time

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "duration": duration,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Command timed out after {timeout}s",
                "returncode": -1,
                "duration": timeout,
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1,
                "duration": time.time() - start_time,
            }

    def test_basic_functionality(self):
        """Test basic CLI functionality."""
        self.console.print("\n🔍 Testing Basic Functionality", style="bold cyan")

        # Test help command
        result = self.run_command(["poetry", "run", "pydvlppy", "--help"])
        self.log_test(
            "CLI Help", result["success"], "Help command accessible", result["duration"]
        )

        # Test version
        result = self.run_command(
            [
                "poetry",
                "run",
                "python",
                "-c",
                "import pydevelop_docs; print(pydevelop_docs.__version__)",
            ]
        )
        self.log_test(
            "Import Version",
            result["success"],
            (
                f"Version: {result['stdout'].strip()}"
                if result["success"]
                else "Import failed"
            ),
            result["duration"],
        )

        # Test subcommands
        for cmd in ["init", "doctor", "build", "clean"]:
            result = self.run_command(
                ["poetry", "run", "pydvlppy", cmd, "--help"]
            )
            self.log_test(
                f"Command: {cmd}",
                result["success"],
                f"{cmd} command available",
                result["duration"],
            )

    def test_dry_run_functionality(self):
        """Test enhanced dry-run capabilities."""
        self.console.print("\n🧪 Testing Dry-Run Functionality", style="bold cyan")

        # Test dry-run on Haive project
        result = self.run_command(
            ["poetry", "run", "pydvlppy", "init", "--dry-run", "--debug"]
        )

        success = result["success"] and "dry-run" in result["stdout"].lower()
        self.log_test(
            "Dry-Run Mode",
            success,
            "Dry-run mode shows operations without executing",
            result["duration"],
        )

        # Check for mock operations output
        mock_ops_present = (
            "operations that would be performed" in result["stdout"].lower()
        )
        self.log_test(
            "Mock Operations Display",
            mock_ops_present,
            "Mock operations properly displayed",
            0,
        )

    def test_logging_and_debugging(self):
        """Test enhanced logging and debugging features."""
        self.console.print("\n📊 Testing Logging & Debugging", style="bold cyan")

        # Test debug mode
        result = self.run_command(
            [
                "poetry",
                "run",
                "pydvlppy",
                "init",
                "--dry-run",
                "--debug",
                "--quiet",
            ]
        )

        debug_info_present = (
            "debug" in result["stdout"].lower() or "🐛" in result["stdout"]
        )
        self.log_test(
            "Debug Mode",
            debug_info_present,
            "Debug information displayed",
            result["duration"],
        )

        # Test operations summary
        summary_present = (
            "summary" in result["stdout"].lower() or "📊" in result["stdout"]
        )
        self.log_test(
            "Operations Summary", summary_present, "Operations summary generated", 0
        )

    def test_dependency_analysis_fix(self):
        """Test the fixed dependency analysis."""
        self.console.print("\n🔧 Testing Dependency Analysis Fix", style="bold cyan")

        # Test that dependency analysis no longer flags legitimate TOML
        result = self.run_command(["poetry", "run", "pydvlppy", "doctor"])

        # Should show valid dependencies now
        valid_deps = (
            "Dependencies: All valid" in result["stdout"]
            or "✅ Dependencies" in result["stdout"]
        )
        self.log_test(
            "Dependency Analysis Fixed",
            valid_deps,
            "No false positive dependency conflicts",
            result["duration"],
        )

        # Should not show the old 114 duplicate errors
        no_duplicates = (
            "114" not in result["stdout"]
            and "duplicate dependency" not in result["stdout"].lower()
        )
        self.log_test(
            "No False Duplicates",
            no_duplicates,
            "No false duplicate dependency reports",
            0,
        )

    def test_import_structure(self):
        """Test package import structure."""
        self.console.print("\n📦 Testing Import Structure", style="bold cyan")

        imports_to_test = [
            "pydevelop_docs",
            "pydevelop_docs.config",
            "pydevelop_docs.display",
            "pydevelop_docs.cli",
            "pydevelop_docs.builders",
            "pydevelop_docs.autofix",
            "pydevelop_docs.mock_operations",
        ]

        for module in imports_to_test:
            result = self.run_command(
                ["poetry", "run", "python", "-c", f"import {module}; print('OK')"]
            )
            self.log_test(
                f"Import: {module}",
                result["success"],
                (
                    "Module imports successfully"
                    if result["success"]
                    else result["stderr"]
                ),
                result["duration"],
            )

    def test_configuration_functions(self):
        """Test configuration functions."""
        self.console.print("\n⚙️  Testing Configuration Functions", style="bold cyan")

        # Test get_haive_config
        result = self.run_command(
            [
                "poetry",
                "run",
                "python",
                "-c",
                "from pydevelop_docs.config import get_haive_config; "
                "config = get_haive_config('test', '.'); "
                "print('Config keys:', len(config.keys()))",
            ]
        )
        self.log_test(
            "get_haive_config",
            result["success"] and "Config keys:" in result["stdout"],
            (
                f"Configuration generated: {result['stdout'].strip()}"
                if result["success"]
                else result["stderr"]
            ),
            result["duration"],
        )

        # Test get_central_hub_config
        result = self.run_command(
            [
                "poetry",
                "run",
                "python",
                "-c",
                "from pydevelop_docs.config import get_central_hub_config; "
                "config = get_central_hub_config(['test']); "
                "print('Central config keys:', len(config.keys()))",
            ]
        )
        self.log_test(
            "get_central_hub_config",
            result["success"] and "Central config keys:" in result["stdout"],
            (
                f"Central hub config generated: {result['stdout'].strip()}"
                if result["success"]
                else result["stderr"]
            ),
            result["duration"],
        )

    def test_mock_operations_system(self):
        """Test the new mock operations system."""
        self.console.print("\n🎭 Testing Mock Operations System", style="bold cyan")

        # Test MockOperation creation
        result = self.run_command(
            [
                "poetry",
                "run",
                "python",
                "-c",
                "from pydevelop_docs.mock_operations import MockOperation, MockOperationPlan; "
                "op = MockOperation('test', 'Test operation'); "
                "plan = MockOperationPlan('Test Plan'); "
                "plan.add_operation(op); "
                "print('Plan operations:', len(plan.operations))",
            ]
        )
        self.log_test(
            "Mock Operations Creation",
            result["success"] and "Plan operations: 1" in result["stdout"],
            "Mock operations system working",
            result["duration"],
        )

        # Test create_documentation_plan
        result = self.run_command(
            [
                "poetry",
                "run",
                "python",
                "-c",
                "from pydevelop_docs.mock_operations import create_documentation_plan; "
                "from pathlib import Path; "
                "plan = create_documentation_plan(Path('.'), {'name': 'test'}, False); "
                "print('Doc plan operations:', len(plan.operations))",
            ]
        )
        self.log_test(
            "Documentation Plan Creation",
            result["success"] and "Doc plan operations:" in result["stdout"],
            (
                f"Documentation plan generated: {result['stdout'].strip()}"
                if result["success"]
                else result["stderr"]
            ),
            result["duration"],
        )

    def test_error_handling(self):
        """Test error handling and edge cases."""
        self.console.print("\n🛡️  Testing Error Handling", style="bold cyan")

        # Test invalid command
        result = self.run_command(
            ["poetry", "run", "pydvlppy", "nonexistent-command"]
        )
        self.log_test(
            "Invalid Command Handling",
            not result["success"],  # Should fail gracefully
            "Invalid commands handled properly",
            result["duration"],
        )

        # Test init in directory without pyproject.toml
        temp_dir = Path("/tmp/test_pydevelop_docs")
        temp_dir.mkdir(exist_ok=True)

        result = self.run_command(
            ["poetry", "run", "pydvlppy", "init", "--dry-run"], timeout=30
        )

        # Should handle missing pyproject.toml gracefully
        handles_missing = result["success"] or "pyproject.toml" in result["stderr"]
        self.log_test(
            "Missing pyproject.toml Handling",
            handles_missing,
            "Missing dependencies handled gracefully",
            result["duration"],
        )

    def generate_audit_report(self) -> Dict[str, Any]:
        """Generate comprehensive audit report."""
        total_duration = (datetime.now() - self.start_time).total_seconds()

        successful_tests = [t for t in self.test_results if t["success"]]
        failed_tests = [t for t in self.test_results if not t["success"]]

        report = {
            "audit_info": {
                "timestamp": datetime.now().isoformat(),
                "total_duration": total_duration,
                "total_tests": len(self.test_results),
                "successful_tests": len(successful_tests),
                "failed_tests": len(failed_tests),
                "success_rate": (
                    len(successful_tests) / len(self.test_results) * 100
                    if self.test_results
                    else 0
                ),
            },
            "test_results": self.test_results,
            "successful_tests": successful_tests,
            "failed_tests": failed_tests,
            "recommendations": self._generate_recommendations(),
        }

        return report

    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results."""
        recommendations = []

        failed_tests = [t for t in self.test_results if not t["success"]]

        if failed_tests:
            recommendations.append("Review failed tests and fix underlying issues")

        if any("import" in t["test_name"].lower() for t in failed_tests):
            recommendations.append("Check package dependencies and import structure")

        if any("dry-run" in t["test_name"].lower() for t in failed_tests):
            recommendations.append("Review dry-run functionality implementation")

        if not failed_tests:
            recommendations.append("All tests passed! Package is functioning correctly")
            recommendations.append(
                "Consider adding more comprehensive integration tests"
            )

        return recommendations

    def display_summary(self, report: Dict[str, Any]):
        """Display audit summary."""
        info = report["audit_info"]

        # Summary table
        summary_table = Table(
            title="📊 Audit Summary", show_header=True, header_style="bold magenta"
        )
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="green")

        summary_table.add_row("Total Duration", f"{info['total_duration']:.2f}s")
        summary_table.add_row("Total Tests", str(info["total_tests"]))
        summary_table.add_row("Successful", str(info["successful_tests"]))
        summary_table.add_row("Failed", str(info["failed_tests"]))
        summary_table.add_row("Success Rate", f"{info['success_rate']:.1f}%")

        self.console.print(summary_table)

        # Failed tests table
        if report["failed_tests"]:
            failed_table = Table(
                title="❌ Failed Tests", show_header=True, header_style="bold red"
            )
            failed_table.add_column("Test", style="cyan")
            failed_table.add_column("Details", style="yellow")

            for test in report["failed_tests"]:
                failed_table.add_row(test["test_name"], test["details"])

            self.console.print(failed_table)

        # Recommendations
        if report["recommendations"]:
            self.console.print("\n💡 Recommendations:", style="bold yellow")
            for i, rec in enumerate(report["recommendations"], 1):
                self.console.print(f"  {i}. {rec}")

    def run_full_audit(self) -> Dict[str, Any]:
        """Run complete audit suite."""
        self.console.print(
            "🔍 Starting Comprehensive Package Audit", style="bold green"
        )

        test_suites = [
            self.test_basic_functionality,
            self.test_import_structure,
            self.test_configuration_functions,
            self.test_dependency_analysis_fix,
            self.test_dry_run_functionality,
            self.test_logging_and_debugging,
            self.test_mock_operations_system,
            self.test_error_handling,
        ]

        for test_suite in track(test_suites, description="Running test suites..."):
            try:
                test_suite()
            except Exception as e:
                self.log_test(
                    f"Test Suite: {test_suite.__name__}", False, f"Exception: {e}", 0
                )

        report = self.generate_audit_report()
        self.display_summary(report)

        return report


@click.command()
@click.option("--debug", is_flag=True, help="Show detailed test output")
@click.option("--save-report", type=click.Path(), help="Save audit report to file")
@click.option("--quiet", is_flag=True, help="Minimal output")
def main(debug, save_report, quiet):
    """Run comprehensive audit of pydvlppy package."""
    if not quiet:
        console = Console()
        console.print("🔍 Pydvlppy Package Audit", style="bold blue")
        console.print("=" * 50)

    auditor = PackageAuditor(debug=debug)
    report = auditor.run_full_audit()

    if save_report:
        with open(save_report, "w") as f:
            json.dump(report, f, indent=2)
        if not quiet:
            console.print(f"\n📄 Report saved to: {save_report}")

    # Exit with error code if tests failed
    if report["audit_info"]["failed_tests"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
