@echo off
title Push to Github
git add .
set /p "commitmessage=Commit Message: "
git commit -m "%commitmessage%"
git push