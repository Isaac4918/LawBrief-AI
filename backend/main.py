from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from services.blob_service import upload_file_to_blob
from services.file_utils import extract_text_from_file
from services.openai_service import analyze_acta

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

origins = [
    "http://localhost",
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # React dev server (si usas create-react-app)
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

app = FastAPI(title="Acta Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration constants
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
ALLOWED_EXTENSIONS = {".txt", ".docx"}
ALLOWED_MIME_TYPES = {
    "text/plain",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
}

async def validate_file(file: UploadFile) -> bool:
    """Valida el archivo antes de procesarlo"""
    # Validar extensión
    filename_lower = file.filename.lower()
    if not any(filename_lower.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail=f"Format not supported. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Validar MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        logger.warning(f"Suspicious MIME type: {file.content_type} for {file.filename}")
    
    return True

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    """
    Endpoint to upload a file and analyze its content.
    Extracts text from paragraphs and images (OCR) in .docx files.

    Parameters:
        file: File to analyze (.txt or .docx)

    Returns:
        {
            "filename": str,
            "result": dict,
            "status": "success"
        }
    """
    logger.info(f"Starting file analysis: {file.filename}")
    
    try:
        # Validate file
        await validate_file(file)
        
        # Read file
        data = await file.read()
        
        # Validate size
        if len(data) > MAX_FILE_SIZE:
            logger.warning(f"File exceeds maximum size: {file.filename} ({len(data)} bytes)")
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum: {MAX_FILE_SIZE / 1024 / 1024} MB"
            )
        
        if len(data) == 0:
            raise HTTPException(status_code=400, detail="File is empty")

        logger.info(f"File validated: {file.filename} ({len(data)} bytes)")

        # Upload file to Blob Storage
        try:
            upload_file_to_blob(file.filename, data)
            logger.info(f"File uploaded to Blob Storage: {file.filename}")
        except Exception as e:
            logger.error(f"Error uploading to Blob Storage: {e}")
            raise HTTPException(status_code=500, detail="Error uploading file")

        # Extract text (with specific error handling)
        try:
            texto_completo = extract_text_from_file(data, file.filename)
            logger.info(f"Text extracted successfully from {file.filename}")

            if not texto_completo or len(texto_completo.strip()) == 0:
                logger.warning(f"No text extracted from file: {file.filename}")
                raise HTTPException(
                    status_code=422,
                    detail="No text could be extracted from the file"
                )
        except ValueError as ve:
            logger.error(f"Validation error: {ve}")
            raise HTTPException(status_code=400, detail=str(ve))
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            raise HTTPException(status_code=500, detail="Error processing file")

        # Analyze with OpenAI
        try:
            result = analyze_acta(texto_completo)
            logger.info(f"Analysis completed for: {file.filename}")
        except Exception as e:
            logger.error(f"Error analyzing with OpenAI: {e}")
            raise HTTPException(status_code=500, detail="Error analyzing content")

        return {
            "filename": file.filename,
            "result": result,
            "status": "success"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Unexpected error processing file"
        )

@app.get("/health")
async def health_check():
    """Endpoint for health check"""
    return {"status": "healthy"}