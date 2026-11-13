from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .models import ConnectAgentRequest, ExecuteTaskRequest
from .registry import registry
from .connector import test_agent, execute_agent
from .world_catalog import RESOURCE_DEPOSITS, ANIMALS, collect_milk
from .autonomous_agents import seed_agent, list_agent, tick_agent

app = FastAPI(title="earth-agent1-farmer-api", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_origin_regex=r"https://.*\.onrender\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/world/resources")
def world_resources():
    """Return the island's current prototype resource catalog and deposit quantities."""
    return RESOURCE_DEPOSITS

@app.get("/api/world/animals")
def world_animals():
    """Return the current prototype animal population catalog."""
    return ANIMALS

@app.post("/api/world/milk/collect")
def collect_cow_milk(hours: float = 1.0):
    if hours <= 0 or hours > 12:
        raise HTTPException(400, "hours must be greater than 0 and at most 12")
    return collect_milk(hours)

@app.post("/api/autonomous/agents/seed")
def seed_autonomous_pair():
    """Create the initial pair: Agent 1 male Farmer, Agent 2 female Gatherer."""
    return {"created": True, "agent": seed_agent()}

@app.get("/api/autonomous/agents")
def get_autonomous_agents():
    return list_agent()

@app.post("/api/autonomous/tick")
def autonomous_tick(environment: dict):
    """Send an environment snapshot; each starter agent senses and selects an action."""
    return tick_agent(environment)

@app.get("/api/agents")
def list_agents():
    return [agent.model_dump() for agent in registry.list()]

@app.post("/api/agents/connect")
def connect_agent(request: ConnectAgentRequest):
    # Registers the endpoint. Test reachability separately via /test.
    record = registry.add(request)
    return {"connected": True, "agent": record.model_dump()}

@app.post("/api/agents/{agent_id}/test")
async def test_connection(agent_id: str):
    record = registry.get(agent_id)
    if not record:
        raise HTTPException(404, "Agent not found")
    try:
        result = await test_agent(record, registry.api_key(agent_id))
        return {"agent_id": agent_id, **result}
    except Exception as exc:
        raise HTTPException(502, f"Agent connection failed: {type(exc).__name__}")

@app.post("/api/agents/{agent_id}/execute")
async def run_task(agent_id: str, request: ExecuteTaskRequest):
    record = registry.get(agent_id)
    if not record:
        raise HTTPException(404, "Agent not found")
    try:
        result = await execute_agent(record, request.task, request.context, registry.api_key(agent_id))
        return {"agent_id": agent_id, "result": result}
    except Exception as exc:
        raise HTTPException(502, f"Agent task failed: {type(exc).__name__}")

@app.delete("/api/agents/{agent_id}")
def delete_agent(agent_id: str):
    if not registry.remove(agent_id):
        raise HTTPException(404, "Agent not found")
    return {"removed": True, "agent_id": agent_id}

@app.websocket("/ws/world")
async def world_socket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json({
                "agents": [agent.model_dump() for agent in registry.list()],
                "island": {"time": "day", "weather": "clear"}
            })
            await websocket.receive_text()  # client sends "tick" to request next update
    except WebSocketDisconnect:
        pass
