from langgraph.graph import StateGraph, END
from nodes import router_node, tool_node, final_node
from State import State

def build_agent_graph() -> StateGraph:
    graph = StateGraph(State)
    graph.add_node("router", router_node)
    graph.add_node("tool_runner", tool_node)
    graph.add_node("final", final_node)

    graph.set_entry_point("router")
    graph.add_edge("router", "tool_runner")
    graph.add_edge("tool_runner", "final")
    graph.add_edge("final", END)
    graph = graph.compile()

    return graph
