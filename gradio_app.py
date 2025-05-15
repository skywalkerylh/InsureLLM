import gradio as gr
import requests
import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod


class ChatClient(ABC):
    @abstractmethod
    def chat(self, message: str) -> str:
        pass

class FastAPIChatClient(ChatClient):
    def __init__(self, api_url: str):
        self.api_url = api_url

    def chat(self, message: str) -> str:
        try:
            response = requests.post(f"{self.api_url}/chat", json={"message": message})
            response.raise_for_status()
            return response.json().get("response", "No response received")
        except requests.RequestException as e:
            return f"Error communicating with API: {str(e)}"

def create_gradio_interface(chat_client: ChatClient):
    def chat_with_bot(message, history=[]):
        return chat_client.chat(message)

    return gr.ChatInterface(chat_with_bot, type="messages")

def main():

    load_dotenv()
    api_url = os.getenv("API_URL")
    client = FastAPIChatClient(api_url=api_url)
    ui = create_gradio_interface(client)
    ui.launch()

if __name__ == "__main__":
    main()
