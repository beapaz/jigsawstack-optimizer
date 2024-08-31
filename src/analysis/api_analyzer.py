import ast
from typing import Dict, List

class APICallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.api_calls = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in ['get', 'post', 'put', 'delete']:
                self.api_calls.append({
                    'method': node.func.attr,
                    'url': node.args[0].s if node.args else None,
                    'line': node.lineno
                })
        self.generic_visit(node)

def analyze_api_calls(parsed_files: Dict[str, ast.AST]) -> List[Dict]:
    all_api_calls = []
    for file_name, tree in parsed_files.items():
        visitor = APICallVisitor()
        visitor.visit(tree)
        all_api_calls.extend([{**call, 'file': file_name} for call in visitor.api_calls])
    return all_api_calls
