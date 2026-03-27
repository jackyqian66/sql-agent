import asyncio
import os
import time
from dotenv import load_dotenv
from init.data_importer import DataImporter
from init.data_ingestor import DataIngestor
from search.keyword_search import KeywordSearch
from search.result_fusion import ResultFusion
from agent.planner import Planner
from agent.supervisor import Supervisor
from agent.reporter import Reporter
from tools.sql_executor import SQLExecutor

class SQLAgent:
    def __init__(self, api_key, base_url=None):
        self.data_importer = DataImporter()
        self.data_ingestor = DataIngestor()
        self.result_fusion = ResultFusion()
        self.planner = Planner(api_key, base_url)
        self.reporter = Reporter(api_key, base_url)
        
        self.tools = {
            "sql": SQLExecutor()
        }
        
        self.supervisor = Supervisor(self.tools, api_key, base_url)
        
        self.index = None
        self.documents = []
    
    async def initialize(self, data_directory):
        load_result = await self.data_ingestor.load_index()
        if load_result["success"]:
            self.index = load_result["index"]
            # 即使加载已有索引，也需要导入文档用于关键词搜索
            import_result = await self.data_importer.import_data(data_directory)
            if import_result["success"]:
                self.documents = import_result["documents"]
            return {"success": True, "message": "Agent initialized with existing index"}
        
        import_result = await self.data_importer.import_data(data_directory)
        if not import_result["success"]:
            return import_result
        
        self.documents = import_result["documents"]
        
        ingest_result = await self.data_ingestor.ingest(self.documents)
        if not ingest_result["success"]:
            return ingest_result
        
        self.index = ingest_result["index"]
        return {"success": True, "message": "Agent initialized with new index"}
    
    async def query(self, user_query):
        return await self.query_with_history(user_query, [])
    
    async def query_with_history(self, user_query, conversation_history=None):
        if not self.index:
            return {"success": False, "error": "Agent not initialized"}
        
        if conversation_history is None:
            conversation_history = []
        
        timing = {}
        total_start = time.time()
        max_retries = 1
        retry_count = 0
        last_error = None
        
        while retry_count <= max_retries:
            start = time.time()
            temp_context = {
                "query": user_query,
                "search_results": [],
                "history": conversation_history,
                "retry_count": retry_count,
                "last_error": last_error
            }
            
            if retry_count > 0:
                print(f"\n{'='*60}")
                print(f"重试第 {retry_count} 次")
                print(f"{'='*60}")
            
            plan_result = await self.planner.plan_with_history(user_query, temp_context, conversation_history)
            if not plan_result["success"]:
                return plan_result
            
            if retry_count == 0:
                timing["planner"] = round(time.time() - start, 3)
            print(f"Plan result: {plan_result}")
            
            plan = plan_result["plan"]
            tools = plan.get("tools", [])
            
            vector_results = None
            keyword_results = None
            fusion_result = None
            
            if "document" in tools:
                start = time.time()
                retriever = self.index.as_retriever(similarity_top_k=5)
                nodes = retriever.retrieve(user_query)
                retrieved_texts = [node.text for node in nodes]
                vector_results = {
                    "success": True,
                    "results": "\n\n".join(retrieved_texts)
                }
                if retry_count == 0:
                    timing["vector_search"] = round(time.time() - start, 3)
                
                start = time.time()
                keyword_search = KeywordSearch(self.documents)
                keyword_results = keyword_search.search(user_query)
                if retry_count == 0:
                    timing["keyword_search"] = round(time.time() - start, 3)
                
                print(f"Vector results: {vector_results}")
                print(f"Keyword results: {keyword_results}")
                
                start = time.time()
                fusion_result = await self.result_fusion.fuse(vector_results, keyword_results)
                if not fusion_result["success"]:
                    return fusion_result
                if retry_count == 0:
                    timing["result_fusion"] = round(time.time() - start, 3)
                print(f"Fusion result: {fusion_result}")
            
            search_context = {}
            if fusion_result:
                search_context = {
                    "vector_text": vector_results.get("results", "") if vector_results else "",
                    "keyword_text": [result.get("text", "") for result in keyword_results.get("results", [])] if keyword_results and keyword_results.get("success") else [],
                    "fusion_results": fusion_result["results"]
                }
            
            start = time.time()
            execute_result = await self.supervisor.execute(plan, search_context)
            print(f"Execute result: {execute_result}")
            
            if retry_count == 0:
                timing["supervisor_execute"] = round(time.time() - start, 3)
            
            if execute_result["success"]:
                start = time.time()
                report_result = await self.reporter.generate_response_with_history(user_query, execute_result["results"], conversation_history)
                if not report_result["success"]:
                    return report_result
                timing["reporter"] = round(time.time() - start, 3)
                
                timing["total"] = round(time.time() - total_start, 3)
                
                print(f"\n{'='*60}")
                print("性能统计")
                print(f"{'='*60}")
                for key, value in timing.items():
                    print(f"{key:<20}: {value:>8.3f}s")
                print(f"{'='*60}\n")
                
                return {
                    "success": True,
                    "response": report_result["response"],
                    "execution_results": execute_result["results"],
                    "timing": timing
                }
            else:
                last_error = execute_result.get("error", "Unknown error")
                print(f"执行失败，错误: {last_error}")
                
                if retry_count < max_retries:
                    retry_count += 1
                    print(f"准备重试... (剩余重试次数: {max_retries - retry_count + 1})")
                else:
                    return execute_result


