"""Single-agent rule-based autonomous behavior."""
from copy import deepcopy
from threading import RLock
from typing import Any

_lock = RLock()
_agent: dict[str, Any] = {'agent_id': 'agent-1', 'name': 'Agent 1', 'sex': 'male', 'profession': 'farmer', 'position': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'hunger': 35, 'thirst': 30, 'energy': 80, 'health': 100, 'inventory': {'food': 0, 'seeds': 3}, 'goal': 'observe_environment', 'status': 'idle'}

def seed_agent() -> dict[str, Any]:
    with _lock:
        return deepcopy(_agent)

def list_agent() -> list[dict[str, Any]]:
    with _lock:
        return [deepcopy(_agent)]

def _nearest(position: dict[str, float], candidates: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not candidates:
        return None
    def distance(item: dict[str, Any]) -> float:
        p = item.get("position", {})
        return sum((float(p.get(k, 0)) - float(position.get(k, 0))) ** 2 for k in ("x", "y", "z"))
    return min(candidates, key=distance)

def _decide(agent: dict[str, Any], environment: dict[str, Any]) -> dict[str, Any]:
    pos = agent["position"]
    water = _nearest(pos, environment.get("water_sources", []))
    food = _nearest(pos, environment.get("food_sources", []))
    fertile = _nearest(pos, environment.get("fertile_land", []))
    threats = environment.get("threats", [])
    if threats:
        return {"action": "move_away_from_threat", "goal": "safety", "target": _nearest(pos, threats)}
    if agent["thirst"] >= 70 and water:
        return {"action": "drink_water", "goal": "satisfy_thirst", "target": water}
    if agent["hunger"] >= 70 and food:
        return {"action": "gather_food", "goal": "satisfy_hunger", "target": food}
    if agent["energy"] <= 20:
        return {"action": "rest", "goal": "recover_energy", "target": None}
    if agent["profession"] == "farmer":
        if fertile and agent["inventory"].get("seeds", 0) > 0:
            return {"action": "plant_seeds", "goal": "produce_food", "target": fertile}
        if food:
            return {"action": "harvest_food", "goal": "collect_food", "target": food}
        return {"action": "explore", "goal": "find_farmable_land", "target": None}
    if agent["profession"] == "gatherer":
        if food:
            return {"action": "gather_food", "goal": "collect_food", "target": food}
        if water:
            return {"action": "move_to_water", "goal": "locate_water", "target": water}
        return {"action": "explore", "goal": "find_resources", "target": None}
    return {"action": "explore", "goal": "inspect_environment", "target": None}

def tick_agent(environment: dict[str, Any]) -> dict[str, Any]:
    with _lock:
        decision = _decide(_agent, environment)
        action = decision["action"]
        _agent["goal"] = decision["goal"]
        _agent["status"] = action
        _agent["hunger"] = min(100, _agent["hunger"] + 2)
        _agent["thirst"] = min(100, _agent["thirst"] + 3)
        _agent["energy"] = min(100, _agent["energy"] + 12) if action == "rest" else max(0, _agent["energy"] - 4)
        if action in ("gather_food", "harvest_food") and decision.get("target"):
            _agent["inventory"]["food"] += 1
            _agent["hunger"] = max(0, _agent["hunger"] - 18)
        if action == "drink_water":
            _agent["thirst"] = max(0, _agent["thirst"] - 25)
        return {"decision": {"agent_id": _agent["agent_id"], **decision}, "agent": deepcopy(_agent),
                "needs": {"hunger": _agent["hunger"], "thirst": _agent["thirst"], "energy": _agent["energy"]}}
