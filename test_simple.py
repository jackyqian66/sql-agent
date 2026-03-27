import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import SQLAgent
from dotenv import load_dotenv

async def test_simple():
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
    print("测试 1: 正常查询 (应该成功)")
    print("="*60)
    query1 = "2024年7月的销售额是多少？"
    result1 = await agent.query(query1)
    print(f"成功: {result1.get('success')}")
    if result1.get('success'):
        print(f"回答: {result1.get('response')}")

if __name__ == "__main__":
    asyncio.run(test_simple())
