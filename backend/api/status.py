from fastapi import APIRouter
from utils.upload_status import upload_status

router = APIRouter()


@router.get("/upload-status")
def get_upload_status():

    return upload_status