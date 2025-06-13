import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def main():
    print("连接到 MCP 服务器: http://127.0.0.1:8000/mcp")
    
    # 使用 HTTP 客户端连接到 FastMCP 服务器
    # 第三个返回值是关闭函数，我们不需要使用
    async with streamablehttp_client("http://127.0.0.1:8000/mcp") as (read_stream, write_stream, _):
        print("HTTP 客户端已连接")
        
        # 创建 MCP 会话
        async with ClientSession(read_stream, write_stream) as session:
            print("ClientSession 已创建，正在初始化...")
            try:
                init_response = await session.initialize()
                print(f"初始化成功: {init_response.server_name} v{init_response.server_version}")
                print(f"服务器能力: {init_response.capabilities}")
            except Exception as e:
                print(f"初始化失败: {e}")
                return

            # 1. 列出工具
            print("\n--- 列出工具 ---")
            tools = await session.list_tools()
            print("可用的工具:")
            for tool in tools:
                print(f"  - 名称: {tool.name}, 描述: {tool.description}")
                if tool.arguments:
                    print("    参数:")
                    for arg in tool.arguments:
                        print(f"      - {arg.name} ({'必选' if arg.required else '可选'}): {arg.description}")

            # 2. 调用 'add' 工具
            print("\n--- 调用 'add' 工具 ---")
            try:
                add_result = await session.call_tool("add", arguments={"a": 10, "b": 5})
                print(f"add(10, 5) 的结果: {add_result}")
            except Exception as e:
                print(f"调用 'add' 工具失败: {e}")

            # 3. 调用 'subtract' 工具
            print("\n--- 调用 'subtract' 工具 ---")
            try:
                subtract_result = await session.call_tool("subtract", arguments={"a": 10, "b": 5})
                print(f"subtract(10, 5) 的结果: {subtract_result}")
            except Exception as e:
                print(f"调用 'subtract' 工具失败: {e}")
            
            # 4. 调用 'multiply' 工具
            print("\n--- 调用 'multiply' 工具 ---")
            try:
                multiply_result = await session.call_tool("multiply", arguments={"a": 10, "b": 5})
                print(f"multiply(10, 5) 的结果: {multiply_result}")
            except Exception as e:
                print(f"调用 'multiply' 工具失败: {e}")

            # 5. 读取 'greeting' 资源
            print("\n--- 读取 'greeting' 资源 ---")
            try:
                content, mime_type = await session.read_resource("greeting://World")
                print(f"读取 greeting://World 资源: 内容='{content}', MIME类型='{mime_type}'")

                content_alice, mime_type_alice = await session.read_resource("greeting://Alice")
                print(f"读取 greeting://Alice 资源: 内容='{content_alice}', MIME类型='{mime_type_alice}'")
            except Exception as e:
                print(f"读取 'greeting' 资源失败: {e}")
            
            # 6. 列出资源
            print("\n--- 列出资源 ---")
            try:
                resources = await session.list_resources()
                print("可用的资源:")
                if resources:
                    for resource in resources:
                        print(f"  - URI: {resource.uri}, 描述: {resource.description}")
                else:
                    print("  (服务器未提供资源列表或 FastMCP 未自动注册)")
            except Exception as e:
                print(f"列出资源失败: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 