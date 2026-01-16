import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from app.mcp.metadata import MCP_METADATA
from app.mcp.schemas import MCPToolInput, MCPToolOutput

# 🔁 IMPORT YOUR EXISTING AGENT (NO CHANGES)
from app.agents.basicagent import agent, Context, config

load_dotenv()
os.environ["USER_AGENT"] = "linux-doc-agent/1.0"

app = FastAPI(
    title=MCP_METADATA["name"],
    version=MCP_METADATA["version"],
    description=MCP_METADATA["description"],
)


# ---------------------------
# MCP DISCOVERY ENDPOINT
# ---------------------------
@app.get("/mcp")
def mcp_info():
    return MCP_METADATA


# ---------------------------
# MCP TOOL LIST
# ---------------------------
@app.get("/mcp/tools")
def list_tools():
    return {
        "tools": [
            {
                "name": "linux.docs.agent",
                "description": (
                    "Query a Linux documentation agent that reads official "
                    "man7, systemd, and nginx documentation and returns "
                    "a documentation-grounded explanation."
                ),
                "input_schema": MCPToolInput.model_json_schema(),
                "output_schema": MCPToolOutput.model_json_schema(),
            }
        ]
    }


# ---------------------------
# MCP TOOL EXECUTION
# ---------------------------
@app.post("/mcp/tools/linux.docs.agent", response_model=MCPToolOutput)
def run_linux_docs_agent(payload: MCPToolInput):
    try:
        response = agent.invoke(
            {"messages": [{"role": "user", "content": payload.query}]},
            config=config,
            context=Context(user_id="mcp-client"),
        )

        final_message = response["messages"][-1].content
        return MCPToolOutput(result=final_message)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
