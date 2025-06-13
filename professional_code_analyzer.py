#!/usr/bin/env python3
"""
专业级智能代码分析系统 - MCP服务器
提供语义级代码分析，超越传统静态分析工具
"""
import os
import ast
import re
import json
import subprocess
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# 创建专业级MCP服务器
mcp = FastMCP("ProfessionalCodeAnalyzer")

# ============================================================================
# 核心数据结构
# ============================================================================

@dataclass
class CodeIssue:
    """代码问题数据结构"""
    severity: str  # critical, warning, suggestion
    category: str  # logic, performance, security, architecture
    message: str
    file_path: str
    line_number: int
    code_snippet: str
    fix_suggestion: str
    confidence: float  # 0.0-1.0

@dataclass
class FunctionMetrics:
    """函数指标数据结构"""
    name: str
    line_start: int
    line_end: int
    complexity: int
    parameter_count: int
    return_complexity: int
    has_docstring: bool
    async_function: bool
    nested_functions: int
    external_calls: List[str]

@dataclass
class ClassMetrics:
    """类指标数据结构"""
    name: str
    line_start: int
    line_end: int
    method_count: int
    property_count: int
    inheritance_depth: int
    has_docstring: bool
    design_pattern: Optional[str]

# ============================================================================
# 核心分析引擎
# ============================================================================

