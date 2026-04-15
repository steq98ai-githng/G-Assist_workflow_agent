@echo off
:: G-Assist 中文外掛 V2 安裝腳本
:: 以管理員身分執行此檔案

net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process '%~dpnx0' -Verb RunAs"
    goto :eof
)

echo =====================================================
echo   G-Assist 中文外掛 V2 安裝中...
echo =====================================================

set "SRC=%~dp0"
set "DST=C:\ProgramData\NVIDIA Corporation\nvtopps\rise\plugins\system_workflow_agent"

:: 確保目標目錄存在
if not exist "%DST%" mkdir "%DST%"

:: 複製核心檔案
echo 正在複製 plugin.py ...
copy /Y "%SRC%plugin.py" "%DST%\plugin.py"

echo 正在複製 manifest.json ...
copy /Y "%SRC%manifest.json" "%DST%\manifest.json"

echo 正在複製依賴與模組 ...
if not exist "%DST%\libs" mkdir "%DST%\libs"
xcopy /E /I /Y "%SRC%libs" "%DST%\libs"

if not exist "%DST%\core" mkdir "%DST%\core"
xcopy /E /I /Y "%SRC%core" "%DST%\core"

if not exist "%DST%\config" mkdir "%DST%\config"
xcopy /E /I /Y "%SRC%config" "%DST%\config"

if not exist "%DST%\mcp" mkdir "%DST%\mcp"
xcopy /E /I /Y "%SRC%mcp" "%DST%\mcp"

if not exist "%DST%\vision" mkdir "%DST%\vision"
xcopy /E /I /Y "%SRC%vision" "%DST%\vision"

if not exist "%DST%\intents" mkdir "%DST%\intents"
xcopy /E /I /Y "%SRC%intents" "%DST%\intents"

:: 清除舊版 exe
if exist "%DST%\ai-chinese-plugin.exe" (
    echo 正在移除舊版 exe ...
    del /F /Q "%DST%\ai-chinese-plugin.exe"
)

echo =====================================================
echo   安裝完成！請重啟 NVIDIA App / G-Assist。
echo =====================================================
pause
