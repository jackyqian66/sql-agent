import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("测试 1: 导入各个模块")
print("=" * 60)

try:
    from agent.planner import Planner
    print("[OK] agent.planner.Planner 导入成功")
except Exception as e:
    print(f"[FAIL] agent.planner.Planner 导入失败: {e}")
    sys.exit(1)

try:
    from agent.supervisor import Supervisor
    print("[OK] agent.supervisor.Supervisor 导入成功")
except Exception as e:
    print(f"[FAIL] agent.supervisor.Supervisor 导入失败: {e}")
    sys.exit(1)

try:
    from agent.reporter import Reporter
    print("[OK] agent.reporter.Reporter 导入成功")
except Exception as e:
    print(f"[FAIL] agent.reporter.Reporter 导入失败: {e}")
    sys.exit(1)

try:
    from tools.sql_executor import SQLExecutor
    print("[OK] tools.sql_executor.SQLExecutor 导入成功")
except Exception as e:
    print(f"[FAIL] tools.sql_executor.SQLExecutor 导入失败: {e}")
    sys.exit(1)

try:
    from main import SQLAgent
    print("[OK] main.SQLAgent 导入成功")
except Exception as e:
    print(f"[FAIL] main.SQLAgent 导入失败: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("测试 2: 实例化各个类（不传真实API Key）")
print("=" * 60)

try:
    planner = Planner("test_key", "test_url", "test_model")
    print("[OK] Planner 实例化成功")
    print(f"   - model_name: {planner.model_name}")
except Exception as e:
    print(f"[FAIL] Planner 实例化失败: {e}")
    sys.exit(1)

try:
    from tools.sql_executor import SQLExecutor
    tools = {"sql": SQLExecutor()}
    supervisor = Supervisor(tools, "test_key", "test_url", "test_model")
    print("[OK] Supervisor 实例化成功")
    print(f"   - model_name: {supervisor.model_name}")
except Exception as e:
    print(f"[FAIL] Supervisor 实例化失败: {e}")
    sys.exit(1)

try:
    reporter = Reporter("test_key", "test_url", "test_model")
    print("[OK] Reporter 实例化成功")
    print(f"   - model_name: {reporter.model_name}")
except Exception as e:
    print(f"[FAIL] Reporter 实例化失败: {e}")
    sys.exit(1)

try:
    agent = SQLAgent("test_key", "test_url", "test_model")
    print("[OK] SQLAgent 实例化成功")
except Exception as e:
    print(f"[FAIL] SQLAgent 实例化失败: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("所有测试通过！代码可以正常运行！")
print("=" * 60)
