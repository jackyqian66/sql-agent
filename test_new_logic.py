import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import SQLAgent
from dotenv import load_dotenv

async def test_new_logic():
    load_dotenv()
    api_key = os.getenv("ARK_API_KEY")
    base_url = os.getenv("ARK_BASE_URL")
    
    if not api_key:
        print("错误: ARK_API_KEY 环境变量未设置")
        return
    
    agent = SQLAgent(api_key, base_url)
    
    print("正在初始化 Agent...")
    init_result = await agent.initialize("./data")
    print(f"初始化结果: {init_result}")
    if not init_result["success"]:
        return
    
    print("\n" + "="*60)
    print("测试 1: 重大错误 - 查询不存在的表 (应该重试)")
    print("="*60)
    
    from agent.planner import Planner
    
    planner = Planner(api_key, base_url)
    
    test_context = {
        "query": "查询不存在的表",
        "search_results": [],
        "history": [],
        "retry_count": 0,
        "last_error": None
    }
    
    plan_result = await planner.plan_with_history("SELECT * FROM non_existent_table", test_context, [])
    print(f"Plan result: {plan_result}")
    
    from agent.supervisor import Supervisor
    from tools.sql_executor import SQLExecutor
    
    supervisor = Supervisor({"sql": SQLExecutor()}, api_key, base_url)
    
    if plan_result["success"]:
        execute_result = await supervisor.execute(plan_result["plan"])
        print(f"Execute result: {execute_result}")
        print(f"成功: {execute_result.get('success')}")
        print(f"错误: {execute_result.get('error')}")
        print(f"是否为重大错误: {execute_result.get('is_critical')}")
    
    print("\n" + "="*60)
    print("测试 2: 正常查询 (应该成功)")
    print("="*60)
    query2 = "2024年7月的销售额是多少？"
    result2 = await agent.query(query2)
    print(f"结果: {result2}")
    print(f"成功: {result2.get('success')}")
    if result2.get('success'):
        print(f"回答: {result2.get('response')}")

if __name__ == "__main__":
    asyncio.run(test_new_logic())
