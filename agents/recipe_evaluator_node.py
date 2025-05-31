"""
Recipe Evaluator Node for LangGraph Workflow

This module contains the node function for recipe evaluation step in the workflow.
"""

import os
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from .agent_definitions import RecipeEvaluatorAgent
from .workflow_state import WorkflowState


def evaluate_recipe_node(state: WorkflowState) -> WorkflowState:
    """
    Node function for recipe evaluation.

    This function handles the second step of the workflow where the generated recipe
    is evaluated for quality, safety, and correctness. It uses the RecipeEvaluatorAgent
    to provide professional feedback and suggestions for improvement.

    Args:
        state: Current workflow state containing the generated recipe

    Returns:
        Updated state with recipe evaluation
    """
    print(f"📋 Recipe Evaluator is evaluating the recipe...")

    # Initialize LLM and agent
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    recipe_evaluator = RecipeEvaluatorAgent(llm)

    # Evaluate the recipe
    evaluation = recipe_evaluator.evaluate_recipe(state["recipe"])

    return {
        **state,
        "evaluation": evaluation,
        "step": "recipe_evaluated"
    }
