@echo off
echo ========================================
echo   停止 SQL Agent 服务
echo ========================================
echo.

echo 正在停止相关进程...
taskkill /FI "WINDOWTITLE eq SQL Agent Backend*" /F 2>nul
taskkill /FI "WINDOWTITLE eq SQL Agent Frontend*" /F 2>nul

echo.
echo 服务已停止
echo.
pause
