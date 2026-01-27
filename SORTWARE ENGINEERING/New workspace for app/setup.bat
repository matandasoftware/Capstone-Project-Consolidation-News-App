@echo off
echo ================================
echo Buroko's Kitchen Setup Script
echo ================================
echo.

echo Refreshing environment variables...
call refreshenv 2>nul
if errorlevel 1 (
    echo Refreshenv not available, trying alternative...
    for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH 2^>nul') do set "PATH=%%b"
)

echo Checking Node.js installation...
node --version
if %ERRORLEVEL% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    echo Then restart this script
    pause
    exit /b 1
)

echo Checking npm installation...
npm --version
if %ERRORLEVEL% neq 0 (
    echo ERROR: npm is not available
    pause
    exit /b 1
)

echo.
echo Node.js and npm are installed successfully!
echo.

echo Installing project dependencies...
echo.

echo Installing root dependencies...
call npm install
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to install root dependencies
    pause
    exit /b 1
)

echo.
echo Installing client dependencies...
cd client
call npm install
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to install client dependencies
    pause
    exit /b 1
)

echo.
echo Installing server dependencies...
cd ..\server
call npm install
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to install server dependencies
    pause
    exit /b 1
)

cd ..
echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo Next steps:
echo 1. Set up Firebase configuration in client\src\config\firebase.js
echo 2. Set up MongoDB (local or cloud)
echo 3. Copy server\.env.example to server\.env and configure
echo 4. Run: npm run dev
echo.
pause
