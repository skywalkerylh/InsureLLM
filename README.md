# InsureLLM: Knowledge Assistant [(Demo)](https://drive.google.com/file/d/1CLrgC36yhEiFpNlJCPIJLkhDR4HHj8_c/view?usp=sharing)
<img src="Fig/ChatbotwithRAG.png" width="600" height="300" />

# 🧠 InsureLLM – RAG-based Insurance Chatbot

I built a chatbot system called InsureLLM, designed to answer insurance-related questions based on internal documents.
It uses **LangChain’s RAG** pipeline, integrated with a local **Llama 3.1** model through an OpenAI-compatible API.

The backend is built with **FastAPI**, exposing endpoints, and the frontend is a simple **Gradio UI**.
I containerized the whole system using Docker and orchestrated the services with **Docker Compose**, so everything can be started with one command.

---

# 🔧 Tech Stack
| Layer       | Technology                                 |
| ----------- | ------------------------------------------ |
| LLM         | Llama3.1 (local, via OpenAI API)           |
| Embedding   | `all-MiniLM-L6-v2` (sentence-transformers) |
| Framework   | LangChain (ConversationalRetrievalChain)   |
| Backend API | FastAPI                                    |
| Frontend UI | Gradio                                     |
| Vector DB   | Chroma                                     |
| Deployment  | Docker, Docker Compose                     |
| Config Mgmt | `.env`, DI (Dependency Injection)          |
