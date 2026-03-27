import asyncio
from tools.sql_executor import SQLExecutor

async def test_sql_queries():
    executor = SQLExecutor()
    
    test_queries = [
        "SELECT * FROM sales LIMIT 5",
        "SELECT product_name, SUM(sales_amount) as total_sales FROM sales GROUP BY product_name ORDER BY total_sales DESC",
        "SELECT month, SUM(sales_amount) as monthly_sales FROM sales GROUP BY month",
        "SELECT COUNT(*) as customer_count FROM customers",
        "SELECT * FROM sales WHERE product_name = 'Product A'"
    ]
    
    print("="*60)
    print("SQL查询测试")
    print("="*60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n测试查询 {i}: {query}")
        print("-"*60)
        
        result = await executor.execute(query)
        
        if result["success"]:
            print(f"[OK] 查询成功!")
            print(f"列: {result['results']['columns']}")
            print(f"行数: {len(result['results']['rows'])}")
            print("结果:")
            for row in result['results']['rows']:
                print(f"  {row}")
        else:
            print(f"[ERROR] 查询失败: {result['error']}")
        
        print()

if __name__ == "__main__":
    asyncio.run(test_sql_queries())
