#!/usr/bin/env python3
"""
Bulk create GitHub issues from CSV using GitHub REST API

Requires:
- GITHUB_TOKEN environment variable with personal access token
- Or specify token via --token parameter

Generate token at: https://github.com/settings/tokens
Scopes needed: repo, project
"""

import csv
import json
import sys
import os
import argparse
import requests
from pathlib import Path

# Color output helpers
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    GRAY = '\033[90m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.CYAN}{msg}{Colors.END}")

def print_debug(msg, verbose=False):
    if verbose:
        print(f"{Colors.GRAY}{msg}{Colors.END}")

def get_github_token(token_arg=None):
    """Get GitHub token from argument, env var, or prompt"""
    if token_arg:
        return token_arg
    
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        return token
    
    # Try to get from git config
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'config', '--global', 'github.token'],
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            return result.stdout.strip()
    except:
        pass
    
    return None

def create_github_issue(owner, repo, token, title, body, labels=None, assignee=None, milestone=None, dry_run=False):
    """Create a single GitHub issue via REST API"""
    
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    data = {
        "title": title,
        "body": body,
    }
    
    if labels and labels.strip():
        data["labels"] = [l.strip() for l in labels.split(",") if l.strip()]
    
    if assignee and assignee.strip():
        data["assignee"] = assignee.strip()
    
    if milestone and milestone.strip():
        data["milestone"] = milestone.strip()
    
    if dry_run:
        print_info(f"DRY RUN: {title}")
        print_debug(f"  URL: {url}")
        print_debug(f"  Body: {body[:60]}...")
        if labels:
            print_debug(f"  Labels: {labels}")
        if assignee:
            print_debug(f"  Assignee: {assignee}")
        if milestone:
            print_debug(f"  Milestone: {milestone}")
        return True
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        
        if response.status_code == 201:
            issue_data = response.json()
            print_success(f"Created: {title} (#{issue_data.get('number')})")
            return True
        elif response.status_code == 422:
            # Issue already exists
            print_warning(f"Skipping (exists): {title}")
            return None
        else:
            error_msg = response.json().get('message', response.text) if response.text else 'Unknown error'
            print_error(f"Failed: {title} - {error_msg}")
            return False
            
    except requests.RequestException as e:
        print_error(f"Exception: {title} - {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Bulk create GitHub issues from CSV'
    )
    parser.add_argument(
        '--csv',
        default='documentation/github-issues-export.csv',
        help='Path to CSV file (default: documentation/github-issues-export.csv)'
    )
    parser.add_argument(
        '--owner',
        default='prashdubey',
        help='GitHub owner/username (default: prashdubey)'
    )
    parser.add_argument(
        '--repo',
        default='FinHub-Financial-Report',
        help='GitHub repository name (default: FinHub-Financial-Report)'
    )
    parser.add_argument(
        '--token',
        help='GitHub personal access token (or set GITHUB_TOKEN env var)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be created without creating (default: False)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output'
    )
    
    args = parser.parse_args()
    
    # Header
    print_info("="*50)
    print_info("GitHub Issues Bulk Creator (Python)")
    print_info("="*50)
    print_info("")
    
    # Step 1: Get token
    print_info("[1/4] Checking authentication...")
    token = get_github_token(args.token)
    if not token:
        print_error("GitHub token not found!")
        print_info("  Set GITHUB_TOKEN environment variable")
        print_info("  Or pass --token parameter")
        print_info("  Generate at: https://github.com/settings/tokens")
        sys.exit(1)
    print_success("GitHub token found")
    
    # Step 2: Check CSV file
    print_info("[2/4] Verifying CSV file...")
    csv_path = Path(args.csv)
    if not csv_path.exists():
        print_error(f"CSV file not found: {args.csv}")
        sys.exit(1)
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            tasks = list(reader)
        print_success(f"CSV loaded: {len(tasks)} tasks found")
    except Exception as e:
        print_error(f"Error loading CSV: {e}")
        sys.exit(1)
    
    # Step 3: Verify repository
    print_info("[3/4] Verifying repository...")
    verify_url = f"https://api.github.com/repos/{args.owner}/{args.repo}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(verify_url, headers=headers, timeout=10)
        if response.status_code == 200:
            repo_data = response.json()
            print_success(f"Repository accessible: {repo_data['full_name']}")
        else:
            print_error(f"Repository not found or not accessible (HTTP {response.status_code})")
            sys.exit(1)
    except Exception as e:
        print_error(f"Error verifying repository: {e}")
        sys.exit(1)
    
    # Step 4: Create issues
    print_info("[4/4] Creating issues from CSV...")
    print_info("")
    
    created = 0
    skipped = 0
    failed = 0
    errors = []
    
    for i, task in enumerate(tasks, 1):
        title = task.get('title', '').strip()
        body = task.get('body', '').strip()
        labels = task.get('labels', '').strip()
        assignee = task.get('assignee', '').strip()
        milestone = task.get('milestone', '').strip()
        
        if not title:
            print_warning(f"Skipping row {i}: missing title")
            skipped += 1
            continue
        
        if not body:
            body = f"Task: {title}"
        
        result = create_github_issue(
            args.owner,
            args.repo,
            token,
            title,
            body,
            labels=labels,
            assignee=assignee,
            milestone=milestone,
            dry_run=args.dry_run
        )
        
        if result is True:
            created += 1
        elif result is None:
            skipped += 1
        else:
            failed += 1
            errors.append({'title': title, 'error': 'HTTP error (see above)'})
    
    # Summary
    print_info("")
    print_info("="*50)
    print_info("SUMMARY")
    print_info("="*50)
    print_success(f"Created:  {created}")
    print_warning(f"Skipped:  {skipped}")
    print_error(f"Failed:   {failed}")
    print_info(f"Total:    {len(tasks)}")
    print_info("")
    
    if args.dry_run:
        print_warning("━"*50)
        print_warning("DRY RUN MODE: No issues were created")
        print_warning("Re-run without --dry-run to create issues")
        print_warning("━"*50)
    
    if errors:
        print_error("")
        print_error("ERRORS:")
        for err in errors:
            print_error(f"  {err['title']}: {err['error']}")
    
    sys.exit(0 if failed == 0 else 1)

if __name__ == '__main__':
    main()
