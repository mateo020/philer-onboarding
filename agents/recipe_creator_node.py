"""
Recipe Creator Node for LangGraph Workflow

This module contains the node function for recipe creation step in the workflow.
"""

import os
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from .agent_definitions import RecipeCreatorAgent
from .workflow_state import WorkflowState


def create_recipe_node(state: WorkflowState) -> WorkflowState:
    """
    Node function for recipe creation.

    This function handles the first step of the workflow where a recipe is created
    based on the user's input. It uses the RecipeCreatorAgent to generate a detailed
    recipe with ingredients, instructions, and cooking information.

    Args:
        state: Current workflow state containing user input

    Returns:
        Updated state with generated recipe
    """
    print(f"🍳 Recipe Creator is creating a recipe...")

    # Initialize LLM and agent
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    recipe_creator = RecipeCreatorAgent(llm)

    # Generate the recipe
    recipe = recipe_creator.create_recipe(state["user_input"])

    return {
        **state,
        "recipe": recipe,
        "step": "recipe_created"
    }
