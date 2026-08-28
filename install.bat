@echo off
title Custom Agent Installer Deployment
echo ==================================================
echo 🚀 Launching Custom Agent Installer Environment...
echo ==================================================
echo.

:: 1. Check if Python is installed on their system
where py >nul 2>nul
if %errorlevel% neq 0 (
    where python >nul 2>nul
    if %errorlevel% neq 0 (
        echo ❌ Error: Python is not installed on this computer!
        echo Please download it from https://python.org
        echo.
        pause
        exit /b
    ) else (
        set PY_CMD=python
    )
) else (
    set PY_CMD=py
)

:: 2. Run your clean python installation script automatically
%PY_CMD% install.py

echo.
echo ==================================================
echo 🏁 Deployment process finished.
echo ==================================================
echo.
pause

