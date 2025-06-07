"""
notrient eval or LangGraph Workflow

This module contains the node function for breakdown of nutritional content.
"""

import os
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from .agent_definitions import NutritionalAnalysisAgent
from .workflow_state import WorkflowState


def analyse_nutrition_node(state: WorkflowState) -> WorkflowState:
    """
    Run the NutritionalAnalysisAgent on the current recipe text.

    Expects `state` to contain a `"recipe"` key with the full recipe string.

    Adds two keys to the state:
        • "nutrient_profile"  – string returned by the agent
        • "step"              – set to "nutrients_analyzed"
    """
    print("🥗  Running nutritional analysis ...")

    # Initialize LLM and agent
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.01,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    nutrition_agent = NutritionalAnalysisAgent(llm)

    nutrient_profile = nutrition_agent.analyse_nutrients(state["recipe"])

    return {
        **state,
        "nutrient_profile": nutrient_profile,
        "step": "nutrients_analyzed",
    }
