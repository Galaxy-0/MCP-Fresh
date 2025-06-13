#!/usr/bin/env python3
"""
最小版本的CodeInsight服务器 - 基于FastMCP
"""
import os
import ast
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

# 创建服务器
mcp = FastMCP("MinimalCodeInsight")

@mcp.tool()
def count_lines(file_path: str) -> Dict[str, Any]:
    """统计文件行数"""
    if not os.path.exists(file_path):
        return {"error": f"文件不存在: {file_path}"}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        return {
            "file_path": file_path,
            "total_lines": len(lines),
            "non_empty_lines": len([line for line in lines if line.strip()]),
            "code_lines": len([line for line in lines if line.strip() and not line.strip().startswith('#')]),
            "comment_lines": len([line for line in lines if line.strip().startswith('#')])
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def analyze_python(file_path: str) -> Dict[str, Any]:
    """分析Python文件结构"""
    # 尝试相对路径和绝对路径
    if not os.path.isabs(file_path):
        # 如果是相对路径，尝试在项目目录中查找
        project_path = "/Users/yuanquan/code_project/GalaxyAI/MCP-Fresh"
        full_path = os.path.join(project_path, file_path)
        if os.path.exists(full_path):
            file_path = full_path
    
    if not os.path.exists(file_path):
        # 提供文件查找建议
        current_dir = os.getcwd()
        project_dir = "/Users/yuanquan/code_project/GalaxyAI/MCP-Fresh"
        return {
            "error": f"文件不存在: {file_path}",
            "current_directory": current_dir,
            "suggestion": f"请尝试使用完整路径或确保文件在 {project_dir} 目录中",
            "available_files": [f for f in os.listdir(project_dir) if f.endswith('.py')][:10]
        }
    
    if not file_path.endswith('.py'):
        return {"error": "只支持Python文件"}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 基本统计
        lines = content.split('\n')
        basic_stats = {
            "file_path": file_path,
            "total_lines": len(lines),
            "code_lines": len([line for line in lines if line.strip() and not line.strip().startswith('#')]),
            "comment_lines": len([line for line in lines if line.strip().startswith('#')])
        }
        
        # AST分析
        try:
            tree = ast.parse(content)
            functions = []
            classes = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        'name': node.name,
                        'line': node.lineno,
                        'args': len(node.args.args)
                    })
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        'name': node.name,
                        'line': node.lineno
                    })
            
            return {
                **basic_stats,
                "functions": functions,
                "classes": classes,
                "functions_count": len(functions),
                "classes_count": len(classes)
            }
            
        except SyntaxError as e:
            return {
                **basic_stats,
                "syntax_error": f"第{e.lineno}行: {e.msg}"
            }
    
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def list_python_files(directory: str = ".") -> Dict[str, Any]:
    """列出目录中的Python文件"""
    try:
        # 默认使用项目目录
        if directory == ".":
            directory = "/Users/yuanquan/code_project/GalaxyAI/MCP-Fresh"
        
        python_files = []
        for item in os.listdir(directory):
            if item.endswith('.py') and os.path.isfile(os.path.join(directory, item)):
                file_path = os.path.join(directory, item)
                file_size = os.path.getsize(file_path)
                python_files.append({
                    "name": item,
                    "path": file_path,
                    "size": file_size
                })
        
        # 按大小排序
        python_files.sort(key=lambda x: x['size'], reverse=True)
        
        return {
            "directory": directory,
            "python_files": python_files,
            "count": len(python_files),
            "total_size": sum(f['size'] for f in python_files)
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_project_overview() -> Dict[str, Any]:
    """获取整个项目的概览信息"""
    try:
        project_dir = "/Users/yuanquan/code_project/GalaxyAI/MCP-Fresh"
        
        # 统计所有Python文件
        all_files = []
        total_lines = 0
        total_functions = 0
        total_classes = 0
        
        for item in os.listdir(project_dir):
            if item.endswith('.py'):
                file_path = os.path.join(project_dir, item)
                
                # 快速分析每个文件
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    lines = len(content.split('\n'))
                    total_lines += lines
                    
                    # 简单计算函数和类数量
                    import ast
                    tree = ast.parse(content)
                    functions = len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
                    classes = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
                    
                    total_functions += functions
                    total_classes += classes
                    
                    all_files.append({
                        "name": item,
                        "lines": lines,
                        "functions": functions,
                        "classes": classes,
                        "size": os.path.getsize(file_path)
                    })
                except:
                    # 如果解析失败，至少记录文件存在
                    all_files.append({
                        "name": item,
                        "lines": 0,
                        "functions": 0,
                        "classes": 0,
                        "size": os.path.getsize(file_path),
                        "error": "解析失败"
                    })
        
        # 按行数排序
        all_files.sort(key=lambda x: x['lines'], reverse=True)
        
        return {
            "project_directory": project_dir,
            "summary": {
                "total_files": len(all_files),
                "total_lines": total_lines,
                "total_functions": total_functions,
                "total_classes": total_classes,
                "largest_files": all_files[:5]
            },
            "all_files": all_files
        }
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # 不要在stdio模式下使用print，会干扰MCP协议通信
    mcp.run(transport="stdio")