# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server project called "MCP-Fresh" that demonstrates different MCP server implementations and client interactions. The project showcases two main MCP server architectures:

1. **FastMCP servers** - HTTP-based servers using `mcp.server.fastmcp.FastMCP`
2. **Standard MCP servers** - stdio-based servers using `mcp.server.Server`

## Common Commands

```bash
# Install dependencies
uv install

# Run FastMCP calculator server (HTTP)
python caculator_server.py

# Run standard MCP calculator server (stdio)
python wearther_server.py

# Test FastMCP server with HTTP client
python calculator_http_client.py

# Test standard MCP server with stdio client  
python calculator_client.py

# Debug and explore MCP capabilities
python debug_fastmcp.py
python find_mcp_examples.py
```

## Architecture

### Server Types

**FastMCP Servers** (`caculator_server.py`):
- HTTP-based servers that run as FastAPI applications
- Use `@mcp.tool()` decorator for tools and `@mcp.resource()` for resources
- Accessible via HTTP endpoints (default: `http://127.0.0.1:8000/mcp`)
- Run with uvicorn server

**Standard MCP Servers** (`wearther_server.py`):
- stdio-based servers using the traditional MCP protocol
- Use `@server.call_tool()` decorator for tools
- Communicate via stdin/stdout streams

### Client Types

**HTTP Clients** (`calculator_http_client.py`):
- Connect to FastMCP servers via `streamablehttp_client`
- Use HTTP transport for MCP protocol communication

**Stdio Clients** (`calculator_client.py`):
- Connect to standard MCP servers via `stdio_client` 
- Use stdio transport with `StdioServerParameters`

### Core MCP Concepts

- **Tools**: Functions that can be called by MCP clients (calculator operations)
- **Resources**: Data that can be read by clients (greeting messages with URI patterns)
- **Sessions**: Manage client-server communication and capabilities

Both server types implement the same calculator tools (add, subtract, multiply) demonstrating protocol compatibility across transport layers.