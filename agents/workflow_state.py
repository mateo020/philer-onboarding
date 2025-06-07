"""
Shared State Definition for LangGraph Workflow

This module contains the WorkflowState TypedDict that is used across all nodes.
"""

from typing import TypedDict


class WorkflowState(TypedDict):
    """
    State object that gets passed between nodes in the workflow.

    This state object maintains all the data that flows through the workflow,
    from the initial user input to the final formatted output.

    Attributes:
        user_input: Original user request for a recipe
        recipe: Generated recipe from the Recipe Creator agent
        evaluation: Evaluation feedback from the Recipe Evaluator agent
        final_output: Final formatted response to return to user
        step: Current step in the workflow (for tracking progress)
    """
    user_input: str
    recipe: str
    nutrition_profile: str
    nutrient_profile: str
    goal_compliance: str
    weight: int
    evaluation: str
    final_output: str
    step: str
