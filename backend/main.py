"""
PromptGuard AI - Main Backend API
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from backend.prompt_engine import (
    validate_prompt,
    improve_prompt,
    generate_response
)

from backend.evaluator import evaluate_response

from backend.database import (
    create_table,
    save_prompt,
    get_all_history
)


# Create FastAPI application
app = FastAPI(
    title="PromptGuard AI",
    description="Intelligent AI Prompt Testing and Evaluation Platform",
    version="1.0.0"
)


# Create database table
create_table()


# Request model
class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    expected_keywords: list[str] = Field(default_factory=list)


# Home API
@app.get("/")
def home():
    return {
        "message": "Welcome to PromptGuard AI API",
        "status": "Running"
    }


# Test prompt API
@app.post("/test-prompt")
def test_prompt(request: PromptRequest):

    try:
        original_prompt = request.prompt

        if not validate_prompt(original_prompt):
            raise ValueError("Prompt cannot be empty.")

        improved = improve_prompt(original_prompt)

        response = generate_response(improved)

        evaluation = evaluate_response(
            response,
            request.expected_keywords
        )

        save_prompt(
            original_prompt,
            improved,
            response,
            evaluation["score"],
            evaluation["status"]
        )

        return {
            "original_prompt": original_prompt,
            "improved_prompt": improved,
            "ai_response": response,
            "evaluation": evaluation
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# Testing history API
@app.get("/history")
def get_history():

    try:
        history = get_all_history()

        return {
            "total_records": len(history),
            "history": history
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )