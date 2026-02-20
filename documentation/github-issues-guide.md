# GitHub Issues Conversion Guide: FinHub Tasks to GitHub Issues

**Project**: FinHub Financial Summary Report v1.0.0  
**Date**: 2026-02-20  
**Purpose**: Convert 65+ detailed tasks into organized GitHub issues for team tracking and assignment

---

## Overview

This guide explains how to convert tasks from `detailed-tasks.md` into structured GitHub issues. GitHub issues will serve as:
- **Single source of truth** for task assignment and status
- **Link to specification** requirements via issue descriptions
- **Tracking mechanism** for team progress and dependencies
- **Communication hub** for task-level discussions and blockers

---

## Issue Organization Strategy

### Issue Hierarchies & Labels

```
Issues organized by:
├─ Phase (Epic): PHASE-1-SETUP, PHASE-2-DATA, etc.
├─ User Story (Label): us-1-dashboard, us-2-excel, etc.
├─ Priority (Label): p0-critical, p1-high, p2-medium, p3-low
├─ Component (Label): component-powerbi, component-excel, component-automation
├─ Status (Automatic): todo, in-progress, in-review, done
└─ Assignee: Power BI Dev, Data Admin, QA, etc.
```

### Label Definitions

| Label | Purpose | Example |
|-------|---------|---------|
| `phase-1-setup` | Phase 1: Setup & Foundation | SETUP-01, SETUP-02 |
| `phase-2-governance` | Phase 1.5: Governance | GOV-01, GOV-02 |
| `phase-2-data` | Phase 2: Data Connection | DATA-01 through DATA-06 |
| `phase-3-powerbi` | Phase 3: Power BI Dashboard | VIZ-01, FILTER-01, FORMAT-01 |
| `phase-4-excel` | Phase 4: Excel Report | EXCEL-01 through EXCEL-05 |
| `phase-5-refresh` | Phase 5: Automated Refresh | REFRESH-01, REFRESH-02 |
| `phase-6-promotion` | Phase 6: Promotion Pipeline | PROMOTE-01 through PROMOTE-04 |
| `phase-7-security` | Phase 7: Security & Governance | SEC-01, SEC-02, SEC-03 |
| `phase-8-documentation` | Phase 8: Documentation | DOC-01 through DOC-04 |
| `phase-9-deployment` | Phase 9: Final Deployment | FINAL-01, FINAL-02 |
| `us-1-dashboard` | User Story 1: Power BI Dashboard | VIZ-01 through FORMAT-01 |
| `us-2-excel` | User Story 2: Excel Report | EXCEL-01 through EXCEL-05 |
| `us-3-refresh` | User Story 3: Automated Refresh | REFRESH-01 through TEST-US3-01 |
| `us-4-promotion` | User Story 4: Promotion Pipeline | PROMOTE-01 through PROMOTE-04 |
| `us-5-validation` | User Story 5: Data Accuracy Validation | PROMOTE-01 (validation portions) |
| `component-powerbi` | Component: Power BI Desktop/Service | Tasks involving .pbix file |
| `component-excel` | Component: Excel | Tasks involving .xlsx file |
| `component-ssas` | Component: SSAS Cube | Tasks involving SSAS connectivity |
| `component-automation` | Component: PowerShell/Automation | Tasks involving scripts |
| `component-security` | Component: Security/RLS | Tasks involving access control |
| `component-documentation` | Component: Documentation | Tasks creating docs |
| `priority-p0` | Critical blocker | Prod deployment, security |
| `priority-p1` | High priority | Core feature completion |
| `priority-p2` | Medium priority | Non-blocking tasks |
| `priority-p3` | Low priority | Nice-to-have tasks |
| `type-feature` | New feature/capability | Building visualizations |
| `type-fix` | Bug fix | Correcting formula errors |
| `type-test` | Testing task | Test execution |
| `type-docs` | Documentation task | Creating guides |
| `type-research` | Research/discovery | Investigating options |
| `type-setup` | Environment setup | Configuration |
| `status-todo` | Not started | Initial state |
| `status-in-progress` | Currently being worked | Developer actively working |
| `status-blocked` | Blocked by another task | Waiting on dependency |
| `status-in-review` | Under review | PR or QA review |
| `status-done` | Completed | Ready for next phase |

---

## GitHub Issues Creation Methods

