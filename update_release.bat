@echo off
setlocal enabledelayedexpansion

:: Ensure .env is ignored
echo Excluding .env file from Git tracking...
if not exist .gitignore (
    echo .env > .gitignore
) else (
    findstr /c:".env" .gitignore >nul || echo .env >> .gitignore
)

git rm --cached .env >nul 2>&1
git add .gitignore
git commit -m "Exclude .env from Git tracking" >nul 2>&1

:: Prompt for the old version
set /p OLD_VERSION="Enter the old version tag (e.g., v1.0): "

:: Prompt for the new version
set /p NEW_VERSION="Enter the new version tag (e.g., v1.1): "

:: Ensure the working directory is clean
git status --porcelain >nul
if not errorlevel 1 (
    echo Working directory is clean.
) else (
    echo Uncommitted changes detected. Staging and committing them...
    git add .
    git commit -m "Auto-commit before releasing version %NEW_VERSION%"
)

:: Push all changes to the repository
echo Pushing all changes to the main repository...
git push origin

:: Create a tag for the old version (specific to Calculator.py)
git checkout latest -- Calculator.py
git add Calculator.py
git commit -m "Tagging old release %OLD_VERSION%"
git tag -a %OLD_VERSION% -m "Tagging old release %OLD_VERSION%"
git push origin %OLD_VERSION%
echo Tagged old release: %OLD_VERSION%

:: Move the "latest" tag to the new version
git tag -f latest
git tag -d %NEW_VERSION% 2>nul
git tag -a %NEW_VERSION% -m "New release %NEW_VERSION%"
git push origin --tags --force
echo Updated latest tag to %NEW_VERSION%.

:: Create a GitHub release for the new version
set /p GITHUB_TOKEN="Enter your GitHub Personal Access Token: "
curl -X POST -H "Authorization: token %GITHUB_TOKEN%" ^
     -H "Accept: application/vnd.github.v3+json" ^
     https://api.github.com/repos/palermostest25/CalculatorPY/releases ^
     -d "{\"tag_name\":\"%NEW_VERSION%\",\"name\":\"Release %NEW_VERSION%\",\"body\":\"Release for version %NEW_VERSION%\",\"target_commitish\":\"main\",\"prerelease\":false}"

echo GitHub release for %NEW_VERSION% created successfully.
pause
