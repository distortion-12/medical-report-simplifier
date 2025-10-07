import re
from typing import List, Dict, Any
from app.models.schemas import NormalizedTest, ReferenceRange, RawExtractionResponse

REFERENCE_RANGES = {
    "Hemoglobin": {"low": 12.0, "high": 15.0, "unit": "g/dL"},
    "WBC": {"low": 4000, "high": 11000, "unit": "/uL"}
}

EXPLANATIONS = {
    "Hemoglobin": {
        "low": "Low hemoglobin may relate to anemia.",
        "high": "High hemoglobin can be a sign of dehydration or other conditions."
    },
    "WBC": {
        "low": "Low white blood cell count can be a sign of a weakened immune system.",
        "high": "High WBC can occur with infections."
    }
}

def extract_raw_tests(raw_text: str) -> RawExtractionResponse:
    """
    Dynamically extracts raw test strings and calculates a confidence score.
    """
    pattern = re.compile(r"(\w+\s+[\d.]+\s+[a-zA-Z\/]+\s+\([^)]+\))")
    matches = pattern.findall(raw_text)
    
    # AI Simulation: Confidence is higher if we find more matches
    confidence = min(0.80 + (len(matches) * 0.1), 1.0)
    
    return RawExtractionResponse(tests_raw=matches, confidence=confidence)

def extract_and_normalize_tests(raw_text: str) -> tuple[List[NormalizedTest], float]:
    """
    Dynamically normalizes tests and calculates a normalization confidence score.
    It now trusts the status from the input text (e.g., "(Low)").
    """
    normalized_tests = []
    
    pattern = re.compile(r"(\w+)\s+([\d.]+)\s+([a-zA-Z\/]+)\s+\(([^)]+)\)")
    matches = pattern.findall(raw_text)
    
    known_tests_count = 0
    for match in matches:
        name, value_str, unit, status_from_text = match
        value = float(value_str)

        if name in REFERENCE_RANGES:
            known_tests_count += 1
            ref = REFERENCE_RANGES[name]
            
            # Use the status directly from the text file
            determined_status = status_from_text.lower()

            normalized_tests.append(NormalizedTest(
                name=name,
                value=value,
                unit=unit,
                status=determined_status,
                ref_range=ReferenceRange(low=ref["low"], high=ref["high"])
            ))

    # AI Simulation: Confidence is based on the ratio of known to unknown tests
    normalization_confidence = (known_tests_count / len(matches)) if matches else 0.0
    
    return normalized_tests, round(normalization_confidence, 2)

def generate_patient_summary(tests: List[NormalizedTest]) -> Dict[str, Any]:
    """
    Dynamically generates a patient-friendly summary and relevant explanations.
    """
    findings = []
    explanations = []
    
    for test in tests:
        if test.status != "normal":
            findings.append(f"{test.status} {test.name}")
            if test.name in EXPLANATIONS and test.status in EXPLANATIONS[test.name]:
                explanations.append(EXPLANATIONS[test.name][test.status])

    if not findings:
        summary = "All test results are within the normal range."
    else:
        summary = f"The report shows { ' and '.join(findings) }."
        
    return {"summary": summary, "explanations": explanations}