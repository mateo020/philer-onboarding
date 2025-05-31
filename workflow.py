"""
Main Workflow for Recipe Creation and Evaluation System

This module implements the LangGraph workflow that coordinates between
the Recipe Creator and Recipe Evaluator agents using modular node functions.
"""

import os
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

from agents import (
    WorkflowState,
    create_recipe_node,
    evaluate_recipe_node,
    format_final_output_node
)

# Load environment variables
load_dotenv()


def build_workflow() -> StateGraph:
    """
    Build the LangGraph workflow using modular node functions.

    This function creates a workflow graph that connects the different
    node functions in a linear sequence: create -> evaluate -> format

    Returns:
        StateGraph: Configured and compiled workflow graph
    """
    # Create the graph
    workflow = StateGraph(WorkflowState)

    # Add nodes using the imported node functions
    workflow.add_node("create_recipe", create_recipe_node)
    workflow.add_node("evaluate_recipe", evaluate_recipe_node)
    workflow.add_node("format_final_output", format_final_output_node)

    # Add edges (define the flow)
    workflow.set_entry_point("create_recipe")
    workflow.add_edge("create_recipe", "evaluate_recipe")
    workflow.add_edge("evaluate_recipe", "format_final_output")
    workflow.add_edge("format_final_output", END)

    return workflow.compile()


def run_workflow(user_input: str) -> str:
    """
    Run the complete workflow for a user request.

    This function initializes the workflow state and executes the entire
    recipe creation and evaluation process.

    Args:
        user_input: User's recipe request

    Returns:
        str: Final formatted response with recipe and evaluation
    """
    print("🚀 Starting Recipe Creation & Evaluation Workflow")
    print(f"User Request: {user_input}\n")

    # Build the workflow
    workflow = build_workflow()

    # Initialize state
    initial_state = WorkflowState(
        user_input=user_input,
        recipe="",
        evaluation="",
        final_output="",
        step="starting"
    )

    # Run the workflow
    result = workflow.invoke(initial_state)

    print("✅ Workflow completed!\n")
    return result["final_output"]


def main():
    """
    Main function for testing the workflow directly.
    """
    # Example usage
    user_request = "I want to make a healthy pasta dish with vegetables and chicken"
    result = run_workflow(user_request)
    print(result)


if __name__ == "__main__":
    main()
