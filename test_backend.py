import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import SQLAgent
from dotenv import load_dotenv

async def test_retry():
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
    query1 = "2024年第三季度的总销售额是多少？"
    result1 = await agent.query(query1)
    print(f"结果: {result1}")
    print(f"成功: {result1.get('success')}")
    if result1.get('success'):
        print(f"回答: {result1.get('response')}")
    
    print("\n" + "="*60)
    print("测试 2: 轻微错误查询 (应该重试)")
    print("="*60)
    query2 = "销售数据在哪里？"
    result2 = await agent.query(query2)
    print(f"结果: {result2}")
    print(f"成功: {result2.get('success')}")
    if result2.get('success'):
        print(f"回答: {result2.get('response')}")

if __name__ == "__main__":
    asyncio.run(test_retry())
