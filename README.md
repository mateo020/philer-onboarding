# Recipe Creation & Evaluation System - Philer Onboarding Project

## 🏗️ Project Architecture

### System Components

```
philer-onboarding/
│
├── agents/                     # Agents package - modular agent components
│   ├── __init__.py            # Package initialization and exports
│   ├── agent_definitions.py   # Agent class definitions and roles
│   ├── workflow_state.py      # Shared workflow state definition
│   ├── recipe_creator_node.py # Recipe creation node function
│   ├── recipe_evaluator_node.py # Recipe evaluation node function
│   └── format_output_node.py  # Output formatting node function
├── frontend/                   # Frontend web interface
│   ├── frontend.py            # FastAPI web server and chat interface
│   └── templates/             # Frontend HTML templates
│       └── chat.html          # Main chat interface
├── workflow.py                 # Main LangGraph workflow orchestration
├── main.py                     # Main entry point to run the frontend server
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── test_setup.py              # Setup validation and testing
├── setup.py                   # Quick setup automation script
└── README.md                  # This file
```

## 🤖 Agent System Design

### Agent 1: Recipe Creator Agent

- **Role**: Creative Recipe Developer
- **Purpose**: Generate detailed, practical recipes based on user requests
- **Capabilities**:
  - Creates complete recipes with ingredients and instructions
  - Considers dietary restrictions and preferences
  - Provides cooking tips and variations
  - Estimates cooking and prep times

### Agent 2: Recipe Evaluator Agent

- **Role**: Recipe Quality Assurance Specialist
- **Purpose**: Evaluate recipes for logic, safety, and quality
- **Capabilities**:
  - Analyzes cooking procedures for correctness
  - Identifies potential food safety issues
  - Suggests recipe improvements
  - Validates ingredient combinations and cooking methods

## 📁 File System Guide

### `agents.py` - Agent Definitions

This file contains the core agent classes and their configurations:

```python
# Key Components:
- RecipeCreatorAgent class: Handles recipe generation
- RecipeEvaluatorAgent class: Handles recipe evaluation
- AGENT_DEFINITIONS: Registry of all available agents
```

**Role**: Defines the "who" - what each agent does and how they behave

### `workflow.py` - LangGraph Workflow

This is the main orchestration file that defines how agents work together:

```python
# Key Components:
- WorkflowState: Defines data structure passed between agents
- RecipeWorkflow class: Orchestrates the multi-agent process
- Node functions: Individual steps in the workflow
- Graph building: Defines the flow between agents
```

**Role**: Defines the "how" - the sequence and logic of agent interactions

## 🚀 Setup Instructions

### 1. Environment Setup

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
copy .env.example .env
# Edit .env file and add your OpenAI API key
```

### 2. Configuration

Edit the `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Running the Application

#### Option A: Run the Full Web Application (Recommended)

```bash
python main.py
```

Then open your browser to: `http://localhost:8000`

## 🔄 Workflow Flow Explanation

### Step-by-Step Process

1. **User Input**: User requests a recipe via the chat interface
2. **Recipe Creation**: Recipe Creator Agent generates a detailed recipe
3. **Recipe Evaluation**: Recipe Evaluator Agent reviews and critiques the recipe
4. **Output Formatting**: System combines both outputs into a user-friendly response
5. **Response Delivery**: Final result is displayed in the chat interface

### State Management

The workflow uses a `WorkflowState` object that gets passed between nodes (this is easier for keeping track of progress and variables):

```python
WorkflowState:
- user_input: Original user request
- recipe: Generated recipe
- evaluation: Professional evaluation
- final_output: Formatted final response
- step: Current workflow stage
```

## 🔧 Customization Ideas

### Extending the System

1. **Add More Agents**: Nutrition analyzer, cost calculator, meal planner
2. **Enhance Workflow**: Add conditional paths, loops, or user feedback
3. **Improve Frontend**: Add voice input, recipe saving, shopping lists
4. **Data Integration**: Connect to recipe databases or nutritional APIs

### Learning Exercises

1. **Modify Agent Behavior**: Change prompts to alter agent personalities
2. **Add Workflow Steps**: Insert additional processing nodes
3. **Create New Agents**: Build agents for other cooking-related tasks
4. **Experiment with State**: Add new fields to track additional information

### Next Steps

1. Read the [LangGraph documentation](https://langchain-ai.github.io/langgraph/)
2. Make custom agents (e.g. specializing in Chinese cuisine by editing agent role)
