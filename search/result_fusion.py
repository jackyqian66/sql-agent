class ResultFusion:
    async def fuse(self, vector_results, keyword_results):
        try:
            fused_results = []
            
            # 处理向量检索结果
            if vector_results.get("success"):
                fused_results.append({
                    "type": "vector",
                    "content": vector_results["results"],
                    "score": 1.0
                })
            
            # 处理关键词检索结果
            if keyword_results.get("success") and keyword_results["results"]:
                max_score = max([r["score"] for r in keyword_results["results"]])
                for result in keyword_results["results"]:
                    fused_results.append({
                        "type": "keyword",
                        "content": result["text"],
                        "score": result["score"] / max_score if max_score > 0 else 0
                    })
            
            return {"success": True, "results": fused_results}
        except Exception as e:
            return {"success": False, "error": str(e)}
