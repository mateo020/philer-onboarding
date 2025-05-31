"""
Format Output Node for LangGraph Workflow

This module contains the node function for formatting the final output in the workflow.
"""

from typing import Dict, Any
from .workflow_state import WorkflowState


def format_final_output_node(state: WorkflowState) -> WorkflowState:
    """
    Node function for formatting the final output.

    This function handles the final step of the workflow where the recipe and
    evaluation are combined into a user-friendly formatted response. It takes
    the outputs from both agents and creates a structured markdown document.

    Args:
        state: Current workflow state containing recipe and evaluation

    Returns:
        Updated state with formatted final output
    """
    print("📝 Formatting final response...")

    final_output = f"""
# Recipe Creation & Evaluation Results

## 🍳 Generated Recipe
{state['recipe']}

---

## 📋 Professional Evaluation
{state['evaluation']}

---

*This recipe was created by our Recipe Creator agent and evaluated by our Recipe Evaluator agent for quality assurance.*
"""

    return {
        **state,
        "final_output": final_output.strip(),
        "step": "completed"
    }