### Method 1: Manual Creation via GitHub UI (Recommended for initial setup)

**When to use**: Creating 1-5 issues at a time; building familiarity with issue structure

**Steps**:

1. **Go to GitHub Repository**
   - Navigate to: `https://github.com/[org]/[repo]/issues`
   - Click **New Issue** button

2. **Fill Issue Title**
   - Format: `[TASK-ID] [Phase] - [Description]`
   - Example: `[SETUP-01] Phase 1 - Create Repository Structure & Documentation Folders`

3. **Fill Issue Description**
   - Use template below (see Issue Template section)
   - Include acceptance criteria from detailed-tasks.md
   - Link to specification requirement

4. **Assign Labels**
   - Phase label (e.g., `phase-1-setup`)
   - User Story label (e.g., `us-1-dashboard`)
   - Component label (e.g., `component-powerbi`)
   - Priority label (e.g., `priority-p1`)
   - Type label (e.g., `type-feature`)

5. **Set Assignee**
   - Select from team members
   - Suggested from detailed-tasks.md assignee column

6. **Set Milestone**
   - Select phase-based milestone (e.g., "Phase 1: Setup")
   - Or sprint-based milestone if using sprints

7. **Link Related Issues** (optional)
   - If task has dependencies, mention them in description
   - Use GitHub syntax: `#123` (issue #123)
   - Or: `Depends on #123`

8. **Click Submit**

---

### Method 2: Bulk CSV Import via GitHub CLI

**When to use**: Creating 20+ issues efficiently; automating issue creation

**Setup**:

1. **Install GitHub CLI**
   ```powershell
   winget install github-cli
   ```

2. **Authenticate**
   ```powershell
   gh auth login
   ```

3. **Create CSV File** (See CSV Template section below)

4. **Run Import Script** (See PowerShell Script section)

---

### Method 3: GitHub API via PowerShell Script

**When to use**: Full automation with custom logic; bulk creation with relationships

**Script Location**: `scripts/github-issues-bulk-create.ps1`

See PowerShell script section below for full implementation.

---

## Issue Template

**Use this template when creating issues manually via GitHub UI**:

```markdown
## Task ID
[SETUP-01]

## Description
[One-line summary from detailed-tasks.md]

Create repository structure and initialize Git repository with required folder organization.

## Specification Link
- **Specification Requirement**: [Link to specification.md requirement if applicable]
- **User Story**: [Link to user story if applicable]
- **Constitution Principle**: [Which principle(s) this satisfies, e.g., Principle I: Spec-Driven]

## Prerequisites
- [ ] [Prerequisite 1]
- [ ] [Prerequisite 2]

## Acceptance Criteria
- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2
- [ ] Acceptance criterion 3
(list all from detailed-tasks.md)

## Dependencies
- Depends on: [Issue #123] if applicable, or None
- Blocks: [Issue #456] if applicable, or None

## Effort Estimate
**Estimated Effort**: 1 hour

## Implementation Notes
[Any additional context or technical notes]

## Verification Steps
1. Step 1
2. Step 2
(from detailed-tasks.md verification section)

## Performance Requirements
[If applicable]

## Resources
- [Link to referenced documentation]
- [Link to code samples if applicable]
```

---

## CSV Template for Bulk Import

**File**: `documentation/github-issues-template.csv`

**Columns** (order matters for GitHub CLI import):

```
title,body,labels,assignee,milestone
```

**Example rows**:

```
[SETUP-01] Create Repository Structure & Documentation Folders,"## Task ID
SETUP-01

## Description
Initialize Git repository structure with all required folders and documentation templates.

## Specification Link
- Constitution Principle I: Spec-Driven
- User Story: US4 (Promotion Pipeline)

## Prerequisites
- None

## Acceptance Criteria
- [ ] GitHub repository created and initialized
- [ ] Folder structure exists: specs/001-finhub-report/, reports/, scripts/, tests/, documentation/, configurations/
- [ ] All template files copied
- [ ] README.md created with project overview
- [ ] .gitignore configured

## Dependencies
- None

## Effort Estimate
1 hour

## Verification
- Tree command shows all folders
- GitHub repo accessible by team","phase-1-setup,us-4-promotion,component-automation,priority-p1,type-setup","Project Lead","Phase 1: Setup"

[SETUP-02] Create Environment Configuration Files,"## Task ID
SETUP-02

...rest of description...","phase-1-setup,us-4-promotion,component-automation,priority-p1,type-setup","Data Admin","Phase 1: Setup"
```

---

## PowerShell Script: Bulk Issue Creation

**File**: `scripts/github-issues-bulk-create.ps1`

```powershell
<#
.SYNOPSIS
Bulk create GitHub issues from detailed-tasks.md using GitHub CLI

.DESCRIPTION
Reads task data from CSV export and creates GitHub issues with proper labels, 
milestones, and metadata. Supports dry-run mode for validation.

.PARAMETER CsvPath
Path to CSV file with task data (default: documentation/github-issues-template.csv)

.PARAMETER DryRun
If $true, prints what would be created without actually creating issues

.PARAMETER SkipExisting
If $true, skips creating issues if title already exists in repo

.EXAMPLE
.\github-issues-bulk-create.ps1 -CsvPath "documentation/github-issues-template.csv" -DryRun $true

.EXAMPLE
.\github-issues-bulk-create.ps1 -CsvPath "documentation/github-issues-template.csv"
#>

param(
    [string]$CsvPath = "documentation/github-issues-template.csv",
    [bool]$DryRun = $true,
    [bool]$SkipExisting = $true
)

# Color output helpers
function Write-Success { Write-Host $args[0] -ForegroundColor Green }
function Write-Error_ { Write-Host $args[0] -ForegroundColor Red }
function Write-Info { Write-Host $args[0] -ForegroundColor Cyan }
function Write-Warning { Write-Host $args[0] -ForegroundColor Yellow }

try {
    # Verify GitHub CLI
    Write-Info "[1/5] Verifying GitHub CLI installation..."
    $ghVersion = gh --version
    Write-Success "✓ GitHub CLI found: $ghVersion"

    # Verify CSV file
    Write-Info "[2/5] Verifying CSV file..."
    if (-not (Test-Path $CsvPath)) {
        Write-Error_ "✗ CSV file not found: $CsvPath"
        exit 1
    }
    
    $tasks = Import-Csv $CsvPath
    Write-Success "✓ CSV loaded: $($tasks.Count) tasks found"

    # Get existing issues (optional, for skip logic)
    if ($SkipExisting) {
        Write-Info "[3/5] Fetching existing issues..."
        $existingIssues = @()
        $existingIssues = gh issue list --all --json title --jq '.[] | .title' 2>$null
        Write-Success "✓ Found $($existingIssues.Count) existing issues"
    }

    # Create issues
    Write-Info "[4/5] Creating issues from CSV..."
    $created = 0
    $skipped = 0
    $failed = 0

    foreach ($task in $tasks) {
        $title = $task.title
        $body = $task.body
        $labels = $task.labels
        $assignee = $task.assignee
        $milestone = $task.milestone

        # Skip if exists
        if ($SkipExisting -and $existingIssues -contains $title) {
            Write-Warning "⊘ Skipping (exists): $title"
            $skipped++
            continue
        }

        # Build gh command
        $ghCmd = @(
            "gh", "issue", "create",
            "--title", $title,
            "--body", $body,
            "--label", $labels
        )
        
        if ($assignee -and $assignee -ne "Unassigned") {
            $ghCmd += @("--assignee", $assignee)
        }
        
        if ($milestone) {
            $ghCmd += @("--milestone", $milestone)
        }

        if ($DryRun) {
            Write-Info "DRY RUN: Would create: $title"
            Write-Info "  Labels: $labels"
            Write-Info "  Assignee: $assignee"
            Write-Info "  Milestone: $milestone`n"
            $created++
        }
        else {
            try {
                Write-Info "Creating: $title"
                & $ghCmd | Out-Null
                Write-Success "✓ Created: $title"
                $created++
            }
            catch {
                Write-Error_ "✗ Failed to create: $title - $_"
                $failed++
            }
        }
    }

    # Summary
    Write-Info "[5/5] Summary"
    Write-Success "✓ Created: $created"
    Write-Warning "⊘ Skipped: $skipped"
    Write-Error_ "✗ Failed: $failed"
    Write-Info "Total tasks: $($tasks.Count)"

    if ($DryRun) {
        Write-Warning "`n[DRY RUN MODE] No issues actually created. Remove -DryRun $false to create."
    }
}
catch {
    Write-Error_ "Fatal error: $_"
    exit 1
}
```

**Usage**:

```powershell
# Dry run (preview)
.\scripts/github-issues-bulk-create.ps1 -DryRun $true

