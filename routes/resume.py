import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from dotenv import load_dotenv

from models.schemas import UploadResponse, ExtractionRequest, ExtractionResponse, TestSummaryResponse
from services.gemini_service import GeminiService, get_gemini_service
from utils.helpers import create_timestamp, normalize_filename

load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

router = APIRouter(prefix="/resume", tags=["resume"])


@router.post("/upload", response_model=UploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """Upload a PDF resume and store it in the uploads directory."""
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    content = await file.read()

    timestamp = create_timestamp()
    normalized_name = normalize_filename(file.filename)
    filename_parts = normalized_name.rsplit(".", 1)
    if len(filename_parts) == 2:
        new_filename = f"{filename_parts[0]}_{timestamp}.{filename_parts[1]}"
    else:
        new_filename = f"{file.filename}_{timestamp}"

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = f"{UPLOAD_DIR}/{new_filename}"

    with open(file_path, "wb") as f:
        f.write(content)

    return UploadResponse(
        filename=new_filename,
        original_filename=file.filename,
        file_path=file_path,
        content_type=file.content_type,
        size=len(content),
        timestamp=timestamp,
    )


@router.post("/extract", response_model=ExtractionResponse)
async def extract_resume(
    request: ExtractionRequest,
    gemini: GeminiService = Depends(get_gemini_service),
):
    """
    Extract structured data from an uploaded PDF resume.
    Takes a file_path and returns extracted profile data.
    """
    try:
        extraction = gemini.extract_resume(request.file_path)
        return ExtractionResponse(
            file_path=request.file_path,
            extraction=extraction,
            success=True,
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


@router.post("/test-gemini", response_model=TestSummaryResponse)
async def test_gemini(
    request: ExtractionRequest,
    gemini: GeminiService = Depends(get_gemini_service),
):
    """Test endpoint to verify Gemini API is working."""
    try:
        summary = gemini.test_pdf_summary(request.file_path)
        print(summary)
        return TestSummaryResponse(
            file_path=request.file_path,
            summary="Skills extracted successfully",
            success=True,
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini test failed: {str(e)}")