class CodeIntelligenceEngine:
    """代码智能分析引擎"""
    
    def __init__(self):
        self.issues: List[CodeIssue] = []
        self.function_metrics: List[FunctionMetrics] = []
        self.class_metrics: List[ClassMetrics] = []
        
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """分析单个文件"""
        if not os.path.exists(file_path):
            return {"error": f"文件不存在: {file_path}"}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            tree = ast.parse(source_code)
            lines = source_code.split('\n')
            
            # 重置分析状态
            self.issues.clear()
            self.function_metrics.clear()
            self.class_metrics.clear()
            
            # 执行多维度分析
            self._analyze_business_logic(tree, lines, file_path)
            self._analyze_performance_patterns(tree, lines, file_path)
            self._analyze_security_risks(tree, lines, file_path)
            self._analyze_architecture_decisions(tree, lines, file_path)
            
            return {
                "file_path": file_path,
                "analysis_summary": {
                    "total_issues": len(self.issues),
                    "critical_issues": len([i for i in self.issues if i.severity == "critical"]),
                    "warnings": len([i for i in self.issues if i.severity == "warning"]),
                    "suggestions": len([i for i in self.issues if i.severity == "suggestion"])
                },
                "issues": [asdict(issue) for issue in self.issues],
                "function_metrics": [asdict(func) for func in self.function_metrics],
                "class_metrics": [asdict(cls) for cls in self.class_metrics],
                "overall_quality_score": self._calculate_quality_score()
            }
            
        except SyntaxError as e:
            return {
                "error": f"语法错误: {e.msg} (第{e.lineno}行)",
                "file_path": file_path
            }
        except Exception as e:
            return {
                "error": f"分析失败: {str(e)}",
                "file_path": file_path
            }
    
    def _analyze_business_logic(self, tree: ast.AST, lines: List[str], file_path: str):
        """分析业务逻辑一致性"""
        
        class BusinessLogicVisitor(ast.NodeVisitor):
            def __init__(self, analyzer):
                self.analyzer = analyzer
                self.lines = lines
                self.file_path = file_path
            
            def visit_FunctionDef(self, node):
                # 分析函数命名与功能的一致性
                self._check_function_naming_consistency(node)
                
                # 分析函数复杂度和职责
                self._analyze_function_responsibility(node)
                
                # 分析错误处理策略
                self._check_error_handling_consistency(node)
                
                self.generic_visit(node)
            
            def _check_function_naming_consistency(self, node):
                """检查函数命名与实际功能的一致性"""
                func_name = node.name.lower()
                
                # 获取函数体中的操作类型
                operations = self._extract_function_operations(node)
                
                # 命名模式检查
                naming_issues = []
                
                if func_name.startswith('get_') and 'return' not in operations:
                    naming_issues.append("函数名暗示获取数据，但没有返回语句")
                
                if func_name.startswith('set_') and 'assignment' not in operations:
                    naming_issues.append("函数名暗示设置数据，但没有赋值操作")
                
                if func_name.startswith('is_') or func_name.startswith('has_'):
                    if 'return' not in operations:
                        naming_issues.append("布尔函数应该有返回值")
                
                if 'save' in func_name and 'file_io' not in operations and 'database' not in operations:
                    naming_issues.append("函数名暗示保存操作，但没有发现文件或数据库操作")
                
                for issue in naming_issues:
                    self.analyzer.issues.append(CodeIssue(
                        severity="warning",
                        category="logic",
                        message=f"命名不一致: {issue}",
                        file_path=self.file_path,
                        line_number=node.lineno,
                        code_snippet=self.lines[node.lineno-1] if node.lineno <= len(self.lines) else "",
                        fix_suggestion=f"考虑重命名函数 '{node.name}' 或调整函数实现以匹配命名意图",
                        confidence=0.7
                    ))
            
            def _extract_function_operations(self, node):
                """提取函数中的操作类型"""
                operations = set()
                
                for child in ast.walk(node):
                    if isinstance(child, ast.Return):
                        operations.add('return')
                    elif isinstance(child, ast.Assign):
                        operations.add('assignment')
                    elif isinstance(child, ast.Call):
                        if hasattr(child.func, 'attr'):
                            if child.func.attr in ['open', 'read', 'write', 'close']:
                                operations.add('file_io')
                            elif child.func.attr in ['execute', 'query', 'commit']:
                                operations.add('database')
                
                return operations
            
            def _analyze_function_responsibility(self, node):
                """分析函数职责单一性"""
                complexity = self._calculate_cyclomatic_complexity(node)
                param_count = len(node.args.args)
                
                # 记录函数指标
                func_metrics = FunctionMetrics(
                    name=node.name,
                    line_start=node.lineno,
                    line_end=getattr(node, 'end_lineno', node.lineno),
                    complexity=complexity,
                    parameter_count=param_count,
                    return_complexity=self._count_return_statements(node),
                    has_docstring=ast.get_docstring(node) is not None,
                    async_function=isinstance(node, ast.AsyncFunctionDef),
                    nested_functions=len([n for n in node.body if isinstance(n, ast.FunctionDef)]),
                    external_calls=self._extract_external_calls(node)
                )
                
                self.analyzer.function_metrics.append(func_metrics)
                
                # 检查是否违反单一职责原则
                if complexity > 10:
                    self.analyzer.issues.append(CodeIssue(
                        severity="warning",
                        category="architecture",
                        message=f"函数复杂度过高 (圈复杂度: {complexity})",
                        file_path=self.file_path,
                        line_number=node.lineno,
                        code_snippet=self.lines[node.lineno-1] if node.lineno <= len(self.lines) else "",
                        fix_suggestion="考虑将此函数拆分为多个更小的函数，每个函数负责单一职责",
                        confidence=0.9
                    ))
                
                if param_count > 5:
                    self.analyzer.issues.append(CodeIssue(
                        severity="suggestion",
                        category="architecture",
                        message=f"函数参数过多 ({param_count}个参数)",
                        file_path=self.file_path,
                        line_number=node.lineno,
                        code_snippet=self.lines[node.lineno-1] if node.lineno <= len(self.lines) else "",
                        fix_suggestion="考虑使用数据类、字典或配置对象来减少参数数量",
                        confidence=0.8
                    ))
            
            def _check_error_handling_consistency(self, node):
                """检查错误处理策略的一致性"""
                try_blocks = [n for n in ast.walk(node) if isinstance(n, ast.Try)]
                bare_excepts = [n for n in ast.walk(node) if isinstance(n, ast.ExceptHandler) and n.type is None]
                
                if bare_excepts:
                    for except_node in bare_excepts:
                        self.analyzer.issues.append(CodeIssue(
                            severity="warning",
                            category="logic",
                            message="使用了裸except子句，可能掩盖重要错误",
                            file_path=self.file_path,
                            line_number=except_node.lineno,
                            code_snippet=self.lines[except_node.lineno-1] if except_node.lineno <= len(self.lines) else "",
                            fix_suggestion="指定具体的异常类型，如 'except ValueError:' 或 'except (TypeError, ValueError):'",
                            confidence=0.9
                        ))
            
            def _calculate_cyclomatic_complexity(self, node):
                """计算圈复杂度"""
                complexity = 1
                for child in ast.walk(node):
                    if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.With, ast.AsyncWith)):
                        complexity += 1
                    elif isinstance(child, ast.Try):
                        complexity += len(child.handlers)
                    elif isinstance(child, (ast.And, ast.Or)):
                        complexity += 1
                return complexity
            
            def _count_return_statements(self, node):
                """计算返回语句数量"""
                return len([n for n in ast.walk(node) if isinstance(n, ast.Return)])
            
            def _extract_external_calls(self, node):
                """提取外部函数调用"""
                calls = []
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        if hasattr(child.func, 'id'):
                            calls.append(child.func.id)
                        elif hasattr(child.func, 'attr'):
                            calls.append(child.func.attr)
                return calls
        
        visitor = BusinessLogicVisitor(self)
        visitor.visit(tree)
    
    def _analyze_performance_patterns(self, tree: ast.AST, lines: List[str], file_path: str):
        """分析性能影响模式"""
        
        class PerformanceVisitor(ast.NodeVisitor):
            def __init__(self, analyzer):
                self.analyzer = analyzer
                self.lines = lines
                self.file_path = file_path
            
            def visit_For(self, node):
                # 检查嵌套循环
                nested_loops = [n for n in ast.walk(node) if isinstance(n, (ast.For, ast.While)) and n != node]
                if nested_loops:
                    self.analyzer.issues.append(CodeIssue(
                        severity="warning",
                        category="performance",
                        message=f"发现嵌套循环，可能导致O(n²)或更高复杂度",
                        file_path=self.file_path,
                        line_number=node.lineno,
                        code_snippet=self.lines[node.lineno-1] if node.lineno <= len(self.lines) else "",
                        fix_suggestion="考虑优化算法，使用哈希表、预计算或其他数据结构来减少时间复杂度",
                        confidence=0.8
                    ))
                
                # 检查循环中的字符串拼接
                string_concats = self._find_string_concatenations(node)
                if string_concats:
                    self.analyzer.issues.append(CodeIssue(
                        severity="warning",
                        category="performance",
                        message="循环中进行字符串拼接，性能较差",
                        file_path=self.file_path,
                        line_number=node.lineno,
                        code_snippet=self.lines[node.lineno-1] if node.lineno <= len(self.lines) else "",
                        fix_suggestion="使用 ''.join() 或 f-string 在循环外进行字符串操作",
                        confidence=0.9
                    ))
                
                self.generic_visit(node)
            
            def _find_string_concatenations(self, node):
                """查找字符串拼接操作"""
                concats = []
                for child in ast.walk(node):
                    if isinstance(child, ast.BinOp) and isinstance(child.op, ast.Add):
                        # 简化检查：假设涉及字符串的加法操作
                        concats.append(child)
                return concats
        
        visitor = PerformanceVisitor(self)
        visitor.visit(tree)
    
    def _analyze_security_risks(self, tree: ast.AST, lines: List[str], file_path: str):
        """分析安全风险"""
        
        class SecurityVisitor(ast.NodeVisitor):
            def __init__(self, analyzer):
                self.analyzer = analyzer
                self.lines = lines
                self.file_path = file_path
            
            def visit_Assign(self, node):
                # 检查硬编码密码和敏感信息
                if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                    value = node.value.value
                    
                    # 检查可能的密码模式
                    if len(value) > 8 and any(keyword in str(node.targets).lower() 
                                           for keyword in ['password', 'secret', 'key', 'token']):
                        self.analyzer.issues.append(CodeIssue(
                            severity="critical",
                            category="security",
                            message="检测到硬编码的敏感信息",
                            file_path=self.file_path,
                            line_number=node.lineno,
                            code_snippet=self.lines[node.lineno-1] if node.lineno <= len(self.lines) else "",
                            fix_suggestion="使用环境变量、配置文件或密钥管理服务来存储敏感信息",
                            confidence=0.8
                        ))
                
                self.generic_visit(node)
            
            def visit_Call(self, node):
                # 检查不安全的函数调用
                if hasattr(node.func, 'id'):
                    func_name = node.func.id
                    if func_name == 'eval':
                        self.analyzer.issues.append(CodeIssue(
                            severity="critical",
                            category="security",
                            message="使用eval()函数存在代码注入风险",
                            file_path=self.file_path,
                            line_number=node.lineno,
                            code_snippet=self.lines[node.lineno-1] if node.lineno <= len(self.lines) else "",
                            fix_suggestion="使用ast.literal_eval()或其他安全的替代方案",
                            confidence=0.95
                        ))
                    elif func_name == 'exec':
                        self.analyzer.issues.append(CodeIssue(
                            severity="critical",
                            category="security",
                            message="使用exec()函数存在代码执行风险",
                            file_path=self.file_path,
                            line_number=node.lineno,
                            code_snippet=self.lines[node.lineno-1] if node.lineno <= len(self.lines) else "",
                            fix_suggestion="重新设计代码逻辑，避免动态代码执行",
                            confidence=0.95
                        ))
                
                self.generic_visit(node)
        
        visitor = SecurityVisitor(self)
        visitor.visit(tree)
    
    def _analyze_architecture_decisions(self, tree: ast.AST, lines: List[str], file_path: str):
        """分析架构决策"""
        
        class ArchitectureVisitor(ast.NodeVisitor):
            def __init__(self, analyzer):
                self.analyzer = analyzer
                self.lines = lines
                self.file_path = file_path
            
            def visit_ClassDef(self, node):
                # 分析类的设计质量
                methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                properties = [n for n in node.body if isinstance(n, ast.Assign)]
                
                class_metrics = ClassMetrics(
                    name=node.name,
                    line_start=node.lineno,
                    line_end=getattr(node, 'end_lineno', node.lineno),
                    method_count=len(methods),
                    property_count=len(properties),
                    inheritance_depth=len(node.bases),
                    has_docstring=ast.get_docstring(node) is not None,
                    design_pattern=self._detect_design_pattern(node, methods)
                )
                
                self.analyzer.class_metrics.append(class_metrics)
                
                # 检查类的职责
                if len(methods) > 15:
                    self.analyzer.issues.append(CodeIssue(
                        severity="warning",
                        category="architecture",
                        message=f"类过于庞大 ({len(methods)}个方法)",
                        file_path=self.file_path,
                        line_number=node.lineno,
                        code_snippet=self.lines[node.lineno-1] if node.lineno <= len(self.lines) else "",
                        fix_suggestion="考虑将类拆分为多个更小的类，遵循单一职责原则",
                        confidence=0.8
                    ))
                
                self.generic_visit(node)
            
            def _detect_design_pattern(self, class_node, methods):
                """检测可能的设计模式"""
                method_names = [m.name for m in methods]
                
                # 单例模式检测
                if '__new__' in method_names and any('instance' in str(ast.dump(m)) for m in methods):
                    return "Singleton"
                
                # 工厂模式检测
                if any(name.startswith('create_') for name in method_names):
                    return "Factory"
                
                # 观察者模式检测
                if 'notify' in method_names and 'subscribe' in method_names:
                    return "Observer"
                
                return None
        
        visitor = ArchitectureVisitor(self)
        visitor.visit(tree)
    
    def _calculate_quality_score(self) -> float:
        """计算代码质量分数 (0-100)"""
        if not self.issues:
            return 100.0
        
        total_penalty = 0
        for issue in self.issues:
            if issue.severity == "critical":
                total_penalty += 20 * issue.confidence
            elif issue.severity == "warning":
                total_penalty += 10 * issue.confidence
            else:  # suggestion
                total_penalty += 5 * issue.confidence
        
        score = max(0, 100 - total_penalty)
        return round(score, 1)