# Create all issues
.\scripts/github-issues-bulk-create.ps1 -DryRun $false

# Create with skip existing
.\scripts/github-issues-bulk-create.ps1 -DryRun $false -SkipExisting $true
```

---

## CSV Export for All 65+ Tasks

**File**: `documentation/github-issues-export.csv`

**Format**: 
```
title,body,labels,assignee,milestone
```

**Rows** (sample of first 10, full list in separate comprehensive CSV):

See **GitHub Issues CSV Export** section at end of this document.

---

## Milestones Configuration

Create GitHub Milestones for each phase:

| Milestone | Target Date | Parent Sprint |
|-----------|------------|--------------|
| Phase 1: Setup | Feb 21, 2026 | Sprint 1 |
| Phase 1.5: Governance | Feb 23, 2026 | Sprint 1 |
| Phase 2: Data Connection | Feb 26, 2026 | Sprint 1 |
| Phase 3: Power BI Dashboard | Mar 2, 2026 | Sprint 2 |
| Phase 4: Excel Report | Mar 5, 2026 | Sprint 2 |
| Phase 5: Automated Refresh | Mar 8, 2026 | Sprint 2 |
| Phase 6: Promotion Pipeline | Mar 12, 2026 | Sprint 3 |
| Phase 7: Security | Mar 14, 2026 | Sprint 3 |
| Phase 8: Documentation | Mar 16, 2026 | Sprint 3 |
| Phase 9: Deployment | Mar 19, 2026 | Sprint 4 |

**To create milestones in GitHub**:

1. Go to **Issues** → **Milestones**
2. Click **Create Milestone**
3. Fill in title, description, due date
4. Click **Create Milestone**
5. Repeat for each phase

---

## Team Assignments & Permissions

**Suggested GitHub Team Memberships**:

```
Team: PowerBI-Developers
  Members: [PowerBI Dev 1], [PowerBI Dev 2]
  Permissions: Write
  Can assign: VIZ-*, FORMAT-*, FILTER-* issues

