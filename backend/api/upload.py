from fastapi import APIRouter, UploadFile, File, HTTPException

from services.upload_service import UploadService

router = APIRouter()


# -----------------------------------------
# Upload PDF
# -----------------------------------------

@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):

    try:

        result = await UploadService.upload_pdf(file)

        return {
            "success": True,
            "message": "PDF indexed successfully.",
            "data": result
        }

    except Exception as e:

        import traceback

        traceback.print_exc()

        raise HTTPException(

            status_code=500,

            detail=str(e)

    )


# -----------------------------------------
# Upload Image
# -----------------------------------------

@router.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):

    try:

        result = await UploadService.upload_image(file)

        return {
            "success": True,
            "message": "Image indexed successfully.",
            "data": result
        }

    except Exception as e:

        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )