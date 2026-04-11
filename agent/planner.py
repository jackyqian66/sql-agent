import json
import requests

class Planner:
    def __init__(self, api_key, base_url="https://ark.cn-beijing.volces.com/api/v3/chat/completions", model_name="doubao-seed-1-8-251228"):
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name

    async def plan(self, query, context):
        return await self.plan_with_history(query, context, [])
    
    async def plan_with_history(self, query, context, conversation_history):
        try:
            history_text = ""
            if conversation_history:
                history_text = "\n\nCONVERSATION HISTORY:\n"
                for msg in conversation_history:
                    history_text += f"{msg['role'].upper()}: {msg['content']}\n"
            
            retry_info = ""
            retry_count = context.get("retry_count", 0)
            last_error = context.get("last_error")
            if retry_count > 0 and last_error:
                retry_info = f"""
PREVIOUS ATTEMPT FAILED:
Retry Count: {retry_count}
Last Error: {last_error}

IMPORTANT: Please fix the issue from the previous attempt. Make sure:
1. SQL syntax is correct
2. Table and column names exist in the database
3. The query logic is sound
"""

            prompt = f"""
You are a SQL Agent Planner. You must create a plan to answer the user's query.

DATABASE SCHEMA:
- Table: sales (id, product_name, sales_amount, month, quarter, year)
- Table: customers (id, customer_name, email, signup_date)

AVAILABLE TOOLS:
- sql: Execute SQL queries on the database

{history_text}

{retry_info}

USER QUERY: {query}

SEARCH CONTEXT:
{json.dumps(context, ensure_ascii=False, indent=2)}

YOUR TASKS:
1. First, decide what type of query this is:
   - If it's about sales data or customers in our database: use SQL tool
   - If it's general knowledge or needs external info: NO tools needed, the LLM will answer directly
   - If it's about sales data, monthly breakdown, product performance, or info in our sales documents: use "document" tool

2. Create simple, clear steps

3. When using SQL, include the exact SQL query in the step like "Execute SQL: [SQL query]"

4. If no tools needed, just create one step like "Answer the question using general knowledge"

IMPORTANT:
- For SQL queries only: tools = ["sql"]
- For general knowledge only: tools = []
- For document search only: tools = ["document"]
- For mixed queries: tools = ["sql", "general", "document"] as needed
- Consider the conversation history when making your plan
- If this is a retry, fix the mistakes from the previous attempt

RESPONSE FORMAT (JSON ONLY):
{{
  "intent": "what the user wants",
  "tools": ["sql"],
  "steps": ["step 1", "step 2"]
}}

EXAMPLES:
1. Sales query:
{{
  "intent": "Calculate total sales for Product A",
  "tools": ["sql"],
  "steps": ["Execute SQL: SELECT SUM(sales_amount) FROM sales WHERE product_name = 'Product A'"]
}}

2. General knowledge query:
{{
  "intent": "Answer the question about capital of France",
  "tools": [],
  "steps": ["Answer the question using general knowledge"]
}}
"""

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            data = {
                "model": self.model_name,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 500
            }

            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            plan = json.loads(content)
            return {"success": True, "plan": plan}
        except Exception as e:
            return {"success": False, "error": str(e)}
