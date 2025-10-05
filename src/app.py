"""
FastAPI application setup and routing.
"""

import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from src.mcp_app.server import MCPServer
from src.mcp_app.models import MCPRequest


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    print("🚀 MCP Server starting up...")
    yield
    print("🛑 MCP Server shutting down...")


app = FastAPI(
    title="MCP FastAPI Server",
    description="Model Context Protocol server with FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

# Initialize MCP server
mcp_server = MCPServer()


@app.get("/")
async def root():
    """Root endpoint with server information"""
    return {
        "name": "MCP FastAPI Server",
        "version": "1.0.0",
        "protocol": "MCP",
        "endpoints": {
            "websocket": "/mcp",
            "http": "/mcp/http",
            "health": "/health",
            "tools": "/tools"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "protocol": "MCP",
        "version": "1.0.0"
    }


@app.get("/tools")
async def list_tools():
    """List available MCP tools via REST"""
    tools = mcp_server.tool_registry.list_tools()
    return {"tools": tools}


@app.websocket("/mcp")
async def mcp_websocket(websocket: WebSocket):
    """MCP protocol WebSocket endpoint"""
    await websocket.accept()
    print(f"✅ Client connected: {websocket.client}")
    
    try:
        while True:
            # Receive and parse message
            data = await websocket.receive_text()
            
            try:
                request_data = json.loads(data)
                request = MCPRequest(**request_data)
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {str(e)}"
                    }
                }
                await websocket.send_text(json.dumps(error_response))
                continue
            
            # Handle MCP request
            response = await mcp_server.handle_request(request)
            
            # Send response
            await websocket.send_text(response.model_dump_json(exclude_none=True))
            
    except WebSocketDisconnect:
        print(f"❌ Client disconnected: {websocket.client}")
    except Exception as e:
        print(f"⚠️  Error: {str(e)}")
        await websocket.close()


@app.post("/mcp/http")
async def mcp_http(request: MCPRequest):
    """MCP protocol HTTP POST endpoint (alternative to WebSocket)"""
    response = await mcp_server.handle_request(request)
    return JSONResponse(
        content=json.loads(response.model_dump_json(exclude_none=True))
    )