# CodeInsight MCP 服务器

## 项目概述

CodeInsight是一个专为Claude设计的智能代码分析MCP服务器，提供深度Python代码分析、质量检测和结构洞察能力。

## 功能特性

### 🔍 核心分析工具

1. **count_lines** - 统计文件行数
   - 总行数、非空行数、代码行数、注释行数
   - 支持多种编程语言文件

2. **analyze_python** - 深度Python文件分析
   - AST语法树解析
   - 函数和类结构分析
   - 语法错误检测
   - 代码复杂度评估

3. **list_python_files** - 项目文件扫描
   - 递归扫描Python文件
   - 文件统计和分类

## 服务器文件

### 🚀 主要版本

- **minimal_code_server.py** - 精简工作版本
  - 3个核心工具
  - 稳定的stdio协议
  - 适合Claude Desktop集成

- **working_code_insight_server.py** - 功能丰富版本
  - 更多高级分析功能
  - 项目概况统计
  - 代码健康度报告

### 🧪 测试客户端

- **minimal_code_client.py** - 对应精简版本的测试
- **working_code_insight_client.py** - 对应功能版本的测试

## 快速开始

### 1. 测试服务器

```bash
# 测试精简版本（推荐）
python3 minimal_code_client.py

# 测试功能版本
python3 working_code_insight_client.py
```

### 2. 集成到Claude Desktop

将以下配置添加到Claude Desktop配置文件：

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "code-insight": {
      "command": "python3",
      "args": [
        "/path/to/your/MCP-Fresh/minimal_code_server.py"
      ],
      "description": "智能代码分析师"
    }
  }
}
```

### 3. 使用示例

在Claude Desktop中，您可以使用以下方式调用服务：

```
# 分析单个文件
@code-insight 请分析这个文件的代码质量: main.py

# 列出项目中的Python文件
@code-insight 显示当前目录下的所有Python文件

# 获取文件的详细统计
@code-insight 统计 app.py 的行数和结构信息
```

## 分析结果示例

### 文件行数统计
```json
{
  "file_path": "example.py",
  "total_lines": 150,
  "non_empty_lines": 120,
  "code_lines": 100,
  "comment_lines": 20
}
```

### Python文件分析
```json
{
  "file_path": "example.py",
  "total_lines": 150,
  "functions_count": 8,
  "classes_count": 2,
  "functions": [
    {
      "name": "calculate_score",
      "line": 25,
      "args": 3
    }
  ],
  "classes": [
    {
      "name": "DataProcessor",
      "line": 45
    }
  ]
}
```

## 技术架构

- **协议**: MCP (Model Context Protocol)
- **传输**: stdio
- **框架**: FastMCP
- **语言**: Python 3.12+
- **依赖**: mcp[cli]>=1.9.0

## 扩展能力

该MCP服务器框架易于扩展，可以添加：

- 更多编程语言支持
- 代码质量评分算法
- 安全漏洞检测
- 性能分析工具
- 代码重构建议
- 依赖关系分析

## 故障排除

### 常见问题

1. **服务器无法启动**
   - 检查Python版本 (需要3.12+)
   - 确认MCP依赖已安装: `pip install mcp[cli]`

2. **Claude Desktop无法连接**
   - 验证配置文件路径正确
   - 确保Python脚本路径是绝对路径
   - 重启Claude Desktop应用

3. **分析结果异常**
   - 检查目标文件是否存在
   - 确认文件编码为UTF-8
   - 验证Python语法是否正确

### 调试模式

```bash
# 直接运行服务器查看日志
python3 minimal_code_server.py

# 使用客户端进行详细测试
python3 minimal_code_client.py
```

## 开发说明

### 添加新工具

1. 在服务器文件中添加新的 `@mcp.tool()` 装饰的函数
2. 确保函数返回JSON可序列化的数据
3. 在客户端中添加对应的测试
4. 更新文档和配置示例

### 性能优化

- 大文件分析时考虑分块处理
- 缓存AST解析结果
- 异步I/O操作
- 内存使用监控

## 许可证

此项目遵循MIT许可证，可自由使用和修改。

---

🎯 **目标**: 让Claude具备专业的代码分析能力，成为真正的AI编程助手