# ============================================================================
# MCP工具接口
# ============================================================================

# ============================================================================
# 项目上下文感知模块
# ============================================================================

class ContextAwareEngine:
    """项目上下文感知分析引擎"""
    
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.tech_debt_score = 0.0
        self.dependency_issues = []
        
    def analyze_project_context(self) -> Dict[str, Any]:
        """分析整个项目的上下文信息"""
        try:
            tech_stack = self._identify_tech_stack()
            architecture_pattern = self._detect_architecture_pattern()
            dependency_health = self._analyze_dependency_health()
            tech_debt = self._calculate_tech_debt()
            
            return {
                "project_root": self.project_root,
                "tech_stack": tech_stack,
                "architecture_pattern": architecture_pattern,
                "dependency_health": dependency_health,
                "tech_debt_assessment": tech_debt,
                "recommendations": self._generate_project_recommendations(tech_stack, tech_debt)
            }
        except Exception as e:
            return {"error": f"项目上下文分析失败: {str(e)}"}
    
    def _identify_tech_stack(self) -> Dict[str, Any]:
        """识别技术栈"""
        tech_stack = {
            "primary_language": "Python",
            "frameworks": [],
            "databases": [],
            "testing_frameworks": [],
            "dependencies": []
        }
        
        # 检查requirements.txt或pyproject.toml
        req_files = ['requirements.txt', 'pyproject.toml', 'setup.py', 'Pipfile']
        for req_file in req_files:
            req_path = os.path.join(self.project_root, req_file)
            if os.path.exists(req_path):
                dependencies = self._parse_dependencies(req_path)
                tech_stack["dependencies"].extend(dependencies)
                
                # 基于依赖推断框架
                for dep in dependencies:
                    dep_lower = dep.lower()
                    if any(fw in dep_lower for fw in ['django', 'flask', 'fastapi', 'tornado']):
                        tech_stack["frameworks"].append(dep)
                    elif any(db in dep_lower for db in ['sqlalchemy', 'django-orm', 'pymongo']):
                        tech_stack["databases"].append(dep)
                    elif any(test in dep_lower for test in ['pytest', 'unittest', 'nose']):
                        tech_stack["testing_frameworks"].append(dep)
        
        return tech_stack
    
    def _parse_dependencies(self, file_path: str) -> List[str]:
        """解析依赖文件"""
        dependencies = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if file_path.endswith('.txt'):
                # requirements.txt格式
                for line in content.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        dep_name = line.split('==')[0].split('>=')[0].split('<=')[0]
                        dependencies.append(dep_name)
            elif file_path.endswith('.toml'):
                # 简化的pyproject.toml解析
                import re
                deps = re.findall(r'"([^"]+)"', content)
                dependencies.extend([dep.split('>=')[0] for dep in deps if '.' not in dep])
                
        except Exception:
            pass
        
        return dependencies
    
    def _detect_architecture_pattern(self) -> str:
        """检测架构模式"""
        # 分析目录结构
        dirs = [d for d in os.listdir(self.project_root) 
                if os.path.isdir(os.path.join(self.project_root, d)) and not d.startswith('.')]
        
        dir_names = [d.lower() for d in dirs]
        
        # MVC模式检测
        if any(d in dir_names for d in ['models', 'views', 'controllers']):
            return "MVC (Model-View-Controller)"
        
        # 微服务模式检测
        if any(d in dir_names for d in ['services', 'api', 'gateway']):
            return "Microservices"
        
        # 分层架构检测
        if any(d in dir_names for d in ['domain', 'infrastructure', 'application']):
            return "Layered Architecture"
        
        # 包结构分析
        if 'src' in dir_names or len([d for d in dirs if not d.startswith('.')]) > 5:
            return "Package-based"
        
        return "Simple/Flat Structure"
    
    def _analyze_dependency_health(self) -> Dict[str, Any]:
        """分析依赖健康度"""
        health_report = {
            "total_dependencies": 0,
            "outdated_dependencies": [],
            "security_vulnerabilities": [],
            "dependency_conflicts": [],
            "health_score": 100.0
        }
        
        # 这里可以集成实际的依赖检查工具
        # 目前提供模拟分析
        
        return health_report
    
    def _calculate_tech_debt(self) -> Dict[str, Any]:
        """计算技术债务"""
        debt_factors = {
            "code_duplication": 0,
            "long_functions": 0,
            "complex_classes": 0,
            "missing_tests": 0,
            "poor_documentation": 0
        }
        
        total_debt_score = 0
        python_files = []
        
        # 扫描所有Python文件
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        # 简化的技术债务评估
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                lines = content.split('\n')
                debt_factors["long_functions"] += len([l for l in lines if 'def ' in l and len(content) > 2000])
                debt_factors["missing_tests"] += 1 if 'test' not in file_path.lower() else 0
                debt_factors["poor_documentation"] += 1 if content.count('"""') < 2 else 0
                
            except Exception:
                continue
        
        total_debt_score = sum(debt_factors.values())
        
        return {
            "debt_factors": debt_factors,
            "total_score": total_debt_score,
            "debt_level": "Low" if total_debt_score < 10 else "Medium" if total_debt_score < 25 else "High",
            "recommended_actions": self._get_debt_reduction_actions(debt_factors)
        }
    
    def _get_debt_reduction_actions(self, debt_factors: Dict[str, int]) -> List[str]:
        """获取债务减少建议"""
        actions = []
        
        if debt_factors["long_functions"] > 3:
            actions.append("重构长函数，将其拆分为更小的函数")
        
        if debt_factors["missing_tests"] > 5:
            actions.append("增加单元测试覆盖率")
        
        if debt_factors["poor_documentation"] > 3:
            actions.append("改善代码文档和注释")
        
        return actions
    
    def _generate_project_recommendations(self, tech_stack: Dict, tech_debt: Dict) -> List[str]:
        """生成项目改进建议"""
        recommendations = []
        
        # 基于技术栈的建议
        if not tech_stack["testing_frameworks"]:
            recommendations.append("建议添加测试框架(如pytest)以提高代码质量")
        
        if tech_debt["debt_level"] == "High":
            recommendations.append("技术债务较高，建议制定重构计划")
        
        # 基于架构的建议
        if tech_stack.get("architecture_pattern") == "Simple/Flat Structure":
            recommendations.append("考虑重构为更清晰的模块化架构")
        
        return recommendations

