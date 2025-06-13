#!/usr/bin/env python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("SimpleCalculator")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract one number from another."""
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b

# Run the server
if __name__ == "__main__":
    mcp.run(transport="stdio")
