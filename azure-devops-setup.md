# Azure DevOps Setup for GitHub Organization Analysis

## Required Configuration Steps

### 1. Service Connections
Navigate to **Project Settings > Service connections** and create:

#### GitHub Service Connection
- **Name**: `github-org-connection`
- **Type**: GitHub
- **Authentication**: Personal Access Token
- **GitHub PAT Scopes Required**:
  ```
  repo                    # Full control of private repositories
  admin:org              # Full control of orgs and teams, read org projects
  read:user              # Read access to user profile data
  read:discussion        # Read discussions
  user:email             # Access user email addresses (read-only)
  ```

### 2. Variable Groups
Create Variable Group: **`github-org-secrets`**

| Variable Name | Value | Is Secret |
|---------------|-------|-----------|
| GITHUB_TOKEN | `your-github-pat` | ✅ Yes |
| AZURE_DEVOPS_TOKEN | `your-azure-devops-pat` | ✅ Yes |
| GITHUB_ORG | `your-org-name` | ❌ No |
| AZURE_DEVOPS_ORG | `your-azure-org` | ❌ No |
| AZURE_DEVOPS_PROJECT | `your-project-name` | ❌ No |

### 3. Azure DevOps Permissions
Ensure your Azure DevOps PAT has these scopes:
- **Project and Team**: Read & Write
- **Graph (Identity)**: Read
- **User Entitlements**: Read
- **Security**: Read

### 4. GitHub Organization Permissions
Your GitHub PAT needs:
- **Organization member** with admin privileges OR
- **Organization owner** access
- Access to **Teams** and **Repository** management

## Environment Variables for Local Development

Create `.env` file:
```env
GITHUB_TOKEN=your_github_personal_access_token
AZURE_DEVOPS_TOKEN=your_azure_devops_personal_access_token
GITHUB_ORG=your_organization_name
AZURE_DEVOPS_ORG=your_azure_devops_organization
AZURE_DEVOPS_PROJECT=your_azure_devops_project_name
```

## Pipeline Setup

### Basic Pipeline Structure
```yaml
trigger:
- main

variables:
- group: github-org-secrets

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.x'

- script: |
    pip install -r requirements.txt
  displayName: 'Install dependencies'

- script: |
    python src/main.py --org $(GITHUB_ORG) --azure-project $(AZURE_DEVOPS_PROJECT)
  displayName: 'Analyze GitHub Organization'
  env:
    GITHUB_TOKEN: $(GITHUB_TOKEN)
    AZURE_DEVOPS_TOKEN: $(AZURE_DEVOPS_TOKEN)
```

## API Endpoints Your Scripts Will Use

### GitHub APIs
- **Organizations**: `GET /orgs/{org}`
- **Repositories**: `GET /orgs/{org}/repos`
- **Teams**: `GET /orgs/{org}/teams`
- **Members**: `GET /orgs/{org}/members`
- **Repository Teams**: `GET /repos/{owner}/{repo}/teams`
- **Repository Collaborators**: `GET /repos/{owner}/{repo}/collaborators`

### Azure DevOps APIs
- **Projects**: `GET https://dev.azure.com/{organization}/_apis/projects`
- **Teams**: `GET https://dev.azure.com/{organization}/{project}/_apis/projects/{project}/teams`
- **Users**: `GET https://dev.azure.com/{organization}/_apis/userentitlements`
- **Repositories**: `GET https://dev.azure.com/{organization}/{project}/_apis/git/repositories`

## Security Best Practices

1. **Never commit tokens** to source control
2. **Use Variable Groups** for sensitive data in pipelines
3. **Rotate tokens** regularly (every 90 days)
4. **Use minimal required scopes** for tokens
5. **Enable audit logging** for both GitHub and Azure DevOps
6. **Use service principals** for production environments

## Troubleshooting Common Issues

### Authentication Errors
- Verify token scopes match requirements
- Check token expiration dates
- Ensure service account has proper org permissions

### API Rate Limits
- GitHub: 5,000 requests/hour for authenticated requests
- Azure DevOps: No published limits but implement retry logic
- Consider implementing caching for large organizations

### Permission Issues
- Ensure Azure DevOps user has project admin rights
- Verify GitHub token has org admin or owner permissions
- Check that target Azure DevOps project exists

## Data Flow Architecture

```
GitHub Organization
    ↓ (GitHub API)
Python Scripts
    ↓ (Processing)
Azure DevOps
    ↓ (Azure DevOps API)
Teams, Users, Projects
```

## Next Steps After Setup

1. **Test authentication** with both APIs
2. **Run scripts locally** with `.env` file
3. **Create Azure DevOps pipeline** using the YAML
4. **Schedule pipeline** to run periodically
5. **Set up monitoring** and alerting for failed runs