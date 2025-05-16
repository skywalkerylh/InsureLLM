import glob
import os
from langchain_chroma.vectorstores import Chroma
from langchain_core.retrievers import BaseRetriever
from langchain.vectorstores.base import VectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from app.services.file_processing import DocumentProcessor
from app.config import Config

class VectorStoreService:
    def __init__(self, vector_store_path: str = "knowledge-base"):

        self.db_path = os.path.abspath("vector_db")
        if self.exists_db(self.db_path):
            embeddings = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL)
            self.vector_store = Chroma(
                persist_directory= self.db_path, 
                embedding_function= embeddings
            )
        else:
            self.vector_store = self._initialize_vector_store(vector_store_path)

    def _initialize_vector_store(self, path: str) -> VectorStore:
        folders = glob.glob(f"{path}/*")
        doc_processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)
        docs = doc_processor.load_documents(folders)
        chunks = doc_processor.split_documents()
        vectors = doc_processor.create_embeddings(chunks)
        return vectors

    def get_retriever(
        self, search_type: str = "similarity", k: int = 4
    ) -> BaseRetriever:

        return self.vector_store.as_retriever(
            search_type=search_type, search_kwargs={"k": k}
        )

    def exists_db(self,path: str) -> bool:
        has_sqlite = os.path.exists(os.path.join(path, "chroma.sqlite3"))
        has_any_index_dir = any(
            os.path.isdir(os.path.join(path, f)) and len(f) == 36  # UUID-like dir
            for f in os.listdir(path)
        )
        return has_sqlite and has_any_index_dir
