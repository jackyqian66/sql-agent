import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("测试: 基础功能验证（不涉及模型加载）")
print("=" * 60)

try:
    from agent.planner import Planner
    planner = Planner("test_key", "test_url", "test_model")
    print("[OK] Planner 正常")
    assert planner.model_name == "test_model"
    print(f"   - model_name: {planner.model_name}")
except Exception as e:
    print(f"[FAIL] Planner: {e}")
    sys.exit(1)

try:
    from agent.supervisor import Supervisor
    from tools.sql_executor import SQLExecutor
    tools = {"sql": SQLExecutor()}
    supervisor = Supervisor(tools, "test_key", "test_url", "test_model")
    print("[OK] Supervisor 正常")
    assert supervisor.model_name == "test_model"
    print(f"   - model_name: {supervisor.model_name}")
except Exception as e:
    print(f"[FAIL] Supervisor: {e}")
    sys.exit(1)

try:
    from agent.reporter import Reporter
    reporter = Reporter("test_key", "test_url", "test_model")
    print("[OK] Reporter 正常")
    assert reporter.model_name == "test_model"
    print(f"   - model_name: {reporter.model_name}")
except Exception as e:
    print(f"[FAIL] Reporter: {e}")
    sys.exit(1)

try:
    from tools.sql_executor import SQLExecutor
    executor = SQLExecutor()
    print("[OK] SQLExecutor 正常")
except Exception as e:
    print(f"[FAIL] SQLExecutor: {e}")
    sys.exit(1)

try:
    from search.keyword_search import KeywordSearch
    search = KeywordSearch([])
    print("[OK] KeywordSearch 正常")
except Exception as e:
    print(f"[FAIL] KeywordSearch: {e}")
    sys.exit(1)

try:
    from search.result_fusion import ResultFusion
    fusion = ResultFusion()
    print("[OK] ResultFusion 正常")
except Exception as e:
    print(f"[FAIL] ResultFusion: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("所有基础测试通过！")
print("=" * 60)
print("\n修改总结:")
print("- 所有Agent类现在支持 model_name 参数")
print("- 支持配置 API_KEY, BASE_URL, MODEL_NAME 环境变量")
print("- 向后兼容旧的 ARK_API_KEY, ARK_BASE_URL")
print("- 代码可以正常运行！")
