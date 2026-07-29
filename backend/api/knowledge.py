from fastapi import APIRouter, Depends

from services.knowledge_service import knowledge_service
from api.deps import get_current_user

router = APIRouter()


@router.get("/knowledge")
def knowledge(user: str = Depends(get_current_user)):
    return knowledge_service.get_knowledge()