from pydantic import BaseModel


class MCPToolInput(BaseModel):
    query: str


class MCPToolOutput(BaseModel):
    result: str
