from fastapi import FastAPI
from pydantic import BaseModel
from graph import build_agent_graph
from State import State
from tool_registry import tool_registry
api = FastAPI(title="Linux Agent API", version="1.0")

# Build agent graph once
agent = build_agent_graph()
tool_registry = tool_registry

# Request model for API
class QueryRequest(BaseModel):
    query: str

@api.get('/')
def home():
    return "Hello ! This is version 1 of the application."



@api.post("/run-query")
def run_query(request: QueryRequest):
    """
    Run a natural language query against the Linux agent.
    """

    # Initialize state
    initial_state = State(
        query=request.query,
        tool_registry=tool_registry,
        tool="",
        result=""
    )

    # Run graph
    result_state = agent.invoke(initial_state)
    raw_output = result_state['result']
    formatted_output = f"```\n{raw_output}\n```"
    return {"answer": formatted_output}

