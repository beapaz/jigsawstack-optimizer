import os
from dotenv import load_dotenv
from ingestion.code_ingestion import ingest_codebase
from analysis.api_analyzer import analyze_api_calls, analyze_string_literals
from mapping.jigsawstack_mapper import map_to_jigsawstack, generate_optimization_report

def export_report(report: str, format: str = 'txt'):
    filename = f"jigsawstack_integration_report.{format}"
    with open(filename, 'w') as f:
        f.write(report)
    print(f"Report exported to {filename}")

def main():
    load_dotenv()
    
    if 'JIGSAWSTACK_API_KEY' not in os.environ:
        print("Error: JIGSAWSTACK_API_KEY environment variable is not set.")
        return

    try:
        repo_url = input("Enter the GitHub repository URL: ")
        parsed_files = ingest_codebase(repo_url)
        api_calls = analyze_api_calls(parsed_files)
        string_urls = analyze_string_literals(parsed_files)
        
        print(f"\nFound {len(api_calls)} API calls:")
        for call in api_calls:
            print(f"File: {call['file']}, Line: {call['line']}, Method: {call['method']}, URL: {call['url']}, Module: {call['module']}")
        
        print(f"\nFound {len(string_urls)} URLs in string literals:")
        for url in string_urls[:10]:  # Show only first 10 URLs to avoid cluttering the output
            print(f"File: {url['file']}, Line: {url['line']}, URL: {url['url']}")
        if len(string_urls) > 10:
            print(f"... and {len(string_urls) - 10} more.")
        
        optimizations = map_to_jigsawstack(api_calls + string_urls)
        report = generate_optimization_report(optimizations)
        
        print("\nOptimization Report:")
        print(report)

        # Export report
        export_choice = input("Do you want to export the report? (y/n): ").lower()
        if export_choice == 'y':
            export_report(report)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