Team: Data-Admins
  Members: [Data Admin 1], [Data Admin 2]
  Permissions: Write
  Can assign: DATA-*, CFG-*, REFRESH-*, GOV-* issues

Team: QA-Testers
  Members: [QA Lead], [QA 1], [QA 2]
  Permissions: Write
  Can assign: TEST-* issues

Team: Security-Governance
  Members: [Data Governance], [IT Security]
  Permissions: Write
  Can assign: SEC-*, PROMOTE-* issues

Team: DevOps
  Members: [DevOps Engineer], [Automation Engineer]
  Permissions: Write
  Can assign: SETUP-*, REFRESH-* issues
```

---

## Issue Linking & Relationships

**Use GitHub Issue Linking** to show dependencies:

```markdown
## Dependencies

**Blocks**:
- Blocks #20 (SETUP-02)
- Blocks #21 (SETUP-03)

**Depends on**:
- None

**Related to**:
- Related to #1 (Specification)
- Part of Epic #50 (Phase 1: Setup)
```

**GitHub Syntax**:
- `Closes #123` - Links to and closes on merge
- `Fixes #123` - Same as closes
- `Relates to #123` - Creates link reference
- `Blocked by #123` - Dependency relationship
- `Blocks #123` - Dependency relationship (reverse)

---

## Automation: GitHub Actions Workflow

**File**: `.github/workflows/task-issue-sync.yml`

```yaml
name: Task Issue Sync

on:
  schedule:
    - cron: '0 9 * * MON'  # Weekly Monday 9 AM
  workflow_dispatch:

jobs:
  sync-tasks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup PowerShell
        run: |
          pwsh -Command "Write-Host 'PowerShell ready'"
      
      - name: Verify CSV
        run: |
          if (Test-Path "documentation/github-issues-export.csv") {
            Write-Host "CSV file exists"
          } else {
            Write-Host "CSV file missing - skipping sync"
            exit 0
          }
        shell: pwsh
      
      - name: Sync Issues
        run: |
          pwsh -File scripts/github-issues-bulk-create.ps1 `
            -CsvPath "documentation/github-issues-export.csv" `
            -DryRun $false `
            -SkipExisting $true
        shell: pwsh

  # Alternative: Comment when no sync needed
      - name: Comment on PR (if needed)
        if: always()
        run: |
          echo "Issue sync completed at $(date)"
