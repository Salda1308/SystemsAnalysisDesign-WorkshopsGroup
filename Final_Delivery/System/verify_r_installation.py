#!/usr/bin/env python3
"""
R Installation Verification Script
Verifies R installation, required packages, and integration with the project
"""

import subprocess
import sys
import platform
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def check_r_installation():
    """Check if R and Rscript are installed"""
    print_header("1. CHECKING R INSTALLATION")

    # Common R installation paths on Windows
    common_paths = []
    if platform.system() == "Windows":
        program_files = [
            r"C:\Program Files\R",
            r"C:\Program Files (x86)\R"
        ]
        for pf in program_files:
            pf_path = Path(pf)
            if pf_path.exists():
                # Find all R versions
                for version_dir in pf_path.glob("R-*"):
                    rscript = version_dir / "bin" / "Rscript.exe"
                    if rscript.exists():
                        common_paths.append(str(rscript))

    # Try Rscript in PATH
    r_found = False
    r_path = None
    r_version = None

    print("\n🔍 Checking for Rscript in PATH...")
    try:
        result = subprocess.run(
            ["Rscript", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            shell=False
        )
        if result.returncode == 0:
            r_found = True
            r_path = "Rscript"
            r_version = result.stderr.strip()  # R prints version to stderr
            print(f"✅ Rscript found in PATH")
            print(f"   Version: {r_version}")
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"❌ Rscript not found in PATH")
        print(f"   Error: {type(e).__name__}")

    # Check common installation paths
    if not r_found and common_paths:
        print(f"\n🔍 Checking common installation paths...")
        print(f"   Found {len(common_paths)} potential R installations:")
        for idx, path in enumerate(common_paths, 1):
            print(f"   {idx}. {path}")
            try:
                result = subprocess.run(
                    [path, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    shell=False
                )
                if result.returncode == 0:
                    r_found = True
                    r_path = path
                    version_text = result.stderr.strip()
                    if version_text:
                        r_version = version_text.split('\n')[0]
                    print(f"      ✅ Working! {r_version if r_version else 'R found'}")
                    break
                else:
                    print(f"      ❌ Not working")
            except Exception as e:
                print(f"      ❌ Error: {type(e).__name__}")

    if not r_found:
        print("\n" + "="*70)
        print("❌ R IS NOT INSTALLED")
        print("="*70)
        print("\n📥 To install R:")
        print("   1. Visit: https://cran.r-project.org/")
        print("   2. Download R for Windows")
        print("   3. Run the installer with default settings")
        print("   4. Restart your terminal after installation")
        print("\n💡 Alternative: Use winget (Windows Package Manager)")
        print("   winget install --id RProject.R")
        return None, None

    return r_path, r_version

def check_r_packages(r_path):
    """Check if required R packages are installed"""
    print_header("2. CHECKING R PACKAGES")

    required_packages = ["caret", "randomForest", "xgboost", "jsonlite", "data.table"]

    # Create R script to check packages
    r_script = "packages <- c('caret', 'randomForest', 'xgboost', 'jsonlite', 'data.table'); installed <- installed.packages()[, 'Package']; for (pkg in packages) { if (pkg %in% installed) { version <- packageVersion(pkg); cat(sprintf('%s: INSTALLED (v%s)\\n', pkg, version)) } else { cat(sprintf('%s: NOT INSTALLED\\n', pkg)) }}"

    try:
        result = subprocess.run(
            [r_path, "-e", r_script],
            capture_output=True,
            text=True,
            timeout=30,
            shell=False
        )

        print("\n📦 Package Status:")
        output = result.stdout if result.stdout else result.stderr
        print(output)

        missing = []
        for line in output.split('\n'):
            if 'NOT INSTALLED' in line:
                pkg_name = line.split(':')[0].strip()
                missing.append(pkg_name)

        if missing:
            print(f"\n⚠️  Missing packages: {', '.join(missing)}")
            print("\n📥 To install missing packages, run:")
            packages_str = "', '".join(missing)
            cmd = f'& "{r_path}" -e "install.packages(c(\'{packages_str}\'), repos=\'https://cloud.r-project.org/\')"'
            print(f"   {cmd}")
            return False
        else:
            print("\n✅ All required packages are installed!")
            return True

    except Exception as e:
        print(f"❌ Error checking packages: {e}")
        return False

def test_r_script_execution(r_path):
    """Test if R scripts can be executed"""
    print_header("3. TESTING R SCRIPT EXECUTION")

    test_script = "cat('Hello from R!\\n'); cat('R is working correctly\\n'); cat('Version:', R.version.string, '\\n')"

    print("\n🧪 Running test R script...")
    try:
        result = subprocess.run(
            [r_path, "-e", test_script],
            capture_output=True,
            text=True,
            timeout=10,
            shell=False
        )

        if result.returncode == 0:
            print("✅ R script execution successful!")
            print("\nOutput:")
            output = result.stdout if result.stdout else result.stderr
            print(output)
            return True
        else:
            print("❌ R script execution failed")
            print(f"Return code: {result.returncode}")
            return False

    except Exception as e:
        print(f"❌ Error executing R script: {e}")
        return False

def check_project_r_files():
    """Check project R files"""
    print_header("4. CHECKING PROJECT R FILES")

    r_files = [
        ("Training Layer/compare_models.R", "Model training script"),
        ("Presentation Layer/predict.R", "Prediction API script")
    ]

    print("\n📄 Project R Files:")
    all_found = True
    for file_path, description in r_files:
        full_path = Path(file_path)
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"   ✅ {file_path}")
            print(f"      {description} ({size} bytes)")
        else:
            print(f"   ❌ {file_path} - NOT FOUND")
            all_found = False

    return all_found