# ============================================================================
# 开发加速器模块  
# ============================================================================

class DevAcceleratorEngine:
    """开发加速器引擎"""
    
    def generate_commit_message(self, file_changes: List[str]) -> str:
        """根据文件变更生成commit消息"""
        if not file_changes:
            return "chore: minor updates"
        
        # 分析变更类型
        change_types = set()
        for change in file_changes:
            if 'test' in change.lower():
                change_types.add('test')
            elif 'doc' in change.lower() or 'readme' in change.lower():
                change_types.add('docs')
            elif 'fix' in change.lower() or 'bug' in change.lower():
                change_types.add('fix')
            elif 'add' in change.lower() or 'new' in change.lower():
                change_types.add('feat')
            else:
                change_types.add('refactor')
        
        # 生成消息
        if 'feat' in change_types:
            return f"feat: implement new functionality ({len(file_changes)} files)"
        elif 'fix' in change_types:
            return f"fix: resolve issues ({len(file_changes)} files)"
        elif 'test' in change_types:
            return f"test: add/update tests ({len(file_changes)} files)"
        elif 'docs' in change_types:
            return f"docs: update documentation ({len(file_changes)} files)"
        else:
            return f"refactor: improve code structure ({len(file_changes)} files)"
    
    def generate_function_docstring(self, func_code: str) -> str:
        """为函数生成docstring"""
        try:
            tree = ast.parse(func_code)
            func_node = tree.body[0] if tree.body and isinstance(tree.body[0], ast.FunctionDef) else None
            
            if not func_node:
                return '"""Function description."""'
            
            func_name = func_node.name
            args = [arg.arg for arg in func_node.args.args]
            
            # 生成基础docstring
            docstring = f'"""{func_name.replace("_", " ").title()}\n\n'
            
            if args:
                docstring += "    Args:\n"
                for arg in args:
                    docstring += f"        {arg}: Description of {arg}\n"
                docstring += "\n"
            
            docstring += "    Returns:\n"
            docstring += "        Description of return value\n"
            docstring += '    """'
            
            return docstring
            
        except Exception:
            return '"""Function description."""'
    
    def suggest_refactoring(self, code: str) -> List[Dict[str, str]]:
        """提供重构建议"""
        suggestions = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # 检查函数长度
                    if hasattr(node, 'end_lineno') and node.end_lineno - node.lineno > 50:
                        suggestions.append({
                            "type": "function_length",
                            "message": f"函数 '{node.name}' 过长，建议拆分",
                            "suggestion": "将函数拆分为多个更小的函数"
                        })
                    
                    # 检查参数数量
                    if len(node.args.args) > 5:
                        suggestions.append({
                            "type": "parameter_count",
                            "message": f"函数 '{node.name}' 参数过多",
                            "suggestion": "使用数据类或配置对象来减少参数数量"
                        })
                
                elif isinstance(node, ast.ClassDef):
                    methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                    if len(methods) > 15:
                        suggestions.append({
                            "type": "class_size",
                            "message": f"类 '{node.name}' 过于庞大",
                            "suggestion": "考虑将类拆分，遵循单一职责原则"
                        })
        
        except Exception:
            pass
        
        return suggestions

