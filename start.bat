@echo off
echo ========================================
echo   SQL Agent - 智能数据库查询助手
echo ========================================
echo.

if not exist ".env" (
    echo [警告] 未找到 .env 文件，请确保已配置 ARK_API_KEY
    echo.
)

echo [1/3] 检查数据库...
if not exist "data\sales.db" (
    echo 创建示例数据库...
    python create_db.py
)

echo.
echo [2/3] 启动后端服务...
start "SQL Agent Backend" cmd /k "cd backend && pip install -r requirements.txt && cd .. && python backend/app.py"

echo 等待后端服务启动...
timeout /t 5 /nobreak > nul

echo.
echo [3/3] 启动前端服务...
start "SQL Agent Frontend" cmd /k "cd frontend && if not exist node_modules (npm install) && npm run dev"

echo.
echo ========================================
echo   服务正在启动中...
echo.
echo   请稍候，然后访问:
echo   🏠 应用首页: http://localhost:3000
echo   🐍 后端API: http://localhost:8000
echo.
echo   按任意键关闭此窗口（服务将继续运行）
echo ========================================
pause > nul
