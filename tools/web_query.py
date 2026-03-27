import requests

class WebQuery:
    async def execute(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return {
                "success": True,
                "results": {
                    "content": response.text,
                    "status_code": response.status_code
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