# 全局分析引擎实例
analyzer = CodeIntelligenceEngine()
context_analyzer = ContextAwareEngine("/Users/yuanquan/code_project/GalaxyAI/MCP-Fresh")
dev_accelerator = DevAcceleratorEngine()

@mcp.tool()
def analyze_code_intelligence(file_path: str) -> Dict[str, Any]:
    """深度智能代码分析 - 业务逻辑、性能、安全、架构
    
    Args:
        file_path: Python文件路径
        
    Returns:
        详细的代码分析报告
    """
    # 处理相对路径
    if not os.path.isabs(file_path):
        project_path = "/Users/yuanquan/code_project/GalaxyAI/MCP-Fresh"
        full_path = os.path.join(project_path, file_path)
        if os.path.exists(full_path):
            file_path = full_path
    
    return analyzer.analyze_file(file_path)

@mcp.tool()
def analyze_project_context() -> Dict[str, Any]:
    """分析整个项目的技术栈、架构模式和技术债务
    
    Returns:
        项目上下文分析报告
    """
    return context_analyzer.analyze_project_context()

@mcp.tool()
def generate_commit_message(changes_description: str) -> str:
    """根据代码变更描述生成规范的commit消息
    
    Args:
        changes_description: 变更描述，如 "添加了新功能，修复了bug"
        
    Returns:
        规范的commit消息
    """
    # 简单解析变更描述
    file_changes = changes_description.split(',')
    return dev_accelerator.generate_commit_message(file_changes)

