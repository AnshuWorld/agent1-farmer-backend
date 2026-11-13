
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict

app = FastAPI(
    title="Agent 1 Farmer Backend",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "status": "ok",
        "agent": "farmer",
        "message": "Farmer backend is running"
    }

@app.get("/health")
async def health():
    return {
        "status": "ok"
    }

class ExecuteRequest(BaseModel):
    agent_id: str = "agent1"
    action: str = "observe"
    state: Dict[str, Any] = {}
    environment: Dict[str, Any] = {}
    context: Dict[str, Any] = {}

@app.post("/execute")
async def execute(request: ExecuteRequest):
    state = request.state
    environment = request.environment

    food = state.get("food", 0)
    energy = state.get("energy", 100)
    health = state.get("health", 100)

    # Farmer agent decision logic
    if energy < 20:
        decision = "rest"
    elif food < 20:
        decision = "farm"
    else:
        decision = "observe"

    return {
        "status": "success",
        "agent_id": request.agent_id,
        "role": "farmer",
        "action": decision,
        "reason": (
            "Low energy: resting"
            if decision == "rest"
            else "Food level is low: farming"
            if decision == "farm"
            else "Resources sufficient: observing environment"
        ),
        "state": {
            "food": food,
            "energy": energy,
            "health": health
        },
        "environment": environment
    }
