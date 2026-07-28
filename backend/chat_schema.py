from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):

    question: str

    image_path: Optional[str] = None