# Git History Cleanup Script for PowerShell
# WARNING: This will rewrite Git history. Backup your repo first!

Write-Host "⚠️  WARNING: This will rewrite your Git history!" -ForegroundColor Red
Write-Host "Make sure you have:"
Write-Host "  1. Backed up your repository"
Write-Host "  2. Informed all collaborators"
Write-Host "  3. Rotated all exposed secrets"
Write-Host ""
$response = Read-Host "Continue? (yes/no)"

if ($response -ne "yes") {
    Write-Host "Aborted." -ForegroundColor Yellow
    exit 1
}

# Create a backup branch
Write-Host "Creating backup branch..." -ForegroundColor Green
git branch backup-before-cleanup

# Create secrets file for BFG
@"
django-insecure-bnwc-^mqdvkb&hr6@6zruk&t6pahdwy0(6fg5r@_9xpoq-8np#
news_app_password
"@ | Out-File -FilePath secrets.txt -Encoding UTF8

Write-Host "`nOption 1: Using git filter-branch" -ForegroundColor Cyan
Write-Host "Removing sensitive file from history..."
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch news_project/settings.py" --prune-empty --tag-name-filter cat -- --all

Write-Host "`nOption 2: Using BFG (if installed)" -ForegroundColor Cyan
Write-Host "To use BFG, download it from https://rtyley.github.io/bfg-repo-cleaner/"
Write-Host "Then run: java -jar bfg.jar --replace-text secrets.txt"

# Clean up
Write-Host "`nCleaning up repository..." -ForegroundColor Green
git reflog expire --expire=now --all
git gc --prune=now --aggressive

Write-Host "`n✅ History cleanup complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Review the changes: git log"
Write-Host "2. Force push: git push origin --force --all"
Write-Host "3. Force push tags: git push origin --force --tags"
Write-Host "4. Delete the backup branch if everything looks good:"
Write-Host "   git branch -D backup-before-cleanup"
Write-Host "`n⚠️  Remember: All collaborators must re-clone the repository!" -ForegroundColor Red
