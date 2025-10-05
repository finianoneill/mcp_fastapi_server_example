# MCP FastAPI Server

A production-ready Model Context Protocol (MCP) server built with FastAPI.

## Directory Structure

```
.
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── README.md                 # Documentation
└── src/
    ├── __init__.py
    ├── app.py                # FastAPI application
    └── mcp_app/
        ├── __init__.py
        ├── models.py         # Pydantic models
        ├── server.py         # MCP server logic
        └── tools.py          # Tool registry & implementations
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Server runs on `http://localhost:8000`

## Endpoints

- `GET /` - Server information
- `GET /health` - Health check
- `GET /tools` - List available tools
- `WS /mcp` - MCP WebSocket endpoint
- `POST /mcp/http` - MCP HTTP endpoint

## Built-in Tools

1. **calculate** - Mathematical calculations
2. **get_time** - Current time in timezone
3. **echo** - Echo messages

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.