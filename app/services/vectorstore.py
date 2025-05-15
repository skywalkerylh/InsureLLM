import glob
from langchain.vectorstores.base import VectorStore
from langchain_core.retrievers import BaseRetriever
from app.services.file_processing import DocumentProcessor

class VectorStoreService:
    def __init__(self, vector_store_path: str = "knowledge-base"):
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
