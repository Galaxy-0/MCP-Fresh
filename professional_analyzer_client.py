#!/usr/bin/env python3
"""
专业级代码分析器测试客户端
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_professional_analyzer():
    """测试专业级代码分析器"""
    server_params = StdioServerParameters(
        command="/Users/yuanquan/code_project/GalaxyAI/MCP-Fresh/.venv/bin/python3",
        args=["professional_code_analyzer.py"],
    )
    
    print("🚀 连接到专业级代码分析器...")
    print("=" * 70)
    
    try:
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                # 初始化
                init_result = await session.initialize()
                print(f"✅ 服务器: {init_result.serverInfo.name}")
                
                # 列出工具
                tools_result = await session.list_tools()
                tools = tools_result.tools
                print(f"🛠️  可用工具: {len(tools)} 个")
                for i, tool in enumerate(tools, 1):
                    print(f"  {i}. {tool.name} - {tool.description}")
                print()
                
                # 1. 测试代码智能分析
                print("🔍 测试智能代码分析:")
                print("-" * 50)
                call_result = await session.call_tool("analyze_code_intelligence", 
                                                    arguments={"file_path": "minimal_code_server.py"})
                result_text = call_result.content[0].text if call_result.content else "{}"
                try:
                    analysis = json.loads(result_text)
                    print(f"📊 质量评分: {analysis.get('overall_quality_score', 0)}/100")
                    print(f"📈 问题统计:")
                    summary = analysis.get('analysis_summary', {})
                    print(f"  - 严重问题: {summary.get('critical_issues', 0)}")
                    print(f"  - 警告: {summary.get('warnings', 0)}")
                    print(f"  - 建议: {summary.get('suggestions', 0)}")
                    
                    # 显示函数指标
                    functions = analysis.get('function_metrics', [])
                    if functions:
                        print(f"⚙️  函数分析:")
                        for func in functions[:3]:
                            print(f"  - {func['name']}(): 复杂度 {func['complexity']}, {func['parameter_count']} 参数")
                except json.JSONDecodeError:
                    print(f"结果: {result_text[:200]}...")
                print()
                
                # 2. 测试项目上下文分析
                print("🏗️  测试项目上下文分析:")
                print("-" * 50)
                call_result = await session.call_tool("analyze_project_context", arguments={})
                result_text = call_result.content[0].text if call_result.content else "{}"
                try:
                    context = json.loads(result_text)
                    print(f"📁 项目根目录: {context.get('project_root', 'N/A')}")
                    print(f"🏛️  架构模式: {context.get('architecture_pattern', 'N/A')}")
                    
                    tech_stack = context.get('tech_stack', {})
                    print(f"🔧 技术栈:")
                    print(f"  - 主语言: {tech_stack.get('primary_language', 'N/A')}")
                    print(f"  - 依赖数量: {len(tech_stack.get('dependencies', []))}")
                    
                    tech_debt = context.get('tech_debt_assessment', {})
                    print(f"💸 技术债务等级: {tech_debt.get('debt_level', 'N/A')}")
                    
                    recommendations = context.get('recommendations', [])
                    if recommendations:
                        print("💡 项目建议:")
                        for rec in recommendations[:3]:
                            print(f"  - {rec}")
                            
                except json.JSONDecodeError:
                    print(f"结果: {result_text[:200]}...")
                print()
                
                # 3. 测试commit消息生成
                print("📝 测试commit消息生成:")
                print("-" * 50)
                call_result = await session.call_tool("generate_commit_message", 
                                                    arguments={"changes_description": "添加新功能, 修复bug, 更新文档"})
                commit_msg = call_result.content[0].text if call_result.content else ""
                print(f"生成的commit消息: {commit_msg}")
                print()
                
                # 4. 测试函数文档生成
                print("📚 测试函数文档生成:")
                print("-" * 50)
                sample_function = """
def calculate_score(user_data, weights, threshold):
    score = 0
    for key, value in user_data.items():
        if key in weights:
            score += value * weights[key]
    return score if score > threshold else 0
"""
                call_result = await session.call_tool("generate_function_docs", 
                                                    arguments={"function_code": sample_function})
                docstring = call_result.content[0].text if call_result.content else ""
                print("生成的docstring:")
                print(docstring)
                print()
                
                # 5. 测试重构建议
                print("🔧 测试重构建议:")
                print("-" * 50)
                call_result = await session.call_tool("suggest_refactoring", 
                                                    arguments={"file_path": "professional_code_analyzer.py"})
                result_text = call_result.content[0].text if call_result.content else "[]"
                try:
                    suggestions = json.loads(result_text)
                    if isinstance(suggestions, list) and suggestions:
                        print("发现的重构建议:")
                        for suggestion in suggestions[:3]:
                            print(f"  - {suggestion['type']}: {suggestion['message']}")
                            print(f"    建议: {suggestion['suggestion']}")
                    else:
                        print("✅ 未发现需要重构的问题")
                except (json.JSONDecodeError, KeyError, TypeError):
                    print(f"结果: {result_text[:200]}...")
                print()
                
                # 6. 测试综合分析报告
                print("📋 测试综合分析报告:")
                print("-" * 50)
                call_result = await session.call_tool("get_comprehensive_analysis", 
                                                    arguments={"file_path": "caculator_server.py"})
                report = call_result.content[0].text if call_result.content else ""
                print("综合分析报告预览:")
                lines = report.split('\n')
                for line in lines[:15]:  # 只显示前15行
                    print(line)
                if len(lines) > 15:
                    print(f"... (还有 {len(lines)-15} 行)")
                print()
                
                print("🎉 所有功能测试完成!")
                print("🎯 专业级代码分析器正常运行")
                print("=" * 70)
    
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🤖 专业级代码分析器测试客户端")
    print("🎯 测试语义级代码分析、项目上下文、开发加速功能")
    print()
    asyncio.run(test_professional_analyzer())