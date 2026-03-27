import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import SQLAgent
from dotenv import load_dotenv

async def test_critical_error():
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
    print("测试: 重大错误 (应该不重试)")
    print("="*60)
    
    from agent.supervisor import Supervisor
    from tools.sql_executor import SQLExecutor
    
    supervisor = Supervisor({"sql": SQLExecutor()}, api_key, base_url)
    
    test_plan = {
        "steps": ["Execute SQL: SELECT * FROM non_existent_table"]
    }
    
    result = await supervisor.execute(test_plan)
    print(f"Supervisor 执行结果: {result}")
    print(f"成功: {result.get('success')}")
    print(f"错误: {result.get('error')}")
    print(f"是否为重大错误: {result.get('is_critical')}")

if __name__ == "__main__":
    asyncio.run(test_critical_error())
