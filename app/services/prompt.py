from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate

class PromptService:    
    def __init__(self):
        pass
    def get_chat_prompt(self) -> ChatPromptTemplate:

        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(self.system_prompt()),
                
                HumanMessagePromptTemplate.from_template(
                    "Context:\n{context}\n\nQuestion:\n{question}"
                ),
            ]
        )

    def system_prompt(self) -> str:
        return (
            "You are an insurance knowledge assistant for InsureLLM employees.\n"
            "Answer questions based on the retrieved documents.\n"
            "If you don't know the answer, say you don't know.\n"
            "'Hi, how can I help you today?' is the greeting message.\n"
            "If user needs more information, provide detailed answers.\n"
            "If user mentioned 'bye', then reply with 'Goodbye! Have a great day!'"
        )
