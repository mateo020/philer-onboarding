"""
Simple FastAPI Chatbot Frontend for Recipe Creation System

This module provides a web-based chat interface to interact with the
Recipe Creation and Evaluation workflow.
"""

from workflow import run_workflow
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title="Recipe Creation Chatbot",
              description="A simple chatbot for creating and evaluating recipes")

# Setup templates (we'll create the HTML template next)
templates = Jinja2Templates(directory=os.path.join(
    os.path.dirname(__file__), "templates"))

# Initialize the workflow
try:
    workflow_ready = True
except Exception as e:
    print(f"Warning: Could not initialize workflow: {e}")
    print("Make sure you have set up your .env file with OPENAI_API_KEY")
    workflow_ready = False


class ChatMessage(BaseModel):
    """Request model for chat messages."""
    message: str


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main chat interface."""
    return templates.TemplateResponse("chat.html", {"request": request})


@app.post("/chat")
async def chat(chat_message: ChatMessage):
    """
    Process a chat message and return the recipe workflow response.

    Args:
        chat_message: User's message

    Returns:
        JSON response with the workflow result
    """
    if not workflow_ready:
        return JSONResponse({
            "response": "Sorry, the recipe system is not properly configured. Please check your environment variables.",
            "error": True
        })
    else:
        try:
            # Run the workflow with the user's message
            result = run_workflow(chat_message.message)

            return JSONResponse({
                "response": result,
                "error": False
            })

        except Exception as e:
            return JSONResponse({
                "response": f"Sorry, I encountered an error: {str(e)}",
                "error": True
            })


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "workflow_ready": workflow_ready}


if __name__ == "__main__":
    print("🚀 Starting Recipe Creation Chatbot Server...")
    print("📱 Open your browser to: http://localhost:8000")
    print("🛑 Press Ctrl+C to stop the server")

    uvicorn.run(
        "frontend:app",
        host="localhost",
        port=8000,
        reload=True,
        log_level="info"
    )
