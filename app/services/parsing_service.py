from typing import List, Dict, Any
from app.models.schemas import NormalizedTest, ReferenceRange

REFERENCE_RANGES = {
    "Hemoglobin": {"low": 12.0, "high": 15.0, "unit": "g/dL"},
    "WBC": {"low": 4000, "high": 11000, "unit": "/uL"}
}

# To extract and standardize lab test results from raw text into objects.
def extract_and_normalize_tests(raw_text: str) -> List[NormalizedTest]:
    """
    Simulates an AI model extracting and normalizing test results from raw text.
    """
    normalized_tests = []
    if "Hemoglobin" in raw_text or "Hemglobin" in raw_text:
        ref = REFERENCE_RANGES["Hemoglobin"]
        normalized_tests.append(NormalizedTest(
            name="Hemoglobin",
            value=10.2,
            unit=ref["unit"],
            status="low",
            ref_range=ReferenceRange(low=ref["low"], high=ref["high"])
        ))
    if "WBC" in raw_text:
        ref = REFERENCE_RANGES["WBC"]
        wbc_value_str = "11200"
        normalized_tests.append(NormalizedTest(
            name="WBC",
            value=float(wbc_value_str),
            unit=ref["unit"],
            status="high",
            ref_range=ReferenceRange(low=ref["low"], high=ref["high"])
        ))
    return normalized_tests

# For creating a simple, patient-facing one-sentence summary of findings.
def generate_patient_summary(tests: List[NormalizedTest]) -> str:
    """
    Simulates an AI model generating a patient-friendly summary.
    """
    findings = []
    for test in tests:
        if test.status != "normal":
            findings.append(f"{test.status} {test.name}")

    if not findings:
        return "All test results are within the normal range."
    else:
        return f"The report shows { ' and '.join(findings) }."