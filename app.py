from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import (
    SystemMessage, HumanMessage, AIMessage
)
load_dotenv()
app = FastAPI()

# Connect to local Qwen3
llm = init_chat_model(
    model="openai/gpt-oss-20b",
    model_provider="groq",
    temperature=0,
)

# Define request structure
class ChatRequest(BaseModel):
    message: str
    history: list[dict[str, str]] = []

# Chat API endpoint
@app.post("/api/chat")
def chat(request: ChatRequest):

    messages = [
        SystemMessage(
            content="Your name is Nova. Give answer in one line, dont think too much"
        )
    ]

    # Restore previous conversation
    for item in request.history:
        if item["role"] == "user":
            messages.append(
                HumanMessage(content=item["content"])
            )
        elif item["role"] == "assistant":
            messages.append(
                AIMessage(content=item["content"])
            )

    # Add current question
    messages.append(
        HumanMessage(content=request.message)
    )

    # Generate AI response
    response = llm.invoke(messages)

    return {"reply": response.content}


# Serve frontend
# Get the current project directory
BASE_DIR = Path(__file__).resolve().parent

# Serve HTML
@app.get("/")
def home():
    return FileResponse(BASE_DIR / "index.html")

# Serve CSS
@app.get("/style.css")
def css():
    return FileResponse(BASE_DIR / "style.css")
FastAPI
