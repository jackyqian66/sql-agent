import json
import requests

class Supervisor:
    def __init__(self, tools, api_key=None, base_url="https://ark.cn-beijing.volces.com/api/v3/chat/completions", model_name="doubao-seed-1-8-251228"):
        self.tools = tools
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name
        
        self.critical_error_keywords = [
            "connection error",
            "timeout",
            "server error",
            "500",
            "502",
            "503",
            "504",
            "api key",
            "authentication",
            "permission",
            "not found",
            "table doesn't exist",
            "column doesn't exist",
            "no such table",
            "no such column"
        ]

    def _is_critical_error(self, error_msg):
        error_lower = error_msg.lower()
        for keyword in self.critical_error_keywords:
            if keyword.lower() in error_lower:
                return True
        return False

    async def execute(self, plan, search_context=None):
        try:
            # 优化：一次性执行所有步骤，而不是每个步骤都调用 LLM
            result = await self._execute_all_steps_with_llm(plan.get("steps", []), search_context)
            return result
        except Exception as e:
            error_msg = str(e)
            is_critical = self._is_critical_error(error_msg)
            return {
                "success": False, 
                "error": error_msg,
                "is_critical": is_critical
            }

    async def _execute_all_steps_with_llm(self, steps, search_context=None):
        try:
            results = []
            
            for step in steps:
                step_lower = step.lower()
                
                if "execute sql:" in step_lower or "sql:" in step_lower:
                    sql_query = step.split(":", 1)[1].strip() if ":" in step else step
                    print(f"执行SQL查询: {sql_query}")
                    
                    sql_executor = self.tools.get("sql")
                    if sql_executor:
                        sql_result = await sql_executor.execute(sql_query)
                        results.append({
                            "step": step,
                            "result": sql_result
                        })
                        
                        if not sql_result["success"]:
                            error_msg = sql_result.get("error", "Unknown error")
                            is_critical = self._is_critical_error(error_msg)
                            return {
                                "success": False, 
                                "error": error_msg,
                                "is_critical": is_critical
                            }
                    else:
                        error_msg = "SQL executor not available"
                        return {
                            "success": False, 
                            "error": error_msg,
                            "is_critical": True
                        }
                else:
                    context_info = ""
                    if search_context:
                        context_info = f"""
Search results:
{json.dumps(search_context, ensure_ascii=False, indent=2)}
"""
                    
                    prompt = f"""
You are a Step Executor. Execute this single step.

STEP TO EXECUTE: {step}

SEARCH CONTEXT:
{context_info}

YOUR TASK:
1. Check if this step needs external information or web search
2. If it needs web search or external info: use your knowledge to answer directly
3. If answer is in search context: extract it from there
4. Return result in exact JSON format below
5. RESPOND QUICKLY - keep your answer concise

RESPONSE FORMAT (JSON ONLY, NO OTHER TEXT):
{{
  "success": true,
  "data": "result data here"
}}
"""
                    
                    if self.api_key:
                        headers = {
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {self.api_key}"
                        }

                        data = {
                            "model": self.model_name,
                            "messages": [{"role": "user", "content": prompt}],
                            "temperature": 0.3,
                            "max_tokens": 500
                        }

                        response = requests.post(self.base_url, headers=headers, json=data)
                        response.raise_for_status()
                        result = response.json()
                        content = result["choices"][0]["message"]["content"]
                        
                        try:
                            parsed_result = json.loads(content)
                            results.append({
                                "step": step,
                                "result": parsed_result
                            })
                        except:
                            results.append({
                                "step": step,
                                "result": {"success": True, "data": content}
                            })
                    else:
                        results.append({
                            "step": step,
                            "result": {"success": True, "data": step}
                        })
            
            return {"success": True, "results": results, "error": None, "is_critical": False}
        except Exception as e:
            error_msg = str(e)
            is_critical = self._is_critical_error(error_msg)
            return {
                "success": False, 
                "error": error_msg,
                "is_critical": is_critical
            }
