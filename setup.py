"""
Quick start script for the Recipe Creation System
"""

import subprocess
import sys
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is sufficient."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    else:
        print(f"✅ Python version: {sys.version.split()[0]}")
        return True


def create_virtual_environment():
    """Create a virtual environment if it doesn't exist."""
    venv_path = Path("venv")

    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True

    print("\n🔧 Creating virtual environment...")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        print("✅ Virtual environment created successfully")
        print("⚠️  Please activate the virtual environment:")
        print("   Windows: venv\\Scripts\\activate")
        print("   PowerShell: .\\venv\\Scripts\\Activate.ps1")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False


def install_requirements():
    """Install required packages."""
    print("\n📦 Installing required packages...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False


def setup_environment():
    """Set up environment file if it doesn't exist."""
    env_file = Path(".env")
    env_example = Path(".env.example")

    if not env_file.exists() and env_example.exists():
        print("\n🔧 Setting up environment file...")
        try:
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✅ Created .env file from .env.example")
            print(
                "⚠️  Please edit .env and add your OpenAI API key before running the application")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    elif env_file.exists():
        print("\n✅ .env file already exists")
        return True
    else:
        print("\n❌ .env.example file not found")
        return False


def run_tests():
    """Run setup validation tests."""
    print("\n🧪 Running setup validation...")
    try:
        subprocess.check_call([sys.executable, "test_setup.py"])
        return True
    except subprocess.CalledProcessError:
        print("❌ Setup validation failed")
        return False


def main():
    """Main setup function."""
    print("🚀 Recipe Creation System - Quick Start Setup")
    print("=" * 50)
    # Check Python version
    if not check_python_version():
        return

    # Create virtual environment
    if not create_virtual_environment():
        return

    # Install requirements
    if not install_requirements():
        return

    # Setup environment
    if not setup_environment():
        return

    # Run validation tests
    print("\n" + "=" * 50)
    print("🎯 Running final validation...")

    if run_tests():
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Edit .env file and add your OpenAI API key")
        print("2. Run: python main.py")
        print("3. Open: http://localhost:8000")
    else:
        print("\n⚠️  Setup completed with issues. Check the test output above.")


if __name__ == "__main__":
    main()
