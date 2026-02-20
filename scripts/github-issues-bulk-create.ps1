<#
.SYNOPSIS
Bulk create GitHub issues from CSV using GitHub CLI

.DESCRIPTION
Reads task data from CSV export and creates GitHub issues with proper labels, 
milestones, and metadata. Supports dry-run mode for validation.

.PARAMETER CsvPath
Path to CSV file with task data (default: documentation/github-issues-export.csv)

.PARAMETER DryRun
If $true, prints what would be created without actually creating issues

.PARAMETER SkipExisting
If $true, skips creating issues if title already exists in repo

.PARAMETER Verbose
Show detailed output for each issue created

.EXAMPLE
.\github-issues-bulk-create.ps1 -CsvPath "documentation/github-issues-export.csv" -DryRun $true

.EXAMPLE
.\github-issues-bulk-create.ps1 -CsvPath "documentation/github-issues-export.csv" -DryRun $false -Verbose $true

.NOTES
Requires GitHub CLI (gh) to be installed and authenticated.
Install: winget install github-cli
Authenticate: gh auth login
#>

param(
    [string]$CsvPath = "documentation/github-issues-export.csv",
    [bool]$DryRun = $true,
    [bool]$SkipExisting = $true,
    [bool]$Verbose = $false
)

# Color output helpers
function Write-Success {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Green
}

function Write-Error_ {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Cyan
}

function Write-Warning_ {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Yellow
}

function Write-Debug_ {
    param([string]$Message)
    if ($Verbose) {
        Write-Host $Message -ForegroundColor Gray
    }
}

try {
    Write-Info "========================================="
    Write-Info "GitHub Issues Bulk Creator"
    Write-Info "========================================="
    Write-Info ""

    # Step 1: Verify GitHub CLI
    Write-Info "[1/5] Verifying GitHub CLI installation..."
    try {
        $ghVersion = gh --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Success "✓ GitHub CLI found"
        }
        else {
            Write-Error_ "✗ GitHub CLI not found or not authenticated"
            Write-Info "  Install: winget install github-cli"
            Write-Info "  Auth: gh auth login"
            exit 1
        }
    }
    catch {
        Write-Error_ "✗ Error checking GitHub CLI: $_"
        exit 1
    }

    # Step 2: Verify CSV file
    Write-Info "[2/5] Verifying CSV file..."
    if (-not (Test-Path $CsvPath)) {
        Write-Error_ "✗ CSV file not found: $CsvPath"
        Write-Info "  Expected path: documentation/github-issues-export.csv"
        exit 1
    }
    
    try {
        $tasks = Import-Csv $CsvPath
        Write-Success "✓ CSV loaded: $($tasks.Count) tasks found"
    }
    catch {
        Write-Error_ "✗ Error loading CSV: $_"
        exit 1
    }

    # Step 3: Get repository info
    Write-Info "[3/5] Verifying GitHub repository..."
    try {
        $repoInfo = gh repo view --json nameWithOwner 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Success "✓ Repository accessible"
        }
        else {
            Write-Error_ "✗ Not in a GitHub repository or not authenticated"
            exit 1
        }
    }
    catch {
        Write-Error_ "✗ Error accessing repository: $_"
        exit 1
    }

    # Step 4 (Optional): Fetch existing issues if skip enabled
    if ($SkipExisting) {
        Write-Info "[4/5] Fetching existing issues..."
        try {
            $existingIssues = gh issue list --all --json title --jq '.[] | .title' 2>$null
            $existingCount = @($existingIssues).Count
            Write-Success "✓ Found $existingCount existing issues"
        }
        catch {
            Write-Warning_ "⚠ Could not fetch existing issues; continuing without skip"
            $existingIssues = @()
        }
    }

    # Step 5: Create issues
    Write-Info "[5/5] Creating issues from CSV..."
    Write-Info ""
    
    $created = 0
    $skipped = 0
    $failed = 0
    $errors = @()

    foreach ($task in $tasks) {
        $title = $task.title
        $body = $task.body
        $labels = $task.labels
        $assignee = $task.assignee
        $milestone = $task.milestone

        # Skip if exists
        if ($SkipExisting -and $existingIssues -contains $title) {
            Write-Warning_ "⊘ Skipping (exists): $title"
            Write-Debug_ "  Labels: $labels"
            $skipped++
            continue
        }

        # Build command
        $createCmd = @("create")
        $createCmd += @("--title", $title)
        $createCmd += @("--body", $body)
        if ($labels) {
            $createCmd += @("--label", $labels)
        }
        if ($assignee -and $assignee -ne "") {
            $createCmd += @("--assignee", $assignee)
        }
        if ($milestone -and $milestone -ne "") {
            $createCmd += @("--milestone", $milestone)
        }

        if ($DryRun) {
            Write-Info "DRY RUN: $title"
            Write-Debug_ "  Body: $($body.Substring(0, [Math]::Min(60, $body.Length)))..."
            Write-Debug_ "  Labels: $labels"
            Write-Debug_ "  Assignee: $assignee"
            Write-Debug_ "  Milestone: $milestone"
            Write-Debug_ ""
            $created++
        }
        else {
            try {
                Write-Info "Creating: $title"
                $output = gh issue $createCmd 2>&1
                if ($LASTEXITCODE -eq 0) {
                    Write-Success "  ✓ Created successfully"
                    Write-Debug_ "  Output: $output"
                    $created++
                }
                else {
                    Write-Error_ "  ✗ Failed"
                    $failed++
                    $errors += @{
                        Title = $title
                        Error = $output
                    }
                }
            }
            catch {
                Write-Error_ "  ✗ Exception: $_"
                $failed++
                $errors += @{
                    Title = $title
                    Error = $_
                }
            }
        }
    }

    # Result summary
    Write-Info ""
    Write-Info "========================================="
    Write-Info "SUMMARY"
    Write-Info "========================================="
    Write-Success "✓ Created:  $created"
    Write-Warning_ "⊘ Skipped:  $skipped"
    Write-Error_ "✗ Failed:   $failed"
    Write-Info "  Total:    $($tasks.Count)"
    Write-Info ""

    if ($DryRun) {
        Write-Warning_ "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        Write-Warning_ "DRY RUN MODE: No issues were created"
        Write-Warning_ "Re-run with -DryRun \$false to create issues"
        Write-Warning_ "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    }

    if ($errors.Count -gt 0) {
        Write-Error_ ""
        Write-Error_ "ERRORS:"
        foreach ($err in $errors) {
            Write-Error_ "  Title: $($err.Title)"
            Write-Error_ "  Error: $($err.Error)"
        }
    }

    # Exit code
    if ($failed -gt 0) {
        exit 1
    }
    else {
        exit 0
    }
}
catch {
    Write-Error_ "Fatal error: $_"
    exit 1
}
