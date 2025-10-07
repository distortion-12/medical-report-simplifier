import orjson
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import ORJSONResponse
from app.models.schemas import FinalReportResponse, ErrorResponse
from app.services import ocr_service, parsing_service, validation_service

# Define a custom ORJSONResponse class to enable pretty-printing
class PrettyORJSON(ORJSONResponse):
    def render(self, content: any) -> bytes:
        return orjson.dumps(content, option=orjson.OPT_INDENT_2)

# Set the custom response class as the default for the entire app
app = FastAPI(
    title="AI-Powered Medical Report Simplifier",
    description="Processes medical reports (text/image) to provide a simplified, patient-friendly summary.",
    version="1.0.0",
    default_response_class=PrettyORJSON
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
    simplified JSON output with dynamic AI-simulated values.
    """
    try:
        content = await file.read()
        
        if file.content_type in ["image/png", "image/jpeg", "image/jpg"]:
            raw_text = await ocr_service.extract_text_from_image(content)
        elif file.content_type == "text/plain":
            raw_text = content.decode("utf-8")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Please upload a .txt, .png, .jpg, or .jpeg file."
            )

        # Step 1: Extract Raw data with dynamic confidence
        raw_extraction = parsing_service.extract_raw_tests(raw_text)

        # Step 2: Normalize Tests with dynamic confidence
        normalized_tests, norm_confidence = parsing_service.extract_and_normalize_tests(raw_text)

        # Step 3: Guardrail - Check for Hallucinations
        validation_service.validate_no_hallucinations(raw_text, normalized_tests)

        # Step 4: Generate dynamic summary and explanations
        summary_data = parsing_service.generate_patient_summary(normalized_tests)

        # Step 5: Final Output with dynamic values
        return FinalReportResponse(
            tests=normalized_tests,
            tests_raw=raw_extraction.tests_raw,
            confidence=raw_extraction.confidence,
            normalization_confidence=norm_confidence,
            summary=summary_data["summary"],
            explanations=summary_data["explanations"]
        )

    except ValueError as ve:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "unprocessed", "reason": str(ve)}
        )
    except Exception as e:
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "reason": f"An unexpected error occurred: {e}"}
        )

@app.get("/", summary="Health Check")
def read_root():
    """Friendly: Basic health check to confirm the API is running."""
    return {"status": "API is running"}