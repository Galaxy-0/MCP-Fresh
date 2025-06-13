#!/usr/bin/env python3
"""
最小版本的CodeInsight客户端
"""
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_minimal():
    """测试最小版本服务器"""
    server_params = StdioServerParameters(
        command="python3",
        args=["minimal_code_server.py"],
    )
    
    print("🚀 连接到MinimalCodeInsight服务器...")
    print("=" * 50)
    
    try:
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                # 初始化
                init_result = await session.initialize()
                print(f"✅ 服务器: {init_result.serverInfo.name}")
                
                # 列出工具
                tools_result = await session.list_tools()
                tools = tools_result.tools
                print(f"🛠️  工具数量: {len(tools)}")
                for i, tool in enumerate(tools, 1):
                    print(f"  {i}. {tool.name} - {tool.description}")
                print()
                
                # 测试count_lines
                print("📊 测试行数统计:")
                call_result = await session.call_tool("count_lines", arguments={"file_path": "caculator_server.py"})
                result = call_result.content[0].text if call_result.content else {}
                # 解析JSON结果
                import json
                try:
                    result = json.loads(result)
                except:
                    print(f"结果: {result}")
                    result = {}
                
                if "error" in result:
                    print(f"❌ {result['error']}")
                else:
                    print(f"✅ 文件: {result.get('file_path', 'N/A')}")
                    print(f"✅ 总行数: {result.get('total_lines', 0)}")
                    print(f"✅ 非空行数: {result.get('non_empty_lines', 0)}")
                    print(f"✅ 代码行数: {result.get('code_lines', 0)}")
                    print(f"✅ 注释行数: {result.get('comment_lines', 0)}")
                print()
                
                # 测试analyze_python
                print("🔍 测试Python文件分析:")
                call_result = await session.call_tool("analyze_python", arguments={"file_path": "caculator_server.py"})
                result_text = call_result.content[0].text if call_result.content else "{}"
                try:
                    result = json.loads(result_text)
                except:
                    print(f"结果: {result_text}")
                    result = {}
                
                if "error" in result:
                    print(f"❌ {result['error']}")
                elif "syntax_error" in result:
                    print(f"⚠️ 语法错误: {result['syntax_error']}")
                else:
                    print(f"✅ 文件: {result.get('file_path', 'N/A')}")
                    print(f"✅ 总行数: {result.get('total_lines', 0)}")
                    print(f"✅ 函数数量: {result.get('functions_count', 0)}")
                    print(f"✅ 类数量: {result.get('classes_count', 0)}")
                    if result.get('functions'):
                        print("⚙️ 函数列表:")
                        for func in result['functions'][:3]:
                            print(f"  - {func['name']} (第{func['line']}行, {func['args']}个参数)")
                print()
                
                # 测试list_python_files
                print("📂 测试Python文件列表:")
                call_result = await session.call_tool("list_python_files", arguments={"directory": "."})
                result_text = call_result.content[0].text if call_result.content else "{}"
                try:
                    result = json.loads(result_text)
                except:
                    print(f"结果: {result_text}")
                    result = {}
                
                if "error" in result:
                    print(f"❌ {result['error']}")
                else:
                    print(f"✅ 目录: {result.get('directory', 'N/A')}")
                    print(f"✅ Python文件数量: {result.get('count', 0)}")
                    print("📄 文件列表:")
                    for file in result.get('python_files', [])[:5]:
                        print(f"  - {file}")
                print()
                
                print("🎉 所有测试完成!")
                print("=" * 50)
    
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🤖 MinimalCodeInsight测试客户端")
    print()
    asyncio.run(test_minimal())