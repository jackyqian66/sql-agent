from llama_index.core import VectorStoreIndex, Document
from llama_index.core.storage import StorageContext
from llama_index.core.vector_stores.simple import SimpleVectorStore
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os
from dotenv import load_dotenv

class DataIngestor:
    def __init__(self):
        self.index = None
        self.index_path = "./index"
        
        load_dotenv()
        
        # 从环境变量获取模型路径，默认使用项目内的模型
        model_path = os.getenv("EMBEDDING_MODEL_PATH", "./models/bge-base-zh-v1.5")
        
        # 如果路径不存在，尝试使用 HuggingFace 模型名称
        if not os.path.exists(model_path):
            model_path = "BAAI/bge-base-zh-v1.5"
        
        print(f"使用嵌入模型: {model_path}")
        
        import logging
        logging.getLogger("transformers").setLevel(logging.ERROR)
        logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
        
        Settings.embed_model = HuggingFaceEmbedding(
            model_name=model_path,
            cache_folder="./models_cache"
        )

    async def ingest(self, documents):
        try:
            self.index = VectorStoreIndex.from_documents(documents, embed_model=Settings.embed_model)
            # 保存索引
            save_result = self.save_index()
            if not save_result["success"]:
                return save_result
            return {"success": True, "index": self.index}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def load_index(self):
        try:
            if os.path.exists(self.index_path):
                # 加载已保存的索引
                vector_store = SimpleVectorStore.from_persist_dir(self.index_path)
                storage_context = StorageContext.from_defaults(vector_store=vector_store)
                self.index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)
                return {"success": True, "index": self.index}
            else:
                return {"success": False, "error": "Index not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def save_index(self):
        try:
            if self.index:
                # 保存索引到磁盘
                self.index.storage_context.persist(persist_dir=self.index_path)
                return {"success": True}
            else:
                return {"success": False, "error": "No index to save"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_index(self):
        return self.index
