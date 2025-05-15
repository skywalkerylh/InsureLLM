# InsureLLM: Knowledge Assistant

[Gradio 前端介面 (gradio_app.py)]
        │
        ▼
HTTP POST 請求到 /chat
        │
        ▼
[FastAPI 後端 (main.py → /chat)]
        │
        ▼
LangChain + ChromaDB回傳答案 (RAG)
        │
        ▼
[Gradio 顯示結果]
