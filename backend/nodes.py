import os
import paramiko
from io import StringIO
from langchain_openai import ChatOpenAI
from State import State
from dotenv import load_dotenv
from tool_registry import tool_registry
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

# --- EC2 Connection Details ---
EC2_HOST = "ec2-18-234-82-251.compute-1.amazonaws.com"
EC2_USER = "ubuntu"
PEM_CONTENT = os.environ["PEM_CONTENT"]


def run_tool(tool_name: str) -> str:
    """
    Executes a whitelisted tool on the EC2 server via SSH and returns the output.
    """
    if tool_name not in tool_registry:
        return f"Unknown tool: {tool_name}"

    remote_script = tool_registry[tool_name]

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key = paramiko.RSAKey.from_private_key(StringIO(PEM_CONTENT))
    try:
        ssh.connect(EC2_HOST, username=EC2_USER, pkey=key)
        stdin, stdout, stderr = ssh.exec_command(f"bash {remote_script}")

        output = stdout.read().decode()
        error = stderr.read().decode()

        ssh.close()

        if error:
            return f"Error:\n{error.strip()}"
        return output.strip()

    except Exception as e:
        return f"SSH connection error: {str(e)}"
    finally:
        ssh.close()
    
    
def router_node(state: State):
    """LLM decides which tool to run based on user query."""
    query = state["query"]
    tool_dict = state["tool_registry"]

    prompt = f"""
    You are an assistant with access to the following tools:
    {tool_dict}
    Based on the below query choose an appropriate tool.
    User query: "{query}"

    Reply ONLY with the tool name (e.g., disk_check) or 'none'.
    eg : "disk_check": "/home/ubuntu/Tools/disk_check.sh" should return the key "disk_check".
    Reply ONLY with the tool name (e.g., disk_check) or 'none'.
    """
    choice = llm.invoke(prompt).content.strip().lower()
    state['tool'] = choice
    return state

def tool_node(state: State):
    """Execute the chosen tool."""
    tool = state['tool']
    if tool == "none":
        return {"result": "No tool execution required."}
    state['result'] = run_tool(tool)
    return state

def final_node(state):
    return state



