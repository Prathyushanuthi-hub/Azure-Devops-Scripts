# GitHub Organization Analysis - Windows PowerShell Runner
# This script runs the analysis locally on Windows without Azure DevOps pipelines

param(
    [string]$GitHubOrg = "",
    [string]$AzureProject = "",
    [switch]$SkipValidation = $false
)

Write-Host "🎯 GitHub Organization Analysis - Windows Runner" -ForegroundColor Green
Write-Host "=" * 50

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found" -ForegroundColor Red
    Write-Host "Please create .env file from template:" -ForegroundColor Yellow
    Write-Host "   Copy-Item .env.template .env" -ForegroundColor Yellow
    Write-Host "   # Then edit .env with your actual tokens" -ForegroundColor Yellow
    exit 1
}

# Load environment variables from .env file
Write-Host "📄 Loading environment variables from .env..." -ForegroundColor Blue
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^#][^=]+)=(.*)$') {
        [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process')
    }
}

# Override with parameters if provided
if ($GitHubOrg) {
    [System.Environment]::SetEnvironmentVariable('GITHUB_ORG', $GitHubOrg, 'Process')
}
if ($AzureProject) {
    [System.Environment]::SetEnvironmentVariable('AZURE_DEVOPS_PROJECT', $AzureProject, 'Process')
}

# Validate required environment variables
Write-Host "🔍 Validating environment variables..." -ForegroundColor Blue
$requiredVars = @('GITHUB_TOKEN', 'GITHUB_ORG', 'AZURE_DEVOPS_TOKEN', 'AZURE_DEVOPS_ORG', 'AZURE_DEVOPS_PROJECT')
$missingVars = @()

foreach ($var in $requiredVars) {
    if (-not [System.Environment]::GetEnvironmentVariable($var)) {
        $missingVars += $var
    }
}

if ($missingVars.Count -gt 0) {
    Write-Host "❌ Missing environment variables: $($missingVars -join ', ')" -ForegroundColor Red
    Write-Host "Please check your .env file" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ All environment variables are set" -ForegroundColor Green

# Install dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Blue
try {
    python -m pip install --upgrade pip --quiet
    python -m pip install -r requirements.txt --quiet
    Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
}
catch {
    Write-Host "❌ Failed to install dependencies: $_" -ForegroundColor Red
    exit 1
}

# Test GitHub connection (if not skipping validation)
if (-not $SkipValidation) {
    Write-Host "🔗 Testing GitHub connection..." -ForegroundColor Blue
    $gitHubTest = python -c @"
import os
import requests
token = os.environ.get('GITHUB_TOKEN')
headers = {'Authorization': f'token {token}'}
response = requests.get('https://api.github.com/user', headers=headers)
if response.status_code == 200:
    user = response.json()
    print(f"✅ GitHub connection successful - authenticated as: {user.get('login', 'Unknown')}")
    exit(0)
else:
    print(f"❌ GitHub authentication failed: {response.status_code}")
    exit(1)
"@

    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ GitHub connection test failed" -ForegroundColor Red
        exit 1
    }

    # Test Azure DevOps connection
    Write-Host "🔗 Testing Azure DevOps connection..." -ForegroundColor Blue
    $azureTest = python -c @"
import os
import requests
import base64
token = os.environ.get('AZURE_DEVOPS_TOKEN')
org = os.environ.get('AZURE_DEVOPS_ORG')
auth = base64.b64encode(f':{token}'.encode()).decode()
headers = {'Authorization': f'Basic {auth}'}
response = requests.get(f'https://dev.azure.com/{org}/_apis/projects?api-version=6.0', headers=headers)
if response.status_code == 200:
    projects = response.json().get('value', [])
    print(f"✅ Azure DevOps connection successful - found {len(projects)} projects")
    exit(0)
else:
    print(f"❌ Azure DevOps authentication failed: {response.status_code}")
    exit(1)
"@

    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Azure DevOps connection test failed" -ForegroundColor Red
        exit 1
    }
}

# Create output directory
if (-not (Test-Path "output")) {
    New-Item -ItemType Directory -Path "output" | Out-Null
}

# Run the analysis
Write-Host "🚀 Running GitHub Organization Analysis..." -ForegroundColor Blue
$org = [System.Environment]::GetEnvironmentVariable('GITHUB_ORG')
$project = [System.Environment]::GetEnvironmentVariable('AZURE_DEVOPS_PROJECT')

Write-Host "   GitHub Organization: $org" -ForegroundColor Cyan
Write-Host "   Azure DevOps Project: $project" -ForegroundColor Cyan

try {
    python src/main.py --org "$org" --azure-project "$project"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Analysis completed successfully!" -ForegroundColor Green
        
        # List output files
        $outputFiles = Get-ChildItem "output" -ErrorAction SilentlyContinue
        if ($outputFiles) {
            Write-Host "`n📁 Generated files in output/:" -ForegroundColor Blue
            foreach ($file in $outputFiles) {
                Write-Host "   - $($file.Name)" -ForegroundColor Gray
            }
        } else {
            Write-Host "   No output files generated" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ Analysis failed with exit code: $LASTEXITCODE" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "❌ Analysis error: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`n🎉 All tasks completed successfully!" -ForegroundColor Green