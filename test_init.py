import sys
import os
import asyncio

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("测试后端初始化")
print("=" * 60)

print("\n[1/4] 检查模型目录...")
model_path = "./models/bge-base-zh-v1.5"
if os.path.exists(model_path):
    print(f"[OK] 模型目录存在: {model_path}")
    files = os.listdir(model_path)
    print(f"   包含文件: {len(files)} 个")
else:
    print(f"[FAIL] 模型目录不存在: {model_path}")
    sys.exit(1)

print("\n[2/4] 测试导入...")
try:
    from main import SQLAgent
    print("[OK] main.SQLAgent 导入成功")
except Exception as e:
    print(f"[FAIL] main.SQLAgent 导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n[3/4] 检查环境变量...")
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

print("\n[4/4] 测试初始化Agent...")
try:
    agent = SQLAgent(api_key, os.getenv("BASE_URL") or os.getenv("ARK_BASE_URL"), os.getenv("MODEL_NAME"))
    print("[OK] SQLAgent 初始化成功")
except Exception as e:
    print(f"[FAIL] SQLAgent 初始化失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("[OK] 所有测试通过！后端可以正常初始化！")
print("=" * 60)
