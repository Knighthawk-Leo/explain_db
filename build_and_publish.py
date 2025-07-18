#!/usr/bin/env python3
"""
Helper script to build and publish the explain_db package to PyPI.

Usage:
    python build_and_publish.py --build          # Build the package only
    python build_and_publish.py --test           # Upload to TestPyPI
    python build_and_publish.py --publish        # Upload to PyPI
    python build_and_publish.py --clean          # Clean build artifacts
"""

import os
import shutil
import subprocess
import sys
import argparse


def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(f"Command: {command}")
        print(f"Exit code: {e.returncode}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)


def clean_build_artifacts():
    """Remove build artifacts and dist directories."""
    dirs_to_remove = ['build', 'dist', 'explain_db.egg-info']
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            print(f"🧹 Removing {dir_name}/")
            shutil.rmtree(dir_name)
    
    print("✅ Build artifacts cleaned")


def build_package():
    """Build the package."""
    clean_build_artifacts()
    
    # Install build tools if not present
    run_command("pip install --upgrade build twine", "Installing/upgrading build tools")
    
    # Build the package
    run_command("python -m build", "Building package")
    
    print("\n📦 Package built successfully!")
    print("Files created:")
    if os.path.exists('dist'):
        for file in os.listdir('dist'):
            print(f"  - dist/{file}")


def upload_to_test_pypi():
    """Upload package to Test PyPI."""
    if not os.path.exists('dist'):
        print("❌ No dist/ directory found. Run build first.")
        sys.exit(1)
    
    print("\n🚀 Uploading to Test PyPI...")
    print("You'll need to enter your Test PyPI credentials.")
    
    run_command(
        "python -m twine upload --repository testpypi dist/*",
        "Uploading to Test PyPI"
    )
    
    print("\n✅ Package uploaded to Test PyPI successfully!")
    print("You can install it with:")
    print("pip install --index-url https://test.pypi.org/simple/ explain_db")


def upload_to_pypi():
    """Upload package to PyPI."""
    if not os.path.exists('dist'):
        print("❌ No dist/ directory found. Run build first.")
        sys.exit(1)
    
    print("\n🚀 Uploading to PyPI...")
    print("You'll need to enter your PyPI credentials.")
    
    confirmation = input("Are you sure you want to upload to PyPI? (yes/no): ")
    if confirmation.lower() != 'yes':
        print("Upload cancelled.")
        sys.exit(0)
    
    run_command("python -m twine upload dist/*", "Uploading to PyPI")
    
    print("\n✅ Package uploaded to PyPI successfully!")
    print("You can install it with:")
    print("pip install explain_db")


def main():
    parser = argparse.ArgumentParser(description="Build and publish explain_db package")
    parser.add_argument('--build', action='store_true', help='Build the package')
    parser.add_argument('--test', action='store_true', help='Upload to Test PyPI')
    parser.add_argument('--publish', action='store_true', help='Upload to PyPI')
    parser.add_argument('--clean', action='store_true', help='Clean build artifacts')
    
    args = parser.parse_args()
    
    if not any([args.build, args.test, args.publish, args.clean]):
        parser.print_help()
        sys.exit(1)
    
    if args.clean:
        clean_build_artifacts()
    
    if args.build:
        build_package()
    
    if args.test:
        if not args.build:
            build_package()
        upload_to_test_pypi()
    
    if args.publish:
        if not args.build:
            build_package()
        upload_to_pypi()


if __name__ == "__main__":
    main() 