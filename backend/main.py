from graph import build_agent_graph
from State import State

if __name__ == "__main__":

    

    # Example query
    tool_registry = {
        "disk_check": "/home/ubuntu/Tools/disk_check.sh",
        "disk_cleanup" : "/home/ubuntu/Tools/disk_cleanup.sh"
    }
    user_query = "Please check the logs on EC2 server"
    initial_state = State(
        query=user_query,
        tool_registry=tool_registry,
        tool="",
        result=""
    )
    
    agent = build_agent_graph()
    
    result = agent.invoke(initial_state)
    
    print("Results using the tool: ", result['tool'], "\n", result['result'])
