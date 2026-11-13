@echo off
title Push Serenity System to GitHub
echo ========================================================
echo               Serenity System :: GitHub Publisher
echo ========================================================
echo.
echo Checking GitHub CLI login status...
gh auth status >nul 2>&1
if errorlevel 1 (
    echo GitHub CLI is not logged in yet.
    echo Please log in via browser:
    gh auth login -w -p https
)

echo.
echo Creating and pushing public repository to GitHub...
gh repo create serenity-system --public --source=. --remote=origin --push --description "High-level programming paradigm workbench, interactive memory engine, and execution runtime (Rust, Go, TS, Python, Java, C++)"

if errorlevel 1 (
    echo.
    echo If the repository already exists on your GitHub, you can push manually:
    echo git push -u origin main
) else (
    echo.
    echo [SUCCESS] Serenity System has been successfully published to your GitHub!
)

pause
