from fastapi import APIRouter
from fastapi import HTTPException

from services.chat_service import ChatService
from chat_schema import ChatRequest

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):

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

        # ====================================================
        # IMAGE CHAT
        # ====================================================

        if request.image_path:

            print("\n✓ IMAGE MODE\n")

            response = ChatService.ask_image(

                request.question,

                request.image_path

            )

        # ====================================================
        # PDF RAG
        # ====================================================

        else:

            print("\n✓ PDF RAG MODE\n")

            response = ChatService.ask(

                request.question

            )

        # ====================================================
        # RESPONSE
        # ====================================================

        return {

    "success": True,

    "question":

        request.question,

    "answer":

        response.get(

            "answer",

            ""

        ),

    "title":

        response.get(

            "title",

            "New Chat"

        ),

    "sources":

        response.get(

            "sources",

            []

        ),

    "graph":

        response.get(

            "graph",

            None

        ),

    "figure":

        response.get(

            "figure",

            None

        ),

    "vision":

        response.get(

            "vision",

            []

        )

}
    except Exception as e:

        import traceback

        traceback.print_exc()

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )