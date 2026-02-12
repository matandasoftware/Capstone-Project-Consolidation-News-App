#!/bin/bash
# Git History Cleanup Script
# WARNING: This will rewrite Git history. Backup your repo first!

echo "⚠️  WARNING: This will rewrite your Git history!"
echo "Make sure you have:"
echo "  1. Backed up your repository"
echo "  2. Informed all collaborators"
echo "  3. Rotated all exposed secrets"
echo ""
read -p "Continue? (yes/no): " response

if [ "$response" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

# Create a backup branch
echo "Creating backup branch..."
git branch backup-before-cleanup

# Option 1: Remove sensitive file from history
echo "Removing sensitive data from history..."
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch news_project/settings.py" \
  --prune-empty --tag-name-filter cat -- --all

# Option 2: Replace secrets in history using BFG (if BFG is installed)
# Create secrets file
cat > secrets.txt << EOF
django-insecure-bnwc-^mqdvkb&hr6@6zruk&t6pahdwy0(6fg5r@_9xpoq-8np#
news_app_password
EOF

echo "If you have BFG installed, run:"
echo "  bfg --replace-text secrets.txt"

# Clean up
echo "Cleaning up repository..."
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo ""
echo "✅ History cleanup complete!"
echo ""
echo "Next steps:"
echo "1. Review the changes: git log"
echo "2. Force push: git push origin --force --all"
echo "3. Force push tags: git push origin --force --tags"
echo "4. Delete the backup branch if everything looks good:"
echo "   git branch -D backup-before-cleanup"
echo ""
echo "⚠️  Remember: All collaborators must re-clone the repository!"
