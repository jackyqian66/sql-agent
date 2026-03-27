import sqlite3
import os

class SchemaQuery:
    def __init__(self, db_path="data/sales.db"):
        self.db_path = db_path

    async def execute(self, table_name=None):
        try:
            if not os.path.exists(self.db_path):
                return {"success": False, "error": f"Database not found: {self.db_path}"}
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if table_name:
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                schema = {}
                for col in columns:
                    schema[col[1]] = {
                        "type": col[2],
                        "not_null": bool(col[3]),
                        "default_value": col[4],
                        "primary_key": bool(col[5])
                    }
                conn.close()
                return {
                    "success": True,
                    "results": {
                        "table": table_name,
                        "schema": schema
                    }
                }
            else:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                
                all_schemas = {}
                for table in tables:
                    cursor.execute(f"PRAGMA table_info({table})")
                    columns = cursor.fetchall()
                    table_schema = {}
                    for col in columns:
                        table_schema[col[1]] = {
                            "type": col[2],
                            "not_null": bool(col[3]),
                            "default_value": col[4],
                            "primary_key": bool(col[5])
                        }
                    all_schemas[table] = table_schema
                
                conn.close()
                return {
                    "success": True,
                    "results": {
                        "tables": tables,
                        "schema": all_schemas
                    }
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
