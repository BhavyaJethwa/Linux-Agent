from typing import TypedDict, Dict

class State(TypedDict):
    """
    Represents the state of the router node.
    
    Attributes:
        query: The user's input query.
        tool: The name of the tool selected by the LLM (optional).
    """
    query: str
    tool_registry: Dict[str,str]
    tool : str
    result : str