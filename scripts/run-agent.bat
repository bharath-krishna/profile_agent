@echo off
REM Navigate to the agent directory
cd /d %~dp0\..\agent

REM Activate the virtual environment
call .venv\Scripts\activate.bat

REM Run the agent
set PORT=8001
uv run main.py
