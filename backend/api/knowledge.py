from fastapi import APIRouter

from services.knowledge_service import knowledge_service

router = APIRouter()

@router.get("/knowledge")

def knowledge():

    return knowledge_service.get_knowledge()