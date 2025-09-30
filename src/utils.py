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