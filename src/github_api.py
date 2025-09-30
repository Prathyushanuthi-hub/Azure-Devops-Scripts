import requests

GITHUB_API_URL = "https://api.github.com"
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
}

def list_repositories(org_name):
    url = f"{GITHUB_API_URL}/orgs/{org_name}/repos"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_repository_details(repo_full_name):
    url = f"{GITHUB_API_URL}/repos/{repo_full_name}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_repository_size(repo_full_name):
    repo_details = get_repository_details(repo_full_name)
    return repo_details.get('size', 0)

def check_repositories(org_name):
    repos = list_repositories(org_name)
    repo_info = []
    for repo in repos:
        full_name = repo['full_name']
        size = get_repository_size(full_name)
        repo_info.append({
            'name': repo['name'],
            'full_name': full_name,
            'size': size,
            'url': repo['html_url'],
            'description': repo['description'],
        })
    return repo_info