@mcp.tool()
def generate_function_docs(function_code: str) -> str:
    """为函数生成标准的docstring文档
    
    Args:
        function_code: 函数代码
        
    Returns:
        生成的docstring
    """
    return dev_accelerator.generate_function_docstring(function_code)

@mcp.tool()
def suggest_refactoring(file_path: str) -> List[Dict[str, str]]:
    """分析代码并提供重构建议
    
    Args:
        file_path: Python文件路径
        
    Returns:
        重构建议列表
    """
    # 处理相对路径
    if not os.path.isabs(file_path):
        project_path = "/Users/yuanquan/code_project/GalaxyAI/MCP-Fresh"
        full_path = os.path.join(project_path, file_path)
        if os.path.exists(full_path):
            file_path = full_path
    
    if not os.path.exists(file_path):
        return [{"type": "error", "message": f"文件不存在: {file_path}", "suggestion": "请检查文件路径"}]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        return dev_accelerator.suggest_refactoring(code)
    except Exception as e:
        return [{"type": "error", "message": f"读取文件失败: {str(e)}", "suggestion": "请检查文件权限"}]

@mcp.tool()
def get_comprehensive_analysis(file_path: str) -> str:
    """获取文件的综合分析报告（包含代码质量、重构建议、技术债务）
    
    Args:
        file_path: Python文件路径
        
    Returns:
        综合分析报告
    """
    # 处理相对路径
    if not os.path.isabs(file_path):
        project_path = "/Users/yuanquan/code_project/GalaxyAI/MCP-Fresh"
        full_path = os.path.join(project_path, file_path)
        if os.path.exists(full_path):
            file_path = full_path
    
    if not os.path.exists(file_path):
        return f"❌ 文件不存在: {file_path}"
    
    # 获取代码智能分析
    analysis = analyze_code_intelligence(file_path)
    if "error" in analysis:
        return f"❌ 分析失败: {analysis['error']}"
    
    # 获取重构建议
    refactor_suggestions = suggest_refactoring(file_path)
    
    # 生成综合报告
    report = f"""
# 🔍 综合代码分析报告

## 📁 文件: {analysis['file_path']}

## 🎯 质量评分: {analysis.get('overall_quality_score', 0)}/100

## 📊 问题概览
- 🚨 严重问题: {analysis['analysis_summary']['critical_issues']}
- ⚠️  警告: {analysis['analysis_summary']['warnings']}
- 💡 建议: {analysis['analysis_summary']['suggestions']}

## 🔧 函数复杂度分析
"""
    
    functions = analysis.get('function_metrics', [])
    if functions:
        for func in functions[:5]:  # 显示前5个函数
            complexity_icon = "🟢" if func['complexity'] <= 5 else "🟡" if func['complexity'] <= 10 else "🔴"
            report += f"- {complexity_icon} **{func['name']}()**: 复杂度 {func['complexity']}, {func['parameter_count']} 参数\n"
    else:
        report += "- 无函数或解析失败\n"
    
    # 添加重构建议
    if refactor_suggestions:
        report += "\n## 💡 重构建议\n"
        for suggestion in refactor_suggestions[:5]:
            report += f"- **{suggestion['type']}**: {suggestion['message']}\n"
            report += f"  - 建议: {suggestion['suggestion']}\n"
    
    # 添加关键问题
    critical_issues = [i for i in analysis.get('issues', []) if i['severity'] == 'critical']
    if critical_issues:
        report += "\n## 🚨 严重问题 (需要立即修复)\n"
        for issue in critical_issues[:3]:
            report += f"- **第{issue['line_number']}行**: {issue['message']}\n"
            report += f"  - 建议: {issue['fix_suggestion']}\n"
    
    # 添加总体建议
    report += "\n## 🎯 总体建议\n"
    score = analysis.get('overall_quality_score', 0)
    if score >= 80:
        report += "- ✅ 代码质量良好，继续保持!\n"
        report += "- 🔍 可关注性能优化和代码简化\n"
    elif score >= 60:
        report += "- 🔧 重点关注严重问题和警告\n"
        report += "- 📚 考虑重构复杂度较高的函数\n"
    else:
        report += "- 🚨 代码质量需要改进\n"
        report += "- 🔧 优先修复安全和逻辑问题\n"
        report += "- 📖 建议进行全面的代码审查\n"
    
    return report

