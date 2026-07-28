from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import LLM_MODEL

from api.chat import router as chat_router
from api.health import router as health_router
from api.upload import router as upload_router
from api.status import router as status_router

from api.knowledge import router as knowledge_router
app = FastAPI(

    title="AI Customer Support",

    version="1.0.0"

)

# ----------------------------------------------------
# CORS
# ----------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",

        "http://localhost:4173",
        "http://127.0.0.1:4173",

        "http://192.168.172.219:4173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# Routers
# ----------------------------------------------------

app.include_router(chat_router)

app.include_router(upload_router)

app.include_router(health_router)

app.include_router(status_router)

app.include_router(knowledge_router)
# ----------------------------------------------------
# Home
# ----------------------------------------------------

@app.get("/")
def home():

    return {

        "application":
            "AI Customer Support Interface",

        "version":
            "1.0",

        "status":
            "Running",

        "llm":
            LLM_MODEL,

        "rag":
            True

    }