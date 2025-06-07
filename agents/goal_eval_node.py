"""
Recipe Creator Node for LangGraph Workflow

This module defines the node function that checks whether the recipe’s
nutrient profile meets a user‑specified dietary goal (e.g.
weight‑loss, muscle‑gain, maintenance).
"""

import os
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from .agent_definitions import EvaluateNutritionalContent
from .workflow_state import WorkflowState


def evaluate_goal_node(state: WorkflowState) -> WorkflowState:
    """
    ""Assess whether the nutrient profile supports the user’s dietary goal.

    Expects `state` to carry two keys:
        • `goal`              – str, e.g. "weight loss", "muscle gain"
        • `nutrient_profile`  – str, textual macro/micro breakdown

    Returns the same state extended with:
        • `goal_compliance` – "YES" or "NO"
        • `step`            – "goal_evaluated"
    """
   

    # Initialize LLM and agent
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    goal_evaluator = EvaluateNutritionalContent(llm)

    # Generate the recipe
    verdict = goal_evaluator.evaluate(state["nutrient_profile"], state["nutrition_profile"])

    return {
        **state,
        "goal_compliance": verdict,
        "step": "goal_evaluated",
    }
