import json
import os
from datetime import datetime
from typing import Dict, List, Any

def format_repository_details(repo):
    """Format repository details for display."""
    return {
        "name": repo.get("name"),
        "url": repo.get("html_url"),
        "size": repo.get("size"),
        "description": repo.get("description"),
        "language": repo.get("language"),
        "created_at": repo.get("created_at"),
        "updated_at": repo.get("updated_at"),
    }

def format_repository_info(repo: Dict[str, Any]) -> Dict[str, Any]:
    """Format repository information for consistent output"""
    return {
        "name": repo.get("name", "Unknown"),
        "full_name": repo.get("full_name", "Unknown"),
        "description": repo.get("description", "No description"),
        "size": repo.get("size", 0),
        "language": repo.get("language", "Unknown"),
        "default_branch": repo.get("default_branch", "main"),
        "private": repo.get("private", False),
        "fork": repo.get("fork", False),
        "archived": repo.get("archived", False),
        "disabled": repo.get("disabled", False),
        "html_url": repo.get("html_url", ""),
        "clone_url": repo.get("clone_url", ""),
        "created_at": repo.get("created_at", ""),
        "updated_at": repo.get("updated_at", ""),
        "pushed_at": repo.get("pushed_at", ""),
        "stargazers_count": repo.get("stargazers_count", 0),
        "watchers_count": repo.get("watchers_count", 0),
        "forks_count": repo.get("forks_count", 0),
        "open_issues_count": repo.get("open_issues_count", 0)
    }

def validate_repository_data(repo_data):
    """Validate the repository data structure."""
    required_keys = ["name", "url", "size"]
    return all(key in repo_data for key in required_keys)

def extract_team_user_info(data):
    """Extract team and user information from the provided data."""
    return {
        "teams": [team["name"] for team in data.get("teams", [])],
        "users": [user["name"] for user in data.get("users", [])],
    }

def save_to_json(data: Dict[str, Any], filename: str, output_dir: str = "output") -> str:
    """Save data to JSON file"""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return filepath

def format_size(size_kb: int) -> str:
    """Format repository size in human-readable format"""
    if size_kb < 1024:
        return f"{size_kb} KB"
    elif size_kb < 1024 * 1024:
        return f"{size_kb / 1024:.1f} MB"
    else:
        return f"{size_kb / (1024 * 1024):.1f} GB"

def create_summary_report(org_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a summary report of the organization analysis"""
    repositories = org_data.get('repositories', [])
    
    total_size = sum(repo.get('size', 0) for repo in repositories)
    languages = {}
    
    for repo in repositories:
        lang = repo.get('language')
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
    
    return {
        "organization": org_data.get('organization', {}).get('name', 'Unknown'),
        "analysis_timestamp": datetime.now().isoformat(),
        "summary": {
            "total_repositories": len(repositories),
            "total_size_kb": total_size,
            "total_size_formatted": format_size(total_size),
            "private_repos": len([r for r in repositories if r.get('private', False)]),
            "public_repos": len([r for r in repositories if not r.get('private', False)]),
            "archived_repos": len([r for r in repositories if r.get('archived', False)]),
            "forked_repos": len([r for r in repositories if r.get('fork', False)]),
            "languages": languages,
            "most_popular_language": max(languages.items(), key=lambda x: x[1])[0] if languages else "None"
        }
    }