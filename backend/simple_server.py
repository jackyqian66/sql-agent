import asyncio
import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import SQLAgent
from dotenv import load_dotenv

agent = None
agent_initialized = False

def init_agent():
    global agent, agent_initialized
    if agent_initialized:
        return {"success": True, "message": "Agent already initialized"}
    
    load_dotenv()
    api_key = os.getenv("ARK_API_KEY")
    base_url = os.getenv("ARK_BASE_URL")
    
    if not api_key:
        return {"success": False, "error": "ARK_API_KEY environment variable is not set"}
    
    agent = SQLAgent(api_key, base_url)
    return {"success": True, "agent": agent}

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response