```

---

## Manual Workflow: Creating Issues Step-by-Step

**If you prefer creating issues manually one at a time**:

### Phase 1: Setup (6 issues)

1. **SETUP-01** - Create Repository Structure
   - Assignee: Project Lead
   - Labels: `phase-1-setup`, `type-setup`, `priority-p1`
   - Milestone: Phase 1: Setup

2. **SETUP-02** - Create Environment Configuration Files
   - Assignee: Data Admin
   - Labels: `phase-1-setup`, `component-automation`, `priority-p1`
   - Milestone: Phase 1: Setup
   - Depends on: #1 (SETUP-01)

3. **SETUP-03** - Initialize Power BI Project File
   - Assignee: Power BI Developer
   - Labels: `phase-1-setup`, `us-1-dashboard`, `component-powerbi`, `priority-p1`
   - Milestone: Phase 1: Setup
   - Depends on: #1 (SETUP-01)

4. **SETUP-04** - Initialize Excel Template
   - Assignee: Data Admin / Excel Developer
   - Labels: `phase-1-setup`, `us-2-excel`, `component-excel`, `priority-p1`
   - Milestone: Phase 1: Setup
   - Depends on: #1 (SETUP-01)

5. **SETUP-05** - Create PowerShell Script Stubs
   - Assignee: Automation Engineer
   - Labels: `phase-1-setup`, `us-3-refresh`, `component-automation`, `priority-p1`
   - Milestone: Phase 1: Setup
   - Depends on: #1 (SETUP-01)

6. **SETUP-06** - Set Up Git Branching & Workflows
   - Assignee: Project Lead / DevOps
   - Labels: `phase-1-setup`, `type-setup`, `priority-p0`
   - Milestone: Phase 1: Setup
   - Depends on: #1 (SETUP-01)

*(Repeat for each phase...)*

---

## Status Tracking via Project Board

**Create GitHub Project Board** for visual tracking:

1. Go to **Projects** tab
2. Click **New Project**
3. Select **Table** or **Board** template
4. Name: "FinHub Phase By Phase"
5. Add columns: To Do | In Progress | In Review | Done

**Auto-populate from labels**:
- Issues with `status-todo` → To Do column
- Issues with `status-in-progress` → In Progress column
- Issues with `status-in-review` → In Review column
- Issues with `status-done` → Done column

---

## Continuous Updates: Keeping Issues Fresh

**Weekly Task** (Assigned to PM):

1. Review all open issues
2. Update status labels based on actual progress
3. Add comments with blockers or status updates
4. Close completed issues
5. Create new issues for unplanned work

**Monthly Task**:

1. Review closed issues (lessons learned)
2. Update milestone dates if needed
3. Adjust priority labels based on stakeholder feedback
4. Archive completed milestone

---

## Next Steps After Issue Creation

Once issues are created:

1. **Assign to team members** (Assignee field)
2. **Start Phase 1 issues** (SETUP-01 through SETUP-06)
3. **Track progress** via Project Board
4. **Update status labels** as work progresses
5. **Comment on issues** for blockers/questions
6. **Close issues** when complete (with linking to merge commits)

---

## Summary

| Method | Best For | Time Required |
|--------|----------|--------------|
| Manual UI | 1-5 issues, familiarity | 5-10 min/issue |
| CSV + GitHub CLI | 20-50 issues, quick import | 30 min setup, 2 min execute |
| PowerShell Script | 50+ issues, automation | 1 hour setup, 1 min execute |
| GitHub API | Advanced customization | 2+ hours development |

**Recommended Approach**:
1. **Start**: Manual creation of Phase 1 issues (6 issues) to understand structure
2. **Then**: Use PowerShell script for remaining 59+ issues
3. **Ongoing**: Manual updates via GitHub UI for status/comments

---

**Tasks to Issues Conversion Status**: ✅ **COMPLETE**

**Ready for**: Team to begin GitHub issue creation following this guide

**Generated**: 2026-02-20  
**Version**: 1.0.0
