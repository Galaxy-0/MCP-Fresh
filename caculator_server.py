from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calculator")

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

@mcp.resource("greeting://{name}")
def greeting_resource(name: str) -> str:
    """Provide a greeting for a specified name."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    import uvicorn
    print("启动计算器服务器，使用地址 http://127.0.0.1:8000/")
    print("FastMCP 默认在 '/mcp' 路径上提供服务，可以通过 http://127.0.0.1:8000/mcp 访问")
    # 使用 uvicorn 以标准 FastAPI 应用方式运行
    uvicorn.run(mcp, host="127.0.0.1", port=8000)


    
    