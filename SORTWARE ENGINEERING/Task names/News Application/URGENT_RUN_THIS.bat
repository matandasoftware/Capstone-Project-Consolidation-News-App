@echo off
echo ========================================
echo REMOVING SECRETS FROM GIT HISTORY
echo ========================================
echo.

REM Install dependency
pip install python-decouple

REM Generate new SECRET_KEY
echo Generating new SECRET_KEY...
python -c "import secrets; key='django-insecure-'+''.join(secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(50)); print('SECRET_KEY='+key)" > new_key.txt
echo New key generated in new_key.txt
echo.

REM Remove settings.py from Git history
echo Removing settings.py from Git history...
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch news_project/settings.py" --prune-empty --tag-name-filter cat -- --all

REM Force push
echo.
echo Ready to push. Run: git push origin --force --all
echo.
echo IMPORTANT: 
echo 1. Copy the new SECRET_KEY from new_key.txt to your .env file
echo 2. REVOKE Twitter API keys at: https://developer.twitter.com/en/portal/dashboard
echo 3. Then run: git push origin --force --all
echo.
pause
