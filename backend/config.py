from pathlib import Path


# =====================================================
# PROJECT ROOT
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

# =====================================================
# DOCUMENTS
# =====================================================

DOCUMENTS_DIR = BASE_DIR / "documents"
MANUALS_DIR = DOCUMENTS_DIR / "manuals"
UPLOADED_DOCUMENTS_DIR = DOCUMENTS_DIR / "uploaded"

# =====================================================
# ARTIFACTS
# =====================================================

ARTIFACTS_DIR = BASE_DIR / "artifacts"

RENDERED_PAGES_DIR = ARTIFACTS_DIR / "rendered_pages"

OCR_OUTPUT_DIR = ARTIFACTS_DIR / "ocr_output"

IMAGE_CLASSIFIER_OUTPUT_DIR = ARTIFACTS_DIR / "image_classifier"

VISION_OUTPUT_DIR = ARTIFACTS_DIR / "vision_output"

GRAPH_OUTPUT_DIR = ARTIFACTS_DIR / "graph_output"

TABLE_OUTPUT_DIR = ARTIFACTS_DIR / "table_output"

EMBEDDING_CACHE_DIR = ARTIFACTS_DIR / "embedding_cache"

FIGURE_INDEX_DIR = ARTIFACTS_DIR / "figure_index"
# =====================================================
# CHROMADB
# =====================================================

CHROMA_DB_PATH = str(BASE_DIR / "chroma_db")

COLLECTION_NAME = "customer_documents"



# =====================================================
# CHUNKING
# =====================================================

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# =====================================================
# OLLAMA
# =====================================================

OLLAMA_HOST = "http://localhost:11434"

LLM_MODEL = "llama3.2:3b"

VISION_MODEL = "llava:7b"

EMBEDDING_MODEL = "nomic-embed-text"

BATCH_SIZE = 16

# =====================================================
# OCR
# =====================================================

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

OCR_DPI = 300

# =====================================================
# PAGE RENDERING
# =====================================================

RENDER_DPI = 300

# ==========================================================
# GRAPH ANALYZER
# ==========================================================

GRAPH_ANALYSIS_DIR = ARTIFACTS_DIR / "graph_analysis"

GRAPH_JSON_DIR = ARTIFACTS_DIR / "graph_json"

GRAPH_ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
GRAPH_JSON_DIR.mkdir(parents=True, exist_ok=True)


MULTIMODAL_OUTPUT_DIR = ARTIFACTS_DIR / "multimodal_chunks"
GRAPH_JSON_DIR = ARTIFACTS_DIR / "graph_json"



UPLOADED_IMAGES_DIR = BASE_DIR / "documents" / "images"
# =====================================================
# CREATE DIRECTORIES
# =====================================================

DIRECTORIES = [

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

    EMBEDDING_CACHE_DIR

]

for directory in DIRECTORIES:

    directory.mkdir(
        parents=True,
        exist_ok=True
    )
