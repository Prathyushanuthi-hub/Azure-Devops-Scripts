# Azure DevOps CLI Commands for Variable Group Setup

# Login to Azure DevOps
az devops login

# Set default organization and project
az devops configure --defaults organization=https://dev.azure.com/your-organization project=your-project

# Create Variable Group
az pipelines variable-group create --name "github-org-secrets" --variables GITHUB_ORG="Canarys Playground" AZURE_DEVOPS_ORG="your-org" AZURE_DEVOPS_PROJECT="Organization details"

# Add secret variables (you'll be prompted to enter values)
az pipelines variable-group variable create --group-id {group-id} --name GITHUB_TOKEN --secret true
az pipelines variable-group variable create --group-id {group-id} --name AZURE_DEVOPS_TOKEN --secret true

# Create pipeline from YAML
az pipelines create --name "GitHub-Org-Analysis" --yml-path azure-pipelines.yml --repository https://github.com/Prathyushanuthi-hub/Azure-Devops-Scripts --branch main