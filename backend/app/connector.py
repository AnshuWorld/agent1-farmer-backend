import httpx
from .models import AgentRecord

TIMEOUT = httpx.Timeout(8.0, connect=3.0)

async def test_agent(record: AgentRecord, api_key: str | None = None) -> dict:
    # Development-only URL handling. Add SSRF restrictions before production use.
    url = f"{record.agent_url}/health"
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    async with httpx.AsyncClient(timeout=TIMEOUT, follow_redirects=False) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return {"reachable": True, "http_status": response.status_code,
                "response": response.json() if response.content else {}}

async def execute_agent(record: AgentRecord, task: str, context: dict, api_key: str | None = None) -> dict:
    url = f"{record.agent_url}/execute"
    payload = {"task_id": "sim-task", "task": task, "context": context}
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    # API keys remain in backend memory and are never included in API responses.
    async with httpx.AsyncClient(timeout=TIMEOUT, follow_redirects=False) as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
