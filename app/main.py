from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Union

from app.models.schemas import FinalReportResponse, ErrorResponse
from app.services import ocr_service, parsing_service, validation_service

app = FastAPI(
    title="AI Medical Report Simplifier",
    description="Processes medical reports (text/image) to provide a simplified, patient-friendly summary.",
    version="1.0.0"
)

@app.post(
    "/process-report/",
    response_model=FinalReportResponse,
    responses={
        200: {"description": "Successfully processed the report."},
        400: {"model": ErrorResponse, "description": "Bad Request (e.g., invalid file, hallucination)."},
        500: {"model": ErrorResponse, "description": "Internal Server Error."}
    },
    summary="Process a Medical Report"
)
async def process_report(file: UploadFile = File(...)):
    """
    Accepts a medical report file (image or .txt) and returns a structured,
    simplified JSON output.

    - **Handles both image and text inputs.** [cite: 27]
    - **Implements guardrails against AI hallucinations.** [cite: 28]
    - **Returns clean, validated JSON.**
    """
    try:
        content = await file.read()
        
        # Step 1: OCR/Text Extraction
        if file.content_type in ["image/png", "image/jpeg", "image/jpg"]:
            raw_text = await ocr_service.extract_text_from_image(content)
        elif file.content_type == "text/plain":
            raw_text = content.decode("utf-8")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Please upload a .txt, .png, .jpg, or .jpeg file."
            )

        # Step 2: Normalize Tests JSON
        normalized_tests = parsing_service.extract_and_normalize_tests(raw_text)

        # Step 3: Guardrail - Check for Hallucinations
        validation_service.validate_no_hallucinations(raw_text, normalized_tests)

        # Step 4: Generate Patient-Friendly Summary
        summary = parsing_service.generate_patient_summary(normalized_tests)

        # Step 5: Final Output
        return FinalReportResponse(tests=normalized_tests, summary=summary)

    except ValueError as ve:
        # Catches guardrail errors or OCR failures
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "unprocessed", "reason": str(ve)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "reason": f"An unexpected error occurred: {e}"}
        )

@app.get("/", summary="Health Check")
def read_root():
    """Friendly: Basic health check to confirm the API is running."""
    return {"status": "API is running"}