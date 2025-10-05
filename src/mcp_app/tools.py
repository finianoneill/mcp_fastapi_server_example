"""
Tool registry and built-in tool implementations.
"""

from typing import Any, Callable


class ToolRegistry:
    """Registry for MCP tools with built-in implementations"""
    
    def __init__(self):
        self.tools: dict[str, dict] = {}
        self._register_builtin_tools()
    
    def _register_builtin_tools(self):
        """Register built-in tools"""
        
        # Calculator tool
        self.register_tool(
            name="calculate",
            description="Perform mathematical calculations safely",
            input_schema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '2 + 2', '10 * 5')"
                    }
                },
                "required": ["expression"]
            },
            handler=self._calculate
        )
        
        # Time tool
        self.register_tool(
            name="get_time",
            description="Get current server time in specified timezone",
            input_schema={
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "Timezone name (e.g., 'UTC', 'America/New_York')",
                        "default": "UTC"
                    }
                }
            },
            handler=self._get_time
        )
        
        # Echo tool
        self.register_tool(
            name="echo",
            description="Echo back the input message",
            input_schema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Message to echo back"
                    }
                },
                "required": ["message"]
            },
            handler=self._echo
        )
    
    def register_tool(
        self,
        name: str,
        description: str,
        input_schema: dict[str, Any],
        handler: Callable
    ):
        """Register a new tool"""
        self.tools[name] = {
            "name": name,
            "description": description,
            "inputSchema": input_schema,
            "handler": handler
        }
    
    def list_tools(self) -> list[dict]:
        """List all available tools"""
        return [
            {
                "name": tool["name"],
                "description": tool["description"],
                "inputSchema": tool["inputSchema"]
            }
            for tool in self.tools.values()
        ]
    
    async def execute_tool(self, name: str, arguments: dict) -> dict:
        """Execute a tool by name with given arguments"""
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not found")
        
        handler = self.tools[name]["handler"]
        return await handler(**arguments)
    
    # Built-in tool implementations
    
    async def _calculate(self, expression: str) -> dict:
        """Safely calculate mathematical expressions"""
        try:
            # Restricted eval for basic math operations only
            allowed_names = {
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow
            }
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return {
                "success": True,
                "result": result,
                "expression": expression
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "expression": expression
            }
    
    async def _get_time(self, timezone: str = "UTC") -> dict:
        """Get current time in specified timezone"""
        from datetime import datetime
        import pytz
        
        try:
            tz = pytz.timezone(timezone)
            current_time = datetime.now(tz)
            return {
                "success": True,
                "time": current_time.isoformat(),
                "timezone": timezone,
                "formatted": current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timezone": timezone
            }
    
    async def _echo(self, message: str) -> dict:
        """Echo the input message"""
        return {
            "success": True,
            "echo": message,
            "length": len(message)
        }