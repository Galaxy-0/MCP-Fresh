import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import mcp.types as types # 导入 MCP 类型

async def main():
    server_command = "python"
    server_args = ["caculator_server.py"] # 确保 calculator_server.py 在 Python 路径上或在同一目录

    server_params = StdioServerParameters(
        command=server_command,
        args=server_args,
    )

    print(f"启动服务器: {server_command} {' '.join(server_args)}")

    async with stdio_client(server_params) as (read_stream, write_stream):
        print("stdio_client 已连接")
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
                print(f"add(10, 5) 的结果: {add_result}") # add_result 就是工具函数的返回值
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
                # 注意: read_resource 返回一个元组 (content, mime_type)
                # content 已经是解码后的字符串，因为我们知道 greeting_resource 返回 str
                content, mime_type = await session.read_resource("greeting://World")
                print(f"读取 greeting://World 资源: 内容='{content}', MIME类型='{mime_type}'")

                content_alice, mime_type_alice = await session.read_resource("greeting://Alice")
                print(f"读取 greeting://Alice 资源: 内容='{content_alice}', MIME类型='{mime_type_alice}'")
            except Exception as e:
                print(f"读取 'greeting' 资源失败: {e}")
            
            # 6. 列出资源 (FastMCP 可能不会显式列出通过装饰器定义的资源，取决于其实现)
            # 但 MCP 协议本身支持列出资源，如果服务器实现了 list_resources 处理器
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