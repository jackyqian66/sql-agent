import sqlite3
import os

class SQLExecutor:
    def __init__(self, db_path="data/sales.db"):
        self.db_path = db_path

    async def execute(self, query):
        try:
            if not os.path.exists(self.db_path):
                return {"success": False, "error": f"Database not found: {self.db_path}"}
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description] if cursor.description else []
            
            results = []
            for row in rows:
                row_dict = {}
                for i, col in enumerate(columns):
                    row_dict[col] = row[i]
                results.append(row_dict)
            
            conn.close()
            
            return {
                "success": True,
                "results": {
                    "rows": results,
                    "columns": columns
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
