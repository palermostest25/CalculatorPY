@echo off
title Pull from Github
robocopy "..\Calculator" "..\Calculator - Backup" /mir
git pull