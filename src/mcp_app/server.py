"""
Core MCP server implementation.
"""

from src.mcp_app.models import MCPRequest, MCPResponse
from src.mcp_app.tools import ToolRegistry


class MCPServer:
    """MCP Protocol Server"""
    
    def __init__(self):
        self.tool_registry = ToolRegistry()
        self.capabilities = {
            "tools": {}
        }
        self.server_info = {
            "name": "mcp-fastapi-server",
            "version": "1.0.0"
        }
    
    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle MCP protocol request"""
        try:
            if request.method == "initialize":
                return self._initialize(request)
            elif request.method == "tools/list":
                return self._list_tools(request)
            elif request.method == "tools/call":
                return await self._call_tool(request)
            else:
                return MCPResponse(
                    id=request.id,
                    error={
                        "code": -32601,
                        "message": f"Method not found: {request.method}"
                    }
                )
        except Exception as e:
            return MCPResponse(
                id=request.id,
                error={
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            )
    
    def _initialize(self, request: MCPRequest) -> MCPResponse:
        """Handle initialize request"""
        return MCPResponse(
            id=request.id,
            result={
                "protocolVersion": "2024-11-05",
                "capabilities": self.capabilities,
                "serverInfo": self.server_info
            }
        )
    
    def _list_tools(self, request: MCPRequest) -> MCPResponse:
        """Handle tools/list request"""
        tools = self.tool_registry.list_tools()
        return MCPResponse(
            id=request.id,
            result={"tools": tools}
        )
    
    async def _call_tool(self, request: MCPRequest) -> MCPResponse:
        """Handle tools/call request"""
        import json
        
        params = request.params or {}
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if not tool_name:
            return MCPResponse(
                id=request.id,
                error={
                    "code": -32602,
                    "message": "Missing tool name"
                }
            )
        
        try:
            result = await self.tool_registry.execute_tool(tool_name, arguments)
            return MCPResponse(
                id=request.id,
                result={
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            )
        except ValueError as e:
            return MCPResponse(
                id=request.id,
                error={
                    "code": -32602,
                    "message": str(e)
                }
            )