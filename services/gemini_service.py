import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

from models.schemas import ResumeExtraction

load_dotenv()

EXTRACTION_PROMPT = """
Extract all resume information from this PDF document.
Return a complete profile with:
- Personal info: full_name, phone_number, email, location, summary
- All work experiences with titles, company names, descriptions, dates, and locations
- Education history with school names, degrees, and time periods
- Skills as a list of strings
- Certifications with names and issuing authorities

Extract dates in ISO format (YYYY-MM-DD). Use null for missing or unavailable fields.
Be thorough and extract all information present in the resume.
"""


class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = os.getenv("GEMINI_MODEL_NAME", "gemini-3-flash-preview")

    def extract_resume(self, file_path: str) -> ResumeExtraction:
        """
        Send PDF to Gemini and extract structured resume data.
        Uses inline/base64 method for PDF processing.
        """
        pdf_path = Path(file_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {file_path}")

        pdf_bytes = pdf_path.read_bytes()

        response = self.client.models.generate_content(
            model=self.model,
            contents=[
                types.Part.from_bytes(
                    data=pdf_bytes,
                    mime_type="application/pdf",
                ),
                EXTRACTION_PROMPT,
            ],
            config={
                "response_mime_type": "application/json",
                "response_schema": ResumeExtraction,
            },
        )

        return ResumeExtraction.model_validate_json(response.text)

    def test_pdf_summary(self, file_path: str) -> str:
        """Simple test: send PDF to Gemini and get a summary."""
        pdf_path = Path(file_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {file_path}")

        pdf_bytes = pdf_path.read_bytes()

        response = self.client.models.generate_content(
            model=self.model,
            contents=[
                types.Part.from_bytes(
                    data=pdf_bytes,
                    mime_type="application/pdf",
                ),
                "Skills as a list of strings",
            ],
            
        )
        return response.text


def get_gemini_service() -> GeminiService:
    return GeminiService()
