#!/usr/bin/env python3
"""
Main entry point for the Recipe Creation System

This script provides a convenient way to start the frontend server
from the base directory of the project.
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add the current directory to Python path to ensure imports work
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))


def main():
    """Start the Recipe Creation Chatbot frontend server."""
    print("🚀 Starting Recipe Creation Chatbot Server...")
    print("📱 Open your browser to: http://localhost:8000")
    print("🛑 Press Ctrl+C to stop the server")
    print()

    try:
        uvicorn.run(
            "frontend.frontend:app",
            host="localhost",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("Make sure you have:")
        print("1. Installed all requirements: pip install -r requirements.txt")
        print("2. Set up your .env file with OPENAI_API_KEY")
        sys.exit(1)


if __name__ == "__main__":
    main()