@mcp.tool()
def get_quality_report(file_path: str) -> str:
    """生成可读的代码质量报告
    
    Args:
        file_path: Python文件路径
        
    Returns:
        格式化的质量报告文本
    """
    analysis = analyze_code_intelligence(file_path)
    
    if "error" in analysis:
        return f"❌ 分析失败: {analysis['error']}"
    
    report = f"""
# 📊 代码质量报告: {analysis['file_path']}

## 🎯 总体评分: {analysis.get('overall_quality_score', 0)}/100

## 📈 问题统计
- 🚨 严重问题: {analysis['analysis_summary']['critical_issues']}
- ⚠️  警告: {analysis['analysis_summary']['warnings']}  
- 💡 建议: {analysis['analysis_summary']['suggestions']}

## 🔍 详细问题分析
"""
    
    # 按严重程度排序问题
    issues = analysis.get('issues', [])
    critical_issues = [i for i in issues if i['severity'] == 'critical']
    warnings = [i for i in issues if i['severity'] == 'warning']
    suggestions = [i for i in issues if i['severity'] == 'suggestion']
    
    if critical_issues:
        report += "\n### 🚨 严重问题 (需要立即修复)\n"
        for issue in critical_issues[:3]:  # 只显示前3个
            report += f"""
**第{issue['line_number']}行 - {issue['category'].title()}**
- 问题: {issue['message']}
- 代码: `{issue['code_snippet']}`
- 建议: {issue['fix_suggestion']}
- 置信度: {issue['confidence']:.0%}
"""
    
    if warnings:
        report += "\n### ⚠️ 警告 (建议修复)\n"
        for issue in warnings[:3]:  # 只显示前3个
            report += f"""
**第{issue['line_number']}行 - {issue['category'].title()}**
- 问题: {issue['message']}
- 建议: {issue['fix_suggestion']}
"""
    
    # 函数复杂度分析
    functions = analysis.get('function_metrics', [])
    if functions:
        complex_functions = [f for f in functions if f['complexity'] > 7]
        if complex_functions:
            report += "\n### ⚙️ 复杂函数分析\n"
            for func in complex_functions[:3]:
                report += f"- **{func['name']}()**: 复杂度 {func['complexity']}, {func['parameter_count']} 参数\n"
    
    # 改进建议
    report += "\n## 💡 优化建议\n"
    if analysis['overall_quality_score'] >= 80:
        report += "- ✅ 代码质量良好，继续保持!\n"
    elif analysis['overall_quality_score'] >= 60:
        report += "- 🔧 重点关注严重问题和警告\n- 📚 考虑重构复杂度较高的函数\n"
    else:
        report += "- 🚨 代码质量需要改进\n- 🔧 优先修复安全和逻辑问题\n- 📖 建议进行代码审查\n"
    
    return report

if __name__ == "__main__":
    mcp.run(transport="stdio")