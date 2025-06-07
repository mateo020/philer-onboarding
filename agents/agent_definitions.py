"""
Agent Definitions for Recipe Creation and Evaluation System

This module defines the roles, purposes, and behaviors of the two agents
used in our LangGraph-based recipe workflow system.
"""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import List
import os

import googlemaps

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
            2. List[(ingredient, quantity (grams)) ] -  Ingredients (and quantities)
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


class EvaluateNutritionalContent:
    """Determine if a nutrient profile supports a specific dietary goal.

    ### Role
    Dietary Goal Compliance Checker

    ### Purpose
    Given a goal (e.g., *weight loss*, *muscle gain*) and a nutrient breakdown string,
    ask an LLM to judge whether the recipe advances that goal. The agent returns a
    single token: **YES** if compliant, **NO** otherwise.
    """

  

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.name = "Nutritional Goal Evaluator"
        self.role = "Dietary Goal Compliance Checker"

        self.prompt_template = ChatPromptTemplate.from_messages([
            (
                "system",
                (
                    "You are a nutrition coach. Evaluate if a nutrient profile aligns "
                    "with the specified dietary goal. Respond ONLY with 'YES' or 'NO'."
                ),
            ),
            (
                "human",
                (
                    "Goal: {goal}\n\nNutrient Profile:\n{nutrients}\n\nDoes this profile support the goal:{goal} given users weight:{weight}?"
                ),
            ),
        ])


    def evaluate(self, goal: str, nutrient_profile: str, weight: str) -> str:
        """Return 'YES' if profile supports goal, else 'NO'."""
        print(f"goal{goal}")
        

        chain = self.prompt_template | self.llm
        response = chain.invoke({"goal": goal, "nutrients": nutrient_profile, "weight": weight})
        verdict = response.content.strip().upper()
        # force normalization
        return "YES" if verdict.startswith("Y") else "NO"
     
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
            - Explicitly mention the fitness goal
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
            ("human", "Please evaluate this recipe:\n\n{recipe} given the Nutritional profile:\n\n{nutritional_profile} and the fitness goal:\n\n{goal}")
        ])

    def evaluate_recipe(self, recipe: str, nutritional_profile: str, goal: str) -> str:
        """Evaluate a recipe and provide feedback."""
        chain = self.prompt_template | self.llm
        response = chain.invoke({"recipe": recipe, "goal": goal, "nutritional_profile": nutritional_profile})
        return response.content
    

class NutritionalAnalysisAgent:
    """
    Agent responsible for analysising nutritional content of the recipie and its ingredients.

    Role: Recipe Nutritional Content Analysis
    Purpose: Analyze recipe's ingredients nutritional content 

    Capabilities:
    - Evaluates each ingredient Nutritional content; Calories, Carbs, fats, sugars, Vitamin breakdown
    - Creates a detail outline of each ingredient in the recipe and the ingredient amount.
    - Classifies the types of nutrients in the recipe.
    - Provide an overall nutrient count.
    
    """
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.name = "Nutrient Analysis"
        self.role = "Analyse nutritional content of recipe ingredients"

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a creative and experienced chef specializing in recipe development.
            Your role is to create detailed nutritional breakdown based on recipe ingredients and their respective amounts
            
            Guidelines:
            - Always provide a complete ingredients list with measurements
            - Include Nutrients such as proteins, fats, carbs, vitamins and sugar ammounts (in grams) found in each ingredient taking into acount ingredient qunatity.
            - Mention any missing nutriens 

            Format your response containing each individual ingredient as:
            a dictionary key value pairs where they key is the nutrient and value is the amount in gram"""),
            ("human", "{user_input}")
        ])

    def analyse_nutrients(self, recipe: str) -> str:
        """Generate a recipe based on user input."""
        chain = self.prompt_template | self.llm
        response = chain.invoke({"user_input": recipe})
        return response.content
    
class NearbyRestaurantsAgent:
    """Recommend nearby restaurants offering cuisine similar to the given recipe.

    ### Role
    Restaurant Recommendation Assistant

    ### Purpose
    Use Google Maps Places API to find restaurants that likely serve dishes matching
    the recipe’s primary cuisine or keyword terms.

    ### Capabilities
    * Extract key cuisine or dish keywords from the recipe using an LLM chain
    * Query Google Places `textsearch` or `nearbysearch` endpoints
    * Return a curated list of restaurants (name, address, rating, price level)
    * Gracefully handle cases where no results are found
    """

    def __init__(
        self,
        llm: ChatOpenAI,
        api_key: str | None = None,
    ):
        # Allow API key via arg or env var
        api_key = api_key or os.getenv("GOOGLE_MAPS_API_KEY")
        if not api_key:
            raise ValueError("Google Maps API key required for NearbyRestaurantsAgent")

        self.llm = llm
        self.gmaps = googlemaps.Client(key=api_key)
        self.name = "Nearby Restaurants Recommender"
        self.role = "Restaurant Recommendation Assistant"

        # Prompt used to extract cuisine/keywords from recipe text
        self.keyword_prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                (
                    "You are a culinary classifier. Given a recipe, output a short comma‑"\
                    "separated list of 1–3 keywords representing the primary cuisine(s) "\
                    "or dish (e.g., 'Italian pasta', 'vegan taco'). Respond **only** "\
                    "with the keywords."
                ),
            ),
            ("human", "{recipe}"),
        ])


    def recommend_restaurants(
        self,
        query: str,
        user_location: str,
        radius_meters: int = 5000,
        max_results: int = 5,
    ) -> List[Dict[str, Any]]:
        """Return a list of restaurant dicts near `user_location` serving similar food."""
        keywords = query

        # Use Places Text Search for flexibility with cuisine keywords
        places_result = self.gmaps.places(
            query=f"{keywords} restaurant",
            location=user_location,
            radius=radius_meters,
            type="restaurant",
        )

        restaurants: List[Dict[str, Any]] = []
        for result in places_result.get("results", [])[:max_results]:
            restaurants.append(
                {
                    "name": result.get("name"),
                    "address": result.get("formatted_address"),
                    "rating": result.get("rating"),
                    "price_level": result.get("price_level"),
                    "user_ratings_total": result.get("user_ratings_total"),
                }
            )

        return restaurants


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
        
    }, 
     
    "nutritional_analysis": {
    "class": NutritionalAnalysisAgent,
    "role": "Nutrition Analyst",
    "purpose": "Provide macro/micronutrient breakdown for recipes",
    "capabilities": [
        "Break down nutrients per ingredient",
        "Summarize calories, macros, vitamins",
        "Identify missing or excessive nutrients",
    ]

    }, 
    "nearby_restaurants": {
        "class": NearbyRestaurantsAgent,
        "role": "Restaurant Recommendation Assistant",
        "purpose": "Recommend local restaurants serving cuisine similar to the recipe",
        "capabilities": [
            "Extract cuisine keywords from recipe",
            "Query Google Places API for matching restaurants",
            "Return curated list with ratings and addresses",
        ]
    },
    "goal_evaluator": {
        "class": EvaluateNutritionalContent,
        "role": "Dietary Goal Compliance Checker",
        "purpose": "Judge if nutrient profile supports a specified goal",
        "capabilities": [
            "Accept goal and nutrient string",
            "Return YES/NO compliance verdict",
        ],
    },
}
