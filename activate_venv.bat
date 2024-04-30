@echo off

REM Check if the script is running on Windows
if "%OS%"=="Windows_NT" (
    echo Activating venv..
    call venv\Scripts\activate
) else (
    echo Not running on Windows
    echo This script is designed to be run on Windows.
)