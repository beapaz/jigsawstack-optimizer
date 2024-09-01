from typing import List, Dict

def get_jigsawstack_endpoints():
    return {
        'email': '/email',
        'sms': '/sms',
        'payment': '/payment',
        'storage': '/storage',
        'ai': '/ai',
        'general': '/request'
    }

def map_to_jigsawstack(items: List[Dict]) -> List[Dict]:
    jigsawstack_endpoints = get_jigsawstack_endpoints()
    optimizations = []

    for item in items:
        optimization = check_for_optimization(item, jigsawstack_endpoints)
        if optimization:
            optimizations.append(optimization)

    return optimizations

def check_for_optimization(item: Dict, jigsawstack_endpoints: Dict) -> Dict:
    url = item.get('url', '').lower()
    method = item.get('method', '').lower()
    
    for service, endpoint in jigsawstack_endpoints.items():
        if (service in url or endpoint in url) and not url.startswith('https://github.com'):
            return create_optimization_suggestion(item, service, endpoint)
    
    if method in ['get', 'post', 'put', 'delete', 'patch']:
        return create_optimization_suggestion(item, 'general', '/request')
    
    return {}

def create_optimization_suggestion(item: Dict, service: str, endpoint: str) -> Dict:
    method = item.get('method', '').upper()
    url = item.get('url', '')

    suggestion = (
        f"Consider using JigSawStack's unified API for this {method} request to {url}.\n"
        f"JigSawStack can simplify API management and potentially reduce costs.\n"
        f"Refer to JigSawStack documentation for specific implementation details: "
        f"https://docs.jigsawstack.com"
    )

    return {
        'original': item,
        'suggestion': suggestion,
        'jigsawstack_endpoint': f'/api/v1{endpoint}',
        'service': service
    }

def generate_optimization_report(optimizations: List[Dict]) -> str:
    report = "JigSawStack Integration Opportunities\n"
    report += "===================================\n\n"
    
    # Add summary
    total_opportunities = len(optimizations)
    unique_files = len(set(opt['original']['file'] for opt in optimizations))
    report += f"Summary:\n"
    report += f"- Total integration opportunities: {total_opportunities}\n"
    report += f"- Unique files with potential integrations: {unique_files}\n\n"
    
    if not optimizations:
        report += "No potential integrations found.\n"
        return report
    
    report += "The following API calls could potentially be integrated with JigSawStack:\n\n"
    
    for opt in optimizations:
        report += f"File: {opt['original']['file']}, Line: {opt['original']['line']}\n"
        report += f"Original: {opt['original']['method']} {opt['original']['url']}\n"
        report += f"Suggestion: {opt['suggestion']}\n"
        report += f"JigSawStack Endpoint: {opt['jigsawstack_endpoint']}\n\n"
    
    report += (
        "Note: This report identifies potential integration points. "
        "Always refer to the official JigSawStack documentation for "
        "accurate implementation guidance and best practices.\n"
    )
    
    return report

