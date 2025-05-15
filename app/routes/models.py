from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ChatRequest(BaseModel):
    message: str
    conversation_id: str = "default"


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    sources: Optional[List[Dict[str, Any]]] = None