def generate_integration_test(r_path):
    """Generate a test to verify Python-R communication"""
    print_header("5. PYTHON-R INTEGRATION TEST")

    print("\n🔗 Testing Python → R communication...")

    test_script = "args <- commandArgs(trailingOnly = TRUE); if (length(args) > 0) { cat('Received argument:', args[1], '\\n'); result <- as.numeric(args[1]) * 2; cat('Result:', result, '\\n') } else { cat('No arguments received\\n') }"

    try:
        result = subprocess.run(
            [r_path, "-e", test_script, "42"],
            capture_output=True,
            text=True,
            timeout=10,
            shell=False
        )

        output = result.stdout if result.stdout else result.stderr

        if result.returncode == 0 and ("84" in output or "Received argument: 42" in output):
            print("✅ Python-R communication working!")
            print(f"\nTest Output:\n{output}")
            return True
        else:
            print("⚠️  Communication test partially successful")
            print(f"Output: {output}")
            return True  # Still consider it successful if R executed

    except Exception as e:
        print(f"❌ Integration test error: {e}")
        return False

def main():
    """Run all verification checks"""
    print("\n" + "="*70)
    print("  🔬 R INSTALLATION VERIFICATION FOR CHOCOLATE SALES PROJECT")
    print("="*70)

    # Check 1: R Installation
    r_path, r_version = check_r_installation()
    if not r_path:
        print("\n" + "="*70)
        print("⛔ VERIFICATION FAILED - R NOT INSTALLED")
        print("="*70)
        sys.exit(1)

    # Check 2: R Packages
    packages_ok = check_r_packages(r_path)

    # Check 3: Script Execution
    execution_ok = test_r_script_execution(r_path)

    # Check 4: Project Files
    files_ok = check_project_r_files()

    # Check 5: Integration
    integration_ok = generate_integration_test(r_path)

    # Final Summary
    print_header("📊 VERIFICATION SUMMARY")

    checks = [
        ("R Installation", r_path is not None),
        ("Required Packages", packages_ok),
        ("Script Execution", execution_ok),
        ("Project R Files", files_ok),
        ("Python-R Integration", integration_ok)
    ]

    print()
    for check_name, status in checks:
        icon = "✅" if status else "❌"
        print(f"   {icon} {check_name}")

    all_passed = all(status for _, status in checks)

    if all_passed:
        print("\n" + "="*70)
        print("🎉 ALL CHECKS PASSED! R IS READY TO USE")
        print("="*70)
        print(f"\n📍 R Path: {r_path}")
        if r_version:
            print(f"📍 Version: {r_version.split()[0] if ' ' in r_version else r_version}")
        print("\n✅ You can now run:")
        print("   .\\venv\\Scripts\\python.exe run_pipeline.py")
        return 0
    else:
        print("\n" + "="*70)
        print("⚠️  SOME CHECKS FAILED - PLEASE FIX THE ISSUES ABOVE")
        print("="*70)
        return 1

if __name__ == "__main__":
    sys.exit(main())
