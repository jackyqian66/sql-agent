from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import os
from dotenv import load_dotenv
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import SQLAgent

app = Flask(__name__)
CORS(app)

agent = None
agent_initialized = False
conversation_history = []

def init_agent():
    global agent, agent_initialized
    if agent_initialized:
        return {"success": True, "message": "Agent already initialized"}
    
    load_dotenv()
    api_key = os.getenv("API_KEY") or os.getenv("ARK_API_KEY")
    base_url = os.getenv("BASE_URL") or os.getenv("ARK_BASE_URL")
    model_name = os.getenv("MODEL_NAME")
    
    if not api_key:
        return {"success": False, "error": "API_KEY environment variable is not set"}
    
    agent = SQLAgent(api_key, base_url, model_name)
    return {"success": True, "agent": agent}

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "initialized": agent_initialized})

@app.route('/api/init', methods=['POST'])
def initialize():
    global agent_initialized
    result = init_agent()
    if not result["success"]:
        return jsonify(result), 400
    
    data = request.json or {}
    data_directory = data.get("data_directory", "./data")
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        init_result = loop.run_until_complete(agent.initialize(data_directory))
        loop.close()
        
        if init_result["success"]:
            agent_initialized = True
        
        return jsonify(init_result)
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print("[ERROR] Initialization failed:")
        print(error_detail)
        return jsonify({"success": False, "error": str(e), "detail": error_detail}), 500

@app.route('/api/query', methods=['POST'])
def query():
    global conversation_history
    if not agent_initialized or not agent:
        return jsonify({"success": False, "error": "Agent not initialized. Call /api/init first."}), 400
    
    data = request.json
    if not data or "query" not in data:
        return jsonify({"success": False, "error": "Query is required"}), 400
    
    user_query = data["query"]
    history = data.get("history", [])
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(agent.query_with_history(user_query, history))
        loop.close()
        
        if result["success"]:
            conversation_history.append({"role": "user", "content": user_query})
            conversation_history.append({"role": "assistant", "content": result.get("response", "")})
        
        return jsonify(result)
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print("[ERROR] Query failed:")
        print(error_detail)
        return jsonify({"success": False, "error": str(e), "detail": error_detail}), 500

if __name__ == '__main__':
    print("Starting SQL Agent Backend...")
    app.run(host='0.0.0.0', port=8000, debug=True)
