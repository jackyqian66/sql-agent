import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("测试后端基本功能")
print("=" * 60)

print("\n[1/3] 测试导入...")
try:
    from backend.app import app
    print("[OK] backend.app 导入成功")
except Exception as e:
    print(f"[FAIL] backend.app 导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n[2/3] 测试环境变量...")
try:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("API_KEY") or os.getenv("ARK_API_KEY")
    print(f"[OK] API_KEY: {'已设置' if api_key else '未设置'}")
    if api_key:
        print(f"   前10位: {api_key[:10]}...")
except Exception as e:
    print(f"[FAIL] 环境变量测试失败: {e}")
    sys.exit(1)

print("\n[3/3] 测试SQLAgent导入...")
try:
    from main import SQLAgent
    print("[OK] main.SQLAgent 导入成功")
except Exception as e:
    print(f"[FAIL] main.SQLAgent 导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("[OK] 所有基本测试通过！")
print("=" * 60)
print("\n现在可以尝试手动启动后端:")
print("  cd backend")
print("  python app.py")
