"""
Test script to validate the setup and demonstrate the workflow
"""

import os
from dotenv import load_dotenv


def test_environment():
    """Test if environment variables are properly configured."""
    print("🔍 Testing Environment Configuration...")

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("   Please copy .env.example to .env and add your API key")
        return False
    elif api_key == "your_openai_api_key_here":
        print("❌ OPENAI_API_KEY is still set to the default placeholder")
        print("   Please update .env with your actual OpenAI API key")
        return False
    else:
        print(f"✅ OPENAI_API_KEY found (ending in: ...{api_key[-4:]})")
        return True


def test_imports():
    """Test if all required packages are installed."""
    print("\n📦 Testing Package Imports...")

    try:
        import langgraph
        print(f"✅ langgraph imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import langgraph: {e}")
        return False

    try:
        import langchain
        print(f"✅ langchain imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import langchain: {e}")
        return False

    try:
        import fastapi
        print(f"✅ fastapi imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import fastapi: {e}")
        return False

    return True


def test_agents():
    """Test if agents can be imported and initialized."""
    print("\n🤖 Testing Agent Definitions...")

    try:
        from agents import RecipeCreatorAgent, RecipeEvaluatorAgent, AGENT_DEFINITIONS
        print("✅ Agent classes imported successfully")
        print(f"✅ Found {len(AGENT_DEFINITIONS)} agent definitions")

        for agent_name, agent_info in AGENT_DEFINITIONS.items():
            print(f"   - {agent_name}: {agent_info['role']}")

        return True
    except ImportError as e:
        print(f"❌ Failed to import agents: {e}")
        return False


def test_workflow():
    """Test if workflow can be imported (but not run without API key)."""
    print("\n🔄 Testing Workflow Import...")

    try:
        from workflow import build_workflow, run_workflow
        from agents import WorkflowState
        print("✅ Workflow functions imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import workflow: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 Running Setup Validation Tests for Recipe Creation System\n")

    env_ok = test_environment()
    imports_ok = test_imports()
    agents_ok = test_agents()
    workflow_ok = test_workflow()

    print("\n" + "="*60)
    print("📊 Test Results Summary:")
    print("="*60)

    if all([env_ok, imports_ok, agents_ok, workflow_ok]):
        print("🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Run 'python main.py' to start the web interface")
        print("2. Open http://localhost:8000 in your browser")
        print("3. Try asking for a recipe!")
    else:
        print("❌ Some tests failed. Please fix the issues above before proceeding.")
        print("\nCommon fixes:")
        if not env_ok:
            print("- Copy .env.example to .env and add your OpenAI API key")
        if not imports_ok:
            print("- Run 'pip install -r requirements.txt'")


if __name__ == "__main__":
    main()
