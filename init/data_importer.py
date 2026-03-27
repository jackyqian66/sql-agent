from llama_index.core import SimpleDirectoryReader

class DataImporter:
    def __init__(self):
        # 不在这里初始化reader，而是在import_data方法中根据目录路径初始化
        pass

    async def import_data(self, directory_path):
        try:
            reader = SimpleDirectoryReader(
                input_dir=directory_path,
                required_exts=[".txt", ".md"]
            )
            documents = reader.load_data()
            return {"success": True, "documents": documents}
        except Exception as e:
            return {"success": False, "error": str(e)}
