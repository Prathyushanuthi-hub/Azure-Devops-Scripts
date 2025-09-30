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