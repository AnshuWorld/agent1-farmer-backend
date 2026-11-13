from uuid import uuid4
from .models import AgentRecord, ConnectAgentRequest

class AgentRegistry:
    def __init__(self):
        self._agents: dict[str, AgentRecord] = {}
        self._api_keys: dict[str, str] = {}

    def add(self, request: ConnectAgentRequest) -> AgentRecord:
        agent_id = f"{request.agent_type}_{uuid4().hex[:8]}"
        record = AgentRecord(
            agent_id=agent_id,
            name=request.name,
            agent_url=str(request.agent_url).rstrip("/"),
            agent_type=request.agent_type,
            framework=request.framework,
        )
        self._agents[agent_id] = record
        if request.api_key:
            self._api_keys[agent_id] = request.api_key
        return record

    def list(self) -> list[AgentRecord]:
        return list(self._agents.values())

    def get(self, agent_id: str) -> AgentRecord | None:
        return self._agents.get(agent_id)

    def api_key(self, agent_id: str) -> str | None:
        return self._api_keys.get(agent_id)

    def remove(self, agent_id: str) -> bool:
        self._api_keys.pop(agent_id, None)
        return self._agents.pop(agent_id, None) is not None

registry = AgentRegistry()
