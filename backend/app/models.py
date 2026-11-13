from typing import Any, Literal
from pydantic import BaseModel, Field, HttpUrl

AgentType = Literal[
    "civil_engineer", "mechanical_engineer", "electrical_engineer",
    "software_engineer", "chemical_engineer", "biologist", "custom"
]

class ConnectAgentRequest(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    agent_url: HttpUrl
    agent_type: AgentType = "custom"
    framework: str = Field(default="custom", max_length=40)
    api_key: str | None = Field(default=None, max_length=500)

class AgentRecord(BaseModel):
    agent_id: str
    name: str
    agent_url: str
    agent_type: AgentType
    framework: str
    connected: bool = True
    status: str = "idle"
    position: dict[str, float] = Field(default_factory=lambda: {"x": 0, "y": 0, "z": 0})

class ExecuteTaskRequest(BaseModel):
    task: str = Field(min_length=1, max_length=2000)
    context: dict[str, Any] = Field(default_factory=dict)
