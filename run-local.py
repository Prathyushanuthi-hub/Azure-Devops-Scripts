#!/usr/bin/env python3
"""
Local runner for GitHub Organization Analysis
This script runs the analysis locally without needing Azure DevOps pipelines
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_environment():
    """Setup local environment for running the analysis"""
    print("🔧 Setting up local environment...")
    
    # Check if .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found. Please create it from .env.template")
        print("   cp .env.template .env")
        print("   # Then edit .env with your actual tokens")
        return False
    
    # Install dependencies
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    
    return True

def validate_environment():
    """Validate that all required environment variables are set"""
    print("🔍 Validating environment variables...")
    
    required_vars = ['GITHUB_TOKEN', 'GITHUB_ORG', 'AZURE_DEVOPS_TOKEN', 'AZURE_DEVOPS_ORG', 'AZURE_DEVOPS_PROJECT']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("   Please check your .env file")
        return False
    
    print("✅ All environment variables are set")
    return True

def test_github_connection():
    """Test GitHub API connection"""
    print("🔗 Testing GitHub connection...")
    
    try:
        import requests
        token = os.getenv('GITHUB_TOKEN')
        headers = {'Authorization': f'token {token}'}
        response = requests.get('https://api.github.com/user', headers=headers)
        
        if response.status_code == 200:
            user = response.json()
            print(f"✅ GitHub connection successful - authenticated as: {user.get('login', 'Unknown')}")
            return True
        else:
            print(f"❌ GitHub authentication failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ GitHub connection error: {e}")
        return False

def test_azure_devops_connection():
    """Test Azure DevOps API connection"""
    print("🔗 Testing Azure DevOps connection...")
    
    try:
        import requests
        import base64
        
        token = os.getenv('AZURE_DEVOPS_TOKEN')
        org = os.getenv('AZURE_DEVOPS_ORG')
        
        auth = base64.b64encode(f':{token}'.encode()).decode()
        headers = {'Authorization': f'Basic {auth}'}
        response = requests.get(f'https://dev.azure.com/{org}/_apis/projects?api-version=6.0', headers=headers)
        
        if response.status_code == 200:
            projects = response.json().get('value', [])
            print(f"✅ Azure DevOps connection successful - found {len(projects)} projects")
            return True
        else:
            print(f"❌ Azure DevOps authentication failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Azure DevOps connection error: {e}")
        return False

def run_analysis():
    """Run the GitHub organization analysis"""
    print("🚀 Running GitHub Organization Analysis...")
    
    github_org = os.getenv('GITHUB_ORG')
    azure_project = os.getenv('AZURE_DEVOPS_PROJECT')
    
    print(f"   GitHub Organization: {github_org}")
    print(f"   Azure DevOps Project: {azure_project}")
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    try:
        # Run the main analysis script
        cmd = [sys.executable, 'src/main.py', '--org', github_org, '--azure-project', azure_project]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Analysis completed successfully!")
            print("\n📊 Output:")
            print(result.stdout)
            
            # List output files
            output_path = Path('output')
            if output_path.exists():
                output_files = list(output_path.glob('*'))
                if output_files:
                    print(f"\n📁 Generated files in output/:")
                    for file in output_files:
                        print(f"   - {file.name}")
                else:
                    print("   No output files generated")
            
            return True
        else:
            print("❌ Analysis failed!")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return False

def main():
    """Main execution function"""
    print("🎯 GitHub Organization Analysis - Local Runner")
    print("=" * 50)
    
    # Load environment variables from .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("⚠️  python-dotenv not installed. Make sure your environment variables are set manually.")
    
    # Setup and validation steps
    if not setup_environment():
        return 1
    
    if not validate_environment():
        return 1
    
    if not test_github_connection():
        return 1
    
    if not test_azure_devops_connection():
        return 1
    
    # Run the analysis
    if not run_analysis():
        return 1
    
    print("\n🎉 All tasks completed successfully!")
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)