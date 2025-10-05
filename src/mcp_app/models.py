"""
Pydantic models for MCP protocol requests and responses.
"""

from typing import Any, Optional
from pydantic import BaseModel, Field


class MCPRequest(BaseModel):
    """MCP JSON-RPC request model"""
    jsonrpc: str = "2.0"
    id: Optional[int | str] = None
    method: str
    params: Optional[dict[str, Any]] = None


class MCPResponse(BaseModel):
    """MCP JSON-RPC response model"""
    jsonrpc: str = "2.0"
    id: Optional[int | str] = None
    result: Optional[dict[str, Any]] = None
    error: Optional[dict[str, Any]] = None


class Tool(BaseModel):
    """Tool definition model"""
    name: str
    description: str
    inputSchema: dict[str, Any] = Field(alias="input_schema")


class ServerInfo(BaseModel):
    """Server information model"""
    name: str
    version: str


class ServerCapabilities(BaseModel):
    """Server capabilities model"""
    tools: dict[str, Any] = {}