from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain_chroma import Chroma
from app.config import Config
import os

class DocumentProcessor:
    def __init__(self, chunk_size, chunk_overlap):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.documents = []
        self.text_splitter = CharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

    def load_documents(self, folders: list[str]) -> list:

        documents = []
        for folder in folders:
            print(folder)
            doc_type = os.path.basename(folder)
            loader = DirectoryLoader(
                folder,
                glob="**/*.md",
                loader_cls=TextLoader,
                loader_kwargs={"encoding": "utf-8"},
            )
            folder_docs = loader.load()
            documents.extend([self._add_metadata(doc, doc_type) for doc in folder_docs])

        self.documents = documents
        return documents

    def split_documents(self) -> list:
        if not self.documents:
            raise ValueError("No documents loaded. Please call load_documents first.")

        return self.text_splitter.split_documents(self.documents)

    def _add_metadata(self, doc, doc_type: str):
        doc.metadata["doc_type"] = doc_type
        return doc

    @staticmethod
    def create_embeddings(chunks: list[Document]):
        # model
        embeddings = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL)

        # create vectordb
        if os.path.exists(Config.DB_NAME):
            Chroma(
                persist_directory=Config.DB_NAME, embedding_function=embeddings
            ).delete_collection()

        # Convert doc text into vectors
        vectorstore = Chroma.from_documents(
            documents=chunks, embedding=embeddings, persist_directory=Config.DB_NAME
        )
        print(f"Vectorstore created with {vectorstore._collection.count()} documents")

        return vectorstore
