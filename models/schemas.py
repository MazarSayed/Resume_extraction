from pydantic import BaseModel, Field


# --- Nested Models for Resume Data ---

class DatePeriod(BaseModel):
    start_date: str | None = Field(default=None, description="Start date")
    end_date: str | None = Field(default=None, description="End date")


class Experience(BaseModel):
    title: str = Field(description="Job title")
    company_name: str = Field(description="Name of the company")
    job_description: str | None = Field(default=None, description="Description of job responsibilities")
    job_started_on: str | None = Field(default=None, description="Start date of employment")
    job_ended_on: str | None = Field(default=None, description="End date of employment, null if current")
    job_location: str | None = Field(default=None, description="Location of the job")


class Education(BaseModel):
    school: str = Field(description="Name of educational institution")
    degree: str | None = Field(default=None, description="Degree obtained or pursued")
    period: DatePeriod | None = Field(default=None, description="Time period of education")


class Certificate(BaseModel):
    name: str = Field(description="Name of the certification")
    authority: str | None = Field(default=None, description="Issuing authority or organization")


# --- Main Resume Schema ---

class Profile(BaseModel):
    full_name: str = Field(description="Full name of the candidate")
    phone_number: str | None = Field(default=None, description="Phone number")
    email: str | None = Field(default=None, description="Email address")
    location: str | None = Field(default=None, description="Current location or address")
    summary: str | None = Field(default=None, description="Professional summary or objective")
    experiences: list[Experience] = Field(default=[], description="List of work experiences")
    educations: list[Education] = Field(default=[], description="List of educational qualifications")
    skills: list[str] = Field(default=[], description="List of skills")
    certificates: list[Certificate] = Field(default=[], description="List of certifications")


class ResumeExtraction(BaseModel):
    """Top-level model for extracted resume data."""
    profile: Profile = Field(description="Complete profile extracted from resume")


# --- API Request/Response Models ---

class UploadResponse(BaseModel):
    filename: str
    original_filename: str
    file_path: str
    content_type: str
    size: int
    timestamp: str


class ExtractionRequest(BaseModel):
    file_path: str = Field(description="Path to the uploaded PDF file")


class ExtractionResponse(BaseModel):
    file_path: str
    extraction: ResumeExtraction
    success: bool = True


class TestSummaryResponse(BaseModel):
    file_path: str
    summary: str
    success: bool = True
