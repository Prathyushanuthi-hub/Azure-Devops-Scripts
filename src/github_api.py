import os
import requests
from typing import List, Dict, Any

class GitHubAPI:
    def __init__(self):
        self.api_url = "https://api.github.com"
        self.token = os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self.token}",
            "User-Agent": "GitHub-Org-Checker/1.0"
        }

    def get_organization_repos(self, org_name: str) -> List[Dict[str, Any]]:
        """Get all repositories from a GitHub organization"""
        url = f"{self.api_url}/orgs/{org_name}/repos"
        params = {
            'type': 'all',
            'sort': 'name',
            'per_page': 100
        }
        
        all_repos = []
        page = 1
        
        while True:
            params['page'] = page
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            repos = response.json()
            if not repos:
                break
                
            all_repos.extend(repos)
            page += 1
            
            # GitHub API pagination limit
            if page > 10:  # Safety limit
                break
                
        return all_repos

    def get_repo_teams(self, org_name: str, repo_name: str) -> List[Dict[str, Any]]:
        """Get teams with access to a repository"""
        url = f"{self.api_url}/repos/{org_name}/{repo_name}/teams"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Warning: Could not fetch teams for {repo_name}: {e}")
            return []

    def get_repo_collaborators(self, org_name: str, repo_name: str) -> List[Dict[str, Any]]:
        """Get collaborators for a repository"""
        url = f"{self.api_url}/repos/{org_name}/{repo_name}/collaborators"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Warning: Could not fetch collaborators for {repo_name}: {e}")
            return []

    def get_organization_details(self, org_name: str) -> Dict[str, Any]:
        """Get organization details"""
        url = f"{self.api_url}/orgs/{org_name}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_organization_members(self, org_name: str) -> List[Dict[str, Any]]:
        """Get all members of an organization"""
        url = f"{self.api_url}/orgs/{org_name}/members"
        params = {'per_page': 100}
        
        all_members = []
        page = 1
        
        while True:
            params['page'] = page
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            members = response.json()
            if not members:
                break
                
            all_members.extend(members)
            page += 1
            
        return all_members

    def get_organization_teams(self, org_name: str) -> List[Dict[str, Any]]:
        """Get all teams in an organization"""
        url = f"{self.api_url}/orgs/{org_name}/teams"
        params = {'per_page': 100}
        
        all_teams = []
        page = 1
        
        while True:
            params['page'] = page
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            teams = response.json()
            if not teams:
                break
                
            all_teams.extend(teams)
            page += 1
            
        return all_teams

# Legacy functions for backward compatibility
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