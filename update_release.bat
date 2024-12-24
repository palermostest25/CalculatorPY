@echo off

title Update Calculator Release

setlocal enabledelayedexpansion

set URL=https://github.com/palermostest25/CalculatorPY/releases/tag/latest
curl -s "%URL%" | findstr "<title>" > temp.txt
for /f "tokens=2 delims= " %%A in ('findstr "<title>" temp.txt') do (
    set "OLD_VERSION=%%A"
)
set "OLD_VERSION=%OLD_VERSION:Release =%"
del temp.txt

echo Old Version: %OLD_VERSION%
set /p "NEW_VERSION=Enter The New Version Tag (eg., 1.1): "
set /p "RELEASE_NOTES=Enter Release Notes For The New Version: "
echo Is All This Information Correct?
pause

git add .
git reset -- ".env"

git status --porcelain >nul
echo Uncommitted Changes Detected. Staging And Committing Them...
git add . || exit /b 1
git commit -m "Auto-Commit Before Releasing Version %NEW_VERSION%" || exit /b 1
git push origin main || exit /b 1

echo Checking If Tag 'latest' Exists...
git tag -l latest >nul
if %errorlevel%==0 (
    echo Creating Tag %OLD_VERSION%
    git tag -d latest >nul 2>&1
    git tag -a %OLD_VERSION% -m "Release For Version %OLD_VERSION%"
    git push origin %OLD_VERSION%
    git push origin :refs/tags/latest >nul 2>&1
    echo Renamed 'latest' Tag To %OLD_VERSION%.
) else (
    echo 'latest' Tag Does Not Exist. Skipping Renaming...
)

echo Creating And Assigning New Tag '%NEW_VERSION%' As 'latest'...
git tag -a %NEW_VERSION% -m "%RELEASE_NOTES%"
git tag -f latest
git push origin %NEW_VERSION%
git push origin latest
echo Assigned 'latest' Tag To %NEW_VERSION%.

echo Creating A GitHub Release For The Old Version...
gh release edit latest --tag %OLD_VERSION% --draft=false
if errorlevel 1 (
    echo Failed To Edit The GitHub Release For %OLD_VERSION%. Please Check Your GitHub CLI Configuration.
    pause
    exit /b 1
)
echo GitHub Release For %OLD_VERSION% Edited Successfully With Tag %OLD_VERSION%.

echo Creating A GitHub Release For The New Version...
gh release create latest --title "%NEW_VERSION%" --notes "%RELEASE_NOTES%" --target main Calculator.py --draft=false
if errorlevel 1 (
    echo Failed To Create The GitHub Release For %NEW_VERSION%. Please Check Your GitHub CLI Configuration.
    pause
    exit /b 1
)
echo GitHub Release For %NEW_VERSION% Created Successfully.

pause
