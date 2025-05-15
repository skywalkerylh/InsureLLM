from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from app.config import Config
from app.services.vectorstore import VectorStoreService
from app.services.prompt import PromptService

class ChatService:
    def __init__(
        self,
        vector_store_service: Optional[VectorStoreService] = None,
        prompt_service: Optional[PromptService] = None,
    ):

        self.vector_store_service = vector_store_service or VectorStoreService()
        self.prompt_service = prompt_service or PromptService()
        self.conversation_memories: Dict[str, ConversationBufferMemory] = {}

    def get_llm(self):
        
        return ChatOpenAI(
            temperature=0.7,
            model_name=Config.DEFAULT_MODEL,
            base_url=Config.BASE_URL,
            api_key=Config.API_KEY,
        )

    def get_memory(self, conversation_id: str) -> ConversationBufferMemory:
        """W/O RAG version"""
        if conversation_id not in self.conversation_memories:
            self.conversation_memories[conversation_id] = ConversationBufferMemory(
                memory_key="chat_history", return_messages=True, output_key="answer"
            )
        return self.conversation_memories[conversation_id]

    def get_chain(self, conversation_id: str):
        """RAG version"""
        memory = self.get_memory(conversation_id)
        llm = self.get_llm()
        retriever = self.vector_store_service.get_retriever()
        chat_prompt = self.prompt_service.get_chat_prompt()

        return ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": chat_prompt},
            verbose=True,
            output_key="answer",
        )

    def process_message(self, message: str, conversation_id: str) -> Dict[str, Any]:

        """query -> get conversation memory -> RAG -> answer"""
        # get rag chain : integrate retrieved docs and conversation memory
        chain = self.get_chain(conversation_id)

        # ConversationalRetrievalChain format: query
        result = chain({"question": message})

        # answer and rag sources
        answer = result.get("answer", "")
        source_documents = result.get("source_documents", [])

        # format : for display 
        sources = []
        for doc in source_documents:
            sources.append({"content": doc.page_content, "metadata": doc.metadata})

        return {
            "response": answer,
            "sources": sources,
            "conversation_id": conversation_id,
        }

    def clear_conversation(self, conversation_id: str) -> bool:
        
        if conversation_id in self.conversation_memories:
            del self.conversation_memories[conversation_id]
            return True
        return False


def get_chat_service():
    return ChatService()
