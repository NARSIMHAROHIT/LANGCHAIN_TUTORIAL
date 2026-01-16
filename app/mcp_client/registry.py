from langchain_mcp import MCPClient


def load_mcp_tools():
    """
    Connects to the MCP server and returns MCP-provided tools
    without redefining or duplicating them.
    """
    client = MCPClient(
        server_url="http://127.0.0.1:8000"
    )

    return client.get_tools()
