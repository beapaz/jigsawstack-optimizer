from ingestion.code_ingestion import ingest_codebase
from analysis.api_analyzer import analyze_api_calls

def main():
    repo_url = input("Enter the GitHub repository URL: ")
    parsed_files = ingest_codebase(repo_url)
    api_calls = analyze_api_calls(parsed_files)
    
    print(f"Found {len(api_calls)} API calls:")
    for call in api_calls:
        print(f"File: {call['file']}, Line: {call['line']}, Method: {call['method']}, URL: {call['url']}")

if __name__ == "__main__":
    main()
