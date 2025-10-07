from pydantic import BaseModel
from typing import List, Optional

class ReferenceRange(BaseModel):
    low: float
    high: float

class NormalizedTest(BaseModel):
    name: str
    value: float
    unit: str
    status: str
    ref_range: ReferenceRange

class FinalReportResponse(BaseModel):
    tests: List[NormalizedTest]
    tests_raw: List[str]
    confidence: float
    normalization_confidence: float
    summary: str
    explanations: List[str]
    status: str = "ok"

class ErrorResponse(BaseModel):
    status: str
    reason: str

# For the raw text extraction response
class RawExtractionResponse(BaseModel):
    tests_raw: List[str]
    confidence: float