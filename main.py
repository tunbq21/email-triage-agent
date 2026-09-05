"""
Email Triage Agent - Web App Entry Point
Chay server: uv run python main.py
"""
import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from graph.builder import build_graph
from tools.gmail_api import fetch_unread_emails

load_dotenv()

app = FastAPI(title="Email Triage Agent API")

# Khoi tao AI Graph
workflow_app = build_graph()

# API Endpoints
@app.get("/api/triage")
async def run_triage():
    """Kich hoat luong doc email va phan loai."""
    try:
        emails = fetch_unread_emails(max_results=5)
    except FileNotFoundError as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    if not emails:
        return {"emails": []}

    results = []
    for email in emails:
        # Chay luong LangGraph cho tung email
        final_state = workflow_app.invoke({"current_email": email})
        
        # Pydantic models khong tu serializable trong FastAPI tra ve dict neu chua cau hinh
        # Nen minh se parse sang dict thu cong
        classification = final_state.get("classification")
        action_taken = final_state.get("action_taken", "unknown")
        
        results.append({
            "id": email.id,
            "sender": email.sender,
            "subject": email.subject,
            "date": email.date,
            "body": email.body[:200] + "..." if len(email.body) > 200 else email.body,
            "classification": {
                "category": classification.category if classification else "UNKNOWN",
                "priority": classification.priority if classification else "P3",
                "confidence": classification.confidence if classification else 0.0
            },
            "action": action_taken
        })
        
    return {"emails": results}

# Mount static files de phuc vu UI
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    print("Khoi tao Email Triage Agent Web Server tai http://localhost:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
