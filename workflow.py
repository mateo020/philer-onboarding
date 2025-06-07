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
    format_final_output_node,
    evaluate_goal_node,
    analyse_nutrition_node,
    nearby_restaurants_node

)

# Load environment variables
load_dotenv()


def build_workflow() -> StateGraph:  # type: ignore[valid-type]
    """Compile the LangGraph recipe workflow graph."""

    graph = StateGraph(WorkflowState)

    # Add each node
    graph.add_node("create_recipe", create_recipe_node)
    graph.add_node("analyse_nutrition", analyse_nutrition_node)
    graph.add_node("evaluate_goal", evaluate_goal_node)
    graph.add_node("evaluate_recipe", evaluate_recipe_node)
    graph.add_node("nearby_restaurants", nearby_restaurants_node)
    graph.add_node("format_final_output", format_final_output_node)


    # Wire edges
    graph.set_entry_point("create_recipe")
    graph.add_edge("create_recipe", "analyse_nutrition")
    graph.add_edge("analyse_nutrition", "evaluate_goal")
 
    graph.add_conditional_edges(
    "evaluate_goal",                     # source node
    lambda s:                            
        "create_recipe" if s["goal_compliance"] == "NO" else "evaluate_recipe",
    [
        "create_recipe",                 # allowed branch if goal not met
        "evaluate_recipe",               # normal forward branch
    ],
)

    graph.add_edge("evaluate_recipe", "format_final_output")
    graph.add_edge("format_final_output", END)

    return graph.compile()


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
        nutrition_profile= "",
        goal_compliance= "",
        goal ="weight loss",
        weight= 200,
        evaluation = "",
        final_output= "",
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
