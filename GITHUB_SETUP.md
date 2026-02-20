# GitHub Issues Setup Guide

## Summary
Two scripts are available to create GitHub issues from the pre-generated CSV export:

### Python Script (Recommended - Working ✓)
- **File**: `scripts/github-issues-bulk-create.py`
- **Requirements**: Python 3.x + `requests` library
- **Status**: ✓ Ready to use (requires GitHub token)

### PowerShell Script (Alternative)
- **File**: `scripts/github-issues-bulk-create.ps1`
- **Requirements**: GitHub CLI (`gh`) installed and authenticated
- **Status**: ⚠ Requires GitHub CLI (not installed in current environment)

---

## Quick Start: Python Script

### Setup

**1. Generate GitHub Personal Access Token**
   - Go to: https://github.com/settings/tokens/new
   - Click: "Generate new token (classic)"
   - Name: `FinHub-Issues`
   - Scopes: ✓ `repo` (or minimal: `repo:status`)
   - Click: "Generate token"
   - **Copy the token immediately** (you won't see it again)

**2. Install Python dependencies** (if not already done)
   ```powershell
   pip install requests
   ```

### Usage

**Option A: Set environment variable (recommended)**
```powershell
$env:GITHUB_TOKEN = "ghp_your_token_here"
python scripts/github-issues-bulk-create.py --dry-run --verbose
```

**Option B: Pass token directly**
```powershell
python scripts/github-issues-bulk-create.py --token "ghp_your_token_here" --dry-run --verbose
```

### Steps to Create Issues

1. **Dry Run (Preview - No changes)**
   ```powershell
   $env:GITHUB_TOKEN = "your_token_here"
   python scripts/github-issues-bulk-create.py --dry-run --verbose
   ```
   This shows what would be created without making any changes.

2. **Live Run (Create all issues)**
   ```powershell
   python scripts/github-issues-bulk-create.py
   ```
   This creates all 45+ issues in your GitHub repository.

### Available Parameters

```powershell
python scripts/github-issues-bulk-create.py `
  --csv "documentation/github-issues-export.csv" `  # CSV file path
  --owner "prashdubey" `                            # GitHub username
  --repo "FinHub-Financial-Report" `                # Repository name
  --token "ghp_..." `                               # GitHub token (or use GITHUB_TOKEN env var)
  --dry-run `                                       # Preview only (no changes)
  --verbose                                         # Show detailed output
```

---

## Alternative: PowerShell Script (Requires GitHub CLI)

### Setup

1. **Install GitHub CLI**
   ```powershell
   winget install github-cli
   ```

2. **Authenticate**
   ```powershell
   gh auth login
   ```

3. **Run the script**
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\scripts/github-issues-bulk-create.ps1 -DryRun $false
   ```

---

## Data Format (CSV)

The `documentation/github-issues-export.csv` contains:

| Column | Description | Example |
|--------|-------------|---------|
| `title` | Issue title | `SETUP-01: Initialize Power BI workspace` |
| `body` | Issue description | `Acceptance Criteria: ...` |
| `labels` | Comma-separated labels | `Phase1,Setup,Technical` |
| `assignee` | GitHub username | `prashdubey` |
| `milestone` | Release milestone | `Phase 1` |

---

## Troubleshooting

### "ModuleNotFoundError: requests"
```powershell
pip install requests
```

### "GitHub token not found"
- Set `GITHUB_TOKEN` environment variable, or
- Pass `--token` parameter with your PAT

### "Repository not found or not accessible"
- Verify token has `repo` scope
- Verify owner/repo names are correct
- Token must have permission to create issues in the repository

### "Issue already exists"
- The script skips duplicate titles by default
- Issues with same title won't be created twice

---

## Results

After running the script with `--token` (not `--dry-run`):

✓ 45+ GitHub issues will be created
✓ Issues will have proper labels, milestones, and descriptions
✓ Each issue links back to specification and acceptance criteria
✓ Team can start Phase 1 implementation immediately

---

## Next Steps

1. Generate GitHub PAT (5 minutes)
2. Run Python script with dry-run (2 minutes)
3. Run Python script live to create issues (2 minutes)
4. Review issues in GitHub repository
5. Assign team members to Phase 1 tasks

---

**Questions?** Review the detailed task descriptions in `specs/001-finhub-report/detailed-tasks.md`
