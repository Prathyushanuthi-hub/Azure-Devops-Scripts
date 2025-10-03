# Variable Group Authorization Guide

## Method 1: During Pipeline Run (Easiest)
1. Run your pipeline with the Variable Group reference
2. When it fails with authorization error, look for:
   - "Authorize resources" button in the pipeline run log
   - Click the button to grant access
3. Rerun the pipeline

## Method 2: Pre-authorize via UI
1. Go to Pipelines → Library → github-org-secrets
2. Click "Security" tab
3. Click "+ Add" 
4. Add these accounts with "User" role:
   - [YourProject] Build Service ([YourOrganization])
   - Project Collection Build Service ([YourOrganization])

## Method 3: Pipeline Settings
1. Go to Pipelines → Pipelines → [Your Pipeline]
2. Click "Edit" → "..." → "Settings"
3. Under "Security", enable:
   - "Limit job authorization scope to current project for non-release pipelines"
4. Add Variable Group permissions

## Method 4: Organization Settings (Admin required)
1. Go to Organization Settings → Pipelines → Settings
2. Under "Security":
   - Enable "Limit job authorization scope to current project for non-release pipelines"
   - Disable "Protect access to repositories in YAML pipelines"
3. This allows broader access but less secure

## Verification Steps
After authorization:
1. Edit your pipeline
2. Look for Variable Group in the "Variables" section
3. Should show "github-org-secrets" with a green checkmark
4. Save and run pipeline

## Troubleshooting
- Make sure Variable Group name exactly matches: "github-org-secrets"
- Ensure you have "Contributor" role in the project
- Check that all variables in the group are properly defined
- Verify secret variables are marked as secrets