# Enterprise Agentic AI Copilot

## Setup assumptions
- Python 3.11+
- Project root is the repository root
- A virtual environment is created locally (for example `.venv`)
- The vector database and indexed policy documents are expected to exist before any end-to-end retrieval workflow is claimed as working

## Local setup
```bash
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirement.txt
python -m pytest -q scripts/test_agent_tools.py
```

## Dispatching a tool
```python
from app.agent.registry import dispatch_tool

result = dispatch_tool(
    "search_department_policies",
    {
        "question": "What is the annual leave policy?",
        "department": "hr",
        "top_k": 3,
    },
)

print(result)
```

The dispatch layer is intentionally allowlisted. It accepts only the registered tool names and validates incoming arguments before execution. Validation failures and execution failures are returned as structured error payloads, not as arbitrary dynamic calls.

## Current limitations
- Retrieval depends on the existing vector-store setup and indexed policy documents.
- No claim of successful end-to-end RAG retrieval is made unless the documents have been indexed and tested in the local environment.
- The allowlist currently includes only `search_department_policies`.

## GitHub workflow
```bash
git checkout -b feature/your-change
git add app/agent/tools.py app/agent/registry.py scripts/test_agent_tools.py .gitignore README.md
git commit -m "Add policy-search tool registry and tests"
git push origin feature/your-change
```
Then open a pull request in GitHub and include a short summary of the validation performed.

