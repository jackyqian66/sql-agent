@echo off
chcp 65001 > nul
echo ========================================
echo   SQL Agent - 一键启动
echo ========================================
echo.

if not exist ".env" (
    echo [错误] 未找到 .env 文件！
    echo.
    echo 请先复制 .env.example 为 .env
    echo 并填入你的 API_KEY
    echo.
    pause
    exit /b 1
)

echo [1/5] 检查模型文件...
if not exist "models\bge-base-zh-v1.5\config.json" (
    echo [错误] 未找到嵌入模型！
    echo.
    echo 请确保 models\bge-base-zh-v1.5 目录存在
    echo.
    pause
    exit /b 1
)
echo [OK] 模型文件已就绪

echo.
echo [2/5] 检查数据库...
if not exist "data\sales.db" (
    echo 创建示例数据库...
    python create_db.py
)
echo [OK] 数据库已就绪

echo.
echo [3/5] 启动后端...
echo 请等待后端启动完成...
start "SQL Agent Backend" cmd /k "cd /d "%~dp0" && python backend/app.py"

echo.
echo 等待后端启动 (15秒)...
timeout /t 15 /nobreak > nul

echo.
echo [4/5] 启动前端...
echo 请等待前端启动完成...
start "SQL Agent Frontend" cmd /k "cd /d "%~dp0frontend" && if not exist node_modules (npm install) && npm run dev"

echo.
echo 等待前端启动 (20秒)...
timeout /t 20 /nobreak > nul

echo.
echo [5/5] 打开浏览器...
echo 正在打开 http://localhost:3000 ...
start http://localhost:3000

echo.
echo ========================================
echo   启动完成！
echo.
echo   前端地址: http://localhost:3000
echo   后端地址: http://localhost:8000
echo.
echo   如果浏览器没有自动打开，请手动访问
echo   前端地址
echo.
echo   按任意键关闭此窗口（服务将继续运行）
echo ========================================
pause > nul
