@echo off
setlocal
cd /d "%~dp0"
echo 💠 Antigravity System Workflow Agent v4.0.4 Starter
echo ---------------------------------------------------
echo [INFO] Environment check: Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found in PATH!
    pause
    goto :eof
)
echo [INFO] Starting Plugin Service (Protocol V2 + GitKraken MCP)...
python plugin.py
echo [INFO] Done.
pause
