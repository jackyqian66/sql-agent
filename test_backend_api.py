import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("测试后端API")
print("=" * 60)

print("\n[1/3] 检查环境变量...")
try:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("API_KEY") or os.getenv("ARK_API_KEY")
    print(f"[OK] API_KEY: {'已设置' if api_key else '未设置'}")
except Exception as e:
    print(f"[FAIL] 环境变量: {e}")
    sys.exit(1)

print("\n[2/3] 检查后端导入...")
try:
    from backend.app import app
    print("[OK] backend.app 导入成功")
except Exception as e:
    print(f"[FAIL] backend.app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n[3/3] 测试Flask应用...")
try:
    with app.test_client() as client:
        response = client.get('/')
        print(f"[OK] Flask测试客户端响应: {response.status_code}")
except Exception as e:
    print(f"[FAIL] Flask测试: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("\n如果上面都正常，尝试手动启动后端:")
print("  cd backend")
print("  python app.py")
print("\n然后在另一个窗口启动前端:")
print("  cd frontend")
print("  npm run dev")
