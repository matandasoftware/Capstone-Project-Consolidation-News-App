#!/bin/bash
echo "========================================"
echo "REMOVING SECRETS FROM GIT HISTORY"
echo "========================================"

# Install dependency
pip install python-decouple

# Generate new SECRET_KEY
echo "Generating new SECRET_KEY..."
python -c "import secrets; key='django-insecure-'+''.join(secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(50)); print('SECRET_KEY='+key)" > new_key.txt

# Remove secrets from Git history using BFG (faster)
echo "Cleaning Git history..."
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch news_project/settings.py" --prune-empty --tag-name-filter cat -- --all

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo ""
echo "✅ DONE! Now run:"
echo "1. Update .env with new key from new_key.txt"
echo "2. git push origin --force --all"
echo "3. REVOKE Twitter keys: https://developer.twitter.com/en/portal/dashboard"
