from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.chat_service import ChatService

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
def chat(request: ChatRequest):

    try:

        response = ChatService.ask(request.question)

        return {

            "success": True,

            "question": request.question,

            "answer": response.get("answer"),

            "sources": response.get("sources", []),

            "graph": response.get("graph"),

            "vision": response.get("vision", [])

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )