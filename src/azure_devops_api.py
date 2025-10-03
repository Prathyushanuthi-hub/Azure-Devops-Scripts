import os
import requests
import base64
from typing import List, Dict, Any

class AzureDevOpsAPI:
    def __init__(self):
        self.api_version = "6.0"
        self.token = os.getenv('AZURE_DEVOPS_TOKEN')
        self.organization = os.getenv('AZURE_DEVOPS_ORG')
        
        if not self.token:
            raise ValueError("AZURE_DEVOPS_TOKEN environment variable is required")
        if not self.organization:
            raise ValueError("AZURE_DEVOPS_ORG environment variable is required")
        
        # Create Basic auth header
        auth_string = f":{self.token}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {auth_b64}',
            'Accept': 'application/json'
        }
        
        self.base_url = f"https://dev.azure.com/{self.organization}"

    def get_projects(self) -> List[Dict[str, Any]]:
        """Get all projects in the organization"""
        url = f"{self.base_url}/_apis/projects?api-version={self.api_version}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get('value', [])

    def get_teams(self, project_name: str) -> List[Dict[str, Any]]:
        """Get all teams in a project"""
        url = f"{self.base_url}/{project_name}/_apis/projects/{project_name}/teams?api-version={self.api_version}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json().get('value', [])
        except requests.exceptions.RequestException as e:
            print(f"Warning: Could not fetch teams for project {project_name}: {e}")
            return []

    def get_users(self) -> List[Dict[str, Any]]:
        """Get all users in the organization"""
        url = f"{self.base_url}/_apis/userentitlements?api-version={self.api_version}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json().get('value', [])
        except requests.exceptions.RequestException as e:
            print(f"Warning: Could not fetch users: {e}")
            return []

    def sync_repository_permissions(self, project_name: str, repo_name: str, teams: List[Dict], collaborators: List[Dict]):
        """Sync repository permissions - placeholder implementation"""
        print(f"Syncing permissions for repository: {repo_name}")
        print(f"  Teams: {len(teams)}")
        print(f"  Collaborators: {len(collaborators)}")
        
        # TODO: Implement actual permission synchronization logic
        # This would involve creating/updating teams and user permissions in Azure DevOps
        return True

    def create_or_update_team(self, project_name: str, team_name: str, description: str = "") -> Dict[str, Any]:
        """Create or update a team in Azure DevOps"""
        # Check if team exists
        teams = self.get_teams(project_name)
        existing_team = next((team for team in teams if team['name'] == team_name), None)
        
        if existing_team:
            print(f"Team '{team_name}' already exists")
            return existing_team
        
        # Create new team
        url = f"{self.base_url}/{project_name}/_apis/projects/{project_name}/teams?api-version={self.api_version}"
        data = {
            "name": team_name,
            "description": description
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            print(f"Created team: {team_name}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating team {team_name}: {e}")
            return {}

# Legacy functions for backward compatibility
def add_repository_to_team(organization, project, team, repository, pat):
    import requests

    url = f"https://dev.azure.com/{organization}/{project}/_apis/projects/{project}/teams/{team}/repositories/{repository}?api-version=6.0"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {pat}'
    }

    response = requests.put(url, headers=headers)

    if response.status_code == 200:
        return True
    else:
        return False


def add_repository_to_user(organization, user_id, repository, pat):
    import requests

    url = f"https://dev.azure.com/{organization}/_apis/userentitlements/{user_id}/repositories/{repository}?api-version=6.0"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {pat}'
    }

    response = requests.put(url, headers=headers)

    if response.status_code == 200:
        return True
    else:
        return False


def get_azure_devops_teams(organization, project, pat):
    import requests

    url = f"https://dev.azure.com/{organization}/{project}/_apis/projects/{project}/teams?api-version=6.0"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {pat}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()['value']
    else:
        return None


def get_azure_devops_users(organization, project, pat):
    import requests

    url = f"https://dev.azure.com/{organization}/_apis/userentitlements?api-version=6.0"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {pat}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()['value']
    else:
        return None