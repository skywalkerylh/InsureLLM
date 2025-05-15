from fastapi import APIRouter, HTTPException, Depends
from app.routes.models import ChatRequest, ChatResponse
from app.services.chatbot import ChatService, get_chat_service

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "welcome to rag chatbot api"}

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest, chat_service: ChatService = Depends(get_chat_service)
):
    try:
        result = chat_service.process_message(
            message=request.message, conversation_id=request.conversation_id
        )

        return ChatResponse(
            response=result["response"],
            conversation_id=result["conversation_id"],
            sources=result["sources"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"chat error handling: {str(e)}")

@router.delete("/conversations/{conversation_id}")
async def clear_conversation(
    conversation_id: str, chat_service: ChatService = Depends(get_chat_service)
):
    success = chat_service.clear_conversation(conversation_id)
    if success:
        return {"status": "success", "message": f"conversation {conversation_id} deleted"}
    return {"status": "not_found", "message": f"conversation {conversation_id} not found"}
