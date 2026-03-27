import json
import requests

class Reporter:
    def __init__(self, api_key, base_url="https://ark.cn-beijing.volces.com/api/v3/chat/completions"):
        self.api_key = api_key
        self.base_url = base_url

    async def generate_response(self, query, results):
        return await self.generate_response_with_history(query, results, [])
    
    async def generate_response_with_history(self, query, results, conversation_history):
        try:
            history_text = ""
            if conversation_history:
                history_text = "\n\nCONVERSATION HISTORY:\n"
                for msg in conversation_history:
                    history_text += f"{msg['role'].upper()}: {msg['content']}\n"

            prompt = f"""
You are a helpful assistant that answers user questions based on provided results.

YOUR TASK:
1. Read and understand the user's question carefully
2. Look at the execution results provided
3. Extract the key information needed to answer the question
4. Write a clear, natural language answer
5. Make sure your answer directly addresses the user's question
6. Use simple, easy-to-understand language
7. If the results contain numbers or statistics, include them in your answer
8. RESPOND QUICKLY - keep your answer concise and to the point
9. Consider the conversation history to provide context-aware answers

{history_text}

USER QUESTION: {query}

EXECUTION RESULTS:
{json.dumps(results, ensure_ascii=False, indent=2)}

Please provide your answer now:
"""

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            data = {
                    "model": "doubao-seed-1-8-251228",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 500
            }

            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return {"success": True, "response": result["choices"][0]["message"]["content"]}
        except Exception as e:
            return {"success": False, "error": str(e)}
