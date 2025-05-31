"""
Agent Definitions for Recipe Creation and Evaluation System

This module defines the roles, purposes, and behaviors of the two agents
used in our LangGraph-based recipe workflow system.
"""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


class RecipeCreatorAgent:
    """
    Agent responsible for creating original recipes based on user input.

    Role: Creative Recipe Developer
    Purpose: Generate detailed, creative recipes with clear ingredients and instructions

    Capabilities:
    - Takes user preferences (cuisine type, dietary restrictions, ingredients)
    - Creates complete recipes with ingredients list and step-by-step instructions
    - Considers cooking time, difficulty level, and serving size
    - Provides creative variations and substitutions when appropriate
    """

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.name = "Recipe Creator"
        self.role = "Creative Recipe Developer"

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a creative and experienced chef specializing in recipe development.
            Your role is to create detailed, practical recipes based on user requests.
            
            Guidelines:
            - Always provide a complete ingredients list with measurements
            - Include step-by-step cooking instructions
            - Mention cooking time, prep time, and serving size
            - Consider dietary restrictions and preferences
            - Be creative but practical
            - Include helpful cooking tips when relevant
            
            Format your response as a structured recipe with:
            1. Recipe Name
            2. Ingredients (with quantities)
            3. Instructions (numbered steps)
            4. Cooking/Prep Time
            5. Serving Size
            6. Optional: Tips or Variations"""),
            ("human", "{user_input}")
        ])

    def create_recipe(self, user_input: str) -> str:
        """Generate a recipe based on user input."""
        chain = self.prompt_template | self.llm
        response = chain.invoke({"user_input": user_input})
        return response.content


class RecipeEvaluatorAgent:
    """
    Agent responsible for evaluating and improving recipes created by the Recipe Creator.

    Role: Recipe Quality Assurance Specialist
    Purpose: Analyze recipes for logic, safety, and quality, then provide improvements

    Capabilities:
    - Evaluates recipe logic and cooking procedures
    - Identifies potential safety issues or cooking problems
    - Suggests improvements for taste, technique, or efficiency
    - Validates ingredient combinations and cooking methods
    - Provides constructive feedback and alternative approaches
    """

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.name = "Recipe Evaluator"
        self.role = "Recipe Quality Assurance Specialist"

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert culinary reviewer and food safety specialist.
            Your role is to evaluate recipes for logic, safety, and quality.
            
            Evaluation Criteria:
            - Cooking logic and procedure correctness
            - Food safety considerations
            - Ingredient compatibility and proportions
            - Cooking time and temperature accuracy
            - Clarity of instructions
            - Potential improvements or alternatives
            
            Provide your evaluation in this format:
            1. Overall Assessment (Good/Needs Improvement/Problematic)
            2. Strengths of the recipe
            3. Areas for improvement
            4. Safety considerations (if any)
            5. Suggested modifications
            6. Final recommendation"""),
            ("human", "Please evaluate this recipe:\n\n{recipe}")
        ])

    def evaluate_recipe(self, recipe: str) -> str:
        """Evaluate a recipe and provide feedback."""
        chain = self.prompt_template | self.llm
        response = chain.invoke({"recipe": recipe})
        return response.content


# Agent registry for easy access
AGENT_DEFINITIONS = {
    "recipe_creator": {
        "class": RecipeCreatorAgent,
        "role": "Creative Recipe Developer",
        "purpose": "Generate detailed, creative recipes based on user preferences",
        "capabilities": [
            "Create complete recipes with ingredients and instructions",
            "Consider dietary restrictions and preferences",
            "Provide cooking tips and variations",
            "Estimate cooking and prep times"
        ]
    },
    "recipe_evaluator": {
        "class": RecipeEvaluatorAgent,
        "role": "Recipe Quality Assurance Specialist",
        "purpose": "Evaluate recipes for logic, safety, and quality",
        "capabilities": [
            "Analyze cooking procedures for correctness",
            "Identify food safety issues",
            "Suggest recipe improvements",
            "Validate ingredient combinations"
        ]
    }
}
