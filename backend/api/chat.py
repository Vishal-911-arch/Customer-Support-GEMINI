from fastapi import APIRouter, HTTPException, Depends

from services.chat_service import ChatService
from chat_schema import ChatRequest
from api.deps import get_current_user

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest, user: str = Depends(get_current_user)):

    try:

        print("\n")
        print("=" * 70)
        print("CHAT REQUEST")
        print("=" * 70)

        print("QUESTION :")
        print(request.question)
        print()

        print("IMAGE PATH :")
        print(request.image_path)
        print("=" * 70)

        history = [
            msg.model_dump()
            for msg in request.history
        ]

        # ====================================================
        # IMAGE CHAT
        # ====================================================

        if request.image_path:

            print("\n✓ IMAGE MODE\n")

            response = ChatService.ask_image(
                request.question,
                request.image_path,
                history=history
            )

        # ====================================================
        # PDF RAG
        # ====================================================

        else:

            print("\n✓ PDF RAG MODE\n")

            response = ChatService.ask(
                request.question,
                history=history
            )

        # ====================================================
        # RESPONSE
        # ====================================================

        return {
            "success": True,
            "question": request.question,
            "answer": response.get("answer", ""),
            "title": response.get("title", "New Chat"),
            "sources": response.get("sources", []),
            "graph": response.get("graph", None),
            "figure": response.get("figure", None),
            "vision": response.get("vision", [])
        }

    except Exception as e:

        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )