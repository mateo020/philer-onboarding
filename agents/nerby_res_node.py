"""
notrient eval or LangGraph Workflow

This module contains the node function for breakdown of nutritional content.
"""

import os
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from .agent_definitions import NearbyRestaurantsAgent
from .workflow_state import WorkflowState


def nearby_restaurants_node(state: WorkflowState) -> WorkflowState:
    """Find nearby restaurants matching the recipe’s cuisine keywords."""

    print("🍽️  Finding nearby restaurants ...")

    # Initialize LLM and agent
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.0,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )

    restaurants_agent = NearbyRestaurantsAgent(llm)

    # ------------------------------------------------------------------
    # Query agent
    # ------------------------------------------------------------------
    try:
        suggestions = restaurants_agent.recommend_restaurants(
            query=state["user_input"],
            user_location= "Toronto",
            radius_meters=5000,  # 5‑km default
            max_results=5,
        )
    except Exception as err:
        # In production you might log this; return empty list on failure
        print(f"⚠️  Error fetching restaurant data: {err}")
        suggestions = []

    return {
        **state,
        "restaurant_suggestions": suggestions,
        "step": "restaurants_suggested",
    }
