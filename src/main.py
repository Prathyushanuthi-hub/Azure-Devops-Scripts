import os
import argparse
from dotenv import load_dotenv
from github_api import GitHubAPI
from azure_devops_api import AzureDevOpsAPI
from utils import format_repository_info
from types.index import RepositoryDetails

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='GitHub Organization Repository Scanner')
    parser.add_argument('--org', required=True, help='GitHub organization name')
    parser.add_argument('--azure-project', help='Azure DevOps project name (optional)')
    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    # Initialize API clients
    github_api = GitHubAPI()
    azure_devops_api = AzureDevOpsAPI()

    try:
        # Fetch repositories from GitHub organization
        print(f"Fetching repositories from {args.org}...")
        repositories = github_api.get_organization_repos(args.org)
        print(f"Found {len(repositories)} repositories")

        for repo in repositories:
            print(f"\nProcessing repository: {repo['name']}")
            
            # Get teams and collaborators
            teams = github_api.get_repo_teams(args.org, repo['name'])
            collaborators = github_api.get_repo_collaborators(args.org, repo['name'])

            # Print repository details
            print(f"Repository Size: {repo['size']} KB")
            print(f"Default Branch: {repo['default_branch']}")
            print(f"Teams with access: {len(teams)}")
            print(f"Collaborators: {len(collaborators)}")

            if args.azure_project:
                # Map to Azure DevOps
                azure_devops_api.sync_repository_permissions(
                    project_name=args.azure_project,
                    repo_name=repo['name'],
                    teams=teams,
                    collaborators=collaborators
                )

    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()