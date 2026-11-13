# Agent 1 — Farmer standalone backend

This is an independent FastAPI Render service for **Agent 1** (male, farmer).
It exposes `/health`, `/api/autonomous/agents/seed`, `/api/autonomous/agents`, and `POST /api/autonomous/tick`.
The tick request passes an environment snapshot containing optional `water_sources`, `food_sources`, `fertile_land`, and `threats` arrays.
The agent selects a bounded rule-based action from the snapshot and its needs. Actual world physics/resource depletion must be handled by the simulation host.

## Render deploy
Deploy this folder as a Render Blueprint from `render.yaml`, or create a Python web service with root directory `backend`, build `pip install -r requirements.txt`, start `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
