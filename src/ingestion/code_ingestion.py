import git
import ast
import os
import tempfile

def clone_repo(repo_url: str, target_path: str) -> str:
    git.Repo.clone_from(repo_url, target_path)
    return target_path

def parse_python_files(repo_path: str) -> dict:
    parsed_files = {}
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r') as f:
                    parsed_files[file] = ast.parse(f.read())
    return parsed_files

def ingest_codebase(repo_url: str) -> dict:
    temp_dir = tempfile.mkdtemp()
    repo_path = clone_repo(repo_url, temp_dir)
    return parse_python_files(repo_path)
