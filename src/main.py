import os
import argparse
import json
from dotenv import load_dotenv
from github_api import GitHubAPI
from azure_devops_api import AzureDevOpsAPI
from utils import format_repository_info, save_to_json, create_summary_report
from types.index import RepositoryDetails

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='GitHub Organization Repository Scanner')
    parser.add_argument('--org', required=True, help='GitHub organization name')
    parser.add_argument('--azure-project', help='Azure DevOps project name (optional)')
    parser.add_argument('--output-dir', default='output', help='Output directory for reports')
    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    print(f"🚀 Starting GitHub Organization Analysis")
    print(f"Organization: {args.org}")
    print(f"Azure DevOps Project: {args.azure_project or 'None'}")
    print("-" * 50)

    try:
        # Initialize API clients
        print("🔧 Initializing API clients...")
        github_api = GitHubAPI()
        azure_devops_api = AzureDevOpsAPI() if args.azure_project else None

        # Get organization details
        print(f"📋 Fetching organization details for '{args.org}'...")
        org_details = github_api.get_organization_details(args.org)
        print(f"Organization: {org_details.get('name', args.org)}")
        print(f"Description: {org_details.get('description', 'No description')}")
        print(f"Public repos: {org_details.get('public_repos', 0)}")
        print(f"Total repos: {org_details.get('total_private_repos', 0) + org_details.get('public_repos', 0)}")

        # Fetch repositories from GitHub organization
        print(f"\n📂 Fetching repositories from {args.org}...")
        repositories = github_api.get_organization_repos(args.org)
        print(f"Found {len(repositories)} repositories")

        # Get organization members and teams
        print(f"\n👥 Fetching organization members...")
        members = github_api.get_organization_members(args.org)
        print(f"Found {len(members)} members")

        print(f"\n👤 Fetching organization teams...")
        teams = github_api.get_organization_teams(args.org)
        print(f"Found {len(teams)} teams")

        # Process each repository
        repo_details = []
        for i, repo in enumerate(repositories, 1):
            print(f"\n📄 Processing repository {i}/{len(repositories)}: {repo['name']}")
            
            # Get teams and collaborators for this repo
            repo_teams = github_api.get_repo_teams(args.org, repo['name'])
            collaborators = github_api.get_repo_collaborators(args.org, repo['name'])

            # Format repository information
            repo_info = format_repository_info(repo)
            repo_info['teams'] = repo_teams
            repo_info['collaborators'] = collaborators
            repo_info['team_count'] = len(repo_teams)
            repo_info['collaborator_count'] = len(collaborators)
            
            repo_details.append(repo_info)

            # Print repository details
            print(f"   Size: {repo_info['size']} KB")
            print(f"   Language: {repo_info['language']}")
            print(f"   Private: {repo_info['private']}")
            print(f"   Teams with access: {len(repo_teams)}")
            print(f"   Collaborators: {len(collaborators)}")

            # Azure DevOps integration
            if azure_devops_api and args.azure_project:
                try:
                    azure_devops_api.sync_repository_permissions(
                        project_name=args.azure_project,
                        repo_name=repo['name'],
                        teams=repo_teams,
                        collaborators=collaborators
                    )
                except Exception as e:
                    print(f"   ⚠️  Azure DevOps sync warning: {e}")

        # Create comprehensive report
        print(f"\n📊 Generating analysis report...")
        analysis_data = {
            'organization': org_details,
            'repositories': repo_details,
            'members': members,
            'teams': teams,
            'analysis_metadata': {
                'total_repositories': len(repositories),
                'total_members': len(members),
                'total_teams': len(teams),
                'github_org': args.org,
                'azure_project': args.azure_project
            }
        }

        # Save detailed report
        os.makedirs(args.output_dir, exist_ok=True)
        detailed_report_path = save_to_json(analysis_data, f"{args.org}_detailed_analysis.json", args.output_dir)
        print(f"✅ Detailed report saved: {detailed_report_path}")

        # Create summary report
        summary_report = create_summary_report(analysis_data)
        summary_report_path = save_to_json(summary_report, f"{args.org}_summary.json", args.output_dir)
        print(f"✅ Summary report saved: {summary_report_path}")

        # Print summary to console
        print(f"\n📈 Analysis Summary:")
        print(f"   Organization: {summary_report['organization']}")
        print(f"   Total Repositories: {summary_report['summary']['total_repositories']}")
        print(f"   Total Size: {summary_report['summary']['total_size_formatted']}")
        print(f"   Public Repos: {summary_report['summary']['public_repos']}")
        print(f"   Private Repos: {summary_report['summary']['private_repos']}")
        print(f"   Most Popular Language: {summary_report['summary']['most_popular_language']}")

        print(f"\n🎉 Analysis completed successfully!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()