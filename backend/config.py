from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-env")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
AUTH_USERNAME = os.getenv("AUTH_USERNAME", "admin")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD", "admin123")

BASE_DIR = Path(__file__).resolve().parent
APP_DATA_DIR = Path(os.getenv("APP_DATA_DIR", str(BASE_DIR)))

DOCUMENTS_DIR = APP_DATA_DIR / "documents"
MANUALS_DIR = DOCUMENTS_DIR / "manuals"
UPLOADED_DOCUMENTS_DIR = DOCUMENTS_DIR / "uploaded"

ARTIFACTS_DIR = APP_DATA_DIR / "artifacts"
RENDERED_PAGES_DIR = ARTIFACTS_DIR / "rendered_pages"
OCR_OUTPUT_DIR = ARTIFACTS_DIR / "ocr_output"
IMAGE_CLASSIFIER_OUTPUT_DIR = ARTIFACTS_DIR / "image_classifier"
VISION_OUTPUT_DIR = ARTIFACTS_DIR / "vision_output"
GRAPH_OUTPUT_DIR = ARTIFACTS_DIR / "graph_output"
TABLE_OUTPUT_DIR = ARTIFACTS_DIR / "table_output"
EMBEDDING_CACHE_DIR = ARTIFACTS_DIR / "embedding_cache"
FIGURE_INDEX_DIR = ARTIFACTS_DIR / "figure_index"
GRAPH_ANALYSIS_DIR = ARTIFACTS_DIR / "graph_analysis"
GRAPH_JSON_DIR = ARTIFACTS_DIR / "graph_json"
MULTIMODAL_OUTPUT_DIR = ARTIFACTS_DIR / "multimodal_chunks"
UPLOADED_IMAGES_DIR = DOCUMENTS_DIR / "images"

CHROMA_DB_PATH = str(APP_DATA_DIR / "chroma_db")
COLLECTION_NAME = "customer_documents"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
BATCH_SIZE = 32

TESSERACT_PATH = os.getenv("TESSERACT_PATH", "")
OCR_DPI = int(os.getenv("OCR_DPI", "300"))
RENDER_DPI = int(os.getenv("RENDER_DPI", "300"))

for directory in [
    DOCUMENTS_DIR,
    MANUALS_DIR,
    UPLOADED_DOCUMENTS_DIR,
    ARTIFACTS_DIR,
    RENDERED_PAGES_DIR,
    OCR_OUTPUT_DIR,
    IMAGE_CLASSIFIER_OUTPUT_DIR,
    VISION_OUTPUT_DIR,
    GRAPH_OUTPUT_DIR,
    TABLE_OUTPUT_DIR,
    EMBEDDING_CACHE_DIR,
    FIGURE_INDEX_DIR,
    GRAPH_ANALYSIS_DIR,
    GRAPH_JSON_DIR,
    MULTIMODAL_OUTPUT_DIR,
    UPLOADED_IMAGES_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)