import ast
from typing import Dict, List
import re

class APICallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.api_calls = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            if node.func.attr.lower() in ['get', 'post', 'put', 'delete', 'patch']:
                url = self.extract_url(node)
                self.api_calls.append({
                    'method': node.func.attr.lower(),
                    'url': url,
                    'line': node.lineno,
                    'col': node.col_offset,
                    'module': self.extract_module(node)
                })
        self.generic_visit(node)

    def extract_url(self, node):
        if node.args:
            if isinstance(node.args[0], ast.Str):
                return node.args[0].s
            elif isinstance(node.args[0], ast.Call) and isinstance(node.args[0].func, ast.Name):
                return f"Function call: {node.args[0].func.id}"
            elif isinstance(node.args[0], ast.Name):
                return f"Variable: {node.args[0].id}"
        for keyword in node.keywords:
            if keyword.arg == 'url':
                if isinstance(keyword.value, ast.Str):
                    return keyword.value.s
                elif isinstance(keyword.value, ast.Name):
                    return f"Variable: {keyword.value.id}"
        return "Unknown"

    def extract_module(self, node):
        if isinstance(node.func.value, ast.Name):
            return node.func.value.id
        elif isinstance(node.func.value, ast.Attribute):
            return node.func.value.attr
        return "Unknown"

def analyze_api_calls(parsed_files: Dict[str, ast.AST]) -> List[Dict]:
    all_api_calls = []
    for file_name, tree in parsed_files.items():
        visitor = APICallVisitor()
        visitor.visit(tree)
        all_api_calls.extend([{**call, 'file': file_name} for call in visitor.api_calls])
    return all_api_calls

def extract_urls_from_strings(content: str) -> List[str]:
    url_pattern = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')
    return url_pattern.findall(content)

def analyze_string_literals(parsed_files: Dict[str, ast.AST]) -> List[Dict]:
    all_urls = []
    for file_name, tree in parsed_files.items():
        for node in ast.walk(tree):
            if isinstance(node, ast.Str):
                urls = extract_urls_from_strings(node.s)
                for url in urls:
                    all_urls.append({
                        'url': url,
                        'line': node.lineno,
                        'col': node.col_offset,
                        'file': file_name
                    })
    return all_urls
